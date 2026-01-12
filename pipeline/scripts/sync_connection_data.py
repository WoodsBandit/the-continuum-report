#!/usr/bin/env python3
"""
sync_connection_data.py - Extract summaries from connection briefs and update entities.json

This script:
1. Scans briefs/connections/*.md for pairwise connection briefs (entity1_entity2.md)
2. Extracts the Editorial Analysis summary from each brief
3. Updates website/data/entities.json with connection summaries and sources

Usage:
    python scripts/sync_connection_data.py [--dry-run]
"""

import json
import logging
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONNECTIONS_DIR = PROJECT_ROOT / "briefs" / "connections"
ENTITIES_JSON = PROJECT_ROOT / "website" / "data" / "entities.json"


def parse_connection_brief(brief_path: Path) -> Optional[Dict]:
    """
    Parse a pairwise connection brief and extract key data.

    Returns dict with:
        - entity1: first entity ID
        - entity2: second entity ID
        - summary: editorial analysis summary (first paragraph)
        - sources: list of source documents
    """
    content = brief_path.read_text(encoding='utf-8')

    # Extract entity IDs from filename (entity1_entity2.md)
    filename = brief_path.stem
    if filename.endswith('_connections'):
        return None  # Skip single-entity connection files

    parts = filename.split('_')
    if len(parts) < 2:
        return None

    # Handle entity IDs with underscores (e.g., epstein-florida-case_ghislaine-maxwell)
    # Find the split point by looking at the markdown title
    title_match = re.search(r'^# CONNECTION BRIEF:\s*(.+?)\s*↔\s*(.+?)\s*$', content, re.MULTILINE)
    if title_match:
        name1 = title_match.group(1).strip()
        name2 = title_match.group(2).strip()
        # Convert names to IDs
        entity1 = name1.lower().replace(' ', '-').replace("'", '').replace('.', '')
        entity2 = name2.lower().replace(' ', '-').replace("'", '').replace('.', '')
    else:
        # Fallback: split filename at underscore
        entity1 = parts[0]
        entity2 = '_'.join(parts[1:])

    # Extract Editorial Analysis section
    editorial_match = re.search(
        r'## Editorial Analysis\s*\n+(?:\*\*.*?\*\*\s*\n+)?(.*?)(?=\n## |\n---|\Z)',
        content,
        re.DOTALL
    )

    summary = ""
    if editorial_match:
        editorial_text = editorial_match.group(1).strip()
        # Get first paragraph as summary
        paragraphs = [p.strip() for p in editorial_text.split('\n\n') if p.strip()]
        if paragraphs:
            # Clean up markdown formatting
            summary = paragraphs[0]
            summary = re.sub(r'\*\*(.+?)\*\*', r'\1', summary)  # Remove bold
            summary = re.sub(r'\*(.+?)\*', r'\1', summary)  # Remove italic
            summary = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', summary)  # Remove links
            summary = summary.replace('\n', ' ').strip()
            # Limit to ~500 chars for UI display
            if len(summary) > 500:
                summary = summary[:497] + '...'

    # Extract Source Documents table
    sources = []
    source_match = re.search(
        r'## Source Documents\s*\n+\|[^\n]+\n\|[-|\s]+\n(.*?)(?=\n## |\n---|\Z)',
        content,
        re.DOTALL
    )

    if source_match:
        source_rows = source_match.group(1).strip().split('\n')
        for row in source_rows:
            if '|' in row:
                cells = [c.strip() for c in row.split('|')]
                cells = [c for c in cells if c]  # Remove empty cells
                if len(cells) >= 3:
                    # Extract ECF number and description
                    ecf = cells[1] if len(cells) > 1 else ''
                    description = cells[2] if len(cells) > 2 else ''

                    # Extract link if present
                    link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', cells[-1] if cells else '')
                    link = link_match.group(2) if link_match else ''

                    if ecf:
                        sources.append({
                            'ecf': ecf,
                            'description': description,
                            'link': link
                        })

    return {
        'entity1': entity1,
        'entity2': entity2,
        'summary': summary,
        'sources': sources,
        'brief_file': brief_path.name
    }


