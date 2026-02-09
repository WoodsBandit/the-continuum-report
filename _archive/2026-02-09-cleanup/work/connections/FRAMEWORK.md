# Connections Framework — Formalized Schema

**Version:** 3.0 (Updated 2026-01-05)
**Created:** 2025-12-25
**Based On:** `/continuum/connection_brief_reference.md`

---

## CORE PRINCIPLE

```
CONNECTION BRIEFS ARE THE SOURCE OF TRUTH.
No connection exists without a corresponding brief.
Each brief contains: quote + source + summary.
No subjective "strength" scoring.
```

---

## Connection Types (Relationship Nature)

These categorize the **nature** of a connection, not its "strength":

| Type | Code | Definition | Example |
|------|------|------------|---------|
| Employment | `EMP` | Formal employment relationship | Groff worked for Epstein |
| Attorney-Client | `ATT` | Legal representation | Dershowitz represented Epstein |
| Family | `FAM` | Blood or marriage relation | Ghislaine daughter of Robert Maxwell |
| Co-Defendant | `DEF` | Named together in legal proceedings | Maxwell in Epstein indictment |
| Co-Conspirator | `CON` | Named in NPA or indictment | Wexner in FBI July 2019 email |
| Accuser-Accused | `ACC` | Allegation relationship | Giuffre accused Prince Andrew |
| Witness-Subject | `WIT` | Testified about another entity | Farmer testified about Maxwell |
| Social | `SOC` | Documented social encounters | Trump at Mar-a-Lago with Epstein |
| Financial | `FIN` | Money flows, investments, donations | Wexner POA to Epstein |
| Institutional | `INST` | Institution investigated/arrested subject | FBI arrested Maxwell |
| Co-Mentioned | `MEN` | Named in same document | Both in flight logs |
| Same Proceeding | `PRO` | Both involved in same case | Both named in Giuffre v. Maxwell |

---

## Connection JSON Schema (v3.0 - Binary Model)

**Note:** `connections.json` is DERIVED from connection briefs via `build_connections_from_briefs.py`.

```json
{
  "id": "uuid-connection-id",
  "source": "entity-id-1",
  "target": "entity-id-2",
  "type": "EMP | ATT | SOC | FIN | etc.",
  "direction": "bidirectional | source-to-target | target-to-source",
  "summary": "One-sentence description of connection nature",
  "evidence": [
    {
      "ecf": "1328-44",
      "page": "54:2-17",
      "quote": "Actual quote from document",
      "source_link": "/sources/giuffre-v-maxwell/ecf-1328-44.pdf"
    }
  ],
  "briefFile": "entity1_entity2_connection.md",
  "sources_count": 3,
  "lastUpdated": "ISO-8601 timestamp"
}
```

**Binary Model:** A connection EXISTS in sources (documented with quote) or it DOESN'T. No subjective scoring.

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
| **Connection Type** | [Type from taxonomy] |
| **Sources** | [Number] court documents with quotes |

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

## Validation Checklist

For each new connection:

- [ ] Connection brief exists (source of truth)
- [ ] At least one quote extracted from source
- [ ] Source document link (hosted PDF)
- [ ] One-sentence summary written
- [ ] Type specified from taxonomy
- [ ] Direction indicated if asymmetric
- [ ] `build_connections_from_briefs.py` run to update JSON
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
