# The Continuum Report - Pipeline Execution Plan
**Date:** 2025-12-25
**Version:** 1.0
**Status:** READY FOR EXECUTION
**Based On:** `/reports/pipeline_brainstorm.md`

---

## EXECUTION OVERVIEW

**Objective:** Execute The Continuum Report's autonomous pipeline (SOP-001 through SOP-003) on all 273 documents in Paperless-ngx.

**Approach:** Phased, conservative, with checkpoints and validation between stages.

**Total Estimated Time:** 42 hours across multiple sessions

**Current Session Scope:** Phase 0 (Preparation) and Phase 1 (Inventory)

---

## PHASE 0: PREPARATION & BACKUP

**Duration:** 30 minutes
**Risk Level:** LOW
**Dependencies:** None
**Success Criteria:** All backups verified, infrastructure tested, baseline documented

### Step 0.1: Create Backup Structure

```bash
# Create backup directory with timestamp
BACKUP_DIR="\\192.168.1.139\continuum\backups\2025-12-25_pre_pipeline"

mkdir "${BACKUP_DIR}"
mkdir "${BACKUP_DIR}\indexes"
mkdir "${BACKUP_DIR}\briefs"
mkdir "${BACKUP_DIR}\website_data"
```

**Verification:**
- [ ] Backup directories created
- [ ] Write access confirmed

### Step 0.2: Backup Indexes

**Files to Backup:**
- `indexes/entity_registry.json`
- `indexes/entity_registry_clean.json`
- `indexes/co_occurrence.json`
- `indexes/co_occurrence_clean.json`
- `indexes/source_mentions.json`
- `indexes/connection_contexts.json`
- `indexes/processed_sources.json`

**Command:**
```bash
cp indexes/*.json "${BACKUP_DIR}/indexes/"
```

**Verification:**
- [ ] 7 files copied
- [ ] File sizes match originals
- [ ] JSON validity confirmed (spot check)

### Step 0.3: Backup Briefs

**Directories to Backup:**
- `briefs/entity/` (38 files)
- `briefs/connections/` (90 files)

**Command:**
```bash
cp -r briefs/entity "${BACKUP_DIR}/briefs/"
cp -r briefs/connections "${BACKUP_DIR}/briefs/"
```

**Verification:**
- [ ] 38 entity briefs backed up
- [ ] 90 connection briefs backed up
- [ ] File sizes match originals

### Step 0.4: Backup Website Data

**Files to Backup:**
- `website/data/entities.json`
- `website/data/connections.json`

**Command:**
```bash
cp website/data/*.json "${BACKUP_DIR}/website_data/"
```

**Verification:**
- [ ] 2 files copied
- [ ] JSON validity confirmed

### Step 0.5: Verify Infrastructure

**Paperless API Check:**
```python
from src.continuum_report.lib.paperless_client import PaperlessClient

client = PaperlessClient()
assert client.health_check(), "Paperless API not accessible"
docs = client.get_documents_page(page_size=1)
total_docs = docs["count"]
print(f"✓ Paperless API accessible: {total_docs} documents")
```

**Network Share Check:**
```bash
# Test write access
echo "test" > "\\192.168.1.139\continuum\test_write.txt"
cat "\\192.168.1.139\continuum\test_write.txt"
rm "\\192.168.1.139\continuum\test_write.txt"
```

**Disk Space Check:**
```bash
# Check available space on continuum share
df -h "\\192.168.1.139\continuum"
# Require: >10GB free
```

**Verification:**
- [ ] Paperless API responds
- [ ] Document count retrieved
- [ ] Network share writable
- [ ] Disk space sufficient (>10GB)

### Step 0.6: Document Baseline Metrics

**Create baseline metrics file:**
```json
{
  "_baseline_date": "2025-12-25T[TIMESTAMP]Z",
  "_phase": "Phase 0 - Pre-Execution",
  "paperless": {
    "total_documents": 273,
    "api_status": "accessible",
    "api_url": "http://192.168.1.139:8040"
  },
  "indexes": {
    "entity_registry_entities": 1861,
    "entity_registry_clean_entities": 1861,
    "co_occurrence_pairs": 117954,
    "co_occurrence_clean_pairs": 95500,
    "source_mentions_sources": 83,
    "connection_contexts_connections": 0,
    "processed_sources_count": 0
  },
  "briefs": {
    "entity_briefs": 38,
    "connection_briefs": 90
  },
  "website": {
    "curated_entities": 5,
    "curated_connections": 131
  },
  "storage": {
    "disk_space_available_gb": "[TO BE MEASURED]"
  }
}
```

