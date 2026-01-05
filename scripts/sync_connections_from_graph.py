#!/usr/bin/env python3
"""
sync_connections_from_graph.py - Sync connections from connections.json into entities.json

This script:
1. Reads connections.json to get the full connection graph
2. For each entity in entities.json, adds any missing connections
3. Optionally enriches with summaries from connection briefs

Usage:
    python scripts/sync_connections_from_graph.py [--dry-run]
"""

import json
import logging
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple, Optional

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONNECTIONS_JSON = PROJECT_ROOT / "website" / "data" / "connections.json"
ENTITIES_JSON = PROJECT_ROOT / "website" / "data" / "entities.json"
BRIEFS_DIR = PROJECT_ROOT / "briefs" / "connections"


def load_connections_graph() -> Dict[str, List[dict]]:
    """
    Load connections.json and build adjacency list.
    Returns dict mapping entity_id -> list of connection objects
    """
    if not CONNECTIONS_JSON.exists():
        logger.error(f"connections.json not found: {CONNECTIONS_JSON}")
        return {}

    with open(CONNECTIONS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    connections = data.get('connections', [])
    logger.info(f"Loaded {len(connections)} connections from connections.json")

    # Build adjacency list
    graph: Dict[str, List[dict]] = {}

    for conn in connections:
        source = conn.get('source')
        target = conn.get('target')
        conn_type = conn.get('type', 'referenced')
        strength = conn.get('strength', 50)
        description = conn.get('description', '')

        if not source or not target:
            continue

        # Add connection from source -> target
        if source not in graph:
            graph[source] = []
        graph[source].append({
            'targetId': target,
            'type': conn_type,
            'strength': strength,
            'description': description,
            'summary': '',
            'sources': []
        })

        # Add connection from target -> source (bidirectional)
        if target not in graph:
            graph[target] = []
        graph[target].append({
            'targetId': source,
            'type': conn_type,
            'strength': strength,
            'description': description,
            'summary': '',
            'sources': []
        })

    return graph


def parse_connection_brief(brief_path: Path) -> Optional[Dict]:
    """
    Parse a pairwise connection brief and extract summary and sources.
    """
    content = brief_path.read_text(encoding='utf-8')

    # Extract entity IDs from title
    title_match = re.search(r'^# CONNECTION BRIEF:\s*(.+?)\s*↔\s*(.+?)\s*$', content, re.MULTILINE)
    if not title_match:
        return None

    name1 = title_match.group(1).strip()
    name2 = title_match.group(2).strip()

    # Convert names to IDs
    def name_to_id(name):
        return name.lower().replace(' ', '-').replace("'", '').replace('.', '')

    entity1 = name_to_id(name1)
    entity2 = name_to_id(name2)

    # Extract Editorial Analysis section
    editorial_match = re.search(
        r'## Editorial Analysis\s*\n+(?:\*\*.*?\*\*\s*\n+)?(.*?)(?=\n## |\n---|\Z)',
        content,
        re.DOTALL
    )

    summary = ""
    if editorial_match:
        editorial_text = editorial_match.group(1).strip()
        paragraphs = [p.strip() for p in editorial_text.split('\n\n') if p.strip()]
        if paragraphs:
            summary = paragraphs[0]
            summary = re.sub(r'\*\*(.+?)\*\*', r'\1', summary)
            summary = re.sub(r'\*(.+?)\*', r'\1', summary)
            summary = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', summary)
            summary = summary.replace('\n', ' ').strip()
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
                cells = [c for c in cells if c]
                if len(cells) >= 3:
                    ecf = cells[1] if len(cells) > 1 else ''
                    description = cells[2] if len(cells) > 2 else ''
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
        'sources': sources
    }


def load_brief_lookup() -> Dict[Tuple[str, str], dict]:
    """
    Load all connection briefs and build lookup by entity pair.
    """
    lookup = {}

    if not BRIEFS_DIR.exists():
        logger.warning(f"Briefs directory not found: {BRIEFS_DIR}")
        return lookup

    for brief_path in BRIEFS_DIR.glob("*.md"):
        if brief_path.name == 'CONNECTION_BRIEF_INDEX.md':
            continue
        if brief_path.stem.endswith('_connections'):
            continue

        try:
            parsed = parse_connection_brief(brief_path)
            if parsed and parsed.get('summary'):
                key1 = (parsed['entity1'], parsed['entity2'])
                key2 = (parsed['entity2'], parsed['entity1'])
                lookup[key1] = parsed
                lookup[key2] = parsed
        except Exception as e:
            logger.warning(f"Failed to parse {brief_path.name}: {e}")

    logger.info(f"Loaded {len(lookup) // 2} connection briefs with summaries")
    return lookup


