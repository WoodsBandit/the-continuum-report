# Connections Work Directory — Index

**Created:** 2025-12-25
**Purpose:** Centralized tracking for connection discovery and documentation work

---

## Directory Structure

```
/continuum/work/connections/
├── INDEX.md              # This file - directory overview
├── LOG.md                # Session-by-session work log
├── FRAMEWORK.md          # Formalized connection types and schemas
├── GAPS.md               # Known missing connections
└── queue/                # Pending connection briefs to generate
```

---

## Connection Framework Reference

**Primary Schema:** `/continuum/connection_brief_reference.md` (590 lines, comprehensive)

### Connection Types (Current)

| Type | Definition | Use When |
|------|------------|----------|
| **documented** | Direct mention in court filings, depositions, sworn testimony | ECF citation exists with explicit mention |
| **referenced** | Indirect mention or same document context | Both named in same filing without direct link |
| **interpreted** | Editorial inference from documentary patterns | Connection inferred from pattern analysis |

### Connection Subtypes (Expanded - per FRAMEWORK.md)

**Documented Subtypes:**
- `employer-employee` — Formal employment relationship
- `attorney-client` — Legal representation
- `family` — Blood or marriage relation
- `co-defendant` — Named together in legal proceedings
- `co-conspirator` — Named in NPA or indictment
- `accuser-accused` — Allegation relationship
- `witness-subject` — Testified about another entity
- `social-documented` — Documented social encounters
- `financial-documented` — Money flows, investments, donations

**Referenced Subtypes:**
- `co-mentioned` — Named in same document
- `same-proceeding` — Both involved in same case
- `same-location` — Both documented at same location

**Interpreted Subtypes:**
- `pattern-inferred` — Connection implied by documentary patterns
- `temporal-proximity` — Connected by time-based evidence
- `network-inferred` — Connected through shared network

---

## Current Connection Stats

**From connection_brief_reference.md (2025-12-21):**

| Metric | Count |
|--------|-------|
| Total Connections | 78 |
| Documented | 52 (67%) |
| Referenced | 15 (19%) |
| Interpreted | 11 (14%) |
| Connection Briefs | 16 files |
| Entities | 15 |

**After FBI Theme (2025-12-25):**

| New Connections | Type |
|-----------------|------|
| FBI ↔ Jeffrey Epstein | Institution-Entity |
| FBI ↔ Les Wexner | Institution-Entity (co-conspirator) |
| FBI ↔ Ghislaine Maxwell | Institution-Entity (arrest) |

---

## Priority Gaps

### Missing Entity Brief Updates

| Entity | Gap | Priority |
|--------|-----|----------|
| ~~**Les Wexner**~~ | ~~FBI co-conspirator designation NOT in brief~~ | ~~CRITICAL~~ **DONE** |
| Jeffrey Epstein | FBI investigation details sparse | HIGH |
| Ghislaine Maxwell | FBI arrest details sparse | HIGH |

### Missing Connection Briefs

| Connection | Basis | Priority |
|------------|-------|----------|
| ~~Wexner ↔ Epstein~~ | ~~Financial, employment, POA~~ | ~~HIGH~~ **DONE** |
| FBI ↔ DOJ | Institutional (NPA decision) | MEDIUM |
| Church Committee ↔ FBI | Congressional oversight | LOW |

### Connection Types Missing from Current Data

Per gap analysis in connection_brief_reference.md:
- No location entities (cannot map geographic patterns)
- No event entities (cannot create timelines)
- No relationship-type field
- No direction indicator
- No date ranges

---

## Work Queue

| Task | Status | Assigned |
|------|--------|----------|
| Update Wexner brief with FBI co-conspirator | DONE | Main session 2025-12-25 |
| Generate Wexner-Epstein connection brief | DONE | Main session 2025-12-25 |
| Audit all 16 connection briefs for subtypes | PENDING | — |
| Add FBI as institution entity | DONE | FBI Theme |
| Create FBI connection briefs | DONE | FBI Theme |
| Build entities.json infrastructure | PENDING | — |
| Build connections.json infrastructure | PENDING | — |

---

## Agent Assignments

| Agent | Task | Status |
|-------|------|--------|
| connection-builder | Add missing connections | ACTIVE |
| — | — | — |

---

## Cross-References

- `/continuum/connection_brief_reference.md` — Master schema reference
- `/continuum/data/connections.json` — Connection data store
- `/continuum/data/connection_briefs.json` — Brief summaries
- `/continuum/briefs/connections/` — Connection brief files
- `/continuum/agents/cross-reference-finder.md` — Discovery agent

---

*The Continuum Report — Connections Work Directory*
