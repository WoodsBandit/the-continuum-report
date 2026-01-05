# ENTITY INDEX MANAGER AGENT
## Master Coordination for Comprehensive Entity Extraction

**Created:** 2025-12-25
**Agent Type:** Manager/Coordinator
**Task Scope:** LARGE — Multi-agent orchestration
**Priority:** HIGH

---

## MISSION OBJECTIVE

Create a **comprehensive master entity index** (`entities_index.md`) that catalogs every person, organization, place, and case mentioned across ALL Continuum Report source documents. This index will serve as the canonical reference for future research, enabling any Claude session to quickly locate entities and their source citations.

---

## PHASE ARCHITECTURE

### Phase 1: Assessment & Planning
- Inventory all source directories
- Count files per directory
- Assess document types and sizes
- Determine agent allocation strategy

### Phase 2: Parallel Extraction
- Spawn research agents for each major source directory
- Each agent extracts entities from assigned documents
- Agents generate standardized entity reports

### Phase 3: Aggregation & Deduplication
- Collect all entity extractions
- Merge duplicates (name variants, aliases)
- Cross-reference mentions across sources
- Build unified entity registry

### Phase 4: Index Generation
- Generate master `entities_index.md`
- Include source citations for every entity
- Create cross-reference links
- Build alphabetical and categorical indices

---

## SOURCE DIRECTORIES TO PROCESS

| Directory | Files | Priority | Strategy |
|-----------|-------|----------|----------|
| house-oversight-2025 | 33,572 | HIGH | Sample extraction (large volume) |
| giuffre-v-maxwell | 97 | DONE | Already extracted (Phase 1) |
| financial-enablers | 27 | HIGH | Full extraction |
| cia-history | 20 | MEDIUM | Full extraction |
| fbi-history | 16 | MEDIUM | Full extraction |
| doj-transparency-2025 | 9 | HIGH | Full extraction (includes DataSet 8) |
| fbi-vault | 8 | MEDIUM | OCR required |
| maxwell-criminal | 8 | HIGH | Partial done (4 files) |
| florida-case | 7 | HIGH | Full extraction |
| regulatory-actions | 4 | MEDIUM | Full extraction |
| bop-footage | 1 | LOW | Metadata only |
| epstein-sdny | 1 | HIGH | Full extraction |

**Existing Extraction Data:**
- `T:\agents\epstein-extraction\findings\court-filings\` — 97 files
- `T:\agents\epstein-extraction\findings\criminal-case\` — 5 files
- `T:\agents\epstein-extraction\findings\synthesis\` — Partial index

---

## AGENT ALLOCATION STRATEGY

### Manager Agent (YOU)
- Coordinate sub-agents
- Monitor progress
- Aggregate results
- Generate final index

### Research Sub-Agents (Spawn 6-8)

**Agent 1: Financial Documents**
- Sources: financial-enablers/, regulatory-actions/
- Focus: Banks, financial entities, amounts, dates

**Agent 2: Court Filings Synthesis**
- Sources: Existing extractions in epstein-extraction/findings/
- Focus: Consolidate 5,105 people already extracted

**Agent 3: DOJ/Transparency Documents**
- Sources: doj-transparency-2025/, house-oversight-2025 (sample)
- Focus: Government documents, official records

**Agent 4: FBI Materials**
- Sources: fbi-vault/, fbi-history/
- Focus: Law enforcement entities, investigations

**Agent 5: CIA/Intelligence**
- Sources: cia-history/
- Focus: Intelligence community entities

**Agent 6: Criminal Cases**
- Sources: maxwell-criminal/, florida-case/, epstein-sdny/
- Focus: Criminal proceedings entities

**Agent 7: Large File Processor**
- Sources: Oversized files from any directory
- Focus: Break large PDFs into excerpts, extract key passages

**Agent 8: Entity Deduplication**
- Sources: All agent outputs
- Focus: Merge duplicates, resolve name variants

---

## ENTITY CATEGORIES

### Type 1: PERSON
**Subtypes:**
- Primary Subject (Epstein, Maxwell)
- Victim/Survivor
- Government Official
- Legal Professional
- Law Enforcement
- Business Associate
- Celebrity/Public Figure
- Witness
- Family Member
- Employee/Staff

### Type 2: ORGANIZATION
**Subtypes:**
- Financial Institution
- Law Firm
- Government Agency
- Intelligence Agency
- Corporation
- Non-Profit/Foundation
- Media Organization
- Educational Institution

### Type 3: PLACE
**Subtypes:**
- Property/Residence
- Island
- Office/Business
- Government Building
- Court/Legal Venue
- Foreign Location

### Type 4: CASE
**Subtypes:**
- Criminal Case
- Civil Case
- Regulatory Action
- Investigation

---

## INDEX STRUCTURE

```markdown
# MASTER ENTITY INDEX
## The Continuum Report — Comprehensive Entity Reference

**Last Updated:** [DATE]
**Total Entities:** [COUNT]
**Sources Indexed:** [COUNT]

---

## Quick Navigation