def sync_connections(dry_run: bool = False) -> Tuple[int, int, int]:
    """
    Sync connections from connections.json into entities.json.

    Returns (entities_updated, connections_added, summaries_added)
    """
    # Load data
    graph = load_connections_graph()
    brief_lookup = load_brief_lookup()

    if not ENTITIES_JSON.exists():
        logger.error(f"entities.json not found: {ENTITIES_JSON}")
        return 0, 0, 0

    with open(ENTITIES_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    entities_updated = 0
    connections_added = 0
    summaries_added = 0

    for entity in data.get('entities', []):
        entity_id = entity.get('id')
        if not entity_id:
            continue

        # Get existing connections
        existing_connections = entity.get('connections', [])

        # Normalize existing connections (handle both string and dict formats)
        existing_targets: Set[str] = set()
        normalized_connections = []

        for conn in existing_connections:
            if isinstance(conn, str):
                existing_targets.add(conn)
                normalized_connections.append({
                    'targetId': conn,
                    'type': 'referenced',
                    'summary': '',
                    'sources': []
                })
            else:
                target_id = conn.get('targetId')
                if target_id:
                    existing_targets.add(target_id)
                    normalized_connections.append(conn)

        # Get connections from graph
        graph_connections = graph.get(entity_id, [])

        # Add missing connections
        entity_modified = False
        for graph_conn in graph_connections:
            target_id = graph_conn.get('targetId')
            if target_id and target_id not in existing_targets:
                # New connection to add
                new_conn = {
                    'targetId': target_id,
                    'type': graph_conn.get('type', 'referenced'),
                    'summary': '',
                    'sources': []
                }

                # Try to get summary from brief
                brief_key = (entity_id, target_id)
                if brief_key in brief_lookup:
                    brief_data = brief_lookup[brief_key]
                    new_conn['summary'] = brief_data.get('summary', '')
                    new_conn['sources'] = brief_data.get('sources', [])
                    if new_conn['summary']:
                        summaries_added += 1

                normalized_connections.append(new_conn)
                existing_targets.add(target_id)
                connections_added += 1
                entity_modified = True
                logger.debug(f"Added connection: {entity_id} -> {target_id}")

        # Also update existing connections with summaries if missing
        for conn in normalized_connections:
            if isinstance(conn, dict) and not conn.get('summary'):
                target_id = conn.get('targetId')
                brief_key = (entity_id, target_id)
                if brief_key in brief_lookup:
                    brief_data = brief_lookup[brief_key]
                    if brief_data.get('summary'):
                        conn['summary'] = brief_data['summary']
                        conn['sources'] = brief_data.get('sources', [])
                        summaries_added += 1
                        entity_modified = True

        if entity_modified:
            entity['connections'] = normalized_connections
            entities_updated += 1

    if not dry_run:
        data['generated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

        with open(ENTITIES_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Updated entities.json: {entities_updated} entities, {connections_added} connections added, {summaries_added} summaries added")
    else:
        logger.info(f"Dry run: would update {entities_updated} entities, add {connections_added} connections, add {summaries_added} summaries")

    return entities_updated, connections_added, summaries_added


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Sync connections from connections.json into entities.json'
    )
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without making changes')
    args = parser.parse_args()

    print("=" * 60)
    print("Connection Graph Sync")
    print("=" * 60)
    print(f"Connections JSON: {CONNECTIONS_JSON}")
    print(f"Entities JSON:    {ENTITIES_JSON}")
    print(f"Briefs dir:       {BRIEFS_DIR}")
    print(f"Dry run:          {args.dry_run}")
    print()

    entities_updated, connections_added, summaries_added = sync_connections(dry_run=args.dry_run)

    print()
    print("Results:")
    print(f"  Entities updated:   {entities_updated}")
    print(f"  Connections added:  {connections_added}")
    print(f"  Summaries added:    {summaries_added}")
    print()

    if args.dry_run:
        print("Dry run complete. Run without --dry-run to apply changes.")
    else:
        print("Sync complete!")

    return 0


if __name__ == '__main__':
    sys.exit(main())
