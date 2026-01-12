#!/usr/bin/env python3
"""
build_connections_from_briefs.py - Build connections ONLY from connection briefs

This script enforces the architectural principle:
    CONNECTION BRIEFS ARE THE SOURCE OF TRUTH.
    NO CONNECTION EXISTS WITHOUT A BRIEF.

Flow:
    briefs/connections/*.md → parse → connections.json + entities.json

This REPLACES the old approach where connections were derived from text mentions
in analytical briefs (build_graph.py:build_connections).

Usage:
    python scripts/build_connections_from_briefs.py [--dry-run]
"""

import json
import logging
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONNECTIONS_BRIEFS_DIR = PROJECT_ROOT / "briefs" / "connections"
WEBSITE_DATA_DIR = PROJECT_ROOT / "website" / "data"
ENTITIES_JSON = WEBSITE_DATA_DIR / "entities.json"
CONNECTIONS_JSON = WEBSITE_DATA_DIR / "connections.json"


def parse_connection_brief(brief_path: Path) -> Optional[Dict]:
    """
    Parse a pairwise connection brief and extract all structured data.

    Returns dict with:
        - entity1, entity2: entity IDs
        - entity1_name, entity2_name: display names
        - summary: editorial analysis (first paragraph)
        - full_summary: complete editorial analysis
        - relationship_type: from classification table
        - direction: bidirectional/unidirectional
        - status: relationship status
        - sources_count: number of source documents
        - sources: list of source documents
        - brief_file: filename

    NOTE: No "strength" scoring - binary model only.
    """
    content = brief_path.read_text(encoding='utf-8')
    filename = brief_path.stem

    # Skip single-entity connection files (*_connections.md)
    if filename.endswith('_connections'):
        return None

    # Skip index files
    if filename in ['CONNECTION_BRIEF_INDEX', 'index']:
        return None

    # Extract entity names from title
    # Format 1: # CONNECTION BRIEF: Entity A ↔ Entity B
    # Format 2: **Subjects:** Entity A ↔ Entity B
    # Format 3: # Entity A ↔ Entity B — Connection Analysis
    title_match = re.search(
        r'^# CONNECTION BRIEF:\s*(.+?)\s*↔\s*(.+?)\s*$',
        content,
        re.MULTILINE
    )

    if not title_match:
        # Try alternative format: **Subjects:** Entity A ↔ Entity B
        title_match = re.search(
            r'\*\*Subjects?:\*\*\s*(.+?)\s*↔\s*(.+?)(?:\s*$|\s*\n)',
            content,
            re.MULTILINE
        )

    if not title_match:
        # Try format: # Entity A ↔ Entity B — Connection Analysis
        title_match = re.search(
            r'^#\s*(.+?)\s*↔\s*(.+?)\s*—',
            content,
            re.MULTILINE
        )

    if not title_match:
        logger.warning(f"Could not parse title from {filename}")
        return None

    entity1_name = title_match.group(1).strip()
    entity2_name = title_match.group(2).strip()

    # Convert names to IDs
    def name_to_id(name: str) -> str:
        return name.lower().replace(' ', '-').replace("'", '').replace('.', '').replace(',', '')

    entity1 = name_to_id(entity1_name)
    entity2 = name_to_id(entity2_name)

    # Extract Relationship Classification table
    relationship_type = ""
    direction = "bidirectional"
    status = ""
    # NOTE: No strength scoring - binary model only

    classification_match = re.search(
        r'## Relationship Classification\s*\n+\|[^\n]+\|\s*\n\|[-|\s]+\|\s*\n((?:\|[^\n]+\|\s*\n)+)',
        content
    )

    if classification_match:
        table_content = classification_match.group(1)
        for line in table_content.strip().split('\n'):
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if len(cells) >= 2:
                key = cells[0].replace('**', '').lower().strip()
                value = cells[1].strip()

                if 'type' in key and 'document' not in key:
                    relationship_type = value
                elif 'direction' in key:
                    direction = value.lower()
                elif 'status' in key:
                    status = value
                # NOTE: 'strength' and 'evidence level' are DEPRECATED - skip them

    # Extract Editorial Analysis section
    editorial_match = re.search(
        r'## Editorial Analysis\s*\n+(?:\*\*.*?\*\*\s*\n+)?(.*?)(?=\n## |\n---|\Z)',
        content,
        re.DOTALL
    )

    summary = ""
    full_summary = ""
    if editorial_match:
        editorial_text = editorial_match.group(1).strip()
        full_summary = editorial_text

        # Get first paragraph as summary
        paragraphs = [p.strip() for p in editorial_text.split('\n\n') if p.strip()]
        if paragraphs:
            summary = paragraphs[0]
            # Clean up markdown formatting
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
                    # Format: # | ECF | Description | Link
                    ecf = cells[1] if len(cells) > 1 else ''
                    description = cells[2] if len(cells) > 2 else ''

                    # Extract link if present
                    link = ""
                    if len(cells) > 3:
                        link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', cells[3])
                        if link_match:
                            link = link_match.group(2)

                    if ecf:
                        sources.append({
                            'ecf': ecf,
                            'description': description,
                            'link': link
                        })

    # Determine if bidirectional
    is_bidirectional = 'bidirectional' in direction.lower()

    # Connection type from relationship_type (use first type if multiple)
    # NOTE: No evidence level - binary model only
    conn_type = relationship_type.split('/')[0].strip() if relationship_type else 'SOC'

    return {
        'entity1': entity1,
        'entity2': entity2,
        'entity1_name': entity1_name,
        'entity2_name': entity2_name,
        'summary': summary,
        'full_summary': full_summary,
        'relationship_type': relationship_type,
        'direction': direction,
        'status': status,
        'sources_count': len(sources),  # Binary model: count sources, no strength scoring
        'type': conn_type,
        'bidirectional': is_bidirectional,
        'sources': sources,
        'brief_file': brief_path.name
    }


