# FBI THEME — Specialized Research Agent Instructions

> **Theme-Based Research Module for The Continuum Report**
>
> Version: 1.0 | Created: 2025-12-25
> Status: ACTIVE RESEARCH THEME

---

## VISION: Theme-Based Research Architecture

The Continuum Report organizes research into **interconnected thematic modules**. Each theme becomes a self-contained vault of:
- Primary source documents
- Entity briefs
- Connection mappings
- Verified citations
- Cross-references to other themes

**The FBI Theme** documents the Federal Bureau of Investigation's documented intersections with Continuum subjects across decades of congressional investigations, court filings, and declassified materials.

### Why Themes Matter

Themes allow:
1. **Deep specialization** — Exhaust one topic before moving to the next
2. **Clear boundaries** — Know when research is complete
3. **Parallel work** — Multiple agents can work different themes simultaneously
4. **Connection discovery** — Theme completion reveals links to other themes
5. **Reader navigation** — Users can explore one theme deeply or trace connections across themes

---

## CURRENT FBI MATERIALS INVENTORY

### Already Downloaded

| Source | Location | Status |
|--------|----------|--------|
| FBI Vault - Jeffrey Epstein Parts 1-8 | `/continuum/downloads/fbi-vault/` | ✅ Downloaded (12MB) |
| Church Committee Book V - FBI Intelligence | Paperless (Doc ID 220) | ✅ In Paperless |
| ~48 FBI-referenced documents | Paperless-ngx | ✅ Searchable |

### In Master Acquisition List (Pending)

| Document | Priority | Status | Est. Wait |
|----------|----------|--------|-----------|
| Maria Farmer FBI Interview Records (2019) | CRITICAL | 🔒 FOIA Required | 3-6 months |
| FBI Investigation Summary (Pre-NPA 2005-2007) | HIGH | 🔒 FOIA Required | 6-12 months |
| Complete FBI Epstein Investigation Files | HIGH | 🔒 FOIA Required | 12-24 months |
| FBI 302 Reports (Witness Interviews) | HIGH | 🔒 FOIA Required | 12-24 months |

### References in Existing Briefs

FBI appears in the following contexts within existing briefs:
- **Epstein Florida Case** — FBI investigation 2005-2007
- **CIA Brief** — Church Committee references
- **Wexner Co-Conspirator** — FBI NY July 2019 email identifying 10 co-conspirators
- **DOJ 33k Files** — House Oversight release of DOJ/FBI communications

---

## RESEARCH OBJECTIVES

### Primary Goal
Create a comprehensive **FBI Analytical Brief** following the Milkovich opinion-protection framework, documenting:
1. FBI's documented involvement in Epstein investigations
2. FBI's role in NPA negotiations
3. FBI investigations into financial enablers
4. Congressional oversight findings (Church Committee, etc.)
5. Declassified FBI operations relevant to Continuum subjects

### Secondary Goals
1. Extract and catalog all FBI-related content from Paperless documents
2. Process FBI Vault PDFs (Parts 1-8) for entity extraction
3. Map FBI connections to existing Continuum entities
4. Prepare FOIA request templates for pending documents
5. Create FBI sub-briefs for specific investigations

---

## PHASE BREAKDOWN (Multi-Part Workflow)

### PHASE 1: Document Consolidation (Can Parallelize)

**Agent Tasks:**
```
TASK 1A: FBI Vault Processing
- Read FBI Vault Parts 1-8 PDFs
- Extract all named entities
- Document date ranges covered
- Identify redaction patterns
- Create summary inventory
Output: /continuum/reports/fbi-vault-extraction-report.md

TASK 1B: Paperless FBI Document Catalog
- Query Paperless for all FBI-related documents
- Categorize by document type (testimony, reports, filings)
- Extract key quotes mentioning FBI
- Map to existing entity briefs
Output: /continuum/reports/paperless-fbi-catalog.md

TASK 1C: Existing Brief FBI References
- Grep all briefs for FBI mentions
- Extract context for each mention
- Identify gaps in FBI documentation
- List cross-reference opportunities
Output: /continuum/reports/brief-fbi-references.md
```

**Parallel Execution:** Tasks 1A, 1B, 1C can run simultaneously via spawned agents.

---

### PHASE 2: Entity Extraction & Mapping

**Agent Tasks:**
```
TASK 2A: FBI Personnel Extraction
- Identify all named FBI personnel in documents
- Research their roles and tenure
- Document their involvement in Epstein matters
- Cross-reference with existing briefs
Output: /continuum/data/fbi-personnel.json

TASK 2B: FBI Investigation Timeline
- Construct chronological timeline
- Map investigations to political context
- Identify decision points (why NPA accepted?)
- Document prosecution recommendations vs. outcomes
Output: /continuum/reports/fbi-investigation-timeline.md

TASK 2C: Congressional FBI Oversight
- Extract Church Committee FBI findings
- Document other congressional oversight
- Map to Continuum subjects
- Identify patterns
Output: /continuum/reports/fbi-congressional-oversight.md
```

