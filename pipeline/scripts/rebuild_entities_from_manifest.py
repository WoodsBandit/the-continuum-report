#!/usr/bin/env python3
"""
rebuild_entities_from_manifest.py - Rebuild entities.json from ONLY manifest-approved entities

ARCHITECTURAL PRINCIPLE:
    MANIFEST.JSON IS THE SOURCE OF TRUTH FOR WHICH ENTITIES APPEAR.
    NO ENTITY APPEARS IN THE VISUALIZATION WITHOUT BEING IN MANIFEST.JSON.

This script:
1. Reads manifest.json to get approved entity IDs
2. For each approved entity, reads and parses its brief
3. Writes entities.json containing ONLY approved entities
4. Validates that all manifest entries have corresponding briefs

Usage:
    python scripts/rebuild_entities_from_manifest.py [--dry-run]
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BRIEFS_DIR = PROJECT_ROOT / "website" / "briefs" / "entity"
WEBSITE_DATA_DIR = PROJECT_ROOT / "website" / "data"
MANIFEST_JSON = WEBSITE_DATA_DIR / "manifest.json"
ENTITIES_JSON = WEBSITE_DATA_DIR / "entities.json"
CONNECTIONS_JSON = WEBSITE_DATA_DIR / "connections.json"


def parse_entity_brief(brief_path: Path) -> Optional[Dict]:
    """Parse an analytical brief and extract entity data."""
    if not brief_path.exists():
        return None

    content = brief_path.read_text(encoding='utf-8')

    # Parse YAML frontmatter
    frontmatter = {}
    if content.startswith('---'):
        end_idx = content.find('---', 3)
        if end_idx > 0:
            yaml_content = content[3:end_idx].strip()
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')

    # Extract entity name from title
    name_match = re.search(r'^#\s+(.+?)(?:\s*\n|$)', content, re.MULTILINE)
    entity_name = name_match.group(1).strip() if name_match else frontmatter.get('entity_name', '')

    # Extract status from Document Classification table
    status_match = re.search(r'\*\*Status\*\*\s*\|\s*(.+?)(?:\s*\||\s*\n)', content)
    status = status_match.group(1).strip() if status_match else 'Unknown'

    # Extract type
    entity_type = frontmatter.get('entity_type', 'person').lower()
    if entity_type in ['legal_designation', 'location', 'place']:
        entity_type = 'location'
    elif entity_type in ['organization', 'org', 'company', 'institution']:
        entity_type = 'organization'
    elif entity_type in ['case', 'legal_case', 'litigation']:
        entity_type = 'case'
    else:
        entity_type = 'person'

    # Extract Executive Summary
    summary = ''
    summary_match = re.search(r'## Executive Summary\s*\n\s*\*\*Editorial Assessment:\*\*\s*(.+?)(?:\n\n---|\n\n##)', content, re.DOTALL)
    if summary_match:
        summary = summary_match.group(1).strip()
    else:
        # Try alternative format
        summary_match = re.search(r'## Executive Summary\s*\n(.+?)(?:\n\n---|\n\n##)', content, re.DOTALL)
        if summary_match:
            summary = summary_match.group(1).strip()

    # Truncate summary for display
    short_summary = summary[:500] + '...' if len(summary) > 500 else summary

    # Extract source documents
    sources = []
    sources_section = re.search(r'## Source Documents.*?\n\n(.*?)(?:\n\n---|\n\n##|$)', content, re.DOTALL)
    if sources_section:
        # Parse table rows
        for row in re.findall(r'\|\s*(\d+[-\d]*)\s*\|\s*([^|]+)\s*\|', sources_section.group(1)):
            sources.append({
                'ecf': row[0].strip(),
                'description': row[1].strip()
            })

    return {
        'name': entity_name,
        'type': entity_type,
        'status': status,
        'summary': short_summary,
        'full_summary': summary,
        'brief_file': brief_path.name,
        'sources': sources,
        'sources_count': int(frontmatter.get('sources_count', len(sources)))
    }


def load_existing_connections(entity_id: str) -> List[Dict]:
    """Load connections for an entity from connections.json."""
    if not CONNECTIONS_JSON.exists():
        return []

    with open(CONNECTIONS_JSON, 'r', encoding='utf-8') as f:
        connections_data = json.load(f)

    connections = []
    for conn in connections_data.get('connections', []):
        if conn.get('source') == entity_id or conn.get('target') == entity_id:
            connections.append(conn)

    return connections


def main(dry_run: bool = False):
    """Rebuild entities.json from manifest.json."""
    print("=" * 60)
    print("REBUILD ENTITIES FROM MANIFEST")
    print("=" * 60)

    # Load manifest
    if not MANIFEST_JSON.exists():
        print(f"ERROR: manifest.json not found at {MANIFEST_JSON}")
        sys.exit(1)

    with open(MANIFEST_JSON, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    approved_entities = manifest.get('briefs', [])
    print(f"\nManifest contains {len(approved_entities)} approved entities")

    # Build entities
    entities = []
    errors = []

    for entry in approved_entities:
        entity_id = entry['id']
        entity_name = entry['name']
        entity_type = entry['type']
        brief_filename = entry['file']

        brief_path = BRIEFS_DIR / brief_filename

        print(f"  Processing: {entity_name}...", end=' ')

        if not brief_path.exists():
            print("MISSING BRIEF!")
            errors.append(f"Missing brief for {entity_id}: {brief_path}")
            continue

        # Parse brief
        parsed = parse_entity_brief(brief_path)
        if not parsed:
            print("PARSE ERROR!")
            errors.append(f"Failed to parse brief for {entity_id}")
            continue

        # Build entity object
        entity = {
            'id': entity_id,
            'name': entity_name,
            'type': entity_type,
            'status': parsed.get('status', 'Unknown'),
            'summary': parsed.get('summary', ''),
            'full_summary': parsed.get('full_summary', ''),
            'brief_file': brief_filename,
            'brief_url': f"/briefs/{entity_id}.html",
            'sources': parsed.get('sources', []),
            'connections': load_existing_connections(entity_id)
        }

        entities.append(entity)
        print("OK")

    print(f"\nBuilt {len(entities)} entities from {len(approved_entities)} manifest entries")

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")

    # Generate output
    output = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'count': len(entities),
        'source': 'manifest.json',
        'entities': entities
    }

    if dry_run:
        print("\n[DRY RUN] Would write entities.json with:")
        print(f"  - {len(entities)} entities")
        print(f"  - Generated timestamp: {output['generated']}")
    else:
        # Backup existing
        if ENTITIES_JSON.exists():
            backup_path = ENTITIES_JSON.with_suffix('.json.bak')
            ENTITIES_JSON.rename(backup_path)
            print(f"\nBacked up existing entities.json to {backup_path.name}")

        # Write new
        with open(ENTITIES_JSON, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"\nWrote {ENTITIES_JSON}")
        print(f"  - {len(entities)} entities (was 120)")

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    main(dry_run)