def scan_connection_briefs() -> List[Dict]:
    """Scan all pairwise connection briefs and parse them."""
    briefs = []

    if not CONNECTIONS_BRIEFS_DIR.exists():
        logger.error(f"Connections briefs directory not found: {CONNECTIONS_BRIEFS_DIR}")
        return briefs

    for brief_path in sorted(CONNECTIONS_BRIEFS_DIR.glob("*.md")):
        try:
            parsed = parse_connection_brief(brief_path)
            if parsed:
                briefs.append(parsed)
                logger.debug(f"Parsed: {parsed['entity1']} <-> {parsed['entity2']}")
        except Exception as e:
            logger.warning(f"Failed to parse {brief_path.name}: {e}")

    logger.info(f"Scanned {len(briefs)} pairwise connection briefs")
    return briefs


def build_connections_json(briefs: List[Dict]) -> Dict:
    """Build connections.json structure from parsed briefs."""
    connections = []
    processed_pairs = set()

    for brief in briefs:
        # Create normalized pair key to avoid duplicates
        pair = tuple(sorted([brief['entity1'], brief['entity2']]))
        if pair in processed_pairs:
            continue
        processed_pairs.add(pair)

        # Build evidence list from sources
        evidence = []
        for src in brief['sources'][:5]:
            evidence.append(src['ecf'])

        connection = {
            'source': pair[0],
            'target': pair[1],
            'sources_count': brief['sources_count'],  # Binary model: count sources, no strength scoring
            'type': brief['type'],
            'evidence': evidence,
            'bidirectional': brief['bidirectional'],
            'source_mentions_target': True,  # Brief exists, so documented
            'target_mentions_source': brief['bidirectional'],
            'summary': brief['summary'],
            'brief_file': brief['brief_file']
        }

        connections.append(connection)

    # Sort by sources_count descending (most documented connections first)
    connections.sort(key=lambda x: -x['sources_count'])

    return {
        'generated': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'count': len(connections),
        'connections': connections,
        'source': 'build_connections_from_briefs.py',
        'note': 'Connections derived ONLY from connection briefs. No connection exists without a brief.'
    }