**Save to:** `\\192.168.1.139\continuum\work\baseline_metrics.json`

**Verification:**
- [ ] Baseline file created
- [ ] All metrics captured
- [ ] File is valid JSON

### Step 0.7: Initialize Execution Log

**Create execution log:**
```markdown
# Pipeline Execution Log
**Started:** 2025-12-25 [TIMESTAMP]
**Mode:** Autonomous Pipeline Execution
**Scope:** All 273 documents in Paperless

## Phase 0: Preparation & Backup
- [TIMESTAMP] Backup directories created
- [TIMESTAMP] Indexes backed up (7 files)
- [TIMESTAMP] Briefs backed up (128 files)
- [TIMESTAMP] Website data backed up (2 files)
- [TIMESTAMP] Infrastructure verified (Paperless API: OK)
- [TIMESTAMP] Baseline metrics documented
- [TIMESTAMP] Phase 0 COMPLETE

## Phase 1: Inventory & Gap Analysis
[TO BE POPULATED]
```

**Save to:** `\\192.168.1.139\continuum\work\pipeline_execution_log.md`

**Verification:**
- [ ] Log file created
- [ ] Phase 0 entries populated
- [ ] Ready for Phase 1 logging

### PHASE 0 COMPLETION CHECKLIST

**Before proceeding to Phase 1, verify:**
- [ ] All backups complete and verified
- [ ] Infrastructure tests passed
- [ ] Baseline metrics documented
- [ ] Execution log initialized
- [ ] NO errors encountered
- [ ] Disk space >10GB available

**If all checks pass:** ✅ PROCEED TO PHASE 1

**If any checks fail:** ❌ HALT and resolve issues first

---

## PHASE 1: INVENTORY & GAP ANALYSIS

**Duration:** 1 hour
**Risk Level:** LOW (read-only operations)
**Dependencies:** Phase 0 complete
**Success Criteria:** Complete document inventory, gap analysis, priority classification

### Step 1.1: Query Paperless for All Documents

**Objective:** Get complete list of all documents with metadata

**Script:**
```python
from src.continuum_report.lib.paperless_client import PaperlessClient
import json

client = PaperlessClient()

# Fetch ALL documents (excluding generated dossiers)
all_docs = client.get_all_documents(
    page_size=100,
    exclude_dossiers=True
)

# Save to inventory file
inventory = {
    "_created": datetime.now().isoformat(),
    "_total_count": len(all_docs),
    "documents": []
}

for doc in all_docs:
    inventory["documents"].append({
        "id": doc["id"],
        "title": doc["title"],
        "created": doc["created"],
        "document_type": doc.get("document_type"),
        "tags": doc.get("tags", []),
        "content_length": len(doc.get("content", "")),
        "has_content": len(doc.get("content", "")) > 100
    })

# Save inventory
with open("\\\\192.168.1.139\\continuum\\work\\document_inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

print(f"Inventory complete: {len(all_docs)} documents")
```

**Output:** `\\192.168.1.139\continuum\work\document_inventory.json`

**Verification:**
- [ ] Inventory file created
- [ ] Document count matches Paperless (273)
- [ ] All documents have metadata
- [ ] Content length calculated for each

### Step 1.2: Analyze Document Types

**Objective:** Categorize documents by type, OCR status, priority

