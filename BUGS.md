# THE CONTINUUM REPORT — Master Bug Tracking

> **Last Updated:** 2026-01-04 (Session 10)
> **Purpose:** Comprehensive bug/fix list for phased agent execution
> **Total Issues:** 25 (3 P0, 8 P1, 8 P2, 6 P3)

---

## Quick Reference

| Priority | Count | Status |
|----------|-------|--------|
| P0 - Critical | 3 | Site unusable without fix |
| P1 - High | 8 | Major functionality broken |
| P2 - Medium | 8 | UX issues, feature incomplete |
| P3 - Low | 6 | Polish, minor issues |

---

## PHASE 1: Infrastructure Critical (P0)

These must be fixed first — site is inaccessible or broken without them.

### BUG-001: Cloudflare Tunnel Instability
- **Severity:** P0 - CRITICAL
- **Category:** Infrastructure
- **Impact:** Site frequently returns Error 1033, completely inaccessible
- **Root Cause:** `cloudflared` container on Tower (192.168.1.139) is unstable
- **File(s):** Docker container configuration
- **Fix:**
  1. Check cloudflared container logs: `docker logs cloudflared-tunnel`
  2. Add health checks and auto-restart
  3. Verify tunnel credentials/configuration
  4. Monitor memory usage (Tower has 16GB limit)
- **Testing:** Site loads reliably for 10+ page loads

### BUG-002: /sources/ Route 404
- **Severity:** P0 - CRITICAL
- **Category:** Website
- **Impact:** Main navigation link leads to error page
- **File(s):**
  - `website/index.html` (lines 1542, 1770)
  - `website/about.html` (lines 806, 1006)
  - `website/legal.html` (lines 443, 608)
- **Fix:** Create `/website/sources/index.html` OR update all links
- **Testing:** Click "Sources" nav link — page loads

### BUG-003: /sources/giuffre-v-maxwell/ Route 404
- **Severity:** P0 - CRITICAL
- **Category:** Website
- **Impact:** "Browse" button in Featured Reports leads nowhere
- **File(s):** `website/index.html` (line 1749)
- **Fix:** Create sources subdirectory structure or update link
- **Testing:** Click "Browse" on Giuffre v. Maxwell card — documents load

---

## PHASE 2: Navigation & Core Functionality (P1)

### BUG-004: Detail Panel Offset (FIX01)
- **Severity:** P1
- **Category:** CSS
- **Impact:** Detail panel content cut off by header
- **File(s):** `website/continuum.html` (~line 176-230)
- **Prompt:** `Prompts/FIX01_DETAIL_PANEL_OFFSET.md`
- **Testing:** Open entity detail — all content visible below header

### BUG-005: Macro Text Overflow (FIX02)
- **Severity:** P1
- **Category:** CSS/Data
- **Impact:** GOV box subtitle overflows bounds
- **File(s):** `website/continuum.html` (~line 2906, 3251)
- **Prompt:** `Prompts/FIX02_MACRO_TEXT_OVERFLOW.md`
- **Testing:** Macro view — all text contained within boxes

### BUG-006: Card Grid Responsive (FIX03)
- **Severity:** P1
- **Category:** CSS
- **Impact:** Cards cut off when not fullscreen
- **File(s):** `website/continuum.html` (~line 1067-1220)
- **Prompt:** `Prompts/FIX03_CARD_GRID_RESPONSIVE.md`
- **Testing:** Resize window — cards remain visible and scrollable

### BUG-007: Side Panel Navigation (FIX04)
- **Severity:** P1
- **Category:** JS Logic
- **Impact:** Side panel click shows wrong view
- **File(s):** `website/continuum.html` (navigation handlers ~line 5175+)
- **Prompt:** `Prompts/FIX04_ENTITIES_DIRECT_ACCESS.md`
- **Dependency:** None
- **Testing:** Click ENTITIES in side panel — shows card grid, defaults to PEOPLE

