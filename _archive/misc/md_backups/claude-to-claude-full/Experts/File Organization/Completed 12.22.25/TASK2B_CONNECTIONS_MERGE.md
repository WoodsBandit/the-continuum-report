# CLAUDE CODE TASK: File Organization — Task 2B Connections Merge & Archive

> **Issued By:** File Organization Expert
> **Date:** 2025-12-22
> **Task:** 2B — Connections Merge & Archive (Approved Actions Only)
> **Priority:** Execute Immediately
> **Authorization:** Option B approved by The Overseer

---

## Objective

Execute the approved safe actions from Option B:
- Merge connections (superset)
- Archive `_updated` files
- DO NOT modify `entities.json`

---

## Step 1: Verify Backups Directory Exists

```bash
mkdir -p /continuum/data/backups
echo "Backups directory confirmed"
```

---

## Step 2: Document Pre-Merge State

```bash
echo "=== PRE-MERGE STATE ==="
echo ""
echo "Current data files:"
ls -la /continuum/data/*.json
echo ""
echo "Current connections.json size and connection count:"
ls -la /continuum/data/connections.json
grep -c '"source":' /continuum/data/connections.json
echo ""
echo "connections_updated.json size and connection count:"
ls -la /continuum/data/connections_updated.json
grep -c '"source":' /continuum/data/connections_updated.json
```

---

## Step 3: Backup Current connections.json

```bash
cp /continuum/data/connections.json /continuum/data/backups/connections_backup_20251222.json
echo "Backed up connections.json to backups/connections_backup_20251222.json"
ls -la /continuum/data/backups/connections_backup_20251222.json
```

---

## Step 4: Replace connections.json with Superset

```bash
cp /continuum/data/connections_updated.json /continuum/data/connections.json
echo "Replaced connections.json with connections_updated.json (superset)"
```

---

## Step 5: Archive connections_updated.json

```bash
mv /continuum/data/connections_updated.json /continuum/data/backups/connections_updated_archived_20251222.json
echo "Archived connections_updated.json to backups/"
```

---

## Step 6: Archive entities_updated.json (Reference for Future Task)

```bash
mv /continuum/data/entities_updated.json /continuum/data/backups/entities_updated_archived_20251222.json
echo "Archived entities_updated.json to backups/ (reference for future 11-entity task)"
```

---

## Step 7: Move Any Other Backup Files to Backups Folder

```bash
# Move any timestamped backups that exist at root of /data/
mv /continuum/data/entities_backup_*.json /continuum/data/backups/ 2>/dev/null && echo "Moved existing entity backups" || echo "No additional entity backups to move"
```

---

## Step 8: Verify entities.json UNCHANGED

```bash
echo ""
echo "=== VERIFYING entities.json UNCHANGED ==="
echo "entities.json current state:"
ls -la /continuum/data/entities.json
echo ""
echo "Entity count (should be 15):"
grep -c '"id":' /continuum/data/entities.json
echo ""
echo "Has tags (should show matches):"
grep -c '"tags"' /continuum/data/entities.json
echo ""
echo "Has connections arrays (should show matches):"
grep -c '"connections"' /continuum/data/entities.json
```

---

## Step 9: Verify Final State

```bash
echo ""
echo "=== POST-MERGE VERIFICATION ==="
echo ""
echo "Data folder contents:"
ls -la /continuum/data/
echo ""
echo "Backups folder contents:"
ls -la /continuum/data/backups/
echo ""
echo "New connections.json connection count (should be 95):"
grep -c '"source":' /continuum/data/connections.json
echo ""
echo "Validating JSON files:"
python3 -c "import json; json.load(open('/continuum/data/entities.json')); print('entities.json: VALID')" 2>&1 || echo "entities.json: INVALID"
python3 -c "import json; json.load(open('/continuum/data/connections.json')); print('connections.json: VALID')" 2>&1 || echo "connections.json: INVALID"
```

---

## Completion Report Format

```
=== TASK 2B COMPLETE ===

Actions Executed:
1. Created/verified /data/backups/ [SUCCESS/FAIL]
2. Backed up connections.json [SUCCESS/FAIL]
3. Replaced connections.json with superset (78 → 95 connections) [SUCCESS/FAIL]
4. Archived connections_updated.json [SUCCESS/FAIL]
5. Archived entities_updated.json (future reference) [SUCCESS/FAIL]
6. Moved additional backups to /backups/ [SUCCESS/SKIPPED]

Verification:
- entities.json: UNCHANGED (15 entities, enriched)
- connections.json: MERGED (now 95 connections)
- JSON validation: [PASS/FAIL]

Final Data State:
- /continuum/data/entities.json: [size] bytes, 15 entities (enriched)
- /continuum/data/connections.json: [size] bytes, 95 connections
- /continuum/data/backups/: [count] archived files

Issues: [NONE / describe]

Ready for Task 3: Briefs Deduplication
```

---

## DO NOT

- ❌ Do NOT modify entities.json
- ❌ Do NOT delete any files
- ❌ Do NOT attempt complex merges

---

*Task prompt created by File Organization Expert — 2025-12-22*
*Authorization: Option B approved by The Overseer*