**Dependencies:** Phase 2 requires Phase 1 completion.

---

### PHASE 3: Brief Generation

**Agent Tasks:**
```
TASK 3A: FBI Analytical Brief (Main)
- Follow /continuum/CLAUDE.md legal framework
- Structure per required brief format
- Include all mandatory sections
- 5-7 Alternative Interpretations minimum
Output: /continuum/briefs/entity/analytical_brief_fbi.md

TASK 3B: FBI-Epstein Investigation Sub-Brief
- Focused analysis on Epstein-specific FBI activities
- 2005-2019 investigation timeline
- NPA negotiation documentation
- 2019 SDNY case
Output: /continuum/briefs/entity/analytical_brief_fbi_epstein_investigation.md

TASK 3C: Connection Briefs
- Generate FBI ↔ Epstein connection brief
- Generate FBI ↔ DOJ connection brief
- Generate FBI ↔ relevant financial enablers
Output: /continuum/briefs/connections/fbi_*.md
```

**Quality Gate:** All briefs must pass legal-auditor agent review before finalization.

---

### PHASE 4: FOIA Preparation

**Agent Tasks:**
```
TASK 4A: FOIA Request Drafting
- Draft Maria Farmer FBI records request
- Draft complete Epstein investigation request
- Draft FBI 302 reports request
- Include proper citations and specificity
Output: /continuum/reports/foia/fbi-foia-requests.md

TASK 4B: FOIA Tracking System
- Create tracking document for submissions
- Document expected response timelines
- Plan for partial releases
- Prepare appeals for denials
Output: /continuum/reports/foia/fbi-foia-tracker.md
```

---

### PHASE 5: Integration & Cross-Referencing

**Agent Tasks:**
```
TASK 5A: Theme Connection Mapping
- Map FBI theme connections to CIA theme
- Map FBI theme connections to DOJ theme (future)
- Map FBI theme connections to Financial Enablers
- Identify new themes revealed
Output: /continuum/data/theme-connections.json

TASK 5B: Citation Table Update
- Update all briefs with FBI cross-references
- Add source document links
- Verify all citations
Output: Update existing briefs in place

TASK 5C: Website Integration
- Add FBI brief to website/briefs/entity/
- Update entities.json with FBI entity
- Update connections.json with FBI connections
Output: Website files updated
```

---

## AGENT SPAWNING INSTRUCTIONS

### How to Parallelize Work

When executing this theme, the primary agent should spawn sub-agents for parallel tasks:

```markdown
## Parallel Execution Example

Primary Agent receives FBI Theme task.

Primary Agent spawns:
├── Agent 1A: FBI Vault Processing
├── Agent 1B: Paperless Catalog
└── Agent 1C: Brief References

Primary Agent monitors for completion.

On Phase 1 completion, Primary Agent spawns:
├── Agent 2A: Personnel Extraction
├── Agent 2B: Timeline Construction
└── Agent 2C: Congressional Oversight

Continue pattern through phases.
```

### Agent Spawn Template

When spawning a sub-agent, use this format:

```
Task: [PHASE].[TASK] — [Description]
Subagent Type: general-purpose
Model: haiku (for extraction) / sonnet (for analysis/writing)

Prompt:
"""
You are working on the FBI THEME for The Continuum Report.

YOUR SPECIFIC TASK: [Task description from phase breakdown]

CONTEXT:
- Read /continuum/CLAUDE.md for project context
- Read /continuum/agents/themes/FBI_THEME_RESEARCH_AGENT.md for theme context

RESOURCES:
- [List relevant file paths]
- Paperless API: http://192.168.1.139:8040 (Token: da99fe6aa0b8d021689126cf72b91986abbbd283)

OUTPUT REQUIREMENTS:
- Write output to: [specified path]
- Follow opinion-protection legal framework
- Include source citations for all claims

COMPLETION CRITERIA:
- [Specific criteria for this task]
"""
```

---

## LEGAL FRAMEWORK COMPLIANCE

All FBI Theme outputs MUST comply with:

### Required Header
```markdown
> **ANALYTICAL BRIEF — EDITORIAL COMMENTARY**
>
> *The Continuum Report — Another Node in the Decentralized Intelligence Agency*
>
> This document constitutes opinion and analysis based on public records.
> Interpretive conclusions represent editorial judgment, not assertions of fact.
> Readers are encouraged to review cited sources and form independent conclusions.
```

