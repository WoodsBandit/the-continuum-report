#!/usr/bin/env python3
"""
Build co_occurrence.json from source_mentions.json

Creates entity pair co-occurrence matrix and cross-references with connections.json.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from itertools import combinations
from collections import defaultdict


def build_co_occurrence(source_mentions):
    """Build co-occurrence matrix from source mentions"""

    pair_to_sources = defaultdict(list)

    # For each source, find all entity pairs
    for source_id, source_data in source_mentions['sources'].items():
        entities = source_data['entities']

        # Generate all unique pairs (alphabetically sorted)
        for entity1, entity2 in combinations(sorted(entities), 2):
            pair_key = f"{entity1}|{entity2}"
            pair_to_sources[pair_key].append(source_id)

    # Build output structure
    pairs = {}
    for pair_key, shared_sources in pair_to_sources.items():
        pairs[pair_key] = {
            'co_mention_count': len(shared_sources),
            'shared_sources': shared_sources,
            'in_connections_json': False,  # Will be updated later
            'has_brief': False  # Will be updated later
        }

    return pairs


def normalize_connection_key(entity1, entity2):
    """Create normalized connection key (alphabetically sorted)"""
    entities = sorted([entity1.lower(), entity2.lower()])
    return f"{entities[0]}|{entities[1]}"


def cross_reference_connections(pairs, connections_data, entities_data):
    """Cross-reference co-occurrence pairs with connections.json and entities.json"""

    # Build set of connection pairs from connections.json
    connection_pairs = set()
    for conn in connections_data['connections']:
        source = conn['source']
        target = conn['target']
        pair_key = normalize_connection_key(source, target)
        connection_pairs.add(pair_key)

    # Build set of entities with briefs from entities.json
    entities_with_briefs = set()
    if entities_data and 'entities' in entities_data:
        for entity in entities_data['entities']:
            entity_id = entity.get('id', '').lower()
            if entity.get('brief_file') or entity.get('brief_url'):
                entities_with_briefs.add(entity_id)

    # Update pairs with cross-reference info
    for pair_key, pair_data in pairs.items():
        # Check if this pair exists in connections.json
        if pair_key in connection_pairs:
            pair_data['in_connections_json'] = True

        # Check if either entity in the pair has a brief
        entity1, entity2 = pair_key.split('|')
        if entity1 in entities_with_briefs or entity2 in entities_with_briefs:
            pair_data['has_brief'] = True

    return pairs


def main():
    # Set up paths
    base_dir = Path(r'C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum')
    source_mentions_file = base_dir / 'indexes' / 'source_mentions.json'
    connections_file = base_dir / 'website' / 'data' / 'connections.json'
    entities_file = base_dir / 'website' / 'data' / 'entities.json'
    output_file = base_dir / 'indexes' / 'co_occurrence.json'

    print(f"Reading source mentions from: {source_mentions_file}")

    # Load source mentions
    with open(source_mentions_file, 'r', encoding='utf-8') as f:
        source_mentions = json.load(f)

    print(f"Processing {source_mentions['source_count']} sources...")

    # Build co-occurrence matrix
    pairs = build_co_occurrence(source_mentions)

    print(f"Found {len(pairs)} unique entity pairs")

    # Load connections.json for cross-reference
    print(f"\nCross-referencing with connections.json...")
    try:
        with open(connections_file, 'r', encoding='utf-8') as f:
            connections_data = json.load(f)
        print(f"Loaded {connections_data['count']} connections")
    except Exception as e:
        print(f"Warning: Could not load connections.json: {e}")
        connections_data = {'connections': []}

    # Load entities.json for brief info
    print(f"Cross-referencing with entities.json...")
    try:
        with open(entities_file, 'r', encoding='utf-8') as f:
            entities_data = json.load(f)
        print(f"Loaded {entities_data['count']} entities")
    except Exception as e:
        print(f"Warning: Could not load entities.json: {e}")
        entities_data = None

    # Cross-reference
    pairs = cross_reference_connections(pairs, connections_data, entities_data)

    # Build output structure
    output = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'pair_count': len(pairs),
        'pairs': pairs
    }

    # Write JSON output
    print(f"\nWriting {len(pairs)} pairs to: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Print summary statistics
    print(f"\n=== Summary ===")
    print(f"Total entity pairs: {len(pairs)}")

    # Count documented vs undocumented
    documented = sum(1 for p in pairs.values() if p['in_connections_json'])
    undocumented = len(pairs) - documented
    print(f"Pairs in connections.json: {documented}")
    print(f"Undocumented pairs: {undocumented}")

    # Count pairs with briefs
    with_briefs = sum(1 for p in pairs.values() if p['has_brief'])
    print(f"Pairs involving entities with briefs: {with_briefs}")

    # Top 10 by co-occurrence count
    top_pairs = sorted(pairs.items(), key=lambda x: x[1]['co_mention_count'], reverse=True)[:10]
    print(f"\nTop 10 pairs by co-occurrence count:")
    for pair_key, data in top_pairs:
        entity1, entity2 = pair_key.split('|')
        in_conn = "Y" if data['in_connections_json'] else "N"
        print(f"  [{in_conn}] {entity1} x {entity2}: {data['co_mention_count']} co-mentions")

    # Statistics
    counts = [p['co_mention_count'] for p in pairs.values()]
    avg_count = sum(counts) / len(counts) if counts else 0
    print(f"\nAverage co-mentions per pair: {avg_count:.1f}")
    print(f"Min co-mentions: {min(counts) if counts else 0}")
    print(f"Max co-mentions: {max(counts) if counts else 0}")

    # High co-occurrence but not in connections.json
    high_undocumented = [
        (k, v) for k, v in pairs.items()
        if v['co_mention_count'] >= 10 and not v['in_connections_json']
    ]
    high_undocumented = sorted(high_undocumented, key=lambda x: x[1]['co_mention_count'], reverse=True)[:10]

    print(f"\nTop 10 undocumented pairs with high co-occurrence (>=10):")
    for pair_key, data in high_undocumented:
        entity1, entity2 = pair_key.split('|')
        print(f"  {entity1} x {entity2}: {data['co_mention_count']} co-mentions")

    print(f"\nDone! Output written to: {output_file}")


if __name__ == '__main__':
    main()
