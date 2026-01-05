# CONNECTION BRIEF GENERATION — Execution Plan

> **Date:** 2024-12-22
> **From:** Connection Brief Methodology Expert
> **For:** Claude Code (Execution)
> **Approved By:** [Pending Overseer Approval]

---

## Priority Queue (Top 15)

Generate connection briefs in this order:

1. Ghislaine Maxwell ↔ Virginia Giuffre
2. Ghislaine Maxwell ↔ Jeffrey Epstein
3. Prince Andrew ↔ Virginia Giuffre
4. Alan Dershowitz ↔ Virginia Giuffre
5. Ghislaine Maxwell ↔ Prince Andrew
6. Jeffrey Epstein ↔ Virginia Giuffre
7. Bill Clinton ↔ Virginia Giuffre
8. Sarah Kellen ↔ Virginia Giuffre
9. Jeffrey Epstein ↔ Epstein Florida Case
10. Ghislaine Maxwell ↔ Giuffre v. Maxwell Case
11. Emmy Taylor ↔ Virginia Giuffre
12. Nadia Marcinkova ↔ Sarah Kellen
13. Lesley Groff ↔ Sarah Kellen
14. Alan Dershowitz ↔ Jeffrey Epstein
15. Glenn Dubin ↔ Virginia Giuffre

---

## Classification Instructions

For each connection, determine:

### Axis 1: Relationship Type (pick one)
- Employer-Employee
- Attorney-Client
- Family
- Financial
- Social
- Accuser-Accused
- Witness-Subject
- Co-Defendant
- Co-Conspirator
- Organizational
- Proximity
- Other

### Axis 2: Evidence Level (pick one)
| Level | Standard |
|-------|----------|
| **Sworn** | Depositions, affidavits, court testimony |
| **Documented** | Contracts, flight logs, corporate filings, photos |
| **Reported** | News articles, investigative reports |
| **Inferred** | Pattern analysis, circumstantial |

---

## Brief Template

Use this exact structure:

```markdown
# CONNECTION BRIEF: [Entity A] ↔ [Entity B]

> **ANALYTICAL BRIEF — EDITORIAL COMMENTARY**
> 
> This document constitutes opinion and analysis based on public records.
> Interpretive conclusions represent editorial judgment, not assertions of fact.

---

## Relationship Classification

| Attribute | Value |
|-----------|-------|
| **Type** | [from 12 types] |
| **Evidence Level** | [Sworn/Documented/Reported/Inferred] |
| **Direction** | [Bidirectional / A→B / B→A] |
| **Status** | [Active / Historical / Alleged] |

---

## The Documented Record

[Direct quotes and citations ONLY — no interpretation]

### Source 1: [Document Title]
> "[Direct quote from source]"
> — ECF [number], [description]

---

## Editorial Analysis

**The following represents the opinions and interpretations of The Continuum Report.**

[Opinion-signaled interpretation: "suggests," "appears to," "in our assessment"]

---

## Alternative Interpretations

1. **[Alternative 1]:** [Explanation]
2. **[Alternative 2]:** [Explanation]
3. **[Alternative 3]:** [Explanation]

---

## Source Documents

| # | ECF | Description | Link |
|---|-----|-------------|------|
| 1 | [#] | [Title] | [URL] |

---

*Generated: [Date]*
```

---

## Output Locations

- Briefs: `T:\briefs\connections\{entityA}_{entityB}.md`
- Update `entities.json` connection summaries after each brief
- Update `connections.json` with relationship type classification

---

## Source Reference

ECF documents available at: `T:\sources\giuffre-v-maxwell\`

---

*Execution plan ready for Overseer approval*