def update_entities_json(briefs: List[Dict], dry_run: bool = False) -> Tuple[int, int]:
    """
    Update entities.json with connections from briefs.

    This REPLACES existing connections - the briefs are the source of truth.
    """
    if not ENTITIES_JSON.exists():
        logger.error(f"entities.json not found: {ENTITIES_JSON}")
        return 0, 0

    with open(ENTITIES_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Build lookup: entity_id -> list of connections from briefs
    entity_connections: Dict[str, List[Dict]] = {}

    for brief in briefs:
        entity1 = brief['entity1']
        entity2 = brief['entity2']

        # Add connection to entity1's list
        if entity1 not in entity_connections:
            entity_connections[entity1] = []

        entity_connections[entity1].append({
            'targetId': entity2,
            'type': brief['type'],
            'summary': brief['summary'],
            'sources': brief['sources'],
            'brief_file': brief['brief_file'],
            'relationship_type': brief['relationship_type'],
            'bidirectional': brief['bidirectional']
        })

        # Add reverse connection to entity2's list (if bidirectional or we have the brief)
        if entity2 not in entity_connections:
            entity_connections[entity2] = []

        entity_connections[entity2].append({
            'targetId': entity1,
            'type': brief['type'],
            'summary': brief['summary'],
            'sources': brief['sources'],
            'brief_file': brief['brief_file'],
            'relationship_type': brief['relationship_type'],
            'bidirectional': brief['bidirectional']
        })

    # Update each entity
    entities_updated = 0
    connections_total = 0

    for entity in data.get('entities', []):
        entity_id = entity.get('id')

        if entity_id in entity_connections:
            # REPLACE connections with brief-derived ones
            old_count = len(entity.get('connections', []))
            new_connections = entity_connections[entity_id]

            entity['connections'] = new_connections
            connections_total += len(new_connections)

            if old_count != len(new_connections):
                entities_updated += 1
                logger.debug(f"Updated {entity_id}: {old_count} -> {len(new_connections)} connections")
        else:
            # Entity has no connections from briefs - clear any existing
            if entity.get('connections'):
                old_count = len(entity['connections'])
                entity['connections'] = []
                entities_updated += 1
                logger.debug(f"Cleared {entity_id}: {old_count} -> 0 connections (no briefs)")

    if not dry_run:
        # Update timestamp
        data['generated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        data['connections_source'] = 'build_connections_from_briefs.py'

        with open(ENTITIES_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Updated entities.json: {entities_updated} entities, {connections_total} total connections")
    else:
        logger.info(f"Dry run: would update {entities_updated} entities, {connections_total} total connections")

    return entities_updated, connections_total


def write_connections_json(connections_data: Dict, dry_run: bool = False) -> None:
    """Write the new connections.json file."""
    if dry_run:
        logger.info(f"Dry run: would write connections.json with {connections_data['count']} connections")
        return

    WEBSITE_DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONNECTIONS_JSON, 'w', encoding='utf-8') as f:
        json.dump(connections_data, f, indent=2, ensure_ascii=False)

    logger.info(f"Wrote connections.json: {connections_data['count']} connections")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Build connections from briefs (briefs are source of truth)'
    )
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without making changes')
    args = parser.parse_args()

    print("=" * 70)
    print("BUILD CONNECTIONS FROM BRIEFS")
    print("=" * 70)
    print()
    print("ARCHITECTURAL PRINCIPLE:")
    print("  Connection briefs are the SOURCE OF TRUTH.")
    print("  No connection exists without a corresponding brief.")
    print()
    print(f"Briefs dir:      {CONNECTIONS_BRIEFS_DIR}")
    print(f"Entities JSON:   {ENTITIES_JSON}")
    print(f"Connections JSON:{CONNECTIONS_JSON}")
    print(f"Dry run:         {args.dry_run}")
    print()

    # Step 1: Scan and parse all connection briefs
    print("Step 1: Scanning connection briefs...")
    briefs = scan_connection_briefs()
    print(f"  Found {len(briefs)} pairwise connection briefs")

    # Count briefs with summaries
    with_summary = sum(1 for b in briefs if b.get('summary'))
    print(f"  {with_summary} have Editorial Analysis summaries")
    print()

    # Step 2: Build connections.json
    print("Step 2: Building connections.json...")
    connections_data = build_connections_json(briefs)
    print(f"  {connections_data['count']} unique connections")
    write_connections_json(connections_data, dry_run=args.dry_run)
    print()

    # Step 3: Update entities.json
    print("Step 3: Updating entities.json...")
    entities_updated, connections_total = update_entities_json(briefs, dry_run=args.dry_run)
    print(f"  {'Would update' if args.dry_run else 'Updated'} {entities_updated} entities")
    print(f"  {connections_total} total connection entries")
    print()

    if args.dry_run:
        print("=" * 70)
        print("DRY RUN COMPLETE. Run without --dry-run to apply changes.")
        print("=" * 70)
    else:
        print("=" * 70)
        print("BUILD COMPLETE.")
        print(f"  - connections.json: {connections_data['count']} connections (from briefs)")
        print(f"  - entities.json: {connections_total} connection entries")
        print()
        print("Orphan connections (no brief) have been REMOVED.")
        print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
