# Continuum Report - Index Builder Scripts

This directory contains Python scripts for building and maintaining the entity extraction indexes.

## Quick Start

### Rebuild All Indexes
```bash
python scripts/rebuild_all_indexes.py
```

This master script runs the complete pipeline:
1. `build_entity_registry.py` - Parse entities_index.md → entity_registry.json
2. `build_source_mentions.py` - Create source→entities inverted index
3. `build_co_occurrence.py` - Build entity co-occurrence matrix
4. `analyze_gaps.py` - Generate gap analysis report

---

## Individual Scripts

### 1. build_entity_registry.py
**Purpose:** Parse the markdown entity extraction report into structured JSON

**Input:**
- `entities_index.md` (329KB markdown file)

**Output:**
- `indexes/entity_registry.json` (2,015 entities)

**Run:**
```bash
python scripts/build_entity_registry.py
```

**Output Structure:**
```json
{
  "generated": "ISO timestamp",
  "count": 2015,
  "entities": {
    "entity-id": {
      "name": "Display Name",
      "mention_count": 76,
      "source_count": 71,
      "sources": ["ecf-1320-11", ...]
    }
  }
}
```

---

### 2. build_source_mentions.py
**Purpose:** Create inverted index mapping sources to entities

**Input:**
- `indexes/entity_registry.json`

**Output:**
- `indexes/source_mentions.json` (83 sources)

**Run:**
```bash
python scripts/build_source_mentions.py
```

**Output Structure:**
```json
{
  "generated": "ISO timestamp",
  "source_count": 83,
  "sources": {
    "ecf-1320-11": {
      "entities": ["ghislaine-maxwell", "jeffrey-epstein", ...],
      "entity_count": 42
    }
  }
}
```

---

### 3. build_co_occurrence.py
**Purpose:** Build entity pair co-occurrence matrix

**Input:**
- `indexes/source_mentions.json`
- `website/data/connections.json` (for cross-reference)
- `website/data/entities.json` (for brief flags)

**Output:**
- `indexes/co_occurrence.json` (117,954 pairs)

**Run:**
```bash
python scripts/build_co_occurrence.py
```

**Output Structure:**
```json
{
  "generated": "ISO timestamp",
  "pair_count": 117954,
  "pairs": {
    "entity1|entity2": {
      "co_mention_count": 52,
      "shared_sources": ["ecf-1320-11", ...],
      "in_connections_json": true,
      "has_brief": false
    }
  }
}
```

---

### 4. analyze_gaps.py
**Purpose:** Generate gap analysis comparing indexes to curated data

**Input:**
- `indexes/entity_registry.json`
- `indexes/source_mentions.json`
- `indexes/co_occurrence.json`
- `website/data/connections.json`
- `website/data/entities.json`

**Output:**
- `reports/index_pipeline_report.md`

**Run:**
```bash
python scripts/analyze_gaps.py
```

**Report Sections:**
1. High co-occurrence pairs missing from connections.json
2. Connections with weak source evidence
3. Entities with many sources but no brief
4. Recommendations for documentation priorities

---

## Requirements

**Python:** 3.7+

**Dependencies:**
- Standard library only (no external packages required)
- `json`, `re`, `pathlib`, `datetime`, `collections`, `itertools`

---

## Data Flow

```
entities_index.md (raw extractions)
        ↓
build_entity_registry.py
        ↓
entity_registry.json
        ↓
build_source_mentions.py
        ↓
source_mentions.json
        ↓
build_co_occurrence.py
        ↓
co_occurrence.json
        ↓
analyze_gaps.py
        ↓
index_pipeline_report.md
```

---

## Normalization Rules

### Entity IDs
- Lowercase
- Spaces → hyphens
- Special chars removed (except hyphens)
- Examples:
  - "Ghislaine Maxwell" → "ghislaine-maxwell"
  - "Case No. 123" → "case-no-123"

### Source IDs
- Format: `ecf-{docket}-{entry}`
- Example: `ecf-1320-11`

### Pair Keys
- Format: `{entity1}|{entity2}`
- Alphabetically sorted
- Example: `ghislaine-maxwell|jeffrey-epstein`

---

## When to Rebuild

Rebuild indexes when:
- New source documents are processed
- `entities_index.md` is updated
- Manual corrections are made to entity registry
- Connections or entities JSON files are updated

**Command:**
```bash
python scripts/rebuild_all_indexes.py
```

---

## Validation

To validate index integrity:

1. **Entity count consistency:**
```python
# All entity IDs in source_mentions should exist in entity_registry
# All source IDs in pairs should exist in source_mentions
```

2. **Cross-reference accuracy:**
```python
# in_connections_json flags should match current connections.json
# has_brief flags should match current entities.json
```

3. **Data types:**
```python
# All counts are non-negative integers
# All IDs are lowercase strings
# All timestamps are ISO 8601 format
```

---

## Troubleshooting

### Issue: Script fails with encoding error
**Solution:** Scripts use UTF-8 encoding. Ensure source files are UTF-8 encoded.

### Issue: Entity count mismatch
**Solution:** Rebuild all indexes from scratch using `rebuild_all_indexes.py`

### Issue: Missing co-occurrence pairs
**Solution:** Verify source_mentions.json was built from latest entity_registry.json

### Issue: Low co-occurrence counts
**Expected behavior.** Most entity pairs appear together infrequently. High co-occurrence (>10) is rare.

---

## Performance

- **entity_registry.py:** ~2 seconds (2,015 entities)
- **source_mentions.py:** ~1 second (83 sources)
- **co_occurrence.py:** ~2 seconds (117,954 pairs)
- **analyze_gaps.py:** ~1 second

**Total pipeline:** ~6 seconds

---

## Future Enhancements

1. **Incremental updates** - Update indexes without full rebuild
2. **Validation script** - Automated data integrity checks
3. **Entity normalization table** - Merge entity variants
4. **Boilerplate filtering** - Exclude legal jargon from extractions
5. **Web UI** - Interactive exploration of co-occurrence relationships

---

## Version History

- **v1.0** (2025-12-24) - Initial pipeline implementation
  - Entity registry builder
  - Source mentions inverted index
  - Co-occurrence matrix
  - Gap analysis report

---

## Related Documentation

- `/indexes/README.md` - Index schema documentation
- `/agents/index-builder.md` - Extraction agent definition
- `/reports/index_pipeline_report.md` - Latest gap analysis
- `/work/index_pipeline_log.md` - Build log