def scan_connection_briefs() -> List[Dict]:
    """Scan all pairwise connection briefs."""
    briefs = []

    if not CONNECTIONS_DIR.exists():
        logger.error(f"Connections directory not found: {CONNECTIONS_DIR}")
        return briefs

    for brief_path in sorted(CONNECTIONS_DIR.glob("*.md")):
        # Skip index and single-entity connection files
        if brief_path.name in ['CONNECTION_BRIEF_INDEX.md']:
            continue
        if brief_path.stem.endswith('_connections'):
            continue

        try:
            parsed = parse_connection_brief(brief_path)
            if parsed:
                briefs.append(parsed)
                logger.debug(f"Parsed brief: {parsed['entity1']} ↔ {parsed['entity2']} (has_summary={bool(parsed['summary'])})")
        except Exception as e:
            logger.warning(f"Failed to parse brief {brief_path.name}: {e}")

    logger.info(f"Scanned {len(briefs)} connection briefs")
    return briefs


def update_entities_json(briefs: List[Dict], dry_run: bool = False) -> Tuple[int, int]:
    """
    Update entities.json with connection summaries from briefs.

    Returns (updated_count, total_connections)
    """
    if not ENTITIES_JSON.exists():
        logger.error(f"entities.json not found: {ENTITIES_JSON}")
        return 0, 0

    with open(ENTITIES_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Build lookup from connection briefs: (entity1, entity2) -> brief data
    brief_lookup = {}
    for brief in briefs:
        # Store both orderings for easy lookup
        key1 = (brief['entity1'], brief['entity2'])
        key2 = (brief['entity2'], brief['entity1'])
        brief_lookup[key1] = brief
        brief_lookup[key2] = brief

    updated_count = 0
    total_connections = 0

    for entity in data.get('entities', []):
        entity_id = entity.get('id')
        connections = entity.get('connections', [])

        for i, conn in enumerate(connections):
            total_connections += 1

            # Handle both string and dict connection formats
            if isinstance(conn, str):
                # Convert string to dict format
                target_id = conn
                connections[i] = {'targetId': target_id, 'type': 'referenced', 'summary': '', 'sources': []}
                conn = connections[i]
            else:
                target_id = conn.get('targetId')

            # Look up brief data
            key = (entity_id, target_id)
            if key in brief_lookup:
                brief_data = brief_lookup[key]

                # Update connection with brief data
                old_summary = conn.get('summary', '')
                new_summary = brief_data.get('summary', '')

                if new_summary and new_summary != old_summary:
                    conn['summary'] = new_summary
                    updated_count += 1
                    logger.debug(f"Updated connection: {entity_id} ↔ {target_id} ({len(new_summary)} chars)")

                # Update sources if present
                if brief_data.get('sources'):
                    conn['sources'] = brief_data['sources']

    if not dry_run:
        # Update timestamp
        data['generated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

        with open(ENTITIES_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Updated entities.json: {updated_count}/{total_connections} connections")
    else:
        logger.info(f"Dry run: would update {updated_count}/{total_connections} connections")

    return updated_count, total_connections


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Sync connection summaries from briefs to entities.json'
    )
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without making changes')
    args = parser.parse_args()

    print("=" * 60)
    print("Connection Data Sync")
    print("=" * 60)
    print(f"Connections dir: {CONNECTIONS_DIR}")
    print(f"Entities JSON:   {ENTITIES_JSON}")
    print(f"Dry run:         {args.dry_run}")
    print()

    # Step 1: Scan connection briefs
    print("Scanning connection briefs...")
    briefs = scan_connection_briefs()
    print(f"  Found {len(briefs)} pairwise connection briefs")

    # Count briefs with summaries
    with_summary = sum(1 for b in briefs if b.get('summary'))
    print(f"  {with_summary} have Editorial Analysis summaries")
    print()

    # Step 2: Update entities.json
    print("Updating entities.json...")
    updated, total = update_entities_json(briefs, dry_run=args.dry_run)
    print(f"  {'Would update' if args.dry_run else 'Updated'} {updated} of {total} connections")
    print()

    if args.dry_run:
        print("Dry run complete. Run without --dry-run to apply changes.")
    else:
        print("Sync complete!")

    return 0


if __name__ == '__main__':
    sys.exit(main())
