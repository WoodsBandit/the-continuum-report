#!/usr/bin/env python3
"""
create_connections_backlog.py - Create backlog of connections needing briefs
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(r"T:")
CONNECTIONS_JSON = PROJECT_ROOT / "website" / "data" / "connections.json"
BACKLOG_JSON = PROJECT_ROOT / "website" / "data" / "connections_backlog.json"

def get_old_connections():
    """Get connections from commit with 107 entries."""
    result = subprocess.run(
        ['git', '-C', str(PROJECT_ROOT), 'show', 'HEAD~2:website/data/connections.json'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return json.loads(result.stdout)
    return None

def main():
    # Load old connections (107)
    old_data = get_old_connections()
    if not old_data:
        print("ERROR: Could not retrieve old connections")
        return

    # Load current connections (70)
    with open(CONNECTIONS_JSON, 'r', encoding='utf-8') as f:
        current_data = json.load(f)

    # Find removed connections (those without brief files)
    current_pairs = {(c['source'], c['target']) for c in current_data['connections']}
    removed = [c for c in old_data['connections'] if (c['source'], c['target']) not in current_pairs]

    print(f"Old connections: {old_data['count']}")
    print(f"Current connections: {current_data['count']}")
    print(f"Removed (need briefs): {len(removed)}")

    # Create backlog
    backlog = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'description': 'Connections documented in entity briefs that need connection brief files written before appearing on the site.',
        'principle': 'No connection appears without a corresponding connection brief documenting the relationship.',
        'count': len(removed),
        'pending_connections': []
    }

    print("\nPending connection briefs to write:")
    for c in removed:
        entry = {
            'source': c['source'],
            'target': c['target'],
            'type': c.get('type', 'referenced'),
            'evidence': c.get('evidence', []),
            'expected_brief_file': f"{c['source']}_{c['target']}.md",
            'summary': c.get('summary', '')
        }
        backlog['pending_connections'].append(entry)
        print(f"  - {c['source']} <-> {c['target']}")

    # Write backlog
    with open(BACKLOG_JSON, 'w', encoding='utf-8') as f:
        json.dump(backlog, f, indent=2, ensure_ascii=False)

    print(f"\nSaved backlog to: {BACKLOG_JSON}")

if __name__ == '__main__':
    main()
