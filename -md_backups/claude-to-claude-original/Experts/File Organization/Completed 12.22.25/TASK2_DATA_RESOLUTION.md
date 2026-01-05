# CLAUDE CODE TASK: File Organization — Task 2 Data File Resolution

> **Issued By:** File Organization Expert
> **Date:** 2025-12-22
> **Task:** 2 of 3 — Data File Resolution
> **Priority:** Execute Immediately
> **Unblocks:** Connection Brief Methodology Expert

---

## Objective

Resolve the data file versioning confusion in `/continuum/data/`. Determine canonical versions, merge if appropriate, and organize backups.

**Critical:** The live site reads `entities.json` and `connections.json` — NOT the `_updated` versions. Changes here affect the live site immediately.

---

## Step 1: Create Backup Directory

```bash
mkdir -p /continuum/data/backups
echo "Created /continuum/data/backups/"
```

---

## Step 2: Document Current State

```bash
echo "=== CURRENT DATA FILE STATE ==="
echo ""
ls -la /continuum/data/
echo ""
echo "File sizes:"
wc -c /continuum/data/*.json
```

---

## Step 3: Diff entities.json vs entities_updated.json

```bash
echo ""
echo "=== ENTITIES DIFF ANALYSIS ==="
echo ""

# Check if both files exist
if [ -f /continuum/data/entities.json ] && [ -f /continuum/data/entities_updated.json ]; then
    echo "Both entities files exist"
    echo ""
    
    # Size comparison
    echo "Size comparison:"
    ls -la /continuum/data/entities.json /continuum/data/entities_updated.json
    echo ""
    
    # Structure comparison - count entities
    echo "Entity count in entities.json:"
    grep -c '"id":' /continuum/data/entities.json || echo "Could not count"
    
    echo "Entity count in entities_updated.json:"
    grep -c '"id":' /continuum/data/entities_updated.json || echo "Could not count"
    echo ""
    
    # Check for key differences
    echo "Checking for 'tags' arrays (enrichment indicator):"
    echo "In entities.json:"
    grep -c '"tags"' /continuum/data/entities.json || echo "0"
    echo "In entities_updated.json:"
    grep -c '"tags"' /continuum/data/entities_updated.json || echo "0"
    echo ""
    
    echo "Checking for 'connections' arrays:"
    echo "In entities.json:"
    grep -c '"connections"' /continuum/data/entities.json || echo "0"
    echo "In entities_updated.json:"
    grep -c '"connections"' /continuum/data/entities_updated.json || echo "0"
    echo ""
    
    # Sample first entity from each
    echo "First entity structure in entities.json:"
    head -50 /continuum/data/entities.json
    echo ""
    echo "First entity structure in entities_updated.json:"
    head -50 /continuum/data/entities_updated.json
    
else
    echo "ERROR: One or both entities files missing"
    ls -la /continuum/data/entities*.json
fi
```

---

## Step 4: Diff connections.json vs connections_updated.json

```bash
echo ""
echo "=== CONNECTIONS DIFF ANALYSIS ==="
echo ""

# Check if both files exist
if [ -f /continuum/data/connections.json ] && [ -f /continuum/data/connections_updated.json ]; then
    echo "Both connections files exist"
    echo ""
    
    # Size comparison
    echo "Size comparison:"
    ls -la /continuum/data/connections.json /continuum/data/connections_updated.json
    echo ""
    
    # Connection count
    echo "Connection count in connections.json:"
    grep -c '"source":' /continuum/data/connections.json || echo "Could not count"
    
    echo "Connection count in connections_updated.json:"
    grep -c '"source":' /continuum/data/connections_updated.json || echo "Could not count"
    echo ""
    
    # Sample structure
    echo "First few connections in connections.json:"
    head -30 /continuum/data/connections.json
    echo ""
    echo "First few connections in connections_updated.json:"
    head -30 /continuum/data/connections_updated.json
    
else
    echo "ERROR: One or both connections files missing"
    ls -la /continuum/data/connections*.json
fi
```

---

## Step 5: Decision Point

Based on the diff analysis, determine which scenario applies:

### Scenario A: `_updated` is Superset (Expected)
If `_updated` files have the same entities PLUS enrichment (tags, connections arrays):

