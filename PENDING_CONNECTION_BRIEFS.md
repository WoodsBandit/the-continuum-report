# Pending Connection Briefs

**Last Updated:** 2026-01-19
**Auto-sync:** This file must be checked/updated whenever briefs are created or connections.json changes.

---

## Overview

This file tracks connections that exist in `website/data/connections.json` but do NOT yet have corresponding brief files in `website/briefs/connections/`.

**Workflow:**
1. Identify connection between entities in source document
2. Add to `connections.json` with evidence array
3. Connection automatically appears here as "pending"
4. Create brief in `website/briefs/connections/{entity1}_{entity2}.md` (alphabetical order)
5. Entry automatically removed from pending list

---

## Pending Connections (Need Briefs)

| Source Entity | Target Entity | Connection Type | Added Date | Evidence | Priority |
|---------------|---------------|-----------------|------------|----------|----------|
| *None currently* | — | — | — | — | — |

---

## Recently Completed (Last 30 Days)

| Connection | Brief Created | Date |
|------------|---------------|------|
| donald-trump ↔ roy-cohn | donald-trump_roy-cohn.md | 2026-01-19 |
| *Tracking starts 2026-01-19* | — | — |

---

## Validation Rules

### Connection is PENDING if:
- Connection exists in `connections.json`
- No file exists at `website/briefs/connections/{source}_{target}.md` (alphabetical order)

### Connection is COMPLETE if:
- Connection exists in `connections.json`
- Brief file exists with alphabetically-sorted filename
- Brief contains required sections (header, public record, editorial analysis, alternative interpretations)

### Naming Convention (CRITICAL)
Connection brief filenames MUST use **alphabetical order** of entity IDs:
- `alan-dershowitz_virginia-giuffre.md` (a before v)
- `bcci_cia.md` (b before c)
- `donald-trump_roy-cohn.md` (d before r)

**NOT:**
- ~~`virginia-giuffre_alan-dershowitz.md`~~ (wrong order)
- ~~`roy-cohn_donald-trump.md`~~ (wrong order)

### Audit Command
```bash
# Find connections in JSON without briefs
# Run from T:\
python -c "
import json
import os
with open('website/data/connections.json') as f:
    connections = json.load(f)['connections']
for c in connections:
    ids = sorted([c['source'], c['target']])
    brief_path = f'website/briefs/connections/{ids[0]}_{ids[1]}.md'
    if not os.path.exists(brief_path):
        print(f'PENDING: {c[\"source\"]} <-> {c[\"target\"]}')
"
```

---

## Source Extraction Queue

Connections identified in source documents but not yet added to connections.json:

| Entity 1 | Entity 2 | Source Document | ECF/Page | Evidence Type | Extraction Date |
|----------|----------|-----------------|----------|---------------|-----------------|
| *Add connections here as discovered* | — | — | — | — | — |

---

## Update Log

| Date | Action | Count |
|------|--------|-------|
| 2026-01-20 | Initial audit - fixed 6 terramar naming mismatches | 0 pending |
| 2026-01-19 | File created | 0 pending |

---

*The Continuum Report — Connection Brief Tracking*