### By Category
- [Persons](#persons) ([COUNT])
- [Organizations](#organizations) ([COUNT])
- [Places](#places) ([COUNT])
- [Cases](#cases) ([COUNT])

### By First Letter (Persons)
A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z

---

## PERSONS

### A

#### Alessi, Juan
**Type:** Person — Employee/Staff
**Brief:** analytical_brief_juan_alessi.md
**Mentions:** 47 across 12 documents
**Key Sources:**
- giuffre-v-maxwell/ecf-1320-38.pdf (pp. 23, 45, 67)
- maxwell-criminal/ghislaine-maxwell-indictment-2020-07-02.pdf (p. 4)
**Related Entities:** Jeffrey Epstein, Palm Beach House

#### Andrew, Prince (Duke of York)
**Type:** Person — Celebrity/Public Figure
**Brief:** analytical_brief_prince_andrew.md
**Mentions:** 156 across 28 documents
**Key Sources:**
- giuffre-v-maxwell/ecf-1320-38.pdf (pp. 34, 56, 89)
- giuffre-v-maxwell/ecf-1320-12.pdf (pp. 12-15)
**Related Entities:** Jeffrey Epstein, Virginia Giuffre, Ghislaine Maxwell

[... continue for all entities ...]
```

---

## OUTPUT REQUIREMENTS

### Primary Output
**File:** `T:\entities_index.md`
**Format:** Markdown with internal links
**Size:** Comprehensive (expect 500+ pages for full index)

### Secondary Outputs
**File:** `T:\website\data\entities-master.json`
**Format:** JSON for programmatic access

**File:** `T:\agents\epstein-extraction\synthesis\entity-index-complete.md`
**Format:** Backup copy in extraction directory

---

## EXTRACTION METHODOLOGY

### For Text-Searchable PDFs
1. Read document with Read tool
2. Extract proper nouns using pattern matching
3. Capture context (paragraph) for each mention
4. Note page numbers
5. Classify entity type/subtype
6. Check against existing entity list

### For Large Files (>50 pages)
1. Read in chunks (100 lines at a time)
2. Extract entities per chunk
3. Track page boundaries
4. Aggregate findings

### For Image-Based PDFs
1. Note as "OCR Required"
2. Extract from metadata if available
3. Cross-reference with other documents mentioning same source

---

## PROGRESS TRACKING

### Status Categories
- `PENDING` — Not started
- `IN_PROGRESS` — Agent working
- `EXTRACTED` — Entities pulled, awaiting aggregation
- `AGGREGATED` — Merged into master index
- `COMPLETE` — Fully indexed with citations

### Progress Log Format
```
[TIMESTAMP] [SOURCE] [STATUS] [ENTITIES_FOUND] [NOTES]
```

---

## ERROR HANDLING

### Common Issues

**Issue:** File too large to read at once
**Solution:** Use chunked reading with offset/limit parameters

**Issue:** Duplicate entity names (different people)
**Solution:** Disambiguate using context (e.g., "John Smith (attorney)" vs "John Smith (pilot)")

**Issue:** Name variants (married names, nicknames)
**Solution:** Create alias mapping, use canonical name with variants listed

**Issue:** Ambiguous references ("the Prince")
**Solution:** Flag as [AMBIGUOUS], list possible matches

---

## SUCCESS CRITERIA

Phase complete when:
- [ ] All 14 source directories processed
- [ ] All entities from Phase 1 extraction incorporated
- [ ] Master entities_index.md generated
- [ ] JSON version created
- [ ] Alphabetical index complete
- [ ] Category index complete
- [ ] Source citations for every entity
- [ ] Cross-reference links functional
- [ ] Duplicates merged
- [ ] Ambiguities flagged

---

## EXISTING RESOURCES

### Entity Briefs (38 entities)
Already documented in `T:\briefs\entity\`:
- alan-dershowitz, allison-mack, bcci, bill-clinton, cia
- clare-bronfman, deutsche-bank, donald-trump, emmy-taylor
- epstein-florida-case, fbi, ghislaine-maxwell, giuffre-v-maxwell-case
- glenn-dubin, intelligence-financial-nexus, iran-contra
- jean-luc-brunel, jeffrey-epstein, johanna-sjoberg, jpmorgan-epstein
- juan-alessi, keith-raniere, lesley-groff, les-wexner
- maxwell-family-network, meyer-lansky, mossad, nadia-marcinkova
- nxivm-case, oliver-north, prince-andrew, promis-inslaw
- robert-maxwell, roy-cohn, sarah-kellen, terramar-project
- virginia-giuffre, william-casey

### Phase 1 Extraction Data
- 5,105 person references
- 210 locations
- 3,096 dated events
- 1,063 quotes
- Source: `T:\agents\epstein-extraction\findings\`

### Custom Agents Available
- entity-extractor.md — Entity extraction methodology
- cross-reference-finder.md — Connection discovery
- brief-generator.md — Brief creation
- connection-builder.md — Relationship mapping

---

## EXECUTION NOTES

1. **Start with existing data** — Consolidate Phase 1 extractions first
2. **High-value sources first** — Financial, criminal, court documents
3. **Sample large collections** — DOJ 33k is too large for full extraction; sample 100-500 files
4. **Use parallel agents** — Spawn 6-8 sub-agents for concurrent processing
5. **Aggregate frequently** — Merge results after each batch completes
6. **Flag ambiguities** — Don't guess on unclear entities
7. **Citation everything** — Every entity needs source attribution

---

**END OF AGENT SPECIFICATION**