```bash
echo "=== EXECUTING SCENARIO A: _updated is superset ==="

# Backup originals with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

cp /continuum/data/entities.json /continuum/data/backups/entities_pre_merge_${TIMESTAMP}.json
echo "Backed up entities.json"

cp /continuum/data/connections.json /continuum/data/backups/connections_pre_merge_${TIMESTAMP}.json
echo "Backed up connections.json"

# Replace originals with updated versions
cp /continuum/data/entities_updated.json /continuum/data/entities.json
echo "Replaced entities.json with entities_updated.json"

cp /continuum/data/connections_updated.json /continuum/data/connections.json
echo "Replaced connections.json with connections_updated.json"

# Move _updated files to backups (no longer needed at root)
mv /continuum/data/entities_updated.json /continuum/data/backups/
mv /continuum/data/connections_updated.json /continuum/data/backups/
echo "Moved _updated files to backups"

# Move any other backup files to backups folder
mv /continuum/data/entities_backup_*.json /continuum/data/backups/ 2>/dev/null
echo "Moved timestamped backups to backups folder"

echo "SCENARIO A COMPLETE"
```

### Scenario B: Files are Conflicting
If files have different/conflicting data (not a superset relationship):

```bash
echo "=== SCENARIO B DETECTED: CONFLICTING DATA ==="
echo "STOPPING - Escalation required"
echo ""
echo "Findings to report to File Organization Expert:"
echo "1. Describe the specific conflicts found"
echo "2. List what data exists in each version"
echo "3. Recommend which version should be canonical"
```

---

## Step 6: Post-Resolution Verification

```bash
echo ""
echo "=== POST-RESOLUTION STATE ==="
echo ""
echo "Data folder contents:"
ls -la /continuum/data/
echo ""
echo "Backups folder contents:"
ls -la /continuum/data/backups/
echo ""
echo "Canonical entities.json structure (first 30 lines):"
head -30 /continuum/data/entities.json
echo ""
echo "Canonical connections.json structure (first 30 lines):"
head -30 /continuum/data/connections.json
```

---

## Step 7: Verify Site Still Works

```bash
echo ""
echo "=== SITE VERIFICATION ==="
echo ""
echo "Checking if entities.json is valid JSON:"
python3 -c "import json; json.load(open('/continuum/data/entities.json')); print('entities.json: VALID JSON')" 2>&1 || echo "entities.json: INVALID JSON"

echo "Checking if connections.json is valid JSON:"
python3 -c "import json; json.load(open('/continuum/data/connections.json')); print('connections.json: VALID JSON')" 2>&1 || echo "connections.json: INVALID JSON"

echo ""
echo "Entity count in canonical entities.json:"
python3 -c "import json; data=json.load(open('/continuum/data/entities.json')); print(f'Entities: {len(data.get(\"entities\", data)) if isinstance(data, dict) else len(data)}')" 2>&1 || echo "Could not count"
```

---

## Completion Report Format

```
=== TASK 2 COMPLETE ===

Scenario Executed: [A: Superset Merge / B: Escalation Required]

Actions Taken:
1. Created /continuum/data/backups/ [SUCCESS/FAIL]
2. Backed up original entities.json [SUCCESS/FAIL/SKIPPED]
3. Backed up original connections.json [SUCCESS/FAIL/SKIPPED]
4. Replaced entities.json with enriched version [SUCCESS/FAIL/SKIPPED]
5. Replaced connections.json with enriched version [SUCCESS/FAIL/SKIPPED]
6. Moved _updated and backup files to /backups/ [SUCCESS/FAIL]
7. Validated JSON files [SUCCESS/FAIL]

Final State:
- /continuum/data/entities.json: [size] bytes, [count] entities
- /continuum/data/connections.json: [size] bytes, [count] connections
- /continuum/data/backups/: [count] backup files

Issues: [NONE / describe]

IF SCENARIO B: Include full diff findings for escalation.

Ready for Task 3: Briefs Deduplication
```

---

## Error Handling

- If JSON validation fails after merge: RESTORE from backups immediately
- If unexpected file structure: STOP and document for escalation
- Do NOT proceed to Task 3 if data files are in uncertain state

---

*Task prompt created by File Organization Expert — 2025-12-22*
