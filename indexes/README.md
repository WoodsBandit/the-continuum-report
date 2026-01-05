# Continuum Report - Index Schemas

This directory contains structured indexes derived from source document analysis.

## File Structure

### `entity_registry.json`
Complete registry of all extracted entities with source mappings.

**Schema:**
```json
{
  "generated": "ISO 8601 timestamp",
  "count": 2008,
  "entities": {
    "normalized-entity-id": {
      "name": "Display Name",
      "mention_count": 76,
      "source_count": 71,
      "sources": ["ecf-1320-11", "ecf-1320-12", ...]
    }
  }
}
```

**Key Properties:**
- `generated`: Timestamp of index generation
- `count`: Total number of unique entities
- `entities`: Object keyed by normalized entity ID (lowercase, hyphenated)
  - `name`: Human-readable display name
  - `mention_count`: Total number of times entity appears across all sources
  - `source_count`: Number of unique sources mentioning this entity
  - `sources`: Array of source identifiers (ECF numbers)

---

### `source_mentions.json`
Inverted index mapping sources to entities mentioned within them.

**Schema:**
```json
{
  "generated": "ISO 8601 timestamp",
  "source_count": 200,
  "sources": {
    "ecf-1320-11": {
      "entities": ["ghislaine-maxwell", "jeffrey-epstein", "virginia-giuffre"],
      "entity_count": 3
    }
  }
}
```

**Key Properties:**
- `generated`: Timestamp of index generation
- `source_count`: Total number of unique sources
- `sources`: Object keyed by source identifier
  - `entities`: Array of entity IDs appearing in this source
  - `entity_count`: Count of unique entities in this source

**Use Cases:**
- Find all entities mentioned in a specific document
- Identify which sources to read for specific entity combinations
- Support source-based filtering in queries

---

### `co_occurrence.json`
Entity co-occurrence matrix tracking which entities appear together in the same sources.

**Schema:**
```json
{
  "generated": "ISO 8601 timestamp",
  "pair_count": 15000,
  "pairs": {
    "entity1|entity2": {
      "co_mention_count": 52,
      "shared_sources": ["ecf-1320-11", "ecf-1320-12"],
      "in_connections_json": true,
      "has_brief": false
    }
  }
}
```

**Key Properties:**
- `generated`: Timestamp of index generation
- `pair_count`: Total number of unique entity pairs
- `pairs`: Object keyed by pipe-separated entity IDs (alphabetically sorted)
  - `co_mention_count`: Number of sources where both entities appear
  - `shared_sources`: Array of source IDs where both entities co-occur
  - `in_connections_json`: Boolean flag - is this pair documented in connections.json?
  - `has_brief`: Boolean flag - does this connection have a written brief?

**Use Cases:**
- Discover undocumented relationships between entities
- Prioritize connection brief writing based on co-occurrence strength
- Validate existing connections against source evidence
- Identify weak connections (low co-occurrence despite connection entry)

---

## Pipeline Flow

```
entities_index.md (raw extractions)
    ↓
entity_registry.json (structured entity data)
    ↓
source_mentions.json (inverted index)
    ↓
co_occurrence.json (relationship detection)
    ↓
Gap analysis → Reports
```

## Normalization Rules

### Entity ID Normalization
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters except hyphens
- Examples:
  - "Ghislaine Maxwell" → "ghislaine-maxwell"
  - "Case No. 123" → "case-no-123"
  - "Prince Andrew" → "prince-andrew"

### Source ID Normalization
- Extract ECF number from file path
- Format: `ecf-{number}-{sub-number}`
- Example: `T:\website\sources\giuffre-v-maxwell\ecf-1320-11.pdf` → `ecf-1320-11`

---

## Maintenance

These indexes are **generated artifacts** and should be rebuilt when:
- New source documents are processed
- Entity extraction rules change
- Manual corrections are made to entity_registry.json

**Rebuild Command:**
```bash
python scripts/build_indexes.py
```

**Last Generated:** 2025-12-24

---

## Related Files

- `/entities_index.md` - Raw extraction report (329KB, 2008 entities)
- `/website/data/entities.json` - Curated entity profiles (37 entities with briefs)
- `/website/data/connections.json` - Documented connections (131 pairs)
- `/reports/index_pipeline_report.md` - Gap analysis and recommendations
