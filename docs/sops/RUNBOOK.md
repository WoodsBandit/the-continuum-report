# The Continuum Report - Pipeline Operations Runbook

**Quick Reference Guide for Pipeline Operations**
**Version:** 1.0
**Last Updated:** 2025-12-25

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Pipeline Status Check](#pipeline-status-check)
3. [Common Operations](#common-operations)
4. [Troubleshooting](#troubleshooting)
5. [Manual Interventions](#manual-interventions)
6. [Emergency Procedures](#emergency-procedures)

---

## Quick Start

### The Two Human Touchpoints

**Touchpoint 1: Upload Source Document**
```bash
# Upload PDF to Paperless-ngx via web interface
# http://localhost:8040/upload

# Pipeline automatically triggers:
# Stage 1 → Stage 2 → Stage 3 → pending_approval/
```

**Touchpoint 2: Approve Briefs**
```bash
# 1. Review briefs in pending_approval/
cd project_root/pending_approval

# 2. Read REVIEW_LOG.md for context
cat REVIEW_LOG.md

# 3. Review each brief
# Check for accuracy, legal compliance, editorial quality

# 4. Move approved briefs to approved/
mv entities/analytical_brief_John_Doe.md ../approved/entities/
mv connections/John_Doe_Acme_Corporation.md ../approved/connections/

# Pipeline automatically publishes:
# Stage 4 → website/ → archive/
```

---

## Pipeline Status Check

### Check If Pipeline Is Running

```bash
# Check for halt signals
ls project_root/PIPELINE_HALTED
ls project_root/PUBLICATION_HALTED

# If these files exist, pipeline is halted
# Remove them to resume operations

# Check last run timestamps
cat project_root/logs\stage1_last_run.txt
cat project_root/logs\stage2_last_run.txt
cat project_root/logs\stage3_last_run.txt
cat project_root/logs\stage4_last_run.txt
```

### Check Current Processing Queue

```bash
# Pending approval (awaiting human review)
ls -lh project_root/pending_approval\entities\
ls -lh project_root/pending_approval\connections\

# Approved (awaiting publication)
ls -lh project_root/approved\entities\
ls -lh project_root/approved\connections\

# Recently published
ls -lth project_root/archive\published\entities\ | head -10
```

### View Recent Errors

```bash
# Check error logs
tail -50 project_root/logs\pipeline_errors.log

# Check stage-specific logs
tail -50 project_root/logs\stage1_ingestion.log
tail -50 project_root/logs\stage2_context_extraction.log
tail -50 project_root/logs\stage3_brief_generation.log
tail -50 project_root/logs\stage4_publication.log
```

---

## Common Operations

### Manually Trigger Pipeline Stages

#### Trigger Stage 1 (Source Ingestion)
```bash
# Manual ingestion of specific document
python project_root/scripts\run_stage1.py \
  --document-id 12345 \
  --file-path "project_root/sources\test\document.pdf"

# Force reprocess existing document
python project_root/scripts\run_stage1.py \
  --document-id 12345 \
  --force-reprocess
```

#### Trigger Stage 2 (Context Extraction)
```bash
# Process specific entities
python project_root/scripts\run_stage2.py \
  --entities "John Doe,Jane Smith"

# Process all entities
python project_root/scripts\run_stage2.py --all
```

#### Trigger Stage 3 (Brief Generation)
```bash
# Generate brief for specific entity
python project_root/scripts\run_stage3.py \
  --entity "John Doe"

# Generate brief for specific connection
python project_root/scripts\run_stage3.py \
  --connection "John Doe|Acme Corporation"

# Process all pending briefs
python project_root/scripts\run_stage3.py --all
```

#### Trigger Stage 4 (Publication)
```bash
# Publish all approved briefs
python project_root/scripts\run_stage4.py

# Publish specific brief
python project_root/scripts\run_stage4.py \
  --brief "analytical_brief_John_Doe.md"
```

### Query Pipeline Data

#### Find Entity Information
```bash
# Search entity registry
jq '.entities["John Doe"]' project_root/indexes\entity_registry.json

# Find all sources mentioning entity
jq '.sources | to_entries | map(select(.value.entities_mentioned | contains(["John Doe"]))) | .[].key' \
  project_root/indexes\source_mentions.json

# Count entity mentions
jq '.entities["John Doe"].mention_count' project_root/indexes\entity_registry.json
```

#### Find Connection Information
```bash
# Get connection details
jq '.pairs["John Doe|Acme Corporation"]' project_root/indexes\co_occurrence.json

# Get connection contexts
jq '.connections["John Doe|Acme Corporation"].contexts' project_root/indexes\connection_contexts.json

# Count connections for entity
jq '.pairs | to_entries | map(select(.key | contains("John Doe"))) | length' \
  project_root/indexes\co_occurrence.json
```

#### Find Source Information
```bash
# Get source details
jq '.sources["src_000042"]' project_root/indexes\source_mentions.json

# Check if source processed
jq '.sources[] | select(.paperless_id == 12345)' project_root/indexes\processed_sources.json

# List all processed sources
jq '.sources[].source_id' project_root/indexes\processed_sources.json
```

### Backup Operations

#### Create Manual Backup
```bash
# Backup all indexes
timestamp=$(date +%Y%m%d_%H%M%S)
mkdir -p project_root/backups\manual_$timestamp

cp project_root/indexes\*.json project_root/backups\manual_$timestamp\

echo "Backup created: manual_$timestamp"
```

#### Restore from Backup
```bash
# List available backups
ls -lh project_root/backups\

# Restore specific backup
backup_name="manual_20251225_120000"

cp project_root/backups\$backup_name\*.json project_root/indexes\

echo "Restored from backup: $backup_name"

# Validate restored files
python project_root/scripts\validate_indexes.py
```

### Website Operations

#### View Website Statistics
```bash
# Count published entities
jq '.entities | length' project_root/website\data\entities.json

# Count published connections
jq '.connections | length' project_root/website\data\connections.json

# Get last update time
jq '._last_updated' project_root/website\data\entities.json

# List recently updated entities
jq '.entities | sort_by(.last_updated) | reverse | .[0:10] | .[].name' \
  project_root/website\data\entities.json
```

#### Rebuild Website Data
```bash
# If entities.json or connections.json corrupted
python project_root/scripts\rebuild_website_data.py

# Validate website data
python project_root/scripts\validate_website_data.py
```

---

## Troubleshooting

### Pipeline Not Processing New Documents

**Symptoms:**
- Document uploaded to Paperless but no activity in logs
- No new entries in processed_sources.json

**Diagnosis:**
```bash
# Check webhook endpoint
curl -X POST http://localhost:5000/api/continuum/ingest \
  -H "Content-Type: application/json" \
  -d '{"test": true}'

# Check Stage 1 trigger script running
ps aux | grep run_stage1

# Check Paperless webhook configuration
# Visit: http://localhost:8040/admin/paperless/webhooks/
```

**Resolution:**
```bash
# Restart webhook listener
pkill -f run_stage1
nohup python project_root/scripts\run_stage1_listener.py &

# Or manually trigger Stage 1 for document
python project_root/scripts\run_stage1.py --document-id 12345
```

### Briefs Not Appearing in pending_approval/

**Symptoms:**
- Stage 2 and 3 logs show activity
- No briefs in pending_approval/

**Diagnosis:**
```bash
# Check Stage 3 errors
tail -100 project_root/logs\stage3_brief_generation.log | grep ERROR

# Check if briefs stuck in briefs/ directory
ls -lh project_root/briefs\entity\
ls -lh project_root/briefs\connections\

# Check legal review failures
grep "ISSUES FOUND" project_root/briefs\entity\*.md
```

**Resolution:**
```bash
# Manually move briefs to pending_approval
cp project_root/briefs\entity\*.md project_root/pending_approval\entities\

# Re-run Stage 3 with verbose logging
python project_root/scripts\run_stage3.py --all --verbose
```

### Legal Review Always Failing

**Symptoms:**
- All briefs marked "ISSUES FOUND"
- Legal review errors in metadata

**Diagnosis:**
```bash
# Check specific legal issues
jq '.legal_issues' project_root/pending_approval\entities\analytical_brief_John_Doe.md

# Check legal-auditor agent availability
python -c "import claude; print(claude.list_agents())"
```

**Resolution:**
```bash
# Review and fix common issues:
# 1. Missing source attribution
# 2. Speculative language
# 3. Unsupported claims

# Manually approve brief (add to metadata)
# legal_review: "MANUAL_OVERRIDE"
# manual_approver: "Your Name"
# approval_reason: "Reason for override"

# Re-run legal review on specific brief
python project_root/scripts\run_legal_review.py \
  --brief "analytical_brief_John_Doe.md"
```

### Publication Failing

**Symptoms:**
- Briefs in approved/ not publishing
- Stage 4 errors in logs

**Diagnosis:**
```bash
# Check Stage 4 errors
tail -100 project_root/logs\stage4_publication.log | grep ERROR

# Check website directory permissions
ls -ld project_root/website\data\
ls -ld project_root/website\briefs\

# Check disk space
df -h project_root/
```

**Resolution:**
```bash
# Fix permissions
chmod -R 755 project_root/website\

# Free disk space if needed
# (Archive or remove old logs, backups)

# Manually trigger publication
python project_root/scripts\run_stage4.py --verbose

# If all else fails, publish to staging
python project_root/scripts\run_stage4.py --staging
```

### Duplicate Entities

**Symptoms:**
- Same entity appears multiple times with different names
- "John Doe" vs "J. Doe" vs "Jonathan Doe"

**Diagnosis:**
```bash
# Search for similar entity names
jq '.entities | keys | map(select(. | contains("Doe")))' \
  project_root/indexes\entity_registry.json
```

**Resolution:**
```bash
# Merge entities using merge script
python project_root/scripts\merge_entities.py \
  --primary "John Doe" \
  --aliases "J. Doe,Jonathan Doe,John C. Doe"

# This will:
# 1. Consolidate all mentions under primary name
# 2. Add variants to aliases
# 3. Merge source lists
# 4. Rebuild affected briefs
```

### Missing Source Files

**Symptoms:**
- Errors about source files not found
- Context extraction failing

**Diagnosis:**
```bash
# Find missing sources
for source in $(jq -r '.sources[].file_path' project_root/indexes\source_mentions.json); do
  if [ ! -f "$source" ]; then
    echo "MISSING: $source"
  fi
done
```

**Resolution:**
```bash
# Re-mirror from Paperless
python project_root/scripts\mirror_sources.py --all

# Or manually copy source
# Find document ID in Paperless, download, copy to sources/paperless_mirror/
```

---

## Manual Interventions

### Reviewing and Approving Briefs

**Standard Approval Process:**
```bash
# 1. Navigate to pending approval
cd project_root/pending_approval

# 2. Read review log
cat REVIEW_LOG.md

# 3. Review entity briefs
cd entities/
for brief in *.md; do
  echo "=== Reviewing: $brief ==="
  head -50 "$brief"  # Read first 50 lines
  read -p "Approve? (y/n): " choice
  if [ "$choice" = "y" ]; then
    mv "$brief" ../../approved/entities/
    echo "Approved: $brief"
  fi
done

# 4. Review connection briefs
cd ../connections/
# (Repeat similar process)

# 5. Verify approved directory
ls -lh ../../approved/entities/
ls -lh ../../approved/connections/

# Stage 4 will auto-publish within 60 seconds
```

**Handling Briefs with Legal Issues:**
```bash
# Find briefs with legal issues
grep -l "legal_review: \"ISSUES FOUND\"" project_root/pending_approval\entities\*.md

# For each brief with issues:
# 1. Open in text editor
# 2. Review legal_issues list in metadata
# 3. Fix identified problems
# 4. Update metadata:
#    legal_review: "MANUAL_APPROVAL"
#    manual_approver: "Your Name"
#    approval_date: "2025-12-25T12:00:00Z"
# 5. Move to approved/

# Example fix: Add source attribution
# BEFORE: "The company engaged in questionable practices."
# AFTER: "According to Document ABC (2024), the company engaged in questionable practices."
```

### Editing Published Briefs

**To Update a Published Brief:**
```bash
# 1. Locate published brief on website
brief_path="project_root/website\briefs\entity\analytical_brief_John_Doe.md"

# 2. Copy to working directory
cp "$brief_path" project_root/briefs\entity\

# 3. Edit the brief
# (Use your preferred editor)

# 4. Update metadata version
# brief_version: "1.2" → "1.3"

# 5. Run through Stage 3 for legal review
python project_root/scripts\run_stage3.py \
  --entity "John Doe" --update-only

# 6. Approve and republish
mv project_root/pending_approval\entities\analytical_brief_John_Doe.md \
   project_root/approved\entities\

# Stage 4 will republish automatically
```

### Adding Entity Manually

**When automatic extraction misses an entity:**
```bash
# 1. Add to entity registry
python project_root/scripts\add_entity.py \
  --name "New Entity Name" \
  --type "PERSON" \
  --source "src_000042" \
  --mention-count 1

# 2. Trigger Stage 2 for context extraction
python project_root/scripts\run_stage2.py \
  --entities "New Entity Name"

# 3. Trigger Stage 3 for brief generation
python project_root/scripts\run_stage3.py \
  --entity "New Entity Name"

# 4. Review and approve as usual
```

### Deleting Entity/Brief

**To remove an entity from the system:**
```bash
# WARNING: This is destructive and should be used carefully

# 1. Remove from entity registry
python project_root/scripts\remove_entity.py \
  --entity "Entity to Remove" \
  --reason "Duplicate/Error/Privacy"

# 2. Remove brief from website
rm project_root/website\briefs\entity\analytical_brief_Entity_to_Remove.md

# 3. Remove from website data
python project_root/scripts\remove_from_website_data.py \
  --entity "Entity to Remove"

# 4. Archive the deletion record
# (Script automatically archives in archive/deletions/)
```

---

## Emergency Procedures

### Emergency Pipeline Shutdown

**When to use:**
- Data corruption detected
- Runaway processing (too many briefs)
- Legal compliance emergency

**Procedure:**
```bash
# 1. Create halt signal
touch project_root/PIPELINE_HALTED

# 2. Kill all running pipeline processes
pkill -f run_stage1
pkill -f run_stage2
pkill -f run_stage3
pkill -f run_stage4

# 3. Verify no processing
ps aux | grep continuum

# 4. Create incident report
cat > project_root/logs\INCIDENT_$(date +%Y%m%d_%H%M%S).txt <<EOF
EMERGENCY SHUTDOWN
Date: $(date)
Reason: [FILL IN REASON]
Operator: [YOUR NAME]
Pipeline state at shutdown:
$(ls -lh project_root/pending_approval\)
$(tail -20 project_root/logs\pipeline_errors.log)
EOF

# 5. Notify team
# (Send alert via your notification system)
```

### Emergency Backup and Restore

**Full System Backup:**
```bash
# Create emergency backup of entire continuum directory
timestamp=$(date +%Y%m%d_%H%M%S)
backup_dir="project_root/backups\emergency_$timestamp"

mkdir -p "$backup_dir"

# Backup indexes (critical)
cp -r project_root/indexes "$backup_dir/"

# Backup briefs
cp -r project_root/briefs "$backup_dir/"

# Backup website data
cp -r project_root/website\data "$backup_dir/"

# Backup pending work
cp -r project_root/pending_approval "$backup_dir/"
cp -r project_root/approved "$backup_dir/"

echo "Emergency backup created: $backup_dir"
```

**Full System Restore:**
```bash
# WARNING: This will overwrite current data

backup_dir="project_root/backups\emergency_20251225_120000"

# 1. Halt pipeline
touch project_root/PIPELINE_HALTED

# 2. Restore indexes
cp -r "$backup_dir/indexes/"* project_root/indexes\

# 3. Restore briefs
cp -r "$backup_dir/briefs/"* project_root/briefs\

# 4. Restore website data
cp -r "$backup_dir/data/"* project_root/website\data\

# 5. Restore pending work
cp -r "$backup_dir/pending_approval/"* project_root/pending_approval\
cp -r "$backup_dir/approved/"* project_root/approved\

# 6. Validate restoration
python project_root/scripts\validate_indexes.py

# 7. Resume pipeline
rm project_root/PIPELINE_HALTED

echo "System restored from: $backup_dir"
```

### Data Corruption Recovery

**If JSON index is corrupted:**
```bash
# 1. Identify corrupted file
python -m json.tool project_root/indexes\entity_registry.json
# (Error indicates corruption)

# 2. Try latest automatic backup
latest_backup=$(ls -td project_root/backups\auto_* | head -1)
cp "$latest_backup/entity_registry.json" project_root/indexes\

# 3. Validate restored file
python -m json.tool project_root/indexes\entity_registry.json

# 4. If no valid backup, rebuild from sources
python project_root/scripts\rebuild_entity_registry.py

# 5. Document the recovery
echo "Recovered entity_registry.json from: $latest_backup" >> \
  project_root/logs\recovery_log.txt
```

### Website Takedown

**If legal issue requires immediate removal:**
```bash
# 1. Identify brief to remove
brief_id="john_doe"

# 2. Remove from website immediately
rm project_root/website\briefs\entity\analytical_brief_${brief_id}.md

# 3. Remove from website data
python project_root/scripts\emergency_remove.py \
  --entity "$brief_id" --reason "Legal takedown request"

# 4. Clear web cache (if applicable)
curl -X PURGE http://localhost:8081/briefs/entity/analytical_brief_${brief_id}.md

# 5. Document takedown
cat > project_root/logs\TAKEDOWN_$(date +%Y%m%d_%H%M%S).txt <<EOF
EMERGENCY TAKEDOWN
Entity: $brief_id
Date: $(date)
Reason: [FILL IN LEGAL REASON]
Operator: [YOUR NAME]
Files removed:
- website/briefs/entity/analytical_brief_${brief_id}.md
- website/data/entities.json (entry removed)
EOF
```

---

## Maintenance Tasks

### Daily Maintenance
```bash
# Check pending approvals
ls project_root/pending_approval\entities\ | wc -l

# Review error logs
tail -50 project_root/logs\pipeline_errors.log

# Verify disk space
df -h project_root/
```

### Weekly Maintenance
```bash
# Archive old logs
python project_root/scripts\archive_logs.py --older-than 30

# Validate data integrity
python project_root/scripts\validate_indexes.py
python project_root/scripts\validate_website_data.py

# Check for duplicate entities
python project_root/scripts\find_duplicates.py

# Review legal compliance
grep -r "legal_review: \"ISSUES FOUND\"" project_root/pending_approval\
```

### Monthly Maintenance
```bash
# Full system backup
python project_root/scripts\full_backup.py

# Analyze pipeline performance
python project_root/scripts\generate_metrics_report.py

# Audit published content
python project_root/scripts\content_audit.py

# Clean up old archives (keep last 6 months)
find project_root/archive\published\ -mtime +180 -exec rm {} \;
```

---

## Quick Reference: File Locations

### Configuration
- SOPs: `project_root/sops\`
- Templates: `project_root/templates\`

### Data
- Indexes: `project_root/indexes\`
- Briefs: `project_root/briefs\`
- Sources: `project_root/sources\`

### Workflow
- Pending Approval: `project_root/pending_approval\`
- Approved: `project_root/approved\`
- Archive: `project_root/archive\`

### Website
- Website Root: `project_root/website\`
- Data: `project_root/website\data\`
- Briefs: `project_root/website\briefs\`
- Sources: `project_root/website\sources\`

### Logs
- All Logs: `project_root/logs\`
- Error Log: `project_root/logs\pipeline_errors.log`

### Backups
- Auto Backups: `project_root/backups\auto_*\`
- Manual Backups: `project_root/backups\manual_*\`
- Emergency: `project_root/backups\emergency_*\`

---

## Contact & Support

### Pipeline Issues
- Check SOPs: `project_root/sops\`
- Check this runbook first
- Review error logs
- Create incident report if needed

### Legal Compliance Questions
- Review SOP-003 Section 6.3 (Legal Checklist)
- Consult legal team before overriding legal review
- Document all manual legal approvals

### Technical Support
- Pipeline Administrator: [Contact Info]
- System Administrator: [Contact Info]
- Emergency Contact: [Contact Info]

---

**Document Control**
- **Version:** 1.0
- **Last Updated:** 2025-12-25
- **Next Review:** 2026-01-25
- **Owner:** Pipeline Operations Team
