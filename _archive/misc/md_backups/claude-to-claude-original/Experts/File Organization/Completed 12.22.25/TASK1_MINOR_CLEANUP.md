# CLAUDE CODE TASK: File Organization — Task 1 Minor Cleanup

> **Issued By:** File Organization Expert
> **Date:** 2025-12-22
> **Task:** 1 of 3 — Minor Cleanup (6 Moves)
> **Priority:** Execute Immediately

---

## Objective

Execute 6 file moves to clean up root-level clutter on Tower. These are zero-risk operations on empty directories and misplaced files.

---

## Pre-Flight

First, create the archive directory if it doesn't exist:

```bash
mkdir -p /mnt/user/continuum/_archive
```

Verify current state before moves:

```bash
echo "=== PRE-MOVE VERIFICATION ==="
echo ""
echo "Checking /entity_data/:"
ls -la /mnt/user/continuum/entity_data/ 2>/dev/null || echo "Directory empty or doesn't exist"
echo ""
echo "Checking /processed/:"
ls -la /mnt/user/continuum/processed/ 2>/dev/null || echo "Directory empty or doesn't exist"
echo ""
echo "Checking root files:"
ls -la /mnt/user/continuum/errors.log 2>/dev/null || echo "errors.log not found"
ls -la /mnt/user/continuum/progress.json 2>/dev/null || echo "progress.json not found"
ls -la /mnt/user/continuum/progress_executive_power.json 2>/dev/null || echo "progress_executive_power.json not found"
ls -la /mnt/user/continuum/CLAUDE_CODE_CONTINUUM_TASK.md 2>/dev/null || echo "CLAUDE_CODE_CONTINUUM_TASK.md not found"
```

---

## Execute Moves

### Move 1: Archive /entity_data/

```bash
mv /mnt/user/continuum/entity_data /mnt/user/continuum/_archive/entity_data
echo "Move 1 complete: entity_data -> _archive/entity_data"
```

### Move 2: Archive /processed/

```bash
mv /mnt/user/continuum/processed /mnt/user/continuum/_archive/processed
echo "Move 2 complete: processed -> _archive/processed"
```

### Move 3: Move errors.log to /logs/

```bash
mv /mnt/user/continuum/errors.log /mnt/user/continuum/logs/errors.log
echo "Move 3 complete: errors.log -> logs/errors.log"
```

### Move 4: Move progress.json to /logs/

```bash
mv /mnt/user/continuum/progress.json /mnt/user/continuum/logs/progress.json
echo "Move 4 complete: progress.json -> logs/progress.json"
```

### Move 5: Move progress_executive_power.json to /logs/

```bash
mv /mnt/user/continuum/progress_executive_power.json /mnt/user/continuum/logs/progress_executive_power.json
echo "Move 5 complete: progress_executive_power.json -> logs/progress_executive_power.json"
```

### Move 6: Move CLAUDE_CODE_CONTINUUM_TASK.md to /config/

```bash
mkdir -p /mnt/user/continuum/config
mv /mnt/user/continuum/CLAUDE_CODE_CONTINUUM_TASK.md /mnt/user/continuum/config/CLAUDE_CODE_CONTINUUM_TASK.md
echo "Move 6 complete: CLAUDE_CODE_CONTINUUM_TASK.md -> config/CLAUDE_CODE_CONTINUUM_TASK.md"
```

---

## Post-Move Verification

```bash
echo ""
echo "=== POST-MOVE VERIFICATION ==="
echo ""
echo "Archive contents:"
ls -la /mnt/user/continuum/_archive/
echo ""
echo "Logs folder contents:"
ls -la /mnt/user/continuum/logs/
echo ""
echo "Config folder contents:"
ls -la /mnt/user/continuum/config/
echo ""
echo "Root level (should be cleaner now):"
ls -la /mnt/user/continuum/ | head -20
```

---

## Completion Report

After all moves complete, output:

```
=== TASK 1 COMPLETE ===

Moves executed:
1. /entity_data/ -> /_archive/entity_data/ [SUCCESS/FAIL]
2. /processed/ -> /_archive/processed/ [SUCCESS/FAIL]
3. /errors.log -> /logs/errors.log [SUCCESS/FAIL]
4. /progress.json -> /logs/progress.json [SUCCESS/FAIL]
5. /progress_executive_power.json -> /logs/progress_executive_power.json [SUCCESS/FAIL]
6. /CLAUDE_CODE_CONTINUUM_TASK.md -> /config/CLAUDE_CODE_CONTINUUM_TASK.md [SUCCESS/FAIL]

Issues encountered: [NONE / describe any issues]

Ready for Task 2: Data File Resolution
```

---

## Error Handling

If any move fails:
- Note which move failed and why
- Continue with remaining moves
- Report all failures in completion summary

---

*Task prompt created by File Organization Expert — 2025-12-22*
