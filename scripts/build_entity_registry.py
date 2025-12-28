#!/usr/bin/env python3
"""
Parse entities_index.md and generate entity_registry.json

Reads the markdown entity extraction report and produces a structured JSON index.
"""

import re
import json
from datetime import datetime
from pathlib import Path


def normalize_entity_id(name):
    """Convert entity name to normalized ID"""
    # Convert to lowercase
    normalized = name.lower()
    # Replace spaces and special chars with hyphens
    normalized = re.sub(r'[^\w\s-]', '', normalized)
    normalized = re.sub(r'[\s_]+', '-', normalized)
    # Remove multiple consecutive hyphens
    normalized = re.sub(r'-+', '-', normalized)
    # Strip leading/trailing hyphens
    normalized = normalized.strip('-')
    return normalized


def extract_source_id(source_path):
    """Extract ECF number from file path"""
    # Match pattern: ecf-XXXX-YY.pdf
    match = re.search(r'ecf-(\d+)-(\d+)\.pdf', source_path)
    if match:
        return f"ecf-{match.group(1)}-{match.group(2)}"
    return None


def parse_entities_index(file_path):
    """Parse entities_index.md and extract structured data"""

    entities = {}
    current_entity = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()

            # Entity header (starts with ###)
            if line.startswith('### '):
                entity_name = line[4:].strip()
                entity_id = normalize_entity_id(entity_name)
                current_entity = entity_id
                entities[entity_id] = {
                    'name': entity_name,
                    'mention_count': 0,
                    'source_count': 0,
                    'sources': []
                }

            # Mentions line
            elif line.startswith('- **Mentions:**') and current_entity:
                # Parse "76 across 71 documents"
                match = re.search(r'(\d+)\s+across\s+(\d+)\s+documents?', line)
                if match:
                    entities[current_entity]['mention_count'] = int(match.group(1))
                    entities[current_entity]['source_count'] = int(match.group(2))

            # Sources line
            elif line.startswith('- **Sources:**') and current_entity:
                # Extract all source paths from this line
                # Sources are comma-separated file paths
                sources_text = line[15:].strip()  # Remove "- **Sources:** "

                # Split by comma and extract ECF numbers
                source_paths = [s.strip() for s in sources_text.split(',')]
                source_ids = []

                for path in source_paths:
                    # Handle "+XX more" notation
                    if '(+' in path and 'more)' in path:
                        continue

                    source_id = extract_source_id(path)
                    if source_id:
                        source_ids.append(source_id)

                entities[current_entity]['sources'] = source_ids

    return entities


def main():
    # Set up paths
    base_dir = Path('/mnt/user/continuum')
    input_file = base_dir / 'entities_index.md'
    output_file = base_dir / 'indexes' / 'entity_registry.json'

    print(f"Reading entities from: {input_file}")

    # Parse the markdown file
    entities = parse_entities_index(input_file)

    # Build output structure
    output = {
        'generated': datetime.utcnow().isoformat() + 'Z',
        'count': len(entities),
        'entities': entities
    }

    # Write JSON output
    print(f"Writing {len(entities)} entities to: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Print summary statistics
    print(f"\n=== Summary ===")
    print(f"Total entities: {len(entities)}")

    # Top 10 by mention count
    top_mentions = sorted(entities.items(), key=lambda x: x[1]['mention_count'], reverse=True)[:10]
    print(f"\nTop 10 by mentions:")
    for entity_id, data in top_mentions:
        print(f"  {data['name']}: {data['mention_count']} mentions across {data['source_count']} sources")

    # Count entities with sources
    with_sources = sum(1 for e in entities.values() if e['sources'])
    print(f"\nEntities with extracted sources: {with_sources}/{len(entities)}")

    print(f"\nDone! Output written to: {output_file}")


if __name__ == '__main__':
    main()