**Script:**
```python
import json

# Load inventory
with open("\\\\192.168.1.139\\continuum\\work\\document_inventory.json") as f:
    inventory = json.load(f)

# Analyze
analysis = {
    "total_documents": len(inventory["documents"]),
    "with_content": 0,
    "without_content": 0,
    "likely_ocr_needed": 0,
    "by_document_type": {},
    "priority_classification": {
        "high": [],
        "medium": [],
        "low": []
    }
}

for doc in inventory["documents"]:
    # Count content status
    if doc["has_content"]:
        analysis["with_content"] += 1
    else:
        analysis["without_content"] += 1
        analysis["likely_ocr_needed"] += 1

    # Count by type
    doc_type = doc.get("document_type", "Unknown")
    if doc_type not in analysis["by_document_type"]:
        analysis["by_document_type"][doc_type] = 0
    analysis["by_document_type"][doc_type] += 1

    # Priority classification (based on title keywords)
    title_lower = doc["title"].lower()
    if any(kw in title_lower for kw in ["epstein", "maxwell", "giuffre", "prince andrew"]):
        analysis["priority_classification"]["high"].append(doc["id"])
    elif any(kw in title_lower for kw in ["deposition", "testimony", "lawsuit", "court"]):
        analysis["priority_classification"]["medium"].append(doc["id"])
    else:
        analysis["priority_classification"]["low"].append(doc["id"])

# Save analysis
with open("\\\\192.168.1.139\\continuum\\work\\document_analysis.json", "w") as f:
    json.dump(analysis, f, indent=2)

print("Analysis complete:")
print(f"  With content: {analysis['with_content']}")
print(f"  Without content (OCR needed): {analysis['without_content']}")
print(f"  High priority: {len(analysis['priority_classification']['high'])}")
print(f"  Medium priority: {len(analysis['priority_classification']['medium'])}")
print(f"  Low priority: {len(analysis['priority_classification']['low'])}")
```

**Output:** `\\192.168.1.139\continuum\work\document_analysis.json`

**Verification:**
- [ ] Analysis file created
- [ ] Document counts add up correctly
- [ ] Priority tiers identified
- [ ] OCR-needed documents flagged

### Step 1.3: Compare Against Processed Sources

**Objective:** Identify which documents have NOT been processed

**Script:**
```python
import json

# Load processed sources
with open("\\\\192.168.1.139\\continuum\\indexes\\processed_sources.json") as f:
    processed = json.load(f)

# Load inventory
with open("\\\\192.168.1.139\\continuum\\work\\document_inventory.json") as f:
    inventory = json.load(f)

# Get list of processed paperless IDs
processed_ids = set([src["paperless_id"] for src in processed["sources"]])

# Identify unprocessed
all_ids = set([doc["id"] for doc in inventory["documents"]])
unprocessed_ids = all_ids - processed_ids

gap_analysis = {
    "total_documents": len(all_ids),
    "processed_count": len(processed_ids),
    "unprocessed_count": len(unprocessed_ids),
    "unprocessed_document_ids": list(unprocessed_ids),
    "coverage_percentage": (len(processed_ids) / len(all_ids)) * 100 if all_ids else 0
}

# Save gap analysis
with open("\\\\192.168.1.139\\continuum\\work\\gap_analysis.json", "w") as f:
    json.dump(gap_analysis, f, indent=2)

print("Gap Analysis:")
print(f"  Total documents: {gap_analysis['total_documents']}")
print(f"  Processed: {gap_analysis['processed_count']}")
print(f"  Unprocessed: {gap_analysis['unprocessed_count']}")
print(f"  Coverage: {gap_analysis['coverage_percentage']:.1f}%")
```

**Output:** `\\192.168.1.139\continuum\work\gap_analysis.json`

**Expected Result:** 273 unprocessed (since processed_sources.json is empty)

**Verification:**
- [ ] Gap analysis file created
- [ ] Unprocessed list complete
- [ ] Coverage percentage calculated

### Step 1.4: Generate Priority Processing List

**Objective:** Create ordered list of documents to process

