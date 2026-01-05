# Epstein Document Extraction Agent

## Mission

Systematically extract, analyze, and catalog information from ALL Epstein-related files in the Continuum archive. Use parallel sub-agents to maximize throughput while maintaining quality and citation standards.

---

## Document Corpus

### Primary Sources

| Location | Files | Type | Status |
|----------|-------|------|--------|
| `T:\downloads\house-oversight\extracted\epstein-pdf\` | 33,564 | DOJ 33k release | Image-based, needs OCR |
| `T:\downloads\doj-combined\` | 7 datasets | DOJ combined PDFs | Mixed |
| `T:\downloads\fbi-vault\` | 8 parts | FBI Vault release | Mixed |
| `T:\website\sources\giuffre-v-maxwell\` | ~50 | Court filings | Text-searchable |
| `T:\website\sources\maxwell-criminal\` | ~30 | Criminal case | Text-searchable |
| `T:\website\sources\florida-case\` | ~20 | Florida prosecution | Text-searchable |
| `T:\website\sources\depositions\` | ~15 | Witness depositions | Text-searchable |

### Estimated Total: 33,700+ documents

---

## Extraction Methodology

### Phase 1: Text-Searchable Documents (Priority)

Target directories with existing text layers:
1. `giuffre-v-maxwell/` — Court filings, depositions
2. `maxwell-criminal/` — Criminal case documents
3. `florida-case/` — Florida prosecution
4. `depositions/` — Witness statements
5. `financial-enablers/` — Bank documents

**Sub-agent tasks:**
- Extract all text content
- Identify entities (names, organizations, locations)
- Extract dates and timeline events
- Catalog document metadata
- Flag redacted sections with hidden text

### Phase 2: DOJ 33k Files (OCR Required)

For image-based PDFs:
1. Run OCR extraction
2. Quality-check OCR output
3. Extract entities and events
4. Cross-reference with Phase 1 findings

### Phase 3: Cross-Reference & Synthesis

1. Build entity relationship map
2. Construct master timeline
3. Identify connection patterns
4. Generate analytical briefs for new entities

---

## Sub-Agent Architecture

### Parallel Processing Model

```
MASTER AGENT (Overseer)
    │
    ├── Sub-Agent 1: Court Filings Extractor
    │   └── Process: giuffre-v-maxwell/*.pdf
    │
    ├── Sub-Agent 2: Criminal Case Extractor
    │   └── Process: maxwell-criminal/*.pdf
    │
    ├── Sub-Agent 3: Deposition Extractor
    │   └── Process: depositions/*.pdf
    │
    ├── Sub-Agent 4: Financial Documents Extractor
    │   └── Process: financial-enablers/*.pdf
    │
    └── Sub-Agent 5: Entity Synthesizer
        └── Compile findings into master index
```

### Sub-Agent Output Format

Each sub-agent produces:
```markdown
## [Document Name]

**File:** [path]
**Pages:** [count]
**Date:** [document date if available]

### Entities Mentioned
- **People:** [names]
- **Organizations:** [orgs]
- **Locations:** [places]
- **Dates:** [timeline events]

### Key Content
[Summary of document content]

### Quotes of Interest
> "[Direct quote]" (Page X)

### Connections to Other Documents
- Related to: [other documents]
- Cross-references: [entities appearing elsewhere]
```

---

## Output Structure

```
T:\agents\epstein-extraction\
├── index.md              # This file
├── log.md                # Activity log (update frequently)
├── findings/
│   ├── court-filings/    # Giuffre v Maxwell extractions
│   ├── criminal-case/    # Maxwell criminal extractions
│   ├── depositions/      # Deposition extractions
│   ├── financial/        # Financial document extractions
│   └── entities/         # Entity-specific compilations
└── synthesis/
    ├── master-timeline.md
    ├── entity-index.md
    └── connection-map.md

T:\reports\epstein-extraction\
├── extraction-summary-[date].md
└── new-entities-[date].md
```

---

## Extraction Targets

### Priority Entities to Track

**Already Documented (37 briefs):**
- Jeffrey Epstein, Ghislaine Maxwell, Virginia Giuffre
- Prince Andrew, Bill Clinton, Donald Trump, Alan Dershowitz
- Les Wexner, Glenn Dubin, Jean-Luc Brunel
- Sarah Kellen, Nadia Marcinkova, Lesley Groff
- [See `/briefs/entity/` for full list]

**Known but Undocumented:**
- Adriana Ross
- Maritza Vasquez
- Igor Zinoviev
- Haley Robson
- Courtney Wild
- [Expand as discovered]

**To Discover:**
- Names under "Jane Doe" designations
- Financial intermediaries
- Property managers
- Travel arrangers
- Other staff/associates

### Priority Information Types

1. **Flight logs** — Passengers, dates, destinations
2. **Financial transactions** — Amounts, parties, dates
3. **Property records** — Addresses, ownership, visitors
4. **Communications** — Emails, messages, calls
5. **Witness statements** — Testimony, allegations
6. **Legal filings** — Motions, orders, settlements

---

## Quality Standards

### Citation Format
Every extracted fact must include:
- Document name
- Page number
- Direct quote when possible

### Verification
- Cross-reference claims across multiple documents
- Flag contradictions or discrepancies
- Note confidence level (verified/alleged/disputed)

### Legal Compliance
- Follow opinion-protection framework
- Distinguish facts from allegations
- Include alternative interpretations for sensitive claims

---

## Commands

### Start Full Extraction
```bash
# Spawn master agent with all sub-agents
# See agent definition: T:\agents\epstein-extractor.md
```

### Check Progress
```bash
# Read log: T:\agents\epstein-extraction\log.md
# Check findings: T:\agents\epstein-extraction\findings\
```

### Generate Summary Report
```bash
# Compile all findings into summary
# Output: T:\reports\epstein-extraction\
```

---

## Integration

### Feeds Into:
- Entity briefs (`/briefs/entity/`)
- Connection briefs (`/briefs/connections/`)
- Master timeline
- Website data (`/website/data/entities.json`)

### Uses:
- Redaction extractor findings
- Paperless-ngx document index
- Existing brief content

---

---

## Current Status

**Phase 1: COMPLETE** (2025-12-24)

### Processing Summary

| Source | Files | Status |
|--------|-------|--------|
| `giuffre-v-maxwell/` | 96 PDFs | ✅ COMPLETE (100%) |
| `maxwell-criminal/` | 4 PDFs | ✅ COMPLETE (100%) |
| `florida-case/` | 6 PDFs | ⚠️ Partial (size limits) |
| `depositions/` | — | ⏭️ SKIPPED (directory not found) |

### Extraction Statistics

| Metric | Count |
|--------|-------|
| Files Processed | 100 |
| Pages Analyzed | ~1,500 |
| Entity References | 5,105 |
| Organizations | 2 |
| Locations | 210 |
| Dated Events | 3,096 |
| Quotes Captured | 1,063 |

### Synthesis Products

| File | Description |
|------|-------------|
| `synthesis/entity-index.md` | Master categorized index (14KB) |
| `synthesis/connection-map.md` | Relationship networks (16KB) |
| `findings/court-filings/_summary.json` | Aggregate statistics |

### Critical Documents Identified

1. **ecf-1320-38.pdf** — Virginia Giuffre Deposition (747 quotes)
2. **ecf-1320-13.pdf** — Investigation Document (215 named individuals)
3. **ghislaine-maxwell-indictment-2020-07-02.pdf** — Full indictment with grooming methodology

### Phase 2 Priorities

1. OCR processing of DOJ 33,564 image-based PDFs
2. FBI Vault document extraction (8 parts)
3. Financial enablers document processing
4. Cross-document relationship graph generation

---

*Created: 2025-12-24*
*Last Updated: 2025-12-24*
*The Continuum Report — Another Node in the Decentralized Intelligence Agency*
