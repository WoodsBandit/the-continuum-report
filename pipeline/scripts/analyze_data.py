import json
from pathlib import Path
from collections import defaultdict
import re

# Define paths
base_path = Path(r"C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum")
entity_registry_path = base_path / "indexes" / "entity_registry.json"
co_occurrence_path = base_path / "indexes" / "co_occurrence.json"
curated_entities_path = base_path / "website" / "data" / "entities.json"

# Load data
print("Loading entity registry...")
with open(entity_registry_path, 'r', encoding='utf-8') as f:
    entity_data = json.load(f)
    entities = entity_data.get('entities', {})

print(f"Total entities: {len(entities)}\n")

# Sort by mention count
sorted_entities = sorted(entities.items(), key=lambda x: x[1]['mention_count'], reverse=True)

print("Top 100 entities by mention count:")
for i, (entity_id, data) in enumerate(sorted_entities[:100]):
    print(f"{i+1}. {entity_id}: {data['mention_count']} mentions, {data['source_count']} sources")

print("\n" + "="*80 + "\n")

# Load co-occurrence data in chunks
print("Analyzing co-occurrence data...")
with open(co_occurrence_path, 'r', encoding='utf-8') as f:
    co_occurrence = json.load(f)

print(f"Total co-occurrence pairs: {len(co_occurrence)}\n")

# Sort by co-mention count
sorted_pairs = sorted(co_occurrence.items(), key=lambda x: x[1]['co_mention_count'], reverse=True)

print("Top 200 pairs by co-mention count:")
for i, (pair_key, data) in enumerate(sorted_pairs[:200]):
    print(f"{i+1}. {pair_key}: {data['co_mention_count']} co-mentions")
