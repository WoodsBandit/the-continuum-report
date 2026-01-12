# CLAUDE CODE TASK: File Organization — Task 3 Briefs Deduplication

> **Issued By:** File Organization Expert
> **Date:** 2025-12-22
> **Task:** 3 of 3 — Briefs Deduplication
> **Priority:** Execute Immediately
> **Authorization:** Pre-approved by The Overseer (Directive_2025-12-22.md)

---

## Objective

Compare `/continuum/briefs/` (canonical) with `/continuum/reports/Analytical Briefs/` (legacy) and archive the legacy location if it's a duplicate or subset.

**Known Context:**
- `/briefs/` is canonical — monitored by `brief_watcher.py`, used by dynamic graph system
- `/reports/Analytical Briefs/` is legacy from old Ollama pipeline
- Expected: Legacy is duplicate or subset of canonical

---

## Step 1: Document Both Directories

```bash
echo "=== BRIEFS DIRECTORY COMPARISON ==="
echo ""
echo "Canonical location: /continuum/briefs/"
echo "File count:"
ls -1 /continuum/briefs/*.md 2>/dev/null | wc -l
echo ""
echo "Files:"
ls -la /continuum/briefs/*.md 2>/dev/null | head -50
echo ""
echo "---"
echo ""
echo "Legacy location: /continuum/reports/Analytical Briefs/"
echo "Checking if directory exists..."
if [ -d "/continuum/reports/Analytical Briefs" ]; then
    echo "Directory EXISTS"
    echo ""
    echo "File count:"
    ls -1 "/continuum/reports/Analytical Briefs/"*.md 2>/dev/null | wc -l
    echo ""
    echo "Files:"
    ls -la "/continuum/reports/Analytical Briefs/" 2>/dev/null
else
    echo "Directory DOES NOT EXIST"
fi
```

---

## Step 2: Compare File Lists

```bash
echo ""
echo "=== FILE LIST COMPARISON ==="
echo ""

# Get just filenames from canonical
echo "Files in /continuum/briefs/ (canonical):"
ls -1 /continuum/briefs/*.md 2>/dev/null | xargs -n1 basename | sort > /tmp/briefs_canonical.txt
cat /tmp/briefs_canonical.txt
echo ""
echo "Count: $(wc -l < /tmp/briefs_canonical.txt)"

# Get just filenames from legacy (if exists)
echo ""
echo "Files in /continuum/reports/Analytical Briefs/ (legacy):"
if [ -d "/continuum/reports/Analytical Briefs" ]; then
    ls -1 "/continuum/reports/Analytical Briefs/"*.md 2>/dev/null | xargs -n1 basename | sort > /tmp/briefs_legacy.txt
    cat /tmp/briefs_legacy.txt 2>/dev/null || echo "(no .md files)"
    echo ""
    echo "Count: $(wc -l < /tmp/briefs_legacy.txt 2>/dev/null || echo 0)"
else
    echo "(directory does not exist)"
    touch /tmp/briefs_legacy.txt
fi
```

---

## Step 3: Identify Differences

```bash
echo ""
echo "=== DIFFERENCE ANALYSIS ==="
echo ""

# Files only in canonical (expected: many or all)
echo "Files ONLY in canonical /briefs/ (good - these are current):"
comm -23 /tmp/briefs_canonical.txt /tmp/briefs_legacy.txt 2>/dev/null || echo "N/A"
echo ""

# Files only in legacy (concern: unique files we might lose)
echo "Files ONLY in legacy /reports/Analytical Briefs/ (CONCERN - would be lost if archived):"
LEGACY_ONLY=$(comm -13 /tmp/briefs_canonical.txt /tmp/briefs_legacy.txt 2>/dev/null)
if [ -z "$LEGACY_ONLY" ]; then
    echo "(none - safe to archive)"
else
    echo "$LEGACY_ONLY"
    echo ""
    echo "WARNING: Legacy contains unique files not in canonical!"
fi
echo ""

# Files in both (duplicates)
echo "Files in BOTH locations (duplicates):"
comm -12 /tmp/briefs_canonical.txt /tmp/briefs_legacy.txt 2>/dev/null || echo "N/A"
```

