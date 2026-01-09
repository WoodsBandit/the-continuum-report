#!/usr/bin/env python3
"""
add_entity_hyperlinks.py - Add hyperlinks to entity names in Connections tables

For each brief's Connections table, replace plain entity names with
markdown hyperlinks: [Entity Name](/briefs/entity-id.html)
"""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(r"T:")
BRIEFS_DIR = PROJECT_ROOT / "website" / "briefs" / "entity"
DATA_DIR = PROJECT_ROOT / "website" / "data"
MANIFEST_JSON = DATA_DIR / "manifest.json"

def load_manifest():
    """Load manifest and build name -> id mapping."""
    with open(MANIFEST_JSON, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    # Build multiple mappings for fuzzy matching
    name_to_id = {}
    for entity in manifest['briefs']:
        name_lower = entity['name'].lower()
        name_to_id[name_lower] = entity['id']

        # Also add common variations
        # Strip common suffixes/prefixes for matching
        if name_lower.endswith(' affair'):
            name_to_id[name_lower.replace(' affair', '')] = entity['id']
        if name_lower.startswith('the '):
            name_to_id[name_lower[4:]] = entity['id']

    # Add explicit mappings for common variations
    explicit_mappings = {
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
        'nxivm/raniere case': 'nxivm-case',
        'the enterprise': None,  # No brief for this
        'richard secord': None,  # No brief for this
        'jeffrey epstein': 'jeffrey-epstein',
        'ghislaine maxwell': 'ghislaine-maxwell',
        'robert maxwell': 'robert-maxwell',
        'donald trump': 'donald-trump',
        'roy cohn': 'roy-cohn',
        'meyer lansky': 'meyer-lansky',
        'keith raniere': 'keith-raniere',
        'allison mack': 'allison-mack',
        'clare bronfman': 'clare-bronfman',
        'virginia giuffre': 'virginia-giuffre',
        'oliver north': 'oliver-north',
        'william casey': 'william-casey',
        'prince andrew': 'prince-andrew',
        'alan dershowitz': 'alan-dershowitz',
        'bill clinton': 'bill-clinton',
        'les wexner': 'les-wexner',
        'glenn dubin': 'glenn-dubin',
        'jean-luc brunel': 'jean-luc-brunel',
        'sarah kellen': 'sarah-kellen',
        'lesley groff': 'lesley-groff',
        'nadia marcinkova': 'nadia-marcinkova',
        'emmy taylor': 'emmy-taylor',
        'johanna sjoberg': 'johanna-sjoberg',
        'juan alessi': 'juan-alessi',
        'deutsche bank': 'deutsche-bank',
        'jp morgan': 'jpmorgan-chase-bank',
        'jpmorgan': 'jpmorgan-chase-bank',
        'jpmorgan chase': 'jpmorgan-chase-bank',
    }
    name_to_id.update(explicit_mappings)

    return name_to_id

def add_hyperlinks_to_connections(content, name_to_id):
    """Add hyperlinks to entity names in Connections table."""
    # Find Connections section
    conn_match = re.search(r'(## Connections\s*\n\n)(.*?)((?:\n---|\n##|\Z))', content, re.DOTALL)
    if not conn_match:
        return content, 0

    prefix = conn_match.group(1)
    conn_section = conn_match.group(2)
    suffix = conn_match.group(3)

    # Process each table row
    lines = conn_section.split('\n')
    new_lines = []
    links_added = 0

    for line in lines:
        # Skip header and separator lines
        if line.startswith('|---') or 'Connected Entity' in line or not line.startswith('|'):
            new_lines.append(line)
            continue

        # Parse: | Entity | Connection Type | Source |
        match = re.match(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', line)
        if match:
            entity_name = match.group(1).strip()
            conn_type = match.group(2).strip()
            source = match.group(3).strip()

            # Skip if already a link
            if entity_name.startswith('['):
                new_lines.append(line)
                continue

            # Look up entity ID
            entity_lower = entity_name.lower()
            entity_id = name_to_id.get(entity_lower)

            if entity_id:
                # Create hyperlink
                linked_name = f"[{entity_name}](/briefs/{entity_id}.html)"
                new_line = f"| {linked_name} | {conn_type} | {source} |"
                new_lines.append(new_line)
                links_added += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    new_conn_section = '\n'.join(new_lines)

    # Reconstruct content
    start = conn_match.start()
    end = conn_match.end()
    new_content = content[:start] + prefix + new_conn_section + suffix + content[end:]

    return new_content, links_added

def main():
    print("=" * 60)
    print("ADD ENTITY HYPERLINKS TO CONNECTIONS TABLES")
    print("=" * 60)

    name_to_id = load_manifest()
    print(f"\nLoaded {len(name_to_id)} entity name mappings")

    briefs = list(BRIEFS_DIR.glob("analytical_brief_*.md"))
    print(f"Found {len(briefs)} brief files")

    total_links = 0
    files_modified = 0

    for brief in sorted(briefs):
        content = brief.read_text(encoding='utf-8')
        new_content, links_added = add_hyperlinks_to_connections(content, name_to_id)

        if links_added > 0:
            brief.write_text(new_content, encoding='utf-8')
            files_modified += 1
            total_links += links_added
            print(f"  [FIXED] {brief.name}: {links_added} links added")

    print(f"\n{'=' * 60}")
    print(f"SUMMARY: {files_modified} files modified, {total_links} links added")
    print("=" * 60)

if __name__ == '__main__':
    main()