### BUG-008: Breadcrumb State (FIX05)
- **Severity:** P1
- **Category:** JS Logic
- **Impact:** [CATEGORY] placeholder shown instead of actual category
- **File(s):** `website/continuum.html` (breadcrumb rendering)
- **Prompt:** `Prompts/FIX05_BREADCRUMB_STATE.md`
- **Dependency:** FIX04
- **Testing:** Navigate — breadcrumb shows "MACRO > PEOPLE > Entity Name"

### BUG-009: Card to Web Transition (FIX06)
- **Severity:** P1
- **Category:** JS Logic
- **Impact:** Blank main area after card click
- **File(s):** `website/continuum.html` (~line 3926)
- **Prompt:** `Prompts/FIX06_CARD_TO_WEB_LAYER.md`
- **Dependency:** FIX04, FIX05
- **Testing:** Click entity card — entity appears in web view with connections panel

### BUG-010: Copyright Year Outdated
- **Severity:** P1
- **Category:** Website
- **Impact:** Shows 2025, should be 2026 (credibility issue)
- **File(s):**
  - `website/index.html` (line 1775)
  - `website/about.html` (line 1010)
  - `website/legal.html` (line 613)
- **Fix:** Update year to 2026 or implement dynamic JavaScript year
- **Testing:** Footer shows "© 2026 The Continuum Report"

### BUG-011: Legal Page Mobile Nav Missing
- **Severity:** P1
- **Category:** Website
- **Impact:** Mobile users cannot navigate from legal.html
- **File(s):** `website/legal.html` (missing mobile-menu-toggle div + JS)
- **Fix:** Add mobile menu toggle matching index.html and about.html
- **Testing:** Mobile viewport — hamburger menu works on legal page

---

## PHASE 3: Data Integration (P2)

### BUG-012: Financial Filter Empty (FIX07)
- **Severity:** P2
- **Category:** Data/Logic
- **Impact:** FINANCIAL category shows 0 entities
- **File(s):**
  - `website/continuum.html` (~line 3814-3822)
  - `website/data/entities.json`
- **Prompt:** `Prompts/FIX07_FINANCIAL_FILTER.md`
- **Pre-Check:** Verify entities have `financial` tag in JSON
- **Testing:** Click FINANCIAL macro — entities with financial tag appear

### BUG-013: Connection Dropdown Empty (FIX08)
- **Severity:** P2
- **Category:** Data Structure
- **Impact:** Connection dropdown shows no data
- **File(s):**
  - `website/continuum.html` (~line 4873)
  - `website/data/entities.json` (connections array)
- **Prompt:** `Prompts/FIX08_CONNECTION_DATA_READING.md`
- **Pre-Check:** Verify connections array structure in entities.json
- **Testing:** Click connection in panel — dropdown shows summary + sources

### BUG-014: Brief Fetch Path (FIX09)
- **Severity:** P2
- **Category:** Path/Server
- **Impact:** Connection briefs not loading
- **File(s):** `website/continuum.html` (brief fetch logic)
- **Prompt:** `Prompts/FIX09_BRIEF_FETCH_PATH.md`
- **Pre-Check:** Verify briefs exist at expected paths: `briefs/connections/*_connections.md`
- **Testing:** Click "View Brief" on connection — brief content loads

### BUG-015: Entity Colors Mismatch (FIX10)
- **Severity:** P2
- **Category:** JS/CSS
- **Impact:** Entity colors don't match specification
- **File(s):** `website/continuum.html` (~line 4201-4210)
- **Prompt:** `Prompts/FIX10_COLOR_SCHEMA.md`
- **Testing:** Verify all 8 entity types have correct colors per spec

### BUG-016: Progressive Web Building (FIX11)
- **Severity:** P2
- **Category:** Feature/JS
- **Impact:** All 70+ nodes visible at once — should progressively reveal
- **File(s):** `website/continuum.html` (~line 4183+)
- **Prompt:** `Prompts/FIX11_PROGRESSIVE_WEB.md`
- **Testing:** Click entity — only that node appears; click connections to reveal more

