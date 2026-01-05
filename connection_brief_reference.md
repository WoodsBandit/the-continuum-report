# Connection Brief System Reference

**Generated:** 2025-12-21 | **Updated:** 2026-01-05
**Purpose:** Comprehensive reference for The Continuum Report's entity and connection system

---

## ARCHITECTURAL PRINCIPLE

```
CONNECTION BRIEFS ARE THE SOURCE OF TRUTH.
No connection exists without a corresponding brief.
Each brief contains: quote + source + summary.
No subjective "strength" scoring.
```

---

## Table of Contents

1. [File Locations](#1-file-locations)
2. [Entity JSON Structure](#2-entity-json-structure)
3. [Connections JSON Structure](#3-connections-json-structure)
4. [Connection Types Taxonomy](#4-connection-types-taxonomy)
5. [Entity Types Inventory](#5-entity-types-inventory)
6. [Existing Connection Documentation](#6-existing-connection-documentation)
7. [Brief Template Structure](#7-brief-template-structure)
8. [Gap Analysis](#8-gap-analysis)
9. [Normalization Recommendations](#9-normalization-recommendations)

---

## 1. File Locations

### Authoritative Data Files

| File | Path | Lines | Last Modified | Purpose |
|------|------|-------|---------------|---------|
| **entities.json** | `/continuum/data/entities.json` | 2,227 | Dec 20 | Primary entity store (15 entities) |
| **connections.json** | `/continuum/data/connections.json` | ~1,200 | Dec 16 | Connection pairs with evidence |
| **connection_briefs.json** | `/continuum/data/connection_briefs.json` | ~1,400 | Dec 20 | Per-entity connection summaries |
| **hierarchy.json** | `/continuum/data/hierarchy.json` | ~120 | Dec 18 | Entity categorization |

### Website Data (Subset)

| File | Path | Purpose |
|------|------|---------|
| entities.json | `/continuum/website/data/entities.json` | Simplified for web display |
| connections.json | `/continuum/website/data/connections.json` | Web-optimized connections |

### Brief Files

| Type | Path | Count |
|------|------|-------|
| Analytical Briefs | `/continuum/briefs/analytical_brief_*.md` | 40 files |
| Connection Briefs | `/continuum/briefs/connections/*_connections.md` | 16 files |

---

## 2. Entity JSON Structure

### Full Entity Schema

```json
{
  "id": "entity-slug",
  "name": "Human Readable Name",
  "type": "person | case | organization",
  "status": "Conviction status or legal standing",
  "summary": "Truncated summary (~500 chars)...",
  "full_summary": "Complete summary paragraph",
  "brief_file": "analytical_brief_entity_name.md",
  "brief_url": "/briefs/entity-slug.html",
  "document_type": "Editorial analysis of civil litigation records",
  "primary_sources": "*Case Name*, No. XX-cv-XXXXX (Court)",
  "sources": [
    {
      "ecf": "1328-44",
      "description": "Deposition of [Name]",
      "filed": "01/05/24"
    }
  ],
  "ecf_citations": ["1328-44", "1331-12"],
  "mentions": ["other-entity-id", "another-entity-id"],
  "mention_details": {
    "other-entity-id": {
      "count": 12,
      "briefFile": "entity1_entity2_connection.md"
    }
  },
  "connections": [
    {
      "targetId": "other-entity-id",
      "type": "SOC | FIN | EMP | ATT | etc.",
      "summary": "One-sentence description of connection",
      "sources_count": 3,
      "briefFile": "entity1_entity2_connection.md"
    }
  ],
  "tags": ["never-charged", "legal", "government"],
  "last_updated": "2025-12-16T01:17:54.194357Z",
  "parsed_from": "/continuum/briefs/analytical_brief_entity_name.md"
}
```

### Representative Entity Examples

#### Person Entity (with allegations)
```json
{
  "id": "prince-andrew",
  "name": "Prince Andrew",
  "type": "person",
  "status": "Never criminally charged; civil lawsuit settled February 2022 without admission of liability",
  "tags": ["never-charged", "royalty"],
  "connections": [
    {"targetId": "virginia-giuffre", "type": "ACC", "sources_count": 27, "briefFile": "prince-andrew_virginia-giuffre.md"},
    {"targetId": "ghislaine-maxwell", "type": "SOC", "sources_count": 14, "briefFile": "ghislaine-maxwell_prince-andrew.md"},
    {"targetId": "jeffrey-epstein", "type": "SOC", "sources_count": 10, "briefFile": "jeffrey-epstein_prince-andrew.md"}
  ]
}
```

#### Case Entity
```json
{
  "id": "giuffre-v-maxwell-case",
  "name": "Giuffre v. Maxwell Civil Case",
  "type": "case",
  "status": "Settled May 2017; documents unsealed January 2024",
  "tags": ["case", "settled"],
  "connections": [
    {"targetId": "ghislaine-maxwell", "type": "DEF", "sources_count": 18},
    {"targetId": "jeffrey-epstein", "type": "MEN", "sources_count": 12},
    {"targetId": "virginia-giuffre", "type": "PRO", "sources_count": 11}
  ]
}
```

#### Organization Entity
```json
{
  "id": "terramar-project",
  "name": "The Terramar Project",
  "type": "organization",
  "status": "Dissolved 2019",
  "tags": ["organization", "dissolved"],
  "connections": [
    {"targetId": "ghislaine-maxwell", "type": "INST", "sources_count": 23, "briefFile": "ghislaine-maxwell_terramar-project.md"},
    {"targetId": "jeffrey-epstein", "type": "FIN", "sources_count": 10, "briefFile": "jeffrey-epstein_terramar-project.md"}
  ]
}
```

---

## 3. Connections JSON Structure

**Note:** `connections.json` is DERIVED from connection briefs via `build_connections_from_briefs.py`.

### Connection Pair Schema (`connections.json`)

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

### Connection Types (Relationship Nature)

| Type | Code | Definition |
|------|------|------------|
| Employment | `EMP` | Formal employment relationship |
| Attorney-Client | `ATT` | Legal representation |
| Family | `FAM` | Blood or marriage relation |
| Co-Defendant | `DEF` | Named together in legal proceedings |
| Co-Conspirator | `CON` | Named in NPA or indictment |
| Accuser-Accused | `ACC` | Allegation relationship |
| Witness-Subject | `WIT` | Testified about another entity |
| Social | `SOC` | Documented social encounters |
| Financial | `FIN` | Money flows, investments, donations |
| Institutional | `INST` | Institution investigated/arrested subject |
| Co-Mentioned | `MEN` | Named in same document |
| Same Proceeding | `PRO` | Both involved in same case |

---

## 4. Connection Types Taxonomy

### Connection Types (Relationship Nature)

These categorize the **nature** of a connection, not subjective "strength":

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

### Binary Model

A connection either EXISTS in a source document or it DOESN'T:
- **EXISTS:** Documented with quote + source + summary in connection brief
- **DOESN'T EXIST:** No connection brief, no connection

No subjective scoring. No "strength" levels. No "evidence levels."

---

## 5. Entity Types Inventory

### Currently Defined Entity Types

| Type | Count | Examples |
|------|-------|----------|
| **person** | 13 | Jeffrey Epstein, Ghislaine Maxwell, Virginia Giuffre |
| **case** | 2 | Giuffre v. Maxwell, Epstein Florida Case |
| **organization** | 1 | The Terramar Project |

### Tags in Use

| Tag | Count | Meaning |
|-----|-------|---------|
| never-charged | 8 | Subject has not faced criminal charges |
| associate | 5 | Inner circle associate |
| government | 2 | Government official |
| convicted | 2 | Criminal conviction |
| case | 2 | Legal case entity |
| finance | 3 | Financial industry connection |
| victim-witness | 1 | Victim/witness in proceedings |
| legal | 1 | Legal profession |
| royalty | 1 | Royal family member |
| deceased | 1 | Deceased individual |
| dissolved | 1 | Dissolved organization |
| settled | 1 | Settled case |

### Missing Entity Types (Gap)

| Suggested Type | Use Case |
|----------------|----------|
| **location** | Little St. James, Zorro Ranch, 9 E 71st St |
| **document** | Specific court filings as entities |
| **event** | 2008 NPA signing, 2019 arrest |
| **institution** | FBI, DOJ SDNY, Palm Beach PD |

---

## 6. Existing Connection Documentation

### Connection Brief Files

16 connection brief markdown files exist in `/continuum/briefs/connections/`:

| Entity | File | Size |
|--------|------|------|
| alan-dershowitz | alan-dershowitz_connections.md | 10KB |
| bill-clinton | bill-clinton_connections.md | 10KB |
| donald-trump | donald-trump_connections.md | 7.5KB |
| emmy-taylor | emmy-taylor_connections.md | 15KB |
| epstein-florida-case | epstein-florida-case_connections.md | 7.4KB |
| ghislaine-maxwell | ghislaine-maxwell_connections.md | 5.7KB |
| giuffre-v-maxwell-case | giuffre-v-maxwell-case_connections.md | 6.1KB |
| glenn-dubin | glenn-dubin_connections.md | 9.5KB |
| jeffrey-epstein | jeffrey-epstein_connections.md | 7KB |
| lesley-groff | lesley-groff_connections.md | 11KB |
| nadia-marcinkova | nadia-marcinkova_connections.md | 13KB |
| prince-andrew | prince-andrew_connections.md | 14KB |
| sarah-kellen | sarah-kellen_connections.md | 19KB |
| terramar-project | terramar-project_connections.md | 10KB |
| virginia-giuffre | virginia-giuffre_connections.md | 16KB |

### Connection Brief Template Structure

```markdown
# [Entity Name] — Connection Analysis

## Editorial Commentary Under First Amendment Protection

**Prepared by:** The Continuum Report
**Generated:** [Date]
**Entity ID:** [entity-id]
**Classification:** Analytical Commentary — Not Statements of Fact

---

## Methodology Statement

[Standard methodology disclaimer]

---

## Connection: [Target Entity Name]

### Summary
[One-sentence description of connection nature and type]

### Documented Evidence
**ECF Doc. XXXX-XX** ([Description], filed [Date]):
> Document references connection context. See primary source for full details.

### Analysis
*The following represents editorial commentary and opinion:*
[Editorial analysis of the connection]

### Alternative Interpretations
[Standard alternative interpretations]

---

## Document Index
[List of all ECF documents cited]

---

## Disclaimer
[Standard First Amendment disclaimer]
```

---

## 7. Brief Template Structure

### Analytical Brief Template (Entity Briefs)

```markdown
# [Subject Name]

> **ANALYTICAL BRIEF — EDITORIAL COMMENTARY**
>
> *The Continuum Report — Another Node in the Decentralized Intelligence Agency*
>
> This document constitutes opinion and analysis based on public court records.
> Interpretive conclusions represent editorial judgment, not assertions of fact.
> Readers are encouraged to review cited sources and form independent conclusions.

---

## Document Classification

| | |
|---|---|
| **Subject** | [Full Name] |
| **Status** | [Criminal/legal status] |
| **Document Type** | Editorial analysis of civil litigation records |
| **Sources** | [Primary case citation] |

---

## Statement of Public Interest
[Why this matters]

---

## Executive Summary
**Editorial Assessment:** [Summary with opinion-signaling language]

---

## The Public Record
*This section presents direct quotations from court documents without editorial comment.*

### [Topic Heading]
**ECF Doc. XXXX-XX, filed MM/DD/YY:**
> [Direct quote]

---

## Editorial Analysis
**The following represents the opinions and interpretations of The Continuum Report.**

[Clearly labeled opinion content]

---

## Alternative Interpretations
A reader reviewing these same documents might reasonably conclude:
- [Alternative 1]
- [Alternative 2]
- [Alternative 3]

---

## Source Documents
| ECF Doc. No. | Filed | Document Description |
|--------------|-------|---------------------|
| XXXX-XX | MM/DD/YY | [Description] |

---

## Methodology and Limitations
[What was and was not reviewed]

---

## Right of Response
[Contact invitation]

---

*Generated: [Date]*
```

---

## 8. Gap Analysis

### Data Completeness Issues

| Issue | Current State | Recommendation |
|-------|---------------|----------------|
| Connection summaries empty | `"summary": ""` in most connections | Generate meaningful summaries |
| Connection sources empty | `"sources": []` in entity connections | Populate with ECF citations |
| Generic document descriptions | "Court Filing" vs specific content | Add descriptive titles |
| Missing connection types | Only 3 types defined | Expand taxonomy (see Section 4) |

### Structural Gaps

| Gap | Impact | Priority |
|-----|--------|----------|
| No location entities | Cannot map geographic patterns | Medium |
| No event entities | Cannot create timelines | Medium |
| No relationship-type field | Cannot distinguish employer vs social | High |
| No direction indicator | Some connections are asymmetric | High |
| No date ranges | Cannot show when connection existed | Medium |

### Connection Brief Quality Issues

| Issue | Example | Fix |
|-------|---------|-----|
| Generic evidence quotes | "Document references connection context" | Extract actual quotes |
| Identical alternative interpretations | Same 4 bullets for every connection | Tailor to specific relationship |
| Missing context | No explanation of relationship nature | Add relationship type and context |

---

## 9. Implementation Guidelines

### Connection Brief Creation

For each connection:
1. Find quote in source document establishing connection
2. Create pairwise connection brief in `/briefs/connections/`
3. Run `python scripts/build_connections_from_briefs.py`
4. Verify connection appears on website

### Connection JSON Schema (Derived from Briefs)

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

### Entity Type Taxonomy

```json
{
  "entityTypes": [
    "person",
    "organization",
    "case",
    "location",
    "event",
    "institution",
    "document"
  ]
}
```

### Connection Brief Quality Standards

1. **Extract actual quotes** — No generic "Document references connection" placeholders
2. **Relationship-specific alternatives** — Tailor to connection type, not copy-paste
3. **Cite page numbers** — ECF doc + page:line when possible
4. **Date precision** — Note if approximate vs. exact
5. **Direction matters** — Accuser→Accused is different from Accused→Accuser

### Validation Checklist

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

## Appendix: Current Entity Inventory

| Entity ID | Name | Type | Tags |
|-----------|------|------|------|
| alan-dershowitz | Alan Dershowitz | person | never-charged, legal |
| bill-clinton | Bill Clinton | person | government |
| donald-trump | Donald Trump | person | never-charged, government, finance |
| emmy-taylor | Emmy Taylor | person | never-charged, associate |
| epstein-florida-case | Epstein Florida Case | case | case |
| ghislaine-maxwell | Ghislaine Maxwell | person | convicted, associate |
| giuffre-v-maxwell-case | Giuffre v. Maxwell Civil Case | case | case, settled |
| glenn-dubin | Glenn Dubin | person | never-charged, finance |
| jeffrey-epstein | Jeffrey Epstein | person | convicted, deceased, finance |
| lesley-groff | Lesley Groff | person | never-charged, associate |
| nadia-marcinkova | Nadia Marcinkova | person | never-charged, associate |
| prince-andrew | Prince Andrew | person | never-charged, royalty |
| sarah-kellen | Sarah Kellen | person | never-charged, associate |
| terramar-project | The Terramar Project | organization | organization, dissolved |
| virginia-giuffre | Virginia Giuffre | person | victim-witness |

---

*Reference document for The Continuum Report connection system normalization*
*Generated by system audit — 2025-12-21*