**Script:**
```python
import json

# Load all analysis files
with open("\\\\192.168.1.139\\continuum\\work\\document_inventory.json") as f:
    inventory = json.load(f)
with open("\\\\192.168.1.139\\continuum\\work\\document_analysis.json") as f:
    analysis = json.load(f)
with open("\\\\192.168.1.139\\continuum\\work\\gap_analysis.json") as f:
    gap = json.load(f)

# Create processing queue
processing_queue = {
    "_created": datetime.now().isoformat(),
    "_note": "Documents ordered by priority for pipeline processing",
    "batch_1_high_priority": [],
    "batch_2_medium_priority": [],
    "batch_3_low_priority": [],
    "batch_4_ocr_needed": []
}

# Get document lookup
doc_lookup = {doc["id"]: doc for doc in inventory["documents"]}

# Assign to batches
for doc_id in gap["unprocessed_document_ids"]:
    doc = doc_lookup[doc_id]

    # Skip if no content (needs OCR)
    if not doc["has_content"]:
        processing_queue["batch_4_ocr_needed"].append(doc_id)
        continue

    # Assign based on priority
    if doc_id in analysis["priority_classification"]["high"]:
        processing_queue["batch_1_high_priority"].append(doc_id)
    elif doc_id in analysis["priority_classification"]["medium"]:
        processing_queue["batch_2_medium_priority"].append(doc_id)
    else:
        processing_queue["batch_3_low_priority"].append(doc_id)

# Add batch summaries
processing_queue["_summary"] = {
    "batch_1_count": len(processing_queue["batch_1_high_priority"]),
    "batch_2_count": len(processing_queue["batch_2_medium_priority"]),
    "batch_3_count": len(processing_queue["batch_3_low_priority"]),
    "batch_4_ocr_count": len(processing_queue["batch_4_ocr_needed"]),
    "total_processable": (
        len(processing_queue["batch_1_high_priority"]) +
        len(processing_queue["batch_2_medium_priority"]) +
        len(processing_queue["batch_3_low_priority"])
    )
}

# Save processing queue
with open("\\\\192.168.1.139\\continuum\\work\\processing_queue.json", "w") as f:
    json.dump(processing_queue, f, indent=2)

print("Processing Queue Created:")
print(f"  Batch 1 (High): {processing_queue['_summary']['batch_1_count']}")
print(f"  Batch 2 (Medium): {processing_queue['_summary']['batch_2_count']}")
print(f"  Batch 3 (Low): {processing_queue['_summary']['batch_3_count']}")
print(f"  Batch 4 (OCR Needed): {processing_queue['_summary']['batch_4_ocr_count']}")
print(f"  Total Processable: {processing_queue['_summary']['total_processable']}")
```

**Output:** `\\192.168.1.139\continuum\work\processing_queue.json`

**Verification:**
- [ ] Queue file created
- [ ] All unprocessed documents assigned to batches
- [ ] Batch counts summarized
- [ ] OCR-needed documents separated

### Step 1.5: Entity Coverage Analysis

**Objective:** Determine which entities need brief updates

**Script:**
```python
import json
from glob import glob

# Load entity registry
with open("\\\\192.168.1.139\\continuum\\indexes\\entity_registry_clean.json") as f:
    registry = json.load(f)

# Get list of existing brief entities
brief_files = glob("\\\\192.168.1.139\\continuum\\briefs\\entity\\*.md")
brief_entities = set()
for bf in brief_files:
    # Extract entity name from filename
    filename = bf.split("\\")[-1]
    entity_name = filename.replace("analytical_brief_", "").replace(".md", "").replace("_", " ").title()
    brief_entities.add(entity_name)

# Analyze entity coverage
entity_coverage = {
    "total_entities": len(registry["entities"]),
    "entities_with_briefs": len(brief_entities),
    "entities_without_briefs": len(registry["entities"]) - len(brief_entities),
    "coverage_percentage": (len(brief_entities) / len(registry["entities"])) * 100,
    "entities_needing_briefs": [],
    "top_20_by_mentions": []
}

# Get top entities by mention count
entities_sorted = sorted(
    registry["entities"].items(),
    key=lambda x: x[1].get("mention_count", 0),
    reverse=True
)

# Top 20
for entity_name, data in entities_sorted[:20]:
    entity_coverage["top_20_by_mentions"].append({
        "name": entity_name,
        "mention_count": data.get("mention_count", 0),
        "has_brief": entity_name in brief_entities
    })

# Entities needing briefs (top 100 without briefs)
count = 0
for entity_name, data in entities_sorted:
    if entity_name not in brief_entities and count < 100:
        entity_coverage["entities_needing_briefs"].append({
            "name": entity_name,
            "mention_count": data.get("mention_count", 0),
            "sources_count": len(data.get("sources", []))
        })
        count += 1

# Save coverage analysis
with open("\\\\192.168.1.139\\continuum\\work\\entity_coverage_analysis.json", "w") as f:
    json.dump(entity_coverage, f, indent=2)

print("Entity Coverage Analysis:")
print(f"  Total entities: {entity_coverage['total_entities']}")
print(f"  With briefs: {entity_coverage['entities_with_briefs']}")
print(f"  Without briefs: {entity_coverage['entities_without_briefs']}")
print(f"  Coverage: {entity_coverage['coverage_percentage']:.1f}%")
```

**Output:** `\\192.168.1.139\continuum\work\entity_coverage_analysis.json`

**Verification:**
- [ ] Coverage file created
- [ ] Top 20 entities identified
- [ ] Brief gaps identified
- [ ] Priority brief targets listed

### Step 1.6: Generate Phase 1 Summary Report

