# Continuum Bug Fix Prompts - Index

Generated: 2024-12-20

## Overview
These prompts address 10 issues discovered after Phase 1-5 implementation. Execute in order for best results.

## Recommended Execution Order

### Tier 1: CSS Fixes (Standalone, Low Risk)
These can be done first as they don't affect logic:

| Order | File | Issue | Complexity |
|-------|------|-------|------------|
| 1 | FIX01_DETAIL_PANEL_OFFSET.md | Detail panel content cut off by header | Simple CSS |
| 2 | FIX02_MACRO_TEXT_OVERFLOW.md | GOV box subtitle overflows bounds | Simple CSS/Data |
| 3 | FIX03_CARD_GRID_RESPONSIVE.md | Cards cut off when not fullscreen | CSS |

### Tier 2: Navigation Logic (Interdependent)
These should be done together:

| Order | File | Issue | Complexity |
|-------|------|-------|------------|
| 4 | FIX04_ENTITIES_DIRECT_ACCESS.md | Side panel click shows wrong view | JS Logic |
| 5 | FIX05_BREADCRUMB_STATE.md | [CATEGORY] placeholder shown | JS Logic |
| 6 | FIX06_CARD_TO_WEB_LAYER.md | Blank main area after card click | JS Logic |

### Tier 3: Data Integration (Requires Investigation)
These need data verification first:

| Order | File | Issue | Complexity |
|-------|------|-------|------------|
| 7 | FIX07_FINANCIAL_FILTER.md | FINANCIAL shows 0 entities | Data/Logic |
| 8 | FIX08_CONNECTION_DATA_READING.md | Connection dropdown empty | Data Structure |
| 9 | FIX09_BRIEF_FETCH_PATH.md | Connection briefs not loading | Path/Server |

### Tier 4: Visual Polish
Can be done last:

| Order | File | Issue | Complexity |
|-------|------|-------|------------|
| 10 | FIX10_COLOR_SCHEMA.md | Entity colors don't match spec | JS/CSS |

## Pre-Execution Checklist

### Before Starting
- [ ] Backup current continuum.html
- [ ] Have browser dev tools open (Console tab)
- [ ] Have access to Tower server
- [ ] Know where entities.json and briefs are located

### Backup Command
```bash
cp /mnt/user/continuum/website/continuum.html /mnt/user/continuum/website/backups/continuum_pre-fixes_$(date +%Y%m%d_%H%M%S).html
```

## Execution Strategy

### Option A: One at a Time (Recommended)
1. Run one fix prompt
2. Test in browser
3. If working, commit/save
4. Move to next fix

### Option B: Batch by Tier
1. Run all Tier 1 fixes
2. Test all CSS changes
3. Run all Tier 2 fixes
4. Test navigation
5. Continue...

## Claude Code Instructions

When running these prompts in Claude Code:
1. Read the full prompt before making changes
2. Create backup first
3. Make the specific changes described
4. Report what was changed
5. Provide testing instructions

## Issue Dependencies

```
FIX04 ─────► FIX05 (breadcrumb depends on category being set)
   │
   └──────► FIX06 (proper entities view needed for card navigation)

FIX07 ─────► FIX08 (filter needs to work before connections show)

FIX09 ◄────  Independent (server path issue)

FIX10 ◄────  Independent (can be done anytime)
```

## Expected Outcomes

After all fixes:
- ✅ Detail panel fully visible below header
- ✅ Macro boxes contain all text within borders
- ✅ Card grid scrollable/responsive on narrow viewports
- ✅ Side panel "ENTITIES" shows card grid (default: PEOPLE)
- ✅ Breadcrumb shows actual category name, not placeholder
- ✅ Card click shows entity in web layer with connections
- ✅ FINANCIAL category shows financial entities
- ✅ Connection dropdowns show real summaries and sources
- ✅ "View Brief" loads actual connection brief documents
- ✅ Entity colors match specification

## Troubleshooting

### If a fix breaks something:
1. Restore from backup
2. Read the prompt more carefully
3. Apply changes incrementally
4. Check browser console for errors

### Common Issues:
- **Syntax errors**: Check for missing semicolons, brackets
- **Path issues**: Verify server file locations
- **Data issues**: Log data to console to verify structure
