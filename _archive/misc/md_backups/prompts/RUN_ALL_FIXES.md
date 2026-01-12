# CONTINUUM FIX ORCHESTRATOR

## OBJECTIVE
Execute all 10 bug fix prompts sequentially to repair the continuum.html visualization system.

## WORKING DIRECTORY
```
/mnt/user/continuum/
```

## PROMPT LOCATION
```
/mnt/user/continuum/Prompts/12.21 fix/
```

## TARGET FILE
```
/mnt/user/continuum/website/continuum.html
```

## PHASE 0: SETUP

### Step 1: Create Backup
```bash
mkdir -p /mnt/user/continuum/website/backups
cp /mnt/user/continuum/website/continuum.html "/mnt/user/continuum/website/backups/continuum_pre-fixes_$(date +%Y%m%d_%H%M%S).html"
```

### Step 2: List Available Fix Prompts
```bash
ls -la "/mnt/user/continuum/Prompts/12.21 fix/"
```

### Step 3: Read the Index First
```bash
cat "/mnt/user/continuum/Prompts/12.21 fix/FIX_INDEX.md"
```

## EXECUTION ORDER

Execute these prompts **in this exact order**:

| Order | Filename | Description |
|-------|----------|-------------|
| 1 | FIX01_DETAIL_PANEL_OFFSET.md | CSS: Detail panel top offset |
| 2 | FIX02_MACRO_TEXT_OVERFLOW.md | CSS: Macro box text overflow |
| 3 | FIX03_CARD_GRID_RESPONSIVE.md | CSS: Card grid responsive |
| 4 | FIX04_ENTITIES_DIRECT_ACCESS.md | JS: Side panel navigation |
| 5 | FIX05_BREADCRUMB_STATE.md | JS: Breadcrumb sync |
| 6 | FIX06_CARD_TO_WEB_LAYER.md | JS: Card click transition |
| 7 | FIX07_FINANCIAL_FILTER.md | JS/Data: Category filter |
| 8 | FIX08_CONNECTION_DATA_READING.md | JS: Connection data reading |
| 9 | FIX09_BRIEF_FETCH_PATH.md | JS: Brief fetch path |
| 10 | FIX10_COLOR_SCHEMA.md | JS/CSS: Color schema |

## EXECUTION PROTOCOL

For each fix (1-10):

1. **Read the prompt file:**
```bash
cat "/mnt/user/continuum/Prompts/12.21 fix/FIX0X_NAME.md"
```

2. **Understand the issue** described in the prompt

3. **Locate the code** in continuum.html at the specified line numbers

4. **Apply the fix** as described in the prompt

5. **Verify the change** was applied correctly

6. **Log completion** before moving to next fix

## IMPORTANT RULES

1. **DO NOT skip fixes** - they may have dependencies
2. **Read each prompt fully** before making changes
3. **Make only the changes specified** in each prompt
4. **If a prompt offers multiple options**, use the "Recommended" option
5. **If you encounter an error**, stop and report it - do not continue blindly
6. **Log what you changed** after each fix

## DATA VERIFICATION (Before FIX07-08)

Before executing FIX07 and FIX08, verify the data structure:

```bash
# Check entities.json exists and show sample
head -100 /mnt/user/continuum/data/entities.json

# Check for tags in entities
grep -o '"tags":\s*\[[^]]*\]' /mnt/user/continuum/data/entities.json | head -20

# Check for connections array structure
grep -A5 '"connections"' /mnt/user/continuum/data/entities.json | head -30
```

## PATH VERIFICATION (Before FIX09)

Before executing FIX09, verify brief locations:

```bash
# Find connection briefs
find /mnt/user/continuum -name "*_connections.md" 2>/dev/null | head -10

# Check briefs directory structure
ls -la /mnt/user/continuum/briefs/ 2>/dev/null
ls -la /mnt/user/continuum/briefs/connections/ 2>/dev/null
```

## COMPLETION REPORT

After all fixes are applied, generate a summary:

```
=== CONTINUUM FIX COMPLETION REPORT ===
Date: [timestamp]
Backup: /mnt/user/continuum/website/backups/continuum_pre-fixes_XXXXXX.html

FIX01 - Detail Panel Offset: [APPLIED/SKIPPED/ERROR]
FIX02 - Macro Text Overflow: [APPLIED/SKIPPED/ERROR]
FIX03 - Card Grid Responsive: [APPLIED/SKIPPED/ERROR]
FIX04 - Entities Direct Access: [APPLIED/SKIPPED/ERROR]
FIX05 - Breadcrumb State: [APPLIED/SKIPPED/ERROR]
FIX06 - Card to Web Layer: [APPLIED/SKIPPED/ERROR]
FIX07 - Financial Filter: [APPLIED/SKIPPED/ERROR]
FIX08 - Connection Data Reading: [APPLIED/SKIPPED/ERROR]
FIX09 - Brief Fetch Path: [APPLIED/SKIPPED/ERROR]
FIX10 - Color Schema: [APPLIED/SKIPPED/ERROR]

Total Applied: X/10
Errors: [list any errors]

Next Steps: [any manual verification needed]
```

## ERROR HANDLING

If any fix fails:
1. Log the error with details
2. Note which fix failed and why
3. Continue to next fix if possible (CSS fixes are independent)
4. Stop if a JS logic fix fails (FIX04-06 are dependent)

## BEGIN EXECUTION

Start by:
1. Creating backup
2. Reading FIX_INDEX.md
3. Reading FIX01_DETAIL_PANEL_OFFSET.md
4. Applying FIX01
5. Continue through FIX10
6. Generate completion report
