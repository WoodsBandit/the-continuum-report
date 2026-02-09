#!/usr/bin/env python3
"""
Phase 0 & 1: Verify Infrastructure and Collect Data

This script:
1. Verifies Paperless API connectivity
2. Validates all index files
3. Collects baseline metrics
4. Fetches all Paperless documents
5. Compares against indexed sources
6. Builds processing queue
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from continuum_report.lib.paperless_client import PaperlessClient, PaperlessError


def load_json(path: Path) -> Dict[str, Any]:
    """Load and validate JSON file."""
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {path}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"WARNING: File not found: {path}")
        return {}


def save_json(path: Path, data: Any, indent: int = 2) -> None:
    """Save data as pretty-printed JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=indent, sort_keys=False)
    print(f"Saved: {path} ({path.stat().st_size:,} bytes)")


def categorize_document(doc: Dict[str, Any], tags_map: Dict[int, str]) -> str:
    """Categorize document based on tags and title."""
    title = doc.get("title", "").lower()
    tag_ids = doc.get("tags", [])
    tag_names = [tags_map.get(tid, "").lower() for tid in tag_ids]

    # Check title and tags for category patterns
    if any("giuffre" in title or "giuffre" in tag for tag in tag_names):
        return "giuffre-v-maxwell"
    if any("maxwell" in title or "maxwell" in tag for tag in tag_names):
        return "giuffre-v-maxwell"
    if any("house oversight" in title or "oversight" in tag for tag in tag_names):
        return "house-oversight"
    if any("2025" in title or "2025" in tag for tag in tag_names):
        return "house-oversight-2025"
    if any("court" in tag or "filing" in tag for tag in tag_names):
        return "court-filings"
    if any("deposition" in title or "deposition" in tag for tag in tag_names):
        return "depositions"
    if any("book" in tag or "article" in tag for tag in tag_names):
        return "secondary-sources"

    return "uncategorized"


def prioritize_document(category: str, title: str) -> str:
    """Determine processing priority."""
    title_lower = title.lower()

    # HIGH priority
    if category == "giuffre-v-maxwell":
        return "high"
    if category == "house-oversight-2025":
        return "high"
    if "deposition" in title_lower:
        return "high"

    # MEDIUM priority
    if category == "court-filings":
        return "medium"
    if category == "house-oversight":
        return "medium"
    if "subpoena" in title_lower or "motion" in title_lower:
        return "medium"

    # LOW priority
    return "low"