**Objective:** Compile all Phase 1 findings into human-readable report

**Output:** `\\192.168.1.139\continuum\work\phase1_summary_report.md`

**Contents:**
```markdown
# Phase 1 Summary Report: Inventory & Gap Analysis
**Date:** 2025-12-25
**Status:** COMPLETE

## Document Inventory

- **Total Documents:** [COUNT]
- **With Text Content:** [COUNT]
- **Without Content (OCR Needed):** [COUNT]

## Processing Status

- **Previously Processed:** [COUNT] (from processed_sources.json)
- **Unprocessed:** [COUNT]
- **Coverage:** [PERCENTAGE]%

## Priority Batches

- **Batch 1 (High Priority):** [COUNT] documents
- **Batch 2 (Medium Priority):** [COUNT] documents
- **Batch 3 (Low Priority):** [COUNT] documents
- **Batch 4 (OCR Needed - Skipped):** [COUNT] documents

## Entity Analysis

- **Total Entities Indexed:** [COUNT]
- **Entities with Briefs:** [COUNT]
- **Entities Needing Briefs:** [COUNT]
- **Coverage:** [PERCENTAGE]%

## Top 10 Entities by Mention Count

1. [Entity Name] - [COUNT] mentions - [HAS BRIEF? Y/N]
2. ...

## Recommendations

### Immediate Processing Priority
[List of high-priority documents to process first]

### Brief Generation Priority
[List of top entities needing briefs]

### OCR Queue
[Count of documents needing OCR before processing]

## Next Steps

Based on this analysis, recommend:
- [ ] Proceed with Phase 2: Entity Extraction on Batch 1
- [ ] Estimated time for Batch 1: [X] hours
- [ ] Expected new entities from Batch 1: [X]
- [ ] Checkpoint after Batch 1 before continuing

---
**Report Generated:** [TIMESTAMP]
**Phase 1 Status:** COMPLETE ✓
```

**Verification:**
- [ ] Report generated
- [ ] All sections populated with data
- [ ] Recommendations clear
- [ ] Next steps defined

### PHASE 1 COMPLETION CHECKLIST

**Before proceeding to Phase 2, verify:**
- [ ] Document inventory complete (273 documents cataloged)
- [ ] Gap analysis complete (unprocessed identified)
- [ ] Priority batches defined
- [ ] Entity coverage analyzed
- [ ] Summary report generated
- [ ] Execution log updated
- [ ] NO errors encountered

**If all checks pass:** ✅ READY FOR PHASE 2 (but CHECKPOINT first)

**Phase 1 Deliverables:**
- `document_inventory.json`
- `document_analysis.json`
- `gap_analysis.json`
- `processing_queue.json`
- `entity_coverage_analysis.json`
- `phase1_summary_report.md`
- Updated `pipeline_execution_log.md`

---

## PHASE 2: ENTITY EXTRACTION (SOP-001)

**Duration:** 2-30 hours (depending on batch size)
**Risk Level:** MEDIUM (writes to indexes)
**Dependencies:** Phase 0 and Phase 1 complete
**Success Criteria:** Entities extracted, indexes updated, no corruption

### NOTE: PHASE 2 WILL BE DETAILED IN NEXT SESSION

**Before starting Phase 2:**
1. Review Phase 1 summary report
2. Validate processing queue
3. Confirm batch size for initial test run
4. Set up checkpoint validation criteria

**Recommended:** Start with Batch 1 (High Priority) as TEST RUN before processing all documents.

---

## EMERGENCY STOP PROCEDURE

**If any of the following occur, HALT immediately:**
1. JSON corruption detected
2. Disk space < 1GB
3. Network share disconnection
4. Repeated API failures (>10 in a row)
5. Unexpected data loss detected

**Recovery Steps:**
1. STOP all processing immediately
2. DO NOT write to any index files
3. Restore from Phase 0 backups if needed
4. Generate diagnostic report
5. Investigate root cause before resuming

---

## EXECUTION STATUS

**Phase 0:** NOT STARTED
**Phase 1:** NOT STARTED
**Phase 2:** NOT STARTED
**Phase 3:** NOT STARTED
**Phase 4:** NOT STARTED

**Current Step:** Ready to begin Phase 0

**Last Updated:** 2025-12-25 (plan created)

---

**END OF EXECUTION PLAN (Phase 0-1)**

**Next Document:** Update this plan with Phase 2-4 details after Phase 1 checkpoint