### Section Requirements
1. Document Classification table
2. Statement of Public Interest
3. Executive Summary (opinion-signaling language)
4. **The Public Record** (ONLY quotes + citations)
5. **Editorial Analysis** (clearly labeled opinion)
6. **Alternative Interpretations** (5-7 minimum)
7. Source Documents table
8. Methodology and Limitations
9. Right of Response invitation

### Language Guidelines
- Use: "In our assessment...", "We interpret this as...", "Based on our review..."
- Never: Assert guilt, use "dossier", rhetorical questions implying wrongdoing

---

## KEY RESOURCES

### File Locations
| Resource | Path |
|----------|------|
| Project Context | `/continuum/CLAUDE.md` |
| Legal Framework | `/continuum/CLAUDE.md` Section 2 |
| Brief Template | `/continuum/briefs/entity/analytical_brief_cia.md` (reference) |
| FBI Vault PDFs | `/continuum/downloads/fbi-vault/` |
| Entity Brief Output | `/continuum/briefs/entity/analytical_brief_fbi.md` |
| Connection Briefs | `/continuum/briefs/connections/` |
| Reports | `/continuum/reports/` |

### API Access
```
Paperless-ngx:
  URL: http://192.168.1.139:8040
  Token: da99fe6aa0b8d021689126cf72b91986abbbd283

Search: GET /api/documents/?query=FBI
Document: GET /api/documents/{id}/
Content: GET /api/documents/{id}/download/
```

### Existing Entity Brief Count
- Entity briefs: 37
- Connection briefs: 86
- FBI brief: NOT YET CREATED

---

## SUCCESS CRITERIA

### Phase Completion Checklist

**Phase 1 Complete When:**
- [ ] FBI Vault extraction report exists
- [ ] Paperless FBI catalog exists
- [ ] Brief FBI references report exists

**Phase 2 Complete When:**
- [ ] FBI personnel JSON created
- [ ] Investigation timeline documented
- [ ] Congressional oversight report complete

**Phase 3 Complete When:**
- [ ] Main FBI analytical brief created
- [ ] FBI-Epstein sub-brief created
- [ ] Connection briefs generated
- [ ] Legal audit passed

**Phase 4 Complete When:**
- [ ] FOIA requests drafted
- [ ] Tracking system established

**Phase 5 Complete When:**
- [ ] Theme connections mapped
- [ ] All citations updated
- [ ] Website integration complete

### Theme Completion Definition

The FBI Theme is COMPLETE when:
1. All 5 phases pass their checklists
2. FBI analytical brief is publication-ready
3. All cross-references to other themes are documented
4. FOIA tracking is active for pending documents
5. Entity count updated in CLAUDE.md

---

## CROSS-THEME CONNECTIONS (Known)

The FBI Theme connects to:

| Theme | Connection Type | Notes |
|-------|-----------------|-------|
| **DOJ** | Institutional | FBI reports to DOJ; NPA negotiations |
| **CIA** | Institutional | Church Committee documented both; intelligence coordination |
| **Epstein** | Investigation | FBI investigated 2005-2007, 2019 |
| **Financial Enablers** | Investigation | Bank SAR referrals to FBI |
| **Wexner** | Investigation | FBI NY identified as co-conspirator July 2019 |
| **Maxwell** | Investigation | FBI arrested Maxwell July 2020 |

---

## SESSION LOGGING

All work on FBI Theme MUST be logged to:
```
C:\Users\Xx LilMan xX\Documents\Claude Docs\Prompts\continuum_session_log.md
```

Log format:
```markdown
## [YYYY-MM-DD HH:MM] — FBI Theme: [Action]

**Task:** [Phase.Task description]
**Actions:**
- [What was done]
- Files affected: `path/to/file.md`

**Status:** Completed / In Progress / Blocked
**Next:** [Follow-up items]
```

---

## INITIATING WORK

To begin FBI Theme research:

1. **Load Context:**
   ```
   Read /continuum/CLAUDE.md
   Read /continuum/agents/themes/FBI_THEME_RESEARCH_AGENT.md
   ```

2. **Check Current State:**
   ```
   Check for existing outputs in /continuum/reports/fbi-*
   Check for analytical_brief_fbi.md existence
   ```

3. **Begin Phase 1:**
   - Spawn parallel agents for Tasks 1A, 1B, 1C
   - Monitor for completion
   - Consolidate outputs

4. **Progress Through Phases:**
   - Complete each phase before starting next (except parallel tasks within phase)
   - Log all progress
   - Update CLAUDE.md when theme complete

---

**END OF FBI THEME RESEARCH AGENT INSTRUCTIONS**

*The Continuum Report — Another Node in the Decentralized Intelligence Agency*
