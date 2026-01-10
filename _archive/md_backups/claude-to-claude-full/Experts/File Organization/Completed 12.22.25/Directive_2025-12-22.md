# FILE ORGANIZATION — Authorized Directive from The Overseer

> **Date:** 2025-12-22
> **From:** The Overseer (High Level Management)
> **To:** File Organization Expert
> **Re:** Authorization to Proceed + Cross-Expert Context

---

## Authorization Granted

You are authorized to proceed with the following tasks in sequential order:

### Task 1: Minor Cleanup (6 Moves)
**Status:** ✅ APPROVED — Execute immediately

| # | From | To |
|---|------|-----|
| 1 | `/entity_data/` | `/_archive/entity_data/` |
| 2 | `/processed/` | `/_archive/processed/` |
| 3 | `/errors.log` | `/logs/errors.log` |
| 4 | `/progress.json` | `/logs/progress.json` |
| 5 | `/progress_executive_power.json` | `/logs/progress_executive_power.json` |
| 6 | `/CLAUDE_CODE_CONTINUUM_TASK.md` | `/config/CLAUDE_CODE_CONTINUUM_TASK.md` |

**Note:** Create `/_archive/` directory if it doesn't exist.

---

### Task 2: Data File Resolution
**Status:** ✅ APPROVED — Execute after Task 1 complete

**The Problem:**
Multiple versions exist in `/data/`:
- `entities.json` (73KB) vs `entities_updated.json` (66KB)
- `connections.json` (29KB) vs `connections_updated.json` (33KB)
- `entities_backup_20251220_215619.json` (55KB)

**Critical Context from Continuum Visualization:**
> `continuum.html` fetches `entities.json` and `connections.json` — NOT the `_updated` versions.

**The Resolution:**
1. Diff `entities.json` vs `entities_updated.json`
2. Diff `connections.json` vs `connections_updated.json`
3. Determine relationship:
   - If `_updated` is a **superset** (same data + additions) → Replace original with `_updated`, move old original to `/data/backups/`
   - If `_updated` is **different/conflicting** → STOP and escalate to The Overseer with findings
4. Create `/data/backups/` if it doesn't exist
5. Move all backup files (`*_backup_*.json`) to `/data/backups/`

**Why This Matters:**
- Connection Brief Methodology Expert is **blocked** waiting for canonical entities.json
- They need to build a Priority Matrix from the entity data
- Until this is resolved, connection brief generation cannot begin

---

### Task 3: Briefs Deduplication
**Status:** ✅ APPROVED — Execute after Task 2 complete

**The Problem:**
Two locations contain briefs:
- `/briefs/` (45 items) — Monitored by `brief_watcher.py`
- `/reports/Analytical Briefs/` — Legacy from old Ollama pipeline

**Your Finding (Confirmed):**
> `/briefs/` is canonical — dynamic graph system reads from here.

**The Resolution:**
1. Compare contents of both directories
2. If `/reports/Analytical Briefs/` is subset or identical to `/briefs/`:
   - Move entire `/reports/Analytical Briefs/` to `/_archive/reports_analytical_briefs/`
3. If `/reports/Analytical Briefs/` contains unique files not in `/briefs/`:
   - STOP and escalate to The Overseer with list of unique files
4. Document result in your STATUS_LOG.md

---

## Cross-Expert Context You Need

### From Infrastructure Lead

**Source Hosting Status:** ✅ Complete
- 97 PDFs live at `/sources/giuffre-v-maxwell/`
- URL pattern: `https://thecontinuumreport.com/sources/giuffre-v-maxwell/ecf-{docket}-{exhibit}.pdf`
- Nginx serving correctly

**Implication for you:**
- `/sources/` is Infrastructure Lead's domain — do NOT modify
- `/downloads/` is working storage, `/sources/` is public-facing — no conflict
- `/documents/public/` relationship to `/sources/` is Infrastructure's concern

---

### From Connection Brief Methodology

**Their Status:** ⏳ Holding — waiting on YOU

**What they need:**
- Canonical `entities.json` with connection data
- They will build a Priority Matrix ranking entity pairs for connection brief generation

**Implication for you:**
- Task 2 (data file resolution) directly unblocks their work
- Confirm which version has the enriched connection data (likely `_updated`)
- Once resolved, notify The Overseer so I can clear their blocker

---

### From Continuum Visualization

**What they confirmed:**
- `continuum.html` fetches from `/data/entities.json` and `/data/connections.json`
- NOT from `_updated` versions
- If you replace originals with `_updated`, the site will immediately use the new data

**Implication for you:**
- Backup originals before any replacement
- Test that site still loads after data file changes (or report for verification)

---

### From Legal Framework

**Briefs Status:**
- 15 analytical briefs rebuilt with First Amendment protections
- All compliant with Milkovich framework

**Implication for you:**
- `/briefs/` is the canonical location for compliant briefs
- After deduplication, Legal Framework Expert may spot-check from `/briefs/`

---

## Execution Protocol

**For each task, Claude Code should:**

1. Create backup before any destructive operation
2. Execute the specified moves/operations
3. Verify success (list directories, confirm files in new locations)
4. Report completion with summary

**Between tasks:**
- Report completion to you (File Organization Expert)
- You verify and log in STATUS_LOG.md
- Then issue next task prompt

---

## Reporting

After each task completes, update your `STATUS_LOG.md` with:
- What was done
- Any issues encountered
- Confirmation of success

After all three tasks complete, notify The Overseer with summary so I can:
1. Confirm blockers cleared for Connection Brief Methodology
2. Update Expert Status
3. Authorize next phase (Infrastructure Lead's Citation Gap Audit)

---

## Constraints

- **ONE Claude Code task at a time** — Do not run parallel operations
- **Escalate conflicts** — If diffs show unexpected differences, stop and report
- **Do not modify `/sources/`** — That's Infrastructure Lead's domain
- **Do not delete** — Archive to `/_archive/` instead

---

## Summary

| Task | Action | Unblocks |
|------|--------|----------|
| 1. Minor Cleanup | 6 file moves | Clean root directory |
| 2. Data Resolution | Diff, merge, backup | Connection Brief Methodology |
| 3. Briefs Dedup | Compare, archive legacy | Clean briefs structure |

**You are cleared to proceed. Start with Task 1.**

---

*Directive issued by The Overseer — 2025-12-22*
