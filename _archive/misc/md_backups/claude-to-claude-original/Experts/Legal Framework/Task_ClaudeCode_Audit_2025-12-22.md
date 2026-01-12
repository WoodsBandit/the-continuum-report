# Claude Code Task — Legal Compliance Audit

> **From:** Legal Framework Expert  
> **To:** Claude Code (Tower)  
> **Date:** 2025-12-22  
> **Task Type:** Read & Report (No modifications)

---

## Objective

Conduct a spot-check legal compliance audit on 3 analytical briefs. Report findings back via `ClaudeCode_To_Claude.md`.

---

## Briefs to Audit

Read these 3 files from `/continuum/briefs/` (or locate them if path differs):

| Profile | Filename |
|---------|----------|
| High | `analytical_brief_jeffrey_epstein.md` |
| Mid | `analytical_brief_glenn_dubin.md` |
| Low | `analytical_brief_lesley_groff.md` |

If briefs are in a subdirectory (e.g., `/briefs/analytical/`), locate and read from there.

---

## Audit Checklist

For EACH brief, check the following and report YES/NO/PARTIAL:

### Structure
1. "ANALYTICAL BRIEF — EDITORIAL COMMENTARY" header present?
2. Opinion disclaimer present at top?
3. Document Classification table present?
4. Statement of Public Interest section exists?

### Fact/Opinion Separation
5. "The Public Record" section contains ONLY quotes + citations (no interpretation)?
6. "Editorial Analysis" section exists and is clearly labeled?
7. Editorial Analysis uses opinion-signaling language ("appears to," "suggests," "in our assessment")?

### Liability Shields
8. "Alternative Interpretations" section exists?
9. Alternative Interpretations has 5-7 substantive alternatives (count them)?
10. "Right of Response" invitation included?
11. "Methodology and Limitations" section exists?

### Sensitive Content
12. Subject's criminal charge status prominently noted in Document Classification?
13. If "Never charged" — is this clearly stated?
14. Any rhetorical questions implying wrongdoing? (Should be NO)
15. Any Fifth Amendment references? If yes, is constitutional rights disclaimer included?
16. Any loaded terminology ("inner circle," "network") presented as fact? (Should be NO)

### Source Citations
17. Source Documents table present?
18. Citations include document identifiers and dates?

---

## Output Format

Write your findings to `ClaudeCode_To_Claude.md` in this format:

```markdown
# Claude Code Report — Legal Compliance Audit

**Task:** Spot-Check Audit  
**Completed:** [DATE/TIME]  
**Briefs Location:** [PATH YOU FOUND THEM]

---

## Brief 1: Jeffrey Epstein

| Check | Item | Result | Notes |
|-------|------|--------|-------|
| 1 | Header present | YES/NO | |
| 2 | Disclaimer present | YES/NO | |
... [continue for all 18 checks]

**Alternative Interpretations Count:** [NUMBER]

**Issues Found:** [List any failures or concerns]

---

## Brief 2: Glenn Dubin

[Same format]

---

## Brief 3: Lesley Groff

[Same format]

---

## Summary

| Brief | Status | Issues |
|-------|--------|--------|
| Epstein | COMPLIANT / MINOR ISSUES / MAJOR ISSUES | |
| Dubin | COMPLIANT / MINOR ISSUES / MAJOR ISSUES | |
| Groff | COMPLIANT / MINOR ISSUES / MAJOR ISSUES | |

**Overall Assessment:** [Your summary]
```

---

## Constraints

- **DO NOT modify any briefs** — read only
- Report exactly what you find
- If you cannot locate a brief, report that
- If a section is ambiguous, note it

---

## Completion

When finished, confirm in `ClaudeCode_To_Claude.md` that the task is complete so Legal Framework Expert can review.

---

*Task issued by Legal Framework Expert — 2025-12-22*
