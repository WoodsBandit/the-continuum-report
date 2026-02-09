# Pending Entity Briefs

**Last Updated:** 2026-01-19
**Auto-sync:** This file must be checked/updated whenever briefs are created or entities.json changes.

---

## Overview

This file tracks entities that exist in `website/data/entities.json` but do NOT yet have corresponding brief files in `website/briefs/entity/`.

**Workflow:**
1. Extract entity from source document
2. Add to `entities.json`
3. Entity automatically appears here as "pending"
4. Create brief in `website/briefs/entity/analytical_brief_{entity_id}.md`
5. Entry automatically removed from pending list

---

## Pending Entities (Need Briefs)

| Entity ID | Entity Name | Type | Added Date | Source Document | Priority |
|-----------|-------------|------|------------|-----------------|----------|
| *None currently* | — | — | — | — | — |

---

## Recently Completed (Last 30 Days)

| Entity ID | Entity Name | Brief Created | Date |
|-----------|-------------|---------------|------|
| *Tracking starts 2026-01-19* | — | — | — |

---

## Validation Rules

### Entity is PENDING if:
- Entity exists in `entities.json`
- No file exists at `website/briefs/entity/analytical_brief_{entity_id}.md`

### Entity is COMPLETE if:
- Entity exists in `entities.json`
- Brief file exists AND contains required sections (header, public record, editorial analysis, alternative interpretations)

### Audit Command
```bash
# Find entities in JSON without briefs
# Run from T:\
python -c "
import json
import os
with open('website/data/entities.json') as f:
    entities = json.load(f)['entities']
for e in entities:
    brief_path = f'website/briefs/entity/analytical_brief_{e[\"id\"].replace(\"-\", \"_\")}.md'
    if not os.path.exists(brief_path):
        print(f'PENDING: {e[\"id\"]} - {e[\"name\"]}')
"
```

---

## Source Extraction Queue

Entities identified in source documents but not yet added to entities.json:

| Entity Name | Source Document | ECF/Page | Extraction Date | Notes |
|-------------|-----------------|----------|-----------------|-------|
| *Add entities here as discovered* | — | — | — | — |

---

## Update Log

| Date | Action | Count |
|------|--------|-------|
| 2026-01-20 | Initial audit - fixed 7 naming mismatches | 0 pending |
| 2026-01-19 | File created | 0 pending |

---

*The Continuum Report — Entity Brief Tracking*
