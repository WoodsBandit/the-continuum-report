# Connections Framework — Formalized Schema

**Version:** 2.0
**Created:** 2025-12-25
**Based On:** `/continuum/connection_brief_reference.md`

---

## Connection Types Hierarchy

### Level 1: Evidence Basis

| Type | Code | Definition |
|------|------|------------|
| **Documented** | `DOC` | Direct mention in court filings, depositions, sworn testimony |
| **Referenced** | `REF` | Indirect mention or same document context |
| **Interpreted** | `INT` | Editorial inference from documentary patterns |

### Level 2: Relationship Nature (Subtypes)

#### Documented Subtypes (`DOC-*`)

| Subtype | Code | Definition | Example |
|---------|------|------------|---------|
| Employment | `DOC-EMP` | Formal employment relationship | Groff worked for Epstein |
| Attorney-Client | `DOC-ATT` | Legal representation | Dershowitz represented Epstein |
| Family | `DOC-FAM` | Blood or marriage relation | Ghislaine daughter of Robert Maxwell |
| Co-Defendant | `DOC-DEF` | Named together in legal proceedings | Maxwell in Epstein indictment |
| Co-Conspirator | `DOC-CON` | Named in NPA or indictment as co-conspirator | Wexner in FBI July 2019 email |
| Accuser-Accused | `DOC-ACC` | Allegation relationship | Giuffre accused Prince Andrew |
| Witness-Subject | `DOC-WIT` | Testified about another entity | Farmer testified about Maxwell |
| Social | `DOC-SOC` | Documented social encounters | Trump at Mar-a-Lago with Epstein |
| Financial | `DOC-FIN` | Money flows, investments, donations | Wexner POA to Epstein |
| Institutional | `DOC-INST` | Institution investigated/arrested subject | FBI arrested Maxwell |

#### Referenced Subtypes (`REF-*`)

| Subtype | Code | Definition | Example |
|---------|------|------------|---------|
| Co-Mentioned | `REF-MEN` | Named in same document | Both in flight logs |
| Same Proceeding | `REF-PRO` | Both involved in same case | Both named in Giuffre v. Maxwell |
| Same Location | `REF-LOC` | Both documented at same location | Both at Little St. James |

#### Interpreted Subtypes (`INT-*`)

| Subtype | Code | Definition | Example |
|---------|------|------------|---------|
| Pattern-Inferred | `INT-PAT` | Connection implied by documentary patterns | Network analysis suggests link |
| Temporal-Proximity | `INT-TMP` | Connected by time-based evidence | Both active 1998-2008 |
| Network-Inferred | `INT-NET` | Connected through shared network | Both connected to same third party |

---

## Connection JSON Schema (v2.0)

```json
{
  "id": "uuid-connection-id",
  "source": "entity-id-1",
  "target": "entity-id-2",
  "type": "documented | referenced | interpreted",
  "subtype": "DOC-CON | DOC-EMP | etc.",
  "direction": "bidirectional | source-to-target | target-to-source",
  "strength": 0-100,
  "dateRange": {
    "start": "YYYY-MM-DD | YYYY-MM | YYYY",
    "end": "YYYY-MM-DD | YYYY-MM | YYYY | ongoing | unknown",
    "precision": "day | month | year | approximate"
  },
  "summary": "One-sentence description of connection nature",
  "evidence": [
    {
      "ecf": "1328-44",
      "page": "54:2-17",
      "quote": "Actual quote from document",
      "description": "Document description",
      "filed": "MM/DD/YY"
    }
  ],
  "briefFile": "connection_brief_filename.md",
  "created": "ISO-8601 timestamp",
  "lastUpdated": "ISO-8601 timestamp",
  "createdBy": "agent-name | manual"
}
```

---

## Entity Types (Expanded)

| Type | Code | Definition | Examples |
|------|------|------------|----------|
| Person | `PER` | Individual human | Jeffrey Epstein, Virginia Giuffre |
| Organization | `ORG` | Company, foundation, nonprofit | Terramar Project, L Brands |
| Institution | `INST` | Government agency, law enforcement | FBI, DOJ, Palm Beach PD |
| Case | `CASE` | Legal proceeding | Giuffre v. Maxwell |
| Location | `LOC` | Property, address, geographic area | Little St. James, 9 E 71st St |
| Event | `EVT` | Specific incident with date | 2008 NPA signing, July 2019 arrest |
| Document | `DOC` | Specific court filing or release | Church Committee Book V |

---

## Connection Brief Template (v2.0)

```markdown
# [Entity 1] ↔ [Entity 2] — Connection Analysis

> **ANALYTICAL BRIEF — EDITORIAL COMMENTARY**
>
> Connection Type: [TYPE-SUBTYPE]
> Direction: [bidirectional | source → target]
> Date Range: [start] – [end]

---

## Document Classification

| | |
|---|---|
| **Subjects** | [Entity 1], [Entity 2] |
| **Connection Type** | [Full type description] |
| **Evidence Basis** | [Number] court documents |
| **Strength Score** | [0-100] |

---

## The Public Record

### Primary Evidence

**ECF Doc. XXXX-XX** ([Description], filed [Date]):
> [Direct quote establishing connection]

[Repeat for each primary source]

---

## Connection Context

[Factual description of relationship nature, timeline, and documented interactions]

---

## Editorial Analysis

**The following represents the opinions and interpretations of The Continuum Report.**

[Clearly labeled opinion content about significance of connection]

---

## Alternative Interpretations

A reader reviewing these same documents might reasonably conclude:
- [Relationship-specific alternative 1]
- [Relationship-specific alternative 2]
- [Relationship-specific alternative 3]

---

## Source Documents

| ECF Doc. No. | Filed | Document Description |
|--------------|-------|---------------------|
| XXXX-XX | MM/DD/YY | [Description] |

---

## Cross-References

- [Entity 1 Brief](link)
- [Entity 2 Brief](link)
- Related connections: [list]

---

*Generated: [Date] | The Continuum Report*
```

---

## Strength Score Calculation

| Component | Points | Max |
|-----------|--------|-----|
| Direct ECF citation | +20 per | 60 |
| Bidirectional mention | +15 | 15 |
| Multiple document types | +10 | 10 |
| Date range documented | +5 | 5 |
| Subtype specified | +5 | 5 |
| Quote extracted | +5 | 5 |

**Total possible:** 100

---

## Validation Checklist

For each new connection:

- [ ] Type accurately reflects evidence basis
- [ ] Subtype specified if documented
- [ ] At least one ECF citation
- [ ] Summary describes nature (not just "connected")
- [ ] Direction indicated if asymmetric
- [ ] Date range included if known
- [ ] Strength score calculated
- [ ] Alternative interpretations are relationship-specific
- [ ] Added to connections.json
- [ ] Connection brief generated (if significant)
- [ ] Entity briefs cross-referenced

---

## Quality Standards

1. **No generic placeholders** — Extract actual quotes, not "Document references connection"
2. **Relationship-specific alternatives** — Tailor to connection type, not copy-paste
3. **Cite page numbers** — ECF doc + page:line when possible
4. **Date precision** — Note if approximate vs. exact
5. **Direction matters** — Accuser→Accused is different from Accused→Accuser

---

*The Continuum Report — Connections Framework v2.0*