### BUG-017: Controls Position (FIX12)
- **Severity:** P2
- **Category:** CSS
- **Impact:** Level indicator/zoom controls overlap detail panel
- **File(s):** `website/continuum.html` (~line 1353-1450)
- **Prompt:** `Prompts/FIX12_REPOSITION_CONTROLS.md`
- **Testing:** Controls at bottom-left, level indicator at bottom-center, no overlap

### BUG-018: Macro Colors (FIX13)
- **Severity:** P2
- **Category:** CSS
- **Impact:** Macro boxes all same color, should be category-specific
- **File(s):** `website/continuum.html` (~line 2906, 3306-3340)
- **Prompt:** `Prompts/FIX13_MACRO_COLORS.md`
- **Testing:** PEOPLE=yellow, GOV=blue, MEDIA=pink, FINANCIAL=green borders

### BUG-019: Continuum Accessibility
- **Severity:** P2
- **Category:** A11y
- **Impact:** Screen readers cannot interact with level switcher
- **File(s):** `website/continuum.html`
- **Fix:** Add ARIA roles/labels to level switching controls
- **Testing:** Tab navigation works, screen reader announces controls

---

## PHASE 4: Visual Polish (P3)

### BUG-020: Equal Node Size (FIX14)
- **Severity:** P3
- **Category:** JS
- **Impact:** Epstein node larger than others (should be equal)
- **File(s):** `website/continuum.html` (~line 4480-4520)
- **Prompt:** `Prompts/FIX14_EQUAL_NODE_SIZE.md`
- **Testing:** All person nodes same size, no ID-based scaling

### BUG-021: Inconsistent Navigation
- **Severity:** P3
- **Category:** Website
- **Impact:** Different pages have different nav structures
- **File(s):** All HTML pages
- **Fix:** Standardize navigation across all pages
- **Testing:** All pages have identical nav structure

### BUG-022: Console Errors - Cloudflare Beacon
- **Severity:** P3
- **Category:** JS
- **Impact:** Minor — Cloudflare analytics errors
- **Fix:** May be related to tunnel instability; can be ignored if tunnel fixed
- **Testing:** No console errors on page load

### BUG-023: Homepage Large Empty Space
- **Severity:** P3
- **Category:** CSS
- **Impact:** Confusing scroll gap between sections
- **File(s):** `website/index.html`
- **Fix:** Review CSS for framework section padding
- **Testing:** Smooth scroll with no excessive gaps

### BUG-024: Missing og:image
- **Severity:** P3
- **Category:** SEO
- **Impact:** Social sharing preview may be broken
- **File(s):** `website/index.html` (line 18)
- **Fix:** Create og-image.jpg (1200x630px) or remove meta tag
- **Testing:** Share URL — preview image appears

### BUG-025: Legal Page Effective Date
- **Severity:** P3
- **Category:** Content
- **Impact:** Minor — outdated date reference
- **File(s):** `website/legal.html` (lines 597-598)
- **Fix:** Update if standards changed, or leave as-is
- **Testing:** Date reflects last actual update

---

## Execution Protocol

### Phase Order
```
PHASE 1 (P0) → PHASE 2 (P1) → PHASE 3 (P2) → PHASE 4 (P3)
     ↓              ↓              ↓              ↓
  3 bugs         8 bugs         8 bugs         6 bugs
```

### Within Each Phase

1. **Backup First**
   ```bash
   cp /mnt/user/continuum/website/continuum.html \
      /mnt/user/continuum/website/backups/continuum_pre-phase$(date +%Y%m%d_%H%M%S).html
   ```

2. **Execute Fixes in Order** (dependencies noted)

3. **Test After Each Fix**
   - Load site in browser
   - Verify specific test case
   - Check console for errors

4. **Commit After Phase Completes**

### Dependency Graph

