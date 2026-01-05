# MASTER ENTITY INDEX — Usage Guide
## The Continuum Report

**Last Updated:** 2025-12-24
**Version:** 1.0

---

## Purpose

The entity index files serve as the **canonical master reference** for all entities (people, organizations, places, cases) mentioned across The Continuum Report source documents. They enable future Claude sessions to:
- Quickly locate any person, organization, or place mentioned in the source materials
- Find exact document citations for each entity mention
- Cross-reference entities across multiple sources
- Identify connection patterns through shared document appearances

---

## Entity Index Files

### 1. Primary Master Index
**File:** `T:\entities_index.md`
**Size:** 322 KB | 8,084 lines
**Format:** Markdown
**Content:** 2,008 unique entities with source citations

### 2. Consolidated Extraction (Phase 1)
**File:** `T:\agents\epstein-extraction\findings\synthesis\CONSOLIDATED_ENTITIES.md`
**Size:** 247 KB | 14,155 lines
**Format:** Markdown (alphabetically organized)
**Content:** 2,428 entities with deduplication applied

### 3. JSON Version (Programmatic Access)
**File:** `T:\website\data\entities-master.json`
**Size:** 516 KB
**Format:** JSON
**Structure:**
```json
{
  "people": { "Name": { "mentions": N, "sources": [...], "source_count": N } },
  "organizations": { ... },
  "locations": { ... }
}
```

---

## How to Use the Index

### For Research Sessions
1. **Search by Name** — Use Ctrl+F or `grep` to find any entity name
2. **Check Sources** — Each entry lists specific PDF documents where the entity appears
3. **Follow Citations** — Source paths point to documents in `T:\website\sources\`
4. **Cross-Reference** — Entities appearing in the same documents may be connected

### For Automated Processing
Use the JSON version (`entities-master.json`) for programmatic access:
```python
import json
with open(r'T:\website\data\entities-master.json') as f:
    entities = json.load(f)

# Find all sources mentioning "Alan Dershowitz"
alan_sources = entities['people'].get('Alan Dershowitz', {}).get('sources', [])
```

---

## Data Sources Indexed

| Source Directory | Documents | Priority |
|-----------------|-----------|----------|
| giuffre-v-maxwell | 97 | COMPLETE |
| maxwell-criminal | 8 | PARTIAL |
| financial-enablers | 27 | HIGH |
| doj-transparency-2025 | 9 | HIGH |
| florida-case | 7 | HIGH |
| fbi-vault | 8 | OCR REQUIRED |
| fbi-history | 16 | PENDING |
| cia-history | 20 | PENDING |
| regulatory-actions | 4 | PENDING |

---

## Top Entities by Mention Count

**Key Persons:**
| Entity | Mentions | Documents |
|--------|----------|-----------|
| Ghislaine Maxwell | 76-85 | 71+ |
| Jeffrey Epstein | 62-66 | 61+ |
| Virginia Giuffre (Roberts) | 58-66 | 40+ |
| Sarah Kellen | 36 | 36 |
| Alan Dershowitz | 31-33 | 30 |
| Prince Andrew | 29-31 | 28 |
| Nadia Marcinkova | 25 | - |
| Jean-Luc Brunel | 21 | - |
| Bill Clinton | 20-21 | 20 |
| Les Wexner | 8 | 7 |

---

## Deduplication Applied

The following name variants have been consolidated:
- **Virginia Giuffre (Roberts)** ← Virginia Roberts, Virginia L. Giuffre, Virginia Lee Roberts, Ms. Roberts
- **Jeffrey Epstein** ← Epstein
- **Ghislaine Maxwell** ← G. Maxwell, Maxwell
- **Prince Andrew** ← Duke of York, Andrew, Prince
- **Jean-Luc Brunel** ← Jean Luc Brunel, John Luc Brunel, Jon Luc Brunel
- **Les Wexner** ← Leslie Wexner, Wexner

---

## Related Resources

**Entity Briefs (38 Detailed Profiles):**
`T:\briefs\entity\`
- alan-dershowitz, bill-clinton, donald-trump, ghislaine-maxwell
- jeffrey-epstein, prince-andrew, virginia-giuffre, les-wexner
- jean-luc-brunel, sarah-kellen, jpmorgan-epstein, deutsche-bank
- And 26 more...

**Raw Extraction Data:**
`T:\agents\epstein-extraction\findings\`
- `court-filings\` — 96 individual document extractions
- `criminal-case\` — 4 individual document extractions
- `synthesis\` — Consolidated reports

**Custom Agents:**
`T:\agents\tasks\`
- entity-extractor.md — Entity extraction methodology
- cross-reference-finder.md — Connection discovery
- connection-builder.md — Relationship mapping

---

## Version History

- **v1.0 (2025-12-24)** — Initial release with Phase 1 extraction data
  - 2,008 unique entities from 100 court/criminal documents
  - JSON version for programmatic access
  - Deduplication for major entities

---

**END OF README**
