# Templates Directory

**Location:** `/continuum/templates/`
**Created:** 2025-12-24
**Purpose:** Standardized templates for all Continuum Report documents

---

## Available Templates

| Template | Purpose | Typical Length |
|----------|---------|----------------|
| `analytical-brief.md` | Full entity brief (person, org, case) | 1500-3000 words |
| `connection-brief.md` | Relationship documentation between two entities | 800-1500 words |
| `summary-connections-brief.md` | Aggregate all connections for one entity | 1500-4000 words |
| `agency-brief.md` | US executive agency documentation | 1500-2500 words |
| `opinion-narrative-short.md` | Quick-read editorial on specific topic/event | 500-1000 words |
| `opinion-narrative-long.md` | In-depth thematic analysis | 2000-5000 words |

---

## Gold Standards

When creating new documents, reference these exemplary briefs:

| Template Type | Gold Standard Example |
|---------------|----------------------|
| Analytical Brief | `analytical_brief_jeffrey_epstein.md` |
| Connection Brief | `ghislaine-maxwell_jeffrey-epstein.md` |
| Summary Connections | `jeffrey-epstein_connections.md` |
| Agency Brief | `analytical_brief_cia.md` |

---

## Key Requirements (All Templates)

### Legal Framework (*Milkovich v. Lorain Journal*, 1990)

1. **Opinion-Protection Header:** Every document must begin with the standard editorial commentary disclaimer
2. **Separated Sections:**
   - "The Public/Documented Record" — ONLY quotes and citations, NO interpretation
   - "Editorial Analysis" — ONLY opinion-signaling language
3. **Alternative Interpretations:** Minimum 5 alternatives (strongest liability shield)
4. **Right of Response:** Contact invitation at the end
5. **Fair Report Privilege:** Noted in fact section headers — applies to accurate reporting of official proceedings
6. **Florida Anti-SLAPP:** Fla. Stat. § 768.295 — protects commentary on matters of public concern (referenced in long-form methodology)

### Citation Requirements

1. **Every quote must have a hyperlinked source PDF**
   ```markdown
   > "Quote text here"
   >
   > — [ECF Doc. 1331-12](https://thecontinuumreport.com/sources/giuffre-v-maxwell/ecf-1331-12.pdf), page X, filed MM/DD/YY
   ```

2. **Source table at end of document:**
   ```markdown
   | Document | Description |
   |----------|-------------|
   | [ECF Doc. XXXX](https://thecontinuumreport.com/sources/...) | Description |
   ```

### Language Guidelines

| DO Write | DON'T Write |
|----------|-------------|
| "In our assessment..." | "was part of the inner circle" |
| "Based on our review..." | "The documents establish..." |
| "We interpret this as..." | "This proves..." |
| "Court filings reference..." | "[Subject] had substantial involvement" |

---

## Workflow

1. **Copy template** to working location
2. **Replace all `[BRACKETED TEXT]`** with content
3. **Delete instruction blocks** at top of template
4. **Verify all source links** work
5. **Run through Quality Checklist** (see below)
6. **Move to appropriate `/briefs/` subdirectory**

---

## Quality Checklist

Before publishing any document:

- [ ] Opinion-protection header present
- [ ] "Public Record" section contains ONLY quotes + citations
- [ ] All interpretive statements use opinion-signaling language
- [ ] Alternative Interpretations section (5-7 minimum)
- [ ] Subject's legal/charge status prominently noted
- [ ] "Right of Response" invitation included
- [ ] No rhetorical questions implying wrongdoing
- [ ] Source citations have working hyperlinks
- [ ] Exculpatory evidence included where applicable
- [ ] No use of "dossier" terminology

---

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Analytical Brief | `analytical_brief_[subject].md` | `analytical_brief_jeffrey_epstein.md` |
| Connection Brief (pair) | `[entity-a]_[entity-b].md` | `ghislaine-maxwell_jeffrey-epstein.md` |
| Summary Connections | `[entity-slug]_connections.md` | `jeffrey-epstein_connections.md` |
| Agency Brief | `analytical_brief_[agency].md` | `analytical_brief_cia.md` |
| Opinion Narrative | `[topic]-[date].md` | `wexner-co-conspirator-2025-12-23.md` |

For connection briefs, order entities alphabetically by last name.

---

## Template Updates

If you identify improvements to these templates:
1. Update the template file
2. Note the change in this README
3. Consider whether existing documents need updating

**Last Updated:** 2025-12-24

---

*The Continuum Report — Another Node in the Decentralized Intelligence Agency*
