#!/usr/bin/env python3
"""
Build source_mentions.json from entity_registry.json

Creates an inverted index mapping source documents to entities mentioned within them.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict


def build_source_mentions(entity_registry):
    """Build inverted index from entity registry"""

    source_to_entities = defaultdict(list)

    # Iterate through all entities and their sources
    for entity_id, entity_data in entity_registry['entities'].items():
        for source_id in entity_data.get('sources', []):
            source_to_entities[source_id].append(entity_id)

    # Build output structure with entity counts
    sources = {}
    for source_id, entity_list in sorted(source_to_entities.items()):
        sources[source_id] = {
            'entities': sorted(entity_list),  # Sort for consistency
            'entity_count': len(entity_list)
        }

    return sources


def main():
    # Set up paths
    base_dir = Path(r'\\192.168.1.139\continuum')
    input_file = base_dir / 'indexes' / 'entity_registry.json'
    output_file = base_dir / 'indexes' / 'source_mentions.json'

    print(f"Reading entity registry from: {input_file}")

    # Load entity registry
    with open(input_file, 'r', encoding='utf-8') as f:
        entity_registry = json.load(f)

    print(f"Processing {entity_registry['count']} entities...")

    # Build source mentions index
    sources = build_source_mentions(entity_registry)

    # Build output structure
    output = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'source_count': len(sources),
        'sources': sources
    }

    # Write JSON output
    print(f"Writing {len(sources)} sources to: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Print summary statistics
    print(f"\n=== Summary ===")
    print(f"Total sources: {len(sources)}")

    # Top 10 sources by entity count
    top_sources = sorted(sources.items(), key=lambda x: x[1]['entity_count'], reverse=True)[:10]
    print(f"\nTop 10 sources by entity count:")
    for source_id, data in top_sources:
        print(f"  {source_id}: {data['entity_count']} entities")

    # Statistics
    entity_counts = [s['entity_count'] for s in sources.values()]
    avg_entities = sum(entity_counts) / len(entity_counts) if entity_counts else 0
    print(f"\nAverage entities per source: {avg_entities:.1f}")
    print(f"Min entities in a source: {min(entity_counts) if entity_counts else 0}")
    print(f"Max entities in a source: {max(entity_counts) if entity_counts else 0}")

    print(f"\nDone! Output written to: {output_file}")


if __name__ == '__main__':
    main()