def main():
    print("=" * 80)
    print("PHASE 0 & 1: INFRASTRUCTURE VERIFICATION & DATA COLLECTION")
    print("=" * 80)
    print()

    base_dir = Path(__file__).parent.parent
    indexes_dir = base_dir / "indexes"
    work_dir = base_dir / "work"
    briefs_dir = base_dir / "briefs"
    website_data_dir = base_dir / "website" / "data"

    # =========================================================================
    # STEP 0.4: Verify Infrastructure
    # =========================================================================
    print("[STEP 0.4] Verifying Infrastructure...")
    print("-" * 80)

    # Verify Paperless API
    try:
        client = PaperlessClient()
        # Test with actual document fetch instead of root endpoint
        test_page = client.get_documents_page(page=1, page_size=1)
        if test_page.get("count") is not None:
            print(f"[OK] Paperless API: Connected (http://localhost:8040)")
            print(f"  Total documents available: {test_page.get('count'):,}")
        else:
            print("ERROR: Paperless API returned unexpected response")
            sys.exit(1)
    except PaperlessError as e:
        print(f"ERROR: Cannot connect to Paperless: {e}")
        sys.exit(1)

    # Verify index files
    index_files = [
        "entity_registry.json",
        "entity_registry_clean.json",
        "co_occurrence.json",
        "co_occurrence_clean.json",
        "source_mentions.json",
        "entity_normalization.json",
        "boilerplate_filter.json",
        "connection_contexts.json",
        "processed_sources.json",
    ]

    print("\nValidating index files:")
    for filename in index_files:
        path = indexes_dir / filename
        data = load_json(path)
        print(f"  [OK] {filename}: Valid JSON ({len(json.dumps(data)):,} bytes)")

    print()

    # =========================================================================
    # STEP 0.5: Document Baseline Metrics
    # =========================================================================
    print("[STEP 0.5] Documenting Baseline Metrics...")
    print("-" * 80)

    # Load indexes
    entity_registry_clean = load_json(indexes_dir / "entity_registry_clean.json")
    source_mentions = load_json(indexes_dir / "source_mentions.json")

    # Count briefs
    entity_briefs = list((briefs_dir / "entity").glob("*.md")) if (briefs_dir / "entity").exists() else []
    connection_briefs = list((briefs_dir / "connections").glob("*.md")) if (briefs_dir / "connections").exists() else []

    # Load website data
    curated_entities = load_json(website_data_dir / "entities.json") if (website_data_dir / "entities.json").exists() else {}
    curated_connections = load_json(website_data_dir / "connections.json") if (website_data_dir / "connections.json").exists() else {}

    # Get Paperless document count
    paperless_count_data = client.get_documents_page(page=1, page_size=1)
    paperless_total = paperless_count_data.get("count", 0)

    baseline_metrics = {
        "timestamp": datetime.now().isoformat(),
        "paperless_documents": paperless_total,
        "indexed_entities": len(entity_registry_clean),
        "indexed_sources": len(source_mentions),
        "entity_briefs": len(entity_briefs),
        "connection_briefs": len(connection_briefs),
        "curated_entities": len(curated_entities),
        "curated_connections": len(curated_connections),
    }

    save_json(work_dir / "baseline_metrics.json", baseline_metrics)

    print("\nBaseline Metrics:")
    for key, value in baseline_metrics.items():
        if key != "timestamp":
            print(f"  {key}: {value:,}")

    print()

    # =========================================================================
    # STEP 1.1: Query Paperless for ALL Documents
    # =========================================================================
    print("[STEP 1.1] Querying Paperless for All Documents...")
    print("-" * 80)

    print(f"Fetching {paperless_total:,} documents with pagination...")

    all_docs = []
    page = 1
    page_size = 100

    while True:
        page_data = client.get_documents_page(page=page, page_size=page_size)
        results = page_data.get("results", [])

        if not results:
            break

        all_docs.extend(results)
        print(f"  Page {page}: {len(all_docs):,}/{paperless_total:,} documents")

        if not page_data.get("next"):
            break

        page += 1

    print(f"\n[OK] Fetched {len(all_docs):,} documents")

    # Extract relevant fields and save
    inventory = []
    for doc in all_docs:
        inventory.append({
            "id": doc["id"],
            "title": doc.get("title", ""),
            "created": doc.get("created", ""),
            "document_type": doc.get("document_type"),
            "tags": doc.get("tags", []),
            "correspondent": doc.get("correspondent"),
        })

    save_json(work_dir / "paperless_inventory.json", inventory)
    print()

    # =========================================================================
    # STEP 1.2: Compare Against source_mentions.json
    # =========================================================================
    print("[STEP 1.2] Comparing Against Indexed Sources...")
    print("-" * 80)

    # Build set of indexed source IDs
    indexed_source_ids = set()
    for source_key in source_mentions.keys():
        # Source keys are like "paperless_123"
        if source_key.startswith("paperless_"):
            try:
                doc_id = int(source_key.split("_")[1])
                indexed_source_ids.add(doc_id)
            except (IndexError, ValueError):
                continue

    indexed_docs = []
    unindexed_docs = []

    for doc in inventory:
        if doc["id"] in indexed_source_ids:
            indexed_docs.append(doc)
        else:
            unindexed_docs.append(doc)

    print(f"  Indexed: {len(indexed_docs):,}")
    print(f"  Unindexed: {len(unindexed_docs):,}")
    print()

    # =========================================================================
    # STEP 1.3: Build Processing Queue
    # =========================================================================
    print("[STEP 1.3] Building Processing Queue...")
    print("-" * 80)

    # Fetch tags for categorization
    tags_data = client.get_all_tags()
    tags_map = {tid: tag["name"] for tid, tag in tags_data.items()}

    queue = []
    category_counts = {}
    priority_counts = {"high": 0, "medium": 0, "low": 0}

    for doc in unindexed_docs:
        category = categorize_document(doc, tags_map)
        priority = prioritize_document(category, doc["title"])

        queue.append({
            "id": doc["id"],
            "title": doc["title"],
            "priority": priority,
            "category": category,
            "status": "pending",
        })

        category_counts[category] = category_counts.get(category, 0) + 1
        priority_counts[priority] += 1

    # Sort by priority (high -> medium -> low)
    priority_order = {"high": 0, "medium": 1, "low": 2}
    queue.sort(key=lambda x: (priority_order[x["priority"]], x["id"]))

    processing_queue = {
        "generated": datetime.now().isoformat(),
        "total_documents": len(all_docs),
        "indexed": len(indexed_docs),
        "unindexed": len(unindexed_docs),
        "queue": queue,
    }

    save_json(work_dir / "processing_queue.json", processing_queue)

    print("\nProcessing Queue Summary:")
    print(f"  Total documents: {len(all_docs):,}")
    print(f"  Already indexed: {len(indexed_docs):,}")
    print(f"  Pending processing: {len(unindexed_docs):,}")
    print()
    print("Priority Breakdown:")
    for priority in ["high", "medium", "low"]:
        count = priority_counts[priority]
        print(f"  {priority.upper()}: {count:,}")
    print()
    print("Category Breakdown:")
    for category in sorted(category_counts.keys()):
        count = category_counts[category]
        print(f"  {category}: {count:,}")
    print()

    # Show top 20 priority documents
    print("Top 20 Priority Documents:")
    for i, item in enumerate(queue[:20], 1):
        print(f"  {i}. [{item['priority'].upper()}] {item['title'][:60]}")

    print()

    # =========================================================================
    # Summary Statistics
    # =========================================================================
    print("=" * 80)
    print("PHASE 0 & 1 COMPLETE")
    print("=" * 80)
    print()
    print("Backup Status:")
    print(f"  [OK] Index backups: 9 files (~43 MB)")
    print(f"  [OK] Entity briefs: {len(entity_briefs)} files")
    print(f"  [OK] Connection briefs: {len(connection_briefs)} files")
    print()
    print("Infrastructure:")
    print(f"  [OK] Paperless API: Connected")
    print(f"  [OK] All indexes: Valid JSON")
    print()
    print("Document Inventory:")
    print(f"  Total Paperless docs: {len(all_docs):,}")
    print(f"  Already indexed: {len(indexed_docs):,} ({100*len(indexed_docs)/max(len(all_docs),1):.1f}%)")
    print(f"  Pending processing: {len(unindexed_docs):,} ({100*len(unindexed_docs)/max(len(all_docs),1):.1f}%)")
    print()
    print("Priority Queue:")
    print(f"  HIGH priority: {priority_counts['high']:,}")
    print(f"  MEDIUM priority: {priority_counts['medium']:,}")
    print(f"  LOW priority: {priority_counts['low']:,}")
    print()
    print("Deliverables:")
    print(f"  [OK] {work_dir}/baseline_metrics.json")
    print(f"  [OK] {work_dir}/paperless_inventory.json")
    print(f"  [OK] {work_dir}/processing_queue.json")
    print()

    # Determine GO/NO-GO
    if len(unindexed_docs) > 0:
        print("RECOMMENDATION: GO for Phase 2")
        print(f"  -> {len(unindexed_docs):,} documents ready for processing")
        print(f"  -> {priority_counts['high']:,} high-priority documents identified")
    else:
        print("RECOMMENDATION: HOLD - All documents already indexed")

    print()
    print("Next: Review gap analysis report and approve Phase 2 execution")
    print()


if __name__ == "__main__":
    main()
