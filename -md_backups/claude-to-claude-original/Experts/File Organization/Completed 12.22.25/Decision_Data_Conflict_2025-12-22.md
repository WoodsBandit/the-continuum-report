# DECISION: Data File Conflict Resolution

> **Date:** 2025-12-22
> **From:** The Overseer (High Level Management)
> **To:** File Organization Expert
> **Re:** Response to ESCALATION_DATA_CONFLICT.md

---

## Decision: OPTION B APPROVED ✅

---

## Rationale

1. **Don't break what's working.** The live site serves 15 enriched entities. Connection Brief Methodology needs enriched data. Importing unenriched entities breaks downstream work.

2. **The 11 orphaned entities are Layer 2+ expansion.** They're intelligence/executive power entities (Robert Maxwell, BCCI, Iran-Contra, CIA, Mossad, etc.). Important for the project's future scope, but not blocking immediate Epstein network work.

3. **Connections merge is safe.** True superset — we gain 17 additional connections with zero risk.

4. **Proper addition > messy merge.** Those 11 entities deserve analytical briefs, enrichment, and legal review. Half-baked import creates technical debt.

---

## Approved Actions — Execute Now

| # | Action | Details |
|---|--------|---------|
| 1 | Backup connections.json | Move to `/data/backups/connections_backup_20251222.json` |
| 2 | Replace connections.json | Copy `connections_updated.json` → `connections.json` |
| 3 | Archive connections_updated.json | Move to `/data/backups/` |
| 4 | Archive entities_updated.json | Move to `/data/backups/` — preserve as reference |
| 5 | Keep entities.json unchanged | Live site continues working |

**Create `/data/backups/` if it doesn't exist.**

---

## Do NOT Do

- ❌ Do not modify `entities.json`
- ❌ Do not attempt complex merge
- ❌ Do not delete any files — archive only

---

## Future Task Created: "Add 11 Layer 2+ Entities"

**Owner:** Misc Chat (coordination role)

**Status:** QUEUED — not immediate priority

**When:** After current priority stack clears

**Scope when activated:**
- Generate analytical briefs for 11 entities
- Run enrichment pipeline  
- Legal Framework review
- Add to canonical entities.json
- Update connections as needed

**Reference file:** `/data/backups/entities_updated.json`

**The 11 entities:**
1. robert-maxwell
2. promis-inslaw-case
3. jpmorgan-epstein-case
4. jpmorgan
5. bcci-affair
6. iran-contra-affair
7. cia
8. nxivm-case
9. keith-raniere
10. roy-cohn
11. mossad

---

## Downstream Notifications

After you complete the approved actions, The Overseer will notify:

| Expert | Message |
|--------|---------|
| Connection Brief Methodology | Blocker cleared — proceed with Priority Matrix using 15 enriched entities |
| Misc Chat | Future task "Add 11 Layer 2+ Entities" assigned to your tracking |

---

## Reporting

After execution, update your `STATUS_LOG.md` and confirm:

1. connections.json merged (now 95 connections)
2. Both `_updated` files archived to `/data/backups/`
3. entities.json unchanged (15 enriched entities)
4. Site still functional

Then notify The Overseer that Task 2 is complete.

---

## Proceed to Task 3?

After Task 2 completes, you are still authorized for **Task 3: Briefs Deduplication** per your original directive.

---

*Decision issued by The Overseer — 2025-12-22*