```
BUG-004 (FIX01) ─────────────────────────────────────┐
BUG-005 (FIX02) ─────────────────────────────────────┤
BUG-006 (FIX03) ─────────────────────────────────────┤ Tier 1: CSS (Independent)
                                                      │
BUG-007 (FIX04) ───► BUG-008 (FIX05) ───► BUG-009 (FIX06)  Tier 2: Navigation (Sequential)
                                                      │
BUG-012 (FIX07) ───► BUG-013 (FIX08)                 │ Tier 3: Data (Sequential)
BUG-014 (FIX09) ─────────────────────────────────────┤ (Independent)
BUG-015 (FIX10) ─────────────────────────────────────┤ (Independent)
                                                      │
BUG-016 (FIX11) ─────────────────────────────────────┤
BUG-017 (FIX12) ─────────────────────────────────────┤ Tier 4: Features (Independent)
BUG-018 (FIX13) ─────────────────────────────────────┤
BUG-020 (FIX14) ─────────────────────────────────────┘
```

---

## Agent Task Files

| Phase | Task File | Status |
|-------|-----------|--------|
| 1 | `agents/tasks/BUGFIX_PHASE1_INFRASTRUCTURE.md` | Pending |
| 2 | `agents/tasks/BUGFIX_PHASE2_NAVIGATION.md` | Pending |
| 3 | `agents/tasks/BUGFIX_PHASE3_DATA.md` | Pending |
| 4 | `agents/tasks/BUGFIX_PHASE4_POLISH.md` | Pending |

---

## Prompt File Locations

All FIX prompts are located at:
```
Local: C:\Users\Xx LilMan xX\Documents\Claude Docs\The Continuum Report\Prompts\
Network: T:\Prompts\ (if synced)
```

| File | Bug Reference |
|------|---------------|
| FIX01_DETAIL_PANEL_OFFSET.md | BUG-004 |
| FIX02_MACRO_TEXT_OVERFLOW.md | BUG-005 |
| FIX03_CARD_GRID_RESPONSIVE.md | BUG-006 |
| FIX04_ENTITIES_DIRECT_ACCESS.md | BUG-007 |
| FIX05_BREADCRUMB_STATE.md | BUG-008 |
| FIX06_CARD_TO_WEB_LAYER.md | BUG-009 |
| FIX07_FINANCIAL_FILTER.md | BUG-012 |
| FIX08_CONNECTION_DATA_READING.md | BUG-013 |
| FIX09_BRIEF_FETCH_PATH.md | BUG-014 |
| FIX10_COLOR_SCHEMA.md | BUG-015 |
| FIX11_PROGRESSIVE_WEB.md | BUG-016 |
| FIX12_REPOSITION_CONTROLS.md | BUG-017 |
| FIX13_MACRO_COLORS.md | BUG-018 |
| FIX14_EQUAL_NODE_SIZE.md | BUG-020 |
| FIX_INDEX.md | Overview |
| RUN_ALL_FIXES.md | Orchestration |

---

## Completion Tracking

| Bug ID | Status | Fixed By | Date | Verified |
|--------|--------|----------|------|----------|
| BUG-001 | [ ] Pending | | | |
| BUG-002 | [ ] Pending | | | |
| BUG-003 | [ ] Pending | | | |
| BUG-004 | [ ] Pending | | | |
| BUG-005 | [ ] Pending | | | |
| BUG-006 | [ ] Pending | | | |
| BUG-007 | [ ] Pending | | | |
| BUG-008 | [ ] Pending | | | |
| BUG-009 | [ ] Pending | | | |
| BUG-010 | [ ] Pending | | | |
| BUG-011 | [ ] Pending | | | |
| BUG-012 | [ ] Pending | | | |
| BUG-013 | [ ] Pending | | | |
| BUG-014 | [ ] Pending | | | |
| BUG-015 | [ ] Pending | | | |
| BUG-016 | [ ] Pending | | | |
| BUG-017 | [ ] Pending | | | |
| BUG-018 | [ ] Pending | | | |
| BUG-019 | [ ] Pending | | | |
| BUG-020 | [ ] Pending | | | |
| BUG-021 | [ ] Pending | | | |
| BUG-022 | [ ] Pending | | | |
| BUG-023 | [ ] Pending | | | |
| BUG-024 | [ ] Pending | | | |
| BUG-025 | [ ] Pending | | | |

---

*This document is the single source of truth for bug tracking. Update completion status as fixes are applied.*