---

## Step 4: Decision Point

Based on analysis, determine which scenario applies:

### Scenario A: Legacy is Subset or Identical (Safe to Archive)

If legacy contains NO unique files (all legacy files exist in canonical):

```bash
echo "=== EXECUTING SCENARIO A: Archiving Legacy ==="

# Create archive directory
mkdir -p /continuum/_archive/reports_analytical_briefs

# Move entire legacy directory contents to archive
mv "/continuum/reports/Analytical Briefs"/* /continuum/_archive/reports_analytical_briefs/ 2>/dev/null

# Remove empty legacy directory
rmdir "/continuum/reports/Analytical Briefs" 2>/dev/null

# Check if /reports/ is now empty
if [ -z "$(ls -A /continuum/reports/ 2>/dev/null)" ]; then
    echo "Note: /continuum/reports/ is now empty - could be removed"
else
    echo "Note: /continuum/reports/ still contains other items:"
    ls -la /continuum/reports/
fi

echo "SCENARIO A COMPLETE - Legacy archived"
```

### Scenario B: Legacy Contains Unique Files (Escalation Required)

If legacy contains files NOT in canonical:

```bash
echo "=== SCENARIO B DETECTED: UNIQUE FILES IN LEGACY ==="
echo "STOPPING - Escalation required"
echo ""
echo "The following files exist ONLY in legacy and would be lost:"
comm -13 /tmp/briefs_canonical.txt /tmp/briefs_legacy.txt
echo ""
echo "Options:"
echo "1. Copy unique files to /continuum/briefs/ before archiving"
echo "2. Keep legacy as-is pending review"
echo "3. Archive but note unique files for recovery"
echo ""
echo "Awaiting File Organization Expert decision."
```

### Scenario C: Legacy Directory Does Not Exist

If `/continuum/reports/Analytical Briefs/` doesn't exist:

```bash
echo "=== SCENARIO C: No Legacy Directory ==="
echo "Nothing to deduplicate - legacy location does not exist"
echo "Task 3 complete by default"
```

---

## Step 5: Post-Archive Verification (If Scenario A)

```bash
echo ""
echo "=== POST-ARCHIVE VERIFICATION ==="
echo ""
echo "Canonical /continuum/briefs/ (should be unchanged):"
ls -1 /continuum/briefs/*.md 2>/dev/null | wc -l
echo "files"
echo ""
echo "Archive contents:"
ls -la /continuum/_archive/reports_analytical_briefs/ 2>/dev/null || echo "(archive not created)"
echo ""
echo "Legacy location (should be gone or empty):"
ls -la "/continuum/reports/Analytical Briefs/" 2>/dev/null || echo "(directory removed)"
echo ""
echo "/continuum/reports/ status:"
ls -la /continuum/reports/ 2>/dev/null || echo "(directory empty or removed)"
```

---

## Completion Report Format

```
=== TASK 3 COMPLETE ===

Scenario Executed: [A: Archived / B: Escalation / C: No Legacy]

Analysis Results:
- Canonical /briefs/: [count] files
- Legacy /reports/Analytical Briefs/: [count] files (or N/A)
- Unique to canonical: [count]
- Unique to legacy: [count] (should be 0 for Scenario A)
- Duplicates: [count]

Actions Taken:
1. Compared file lists [COMPLETE]
2. Identified differences [COMPLETE]
3. [Archived legacy to /_archive/ / STOPPED for escalation / No action needed]

Final State:
- /continuum/briefs/: [count] files (canonical, unchanged)
- /continuum/_archive/reports_analytical_briefs/: [count] files (if archived)
- /continuum/reports/Analytical Briefs/: [REMOVED / KEPT / N/A]

Issues: [NONE / describe]

=== ALL THREE TASKS COMPLETE ===
```

---

## Error Handling

- If legacy contains unique files: STOP and document for escalation
- Do NOT delete any files — archive only
- Preserve file permissions when moving

---

*Task prompt created by File Organization Expert — 2025-12-22*
