# INFRASTRUCTURE LEAD — Authorized Directive from The Overseer

> **Date:** 2025-12-22
> **From:** The Overseer (High Level Management)
> **To:** Infrastructure Lead Expert
> **Re:** Claude Code Available — Proceed with Citation Gap Audit

---

## Status: ✅ CLEARED TO PROCEED

File Organization Expert has completed their Claude Code work. The execution layer is now available for your tasks.

---

## Authorization: Citation Gap Audit

**Task:** Scan all 15 analytical briefs for ECF citations and compare against hosted source files.

**Purpose:** Identify gaps between what briefs cite and what's actually hosted at `/sources/giuffre-v-maxwell/`

---

## Current State

| Resource | Status |
|----------|--------|
| Source hosting | ✅ 97 PDFs live at `/sources/giuffre-v-maxwell/` |
| Briefs location | `/continuum/briefs/` (42 files, canonical) |
| URL pattern | `ecf-{docket}-{exhibit}.pdf` |

---

## Deliverable: Gap Report

| ECF Citation | Brief(s) Citing | Hosted? | Action Needed |
|--------------|-----------------|---------|---------------|
| ecf-1328-44 | analytical_brief_marcinkova.md | ✅ Yes | None |
| ecf-1331-14 | analytical_brief_xxx.md | ❌ No | Check Paperless / PACER |
| ... | ... | ... | ... |

**Categories:**
1. ✅ Cited AND hosted — ready for linking
2. ⚠️ Cited but NOT hosted, EXISTS in Paperless — export needed
3. ❌ Cited but NOT hosted, NOT in Paperless — PACER acquisition needed

---

## Authority Granted

Per previous authorization:
- **You may export from Paperless** to fill gaps without escalation
- Documents in Paperless tagged `CASE: Giuffre-v-Maxwell` (or equivalent)

---

## Claude Code Task

Write a task prompt for Claude Code to:

1. **Extract all ECF citations** from briefs in `/continuum/briefs/`
   - Pattern: `ecf-XXXX-XX` or similar
   
2. **List all files** in `/continuum/sources/giuffre-v-maxwell/`

3. **Compare and report:**
   - Citations found in briefs
   - Files available in sources
   - Gaps (cited but not hosted)

4. **Check Paperless** for gap documents:
   - Query API for missing ECF numbers
   - Report which can be exported vs. which need acquisition

---

## Context from Other Experts

### File Organization (Just Completed)
- `/briefs/` confirmed canonical (42 files)
- `/sources/` is your domain — no conflicts

### Connection Brief Methodology (Now Active)
- Building Priority Matrix
- Will need source documents for connection brief citations
- Your audit informs their work

### Legal Framework (Running Audit)
- Spot-checking brief compliance
- No impact on your work

---

## Reporting

After audit completes:
1. Provide Gap Report table
2. List documents you can export from Paperless
3. List documents requiring PACER acquisition
4. Estimate for filling gaps

---

**You are cleared to proceed. Claude Code is available.**

---

*Directive issued by The Overseer — 2025-12-22*
