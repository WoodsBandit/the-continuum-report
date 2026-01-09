#!/usr/bin/env python3
"""
sync_brief_connections.py - Sync connections from briefs to connections.json

This script:
1. Reads manifest.json to get all approved entities
2. Checks connections.json to find which entities have no connections
3. Parses brief files to extract connections tables
4. Adds missing connections to connections.json
"""

import json
import re
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(r"T:")
BRIEFS_DIR = PROJECT_ROOT / "website" / "briefs" / "entity"
DATA_DIR = PROJECT_ROOT / "website" / "data"
MANIFEST_JSON = DATA_DIR / "manifest.json"
CONNECTIONS_JSON = DATA_DIR / "connections.json"

def load_manifest():
    """Load manifest.json and return entity ID -> name mapping."""
    with open(MANIFEST_JSON, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    return {e['id']: e for e in manifest['briefs']}

def load_connections():
    """Load connections.json."""
    with open(CONNECTIONS_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_entities_in_connections(connections_data):
    """Get set of entity IDs that appear in connections."""
    entities = set()
    for conn in connections_data.get('connections', []):
        entities.add(conn['source'])
        entities.add(conn['target'])
    return entities

def name_to_id(name, entities):
    """Convert entity name to ID by fuzzy matching."""
    name_lower = name.lower().strip()

    # Direct matches
    for eid, entity in entities.items():
        if entity['name'].lower() == name_lower:
            return eid

    # Partial matches
    for eid, entity in entities.items():
        if name_lower in entity['name'].lower() or entity['name'].lower() in name_lower:
            return eid

    # Special cases
    name_map = {
        'cia': 'cia',
        'central intelligence agency': 'cia',
        'iran-contra affair': 'iran-contra-case',
        'iran-contra': 'iran-contra-case',
        'bcci': 'bcci',
        'bcci affair': 'bcci',
        'mossad': 'mossad',
        'promis/inslaw': 'promis-inslaw-case',
        'promis/inslaw affair': 'promis-inslaw-case',
        'nxivm': 'nxivm-case',
        'nxivm case': 'nxivm-case',
        'oliver north': 'oliver-north',
        'jeffrey epstein': 'jeffrey-epstein',
        'ghislaine maxwell': 'ghislaine-maxwell',
        'robert maxwell': 'robert-maxwell',
        'roy cohn': 'roy-cohn',
        'meyer lansky': 'meyer-lansky',
        'keith raniere': 'keith-raniere',
        'allison mack': 'allison-mack',
        'clare bronfman': 'clare-bronfman',
        'virginia giuffre': 'virginia-giuffre',
    }

    if name_lower in name_map:
        return name_map[name_lower]

    return None

def parse_connections_from_brief(brief_path, entities):
    """Parse the Connections table from a brief file."""
    content = brief_path.read_text(encoding='utf-8')

    # Find the Connections section
    conn_match = re.search(r'## Connections\s*\n\n(.*?)(?:\n---|\n##|\Z)', content, re.DOTALL)
    if not conn_match:
        return []

    conn_section = conn_match.group(1)

    # Parse table rows (skip header)
    connections = []
    lines = conn_section.strip().split('\n')

    for line in lines:
        # Skip header and separator lines
        if line.startswith('|---') or 'Connected Entity' in line:
            continue

        # Parse: | Entity | Connection Type | Source |
        match = re.match(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', line)
        if match:
            entity_name = match.group(1).strip()
            conn_type = match.group(2).strip().lower()
            source = match.group(3).strip()

            # Map connection type to our schema
            if 'central' in conn_type or 'direct' in conn_type:
                conn_type = 'documented'
            elif 'referenced' in conn_type or 'knowledge' in conn_type:
                conn_type = 'referenced'
            else:
                conn_type = 'referenced'

            target_id = name_to_id(entity_name, entities)
            if target_id:
                connections.append({
                    'target_name': entity_name,
                    'target_id': target_id,
                    'type': conn_type,
                    'evidence': [source] if source else []
                })

    return connections

def main():
    print("=" * 60)
    print("SYNC BRIEF CONNECTIONS TO CONNECTIONS.JSON")
    print("=" * 60)

    # Load data
    entities = load_manifest()
    connections_data = load_connections()
    entities_with_connections = get_entities_in_connections(connections_data)

    print(f"\nTotal entities in manifest: {len(entities)}")
    print(f"Entities with connections: {len(entities_with_connections)}")

    # Find entities without connections
    entities_without = set(entities.keys()) - entities_with_connections
    print(f"Entities WITHOUT connections: {len(entities_without)}")

    if entities_without:
        print("\nEntities without connections:")
        for eid in sorted(entities_without):
            print(f"  - {entities[eid]['name']} ({eid})")

    # Parse briefs for missing connections
    new_connections = []

    for eid in entities_without:
        entity = entities[eid]
        brief_path = BRIEFS_DIR / entity['file']

        if not brief_path.exists():
            print(f"\n  Warning: Brief not found for {eid}")
            continue

        conns = parse_connections_from_brief(brief_path, entities)

        if conns:
            print(f"\n  {entity['name']}: found {len(conns)} connections")

            for conn in conns:
                # Only add if target is also in manifest
                if conn['target_id'] in entities:
                    new_conn = {
                        'source': eid,
                        'target': conn['target_id'],
                        'strength': 40,  # Default lower strength for inferred connections
                        'type': conn['type'],
                        'evidence': conn['evidence'],
                        'bidirectional': False,
                        'source_mentions_target': True,
                        'target_mentions_source': False,
                        'summary': f"Connection documented in {entity['name']} analytical brief.",
                        'brief_file': None  # No separate connection brief
                    }
                    new_connections.append(new_conn)
                    print(f"    + {conn['target_name']} ({conn['type']})")

    print(f"\n{'=' * 60}")
    print(f"Total new connections to add: {len(new_connections)}")

    if new_connections:
        # Add to connections data
        connections_data['connections'].extend(new_connections)
        connections_data['count'] = len(connections_data['connections'])
        connections_data['generated'] = datetime.now(timezone.utc).isoformat()

        # Write back
        with open(CONNECTIONS_JSON, 'w', encoding='utf-8') as f:
            json.dump(connections_data, f, indent=2, ensure_ascii=False)

        print(f"\nUpdated connections.json:")
        print(f"  - Total connections: {connections_data['count']}")

    print("=" * 60)
    print("DONE")
    print("=" * 60)

if __name__ == '__main__':
    main()
