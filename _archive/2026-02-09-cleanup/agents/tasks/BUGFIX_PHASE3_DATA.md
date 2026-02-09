# BUGFIX PHASE 3: Data Integration (P2)

> **Priority:** MEDIUM - UX issues, features incomplete
> **Estimated Duration:** 2-3 hours
> **Dependencies:** Phase 2 complete (navigation working)

---

## Pre-Flight Checklist

- [ ] Phase 2 complete - navigation works
- [ ] Read T:\BUGS.md for full context
- [ ] Backup continuum.html before changes
- [ ] Verify data files exist and are valid JSON

### Backup Command
```bash
cp /mnt/user/continuum/website/continuum.html \
   /mnt/user/continuum/website/backups/continuum_pre-phase3_$(date +%Y%m%d_%H%M%S).html
```

### Data Verification
```bash
# Check entities.json structure
head -100 /mnt/user/continuum/website/data/entities.json

# Verify JSON is valid
python3 -c "import json; json.load(open('/mnt/user/continuum/website/data/entities.json'))"

# Check for financial entities
grep -i '"tags".*financial' /mnt/user/continuum/website/data/entities.json | head -5

# Check connections structure
grep -A10 '"connections"' /mnt/user/continuum/website/data/entities.json | head -30
```

---

## Data Integration Fixes

### BUG-012: Financial Filter Empty (FIX07)

**Prompt File:** `Prompts/FIX07_FINANCIAL_FILTER.md`

**Problem:** FINANCIAL category shows 0 entities

**Files:**
- `website/continuum.html` (~line 3814-3822)
- `website/data/entities.json`

**Diagnosis:**
1. Check if entities have `financial` tag:
   ```bash
   grep -c '"financial"' /mnt/user/continuum/website/data/entities.json
   ```
2. Check filter logic in continuum.html

**Quick Fix:**
- Ensure filter uses correct tag name (case-sensitive)
- May need to add "financial" tag to relevant entities
- Verify filter function matches tag structure

**Test:** Click FINANCIAL macro - entities with financial tag appear

---

### BUG-013: Connection Dropdown Empty (FIX08)

**Prompt File:** `Prompts/FIX08_CONNECTION_DATA_READING.md`

**Problem:** Connection dropdown shows no data

**Files:**
- `website/continuum.html` (~line 4873)
- `website/data/entities.json` (connections array)

**Diagnosis:**
```bash
# Check connections array structure
grep -A20 '"connections":' /mnt/user/continuum/website/data/entities.json | head -50
```

**Quick Fix:**
- Verify code reads `entity.connections` array correctly
- Check if connection summary and sources are populated
- Add console.log debugging if needed

**Test:** Click connection in panel - dropdown shows summary + sources

---

### BUG-014: Brief Fetch Path (FIX09)

**Prompt File:** `Prompts/FIX09_BRIEF_FETCH_PATH.md`

**Problem:** Connection briefs not loading

**Diagnosis:**
```bash
# Find connection briefs
find /mnt/user/continuum -name "*_connections.md" 2>/dev/null | head -10

# Check briefs directory
ls -la /mnt/user/continuum/website/briefs/connections/ | head -20
```

**Quick Fix:**
- Verify fetch path matches actual file locations
- Check for CORS issues if loading from different origin
- Ensure file extensions match (.md vs .html)

**Test:** Click "View Brief" on connection - brief content loads

---

### BUG-015: Entity Colors Mismatch (FIX10)

**Prompt File:** `Prompts/FIX10_COLOR_SCHEMA.md`

**Problem:** Entity colors don't match specification

**File:** `website/continuum.html` (~line 4201-4210)

**Color Specification:**
| Entity Type | Color |
|-------------|-------|
| Person: Gov Employee | #E57373 (Reddish) |
| Person: CEO/Board | #4DD0E1 (Tealish) |
| Person: Other | #FFD54F (Yellow) |
| Org: Banking/Financial | #81C784 (Green) |
| Org: Media | #F48FB1 (Pink) |
| Org: Government | #5C6BC0 (Dark Blue) |
| Org: Other | #9575CD (Purple) |
| Case | #FFB74D (Orange) |

**Quick Fix:**
- Find `getEntityColor()` or similar function
- Update color mappings to match spec
- Test each entity type

**Test:** Verify all 8 entity types have correct colors per spec

---

### BUG-016: Progressive Web Building (FIX11)

**Prompt File:** `Prompts/FIX11_PROGRESSIVE_WEB.md`

**Problem:** All 70+ nodes visible at once - should progressively reveal

**File:** `website/continuum.html` (~line 4183+)

**This is a larger feature implementation:**
1. Track revealed nodes in Graph object
2. Modify node display on entity selection
3. Add "Show All Connections" button
4. Make connection clicks reveal nodes
5. Add visual indicators for revealed/unrevealed

**Test:** Click entity - only that node appears; click connections to reveal more

---

### BUG-017: Controls Position (FIX12)

**Prompt File:** `Prompts/FIX12_REPOSITION_CONTROLS.md`

**Problem:** Level indicator/zoom controls overlap detail panel

**File:** `website/continuum.html` (~line 1353-1450)

**Quick Fix:**
- Move level indicator to bottom-center
- Move zoom controls to bottom-left
- Ensure no overlap with detail panel

**Test:** Controls at bottom-left, level indicator at bottom-center, no overlap

---

### BUG-018: Macro Colors (FIX13)

**Prompt File:** `Prompts/FIX13_MACRO_COLORS.md`

**Problem:** Macro boxes all same color, should be category-specific

**File:** `website/continuum.html` (~line 2906, 3306-3340)

**Color Specification:**
- PEOPLE → Yellow border (#FFD54F)
- GOVERNMENT → Dark Blue border (#5C6BC0)
- MEDIA → Pink border (#F48FB1)
- FINANCIAL → Green border (#81C784)

**Quick Fix:**
- Update category definitions with color property
- Change box stroke to use `category.color`
- Keep center circle and lines gold

**Test:** Each macro box has category-specific border color

---

### BUG-019: Continuum Accessibility

**Problem:** Screen readers cannot interact with level switcher

**File:** `website/continuum.html`

**Quick Fix:**
- Add `role="button"` to clickable elements
- Add `aria-label` descriptions
- Ensure `tabindex` allows keyboard navigation
- Add focus indicators

**Test:** Tab navigation works, screen reader announces controls

---

## Phase 3 Completion Report

```
=== PHASE 3 COMPLETION REPORT ===
Date: [YYYY-MM-DD HH:MM]
Session: [Session Number]

DATA FIXES:
BUG-012 - Financial Filter: [FIXED/PARTIAL/BLOCKED]
BUG-013 - Connection Dropdown: [FIXED/PARTIAL/BLOCKED]
BUG-014 - Brief Fetch Path: [FIXED/PARTIAL/BLOCKED]
BUG-015 - Entity Colors: [FIXED/PARTIAL/BLOCKED]

FEATURE FIXES:
BUG-016 - Progressive Web: [FIXED/PARTIAL/BLOCKED]
BUG-017 - Controls Position: [FIXED/PARTIAL/BLOCKED]
BUG-018 - Macro Colors: [FIXED/PARTIAL/BLOCKED]
BUG-019 - Accessibility: [FIXED/PARTIAL/BLOCKED]

Total Fixed: X/8
Blockers: [List any blockers]

Ready for Phase 4: [YES/NO]
```

---

## Next Phase

After Phase 3 is complete, proceed to:
**`T:\agents\tasks\BUGFIX_PHASE4_POLISH.md`**

---

*Generated by Session 10 - 2026-01-04*
