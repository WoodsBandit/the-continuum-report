"""
The Continuum Report - Stage 1: Source Ingestion

Processes documents from Paperless-ngx, extracts entities, and updates:
- entity_registry.json
- source_mentions.json
- processed_sources.json

Trigger: Paperless webhook (via webhook_listener.py)
Output: Updated entity indexes

Usage:
    # Process ingestion queue
    python run_stage1.py

    # Process specific document
    python run_stage1.py --document-id 12345

    # Dry run (no index updates)
    python run_stage1.py --dry-run
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from logging_config import get_logger
from config import settings
from paperless_client import PaperlessClient

logger = get_logger("stage1_ingestion")


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(os.environ.get("CONTINUUM_BASE_DIR", "/mnt/user/continuum"))
INDEXES_DIR = BASE_DIR / "indexes"
LOGS_DIR = BASE_DIR / "logs"

# Index files
ENTITY_REGISTRY = INDEXES_DIR / "entity_registry.json"
SOURCE_MENTIONS = INDEXES_DIR / "source_mentions.json"
PROCESSED_SOURCES = INDEXES_DIR / "processed_sources.json"
INGESTION_QUEUE = INDEXES_DIR / "ingestion_queue.json"


# =============================================================================
# INDEX MANAGEMENT
# =============================================================================

def load_json_file(path: Path, default=None):
    """Load JSON file safely."""
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error(f"Error loading {path}: {e}")
    return default if default is not None else {}


def save_json_file(path: Path, data) -> bool:
    """Save JSON file safely with backup."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        # Create backup if file exists
        if path.exists():
            backup_path = path.with_suffix(".json.bak")
            path.rename(backup_path)

        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    except Exception as e:
        logger.error(f"Error saving {path}: {e}")
        return False


def load_entity_registry() -> dict:
    """Load entity registry."""
    return load_json_file(ENTITY_REGISTRY, {})


def save_entity_registry(registry: dict) -> bool:
    """Save entity registry."""
    return save_json_file(ENTITY_REGISTRY, registry)


def load_source_mentions() -> dict:
    """Load source mentions index."""
    return load_json_file(SOURCE_MENTIONS, {})


def save_source_mentions(mentions: dict) -> bool:
    """Save source mentions index."""
    return save_json_file(SOURCE_MENTIONS, mentions)


def load_processed_sources() -> dict:
    """Load processed sources index."""
    return load_json_file(PROCESSED_SOURCES, {})


def save_processed_sources(sources: dict) -> bool:
    """Save processed sources index."""
    return save_json_file(PROCESSED_SOURCES, sources)


def load_ingestion_queue() -> list:
    """Load ingestion queue."""
    return load_json_file(INGESTION_QUEUE, [])


def save_ingestion_queue(queue: list) -> bool:
    """Save ingestion queue."""
    return save_json_file(INGESTION_QUEUE, queue)


# =============================================================================
# DOCUMENT PROCESSING
# =============================================================================

def get_document_content(client: PaperlessClient, document_id: int) -> Optional[str]:
    """Fetch document content from Paperless."""
    try:
        # Get document metadata
        doc = client.get_document(document_id)
        if not doc:
            logger.error(f"Document {document_id} not found")
            return None

        # Get document content/text
        content = client.get_document_content(document_id)
        return content

    except Exception as e:
        logger.error(f"Error fetching document {document_id}: {e}")
        return None


def process_document_with_claude(
    document_id: int,
    document_title: str,
    document_content: str,
    dry_run: bool = False,
) -> dict:
    """
    Process document through Claude for entity extraction.

    Returns dict with extracted entities and metadata.
    """
    from invoke_claude import invoke_claude_with_sop

    task_description = f"""
Process source document for entity extraction.

DOCUMENT METADATA:
- ID: {document_id}
- Title: {document_title}

DOCUMENT CONTENT:
{document_content[:50000]}  # Truncate to avoid token limits

YOUR TASK:
1. Extract ALL entities mentioned in this document:
   - People (full names, aliases, titles)
   - Organizations (companies, agencies, foundations)
   - Locations (addresses, cities, countries, properties)
   - Dates and time periods
   - Financial amounts and transactions
   - Documents and case references

2. For each entity, provide:
   - canonical_name: The standard form of the name
   - entity_type: person, organization, location, date, financial, document
   - mentions: List of exact text mentions found
   - context: Brief context of how entity appears in document

3. Output ONLY valid JSON in this format:
```json
{{
    "document_id": {document_id},
    "entities_extracted": [
        {{
            "canonical_name": "Name Here",
            "entity_type": "person",
            "mentions": ["exact mention 1", "exact mention 2"],
            "context": "Brief context"
        }}
    ],
    "extraction_summary": "Brief summary of what was found"
}}
```

IMPORTANT: Extract ALL entities, not just the most prominent ones.
Include BOTH new entities and known entities from the registry.
"""

    if dry_run:
        logger.info(f"[DRY RUN] Would process document {document_id}")
        return {
            "document_id": document_id,
            "entities_extracted": [],
            "extraction_summary": "Dry run - no processing",
            "dry_run": True,
        }

    result = invoke_claude_with_sop(
        sop_number=1,
        task_description=task_description,
        additional_context={
            "document_id": document_id,
            "document_title": document_title,
            "content_length": len(document_content),
        },
        timeout=300,  # 5 minutes
    )

    if not result.success:
        logger.error(f"Claude processing failed: {result.error}")
        return {
            "document_id": document_id,
            "error": result.error,
            "entities_extracted": [],
        }

    # Parse Claude's JSON output
    try:
        # Find JSON in output
        output = result.output
        json_start = output.find("{")
        json_end = output.rfind("}") + 1

        if json_start >= 0 and json_end > json_start:
            json_str = output[json_start:json_end]
            return json.loads(json_str)
        else:
            logger.warning("No JSON found in Claude output")
            return {
                "document_id": document_id,
                "raw_output": output,
                "entities_extracted": [],
            }

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Claude JSON output: {e}")
        return {
            "document_id": document_id,
            "parse_error": str(e),
            "raw_output": result.output[:1000],
            "entities_extracted": [],
        }


def update_indexes(
    document_id: int,
    document_title: str,
    extraction_result: dict,
) -> bool:
    """Update all index files with extraction results."""
    try:
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Load current indexes
        entity_registry = load_entity_registry()
        source_mentions = load_source_mentions()
        processed_sources = load_processed_sources()

        entities = extraction_result.get("entities_extracted", [])
        logger.info(f"Updating indexes with {len(entities)} entities from document {document_id}")

        # Update entity registry
        for entity in entities:
            canonical_name = entity.get("canonical_name", "").strip()
            if not canonical_name:
                continue

            # Create or update entity entry
            entity_key = canonical_name.lower().replace(" ", "_")

            if entity_key not in entity_registry:
                entity_registry[entity_key] = {
                    "canonical_name": canonical_name,
                    "entity_type": entity.get("entity_type", "unknown"),
                    "first_seen": timestamp,
                    "source_count": 0,
                    "sources": [],
                    "aliases": [],
                }

            # Add source reference
            source_ref = f"doc_{document_id}"
            if source_ref not in entity_registry[entity_key]["sources"]:
                entity_registry[entity_key]["sources"].append(source_ref)
                entity_registry[entity_key]["source_count"] = len(entity_registry[entity_key]["sources"])

            entity_registry[entity_key]["last_updated"] = timestamp

            # Update source mentions
            if canonical_name not in source_mentions:
                source_mentions[canonical_name] = {
                    "entity": canonical_name,
                    "mentions": [],
                }

            source_mentions[canonical_name]["mentions"].append({
                "source_id": document_id,
                "source_title": document_title,
                "contexts": entity.get("mentions", []),
                "extracted_at": timestamp,
            })

        # Update processed sources
        source_key = f"doc_{document_id}"
        processed_sources[source_key] = {
            "document_id": document_id,
            "title": document_title,
            "processed_at": timestamp,
            "entities_found": len(entities),
            "extraction_summary": extraction_result.get("extraction_summary", ""),
        }

        # Save all indexes
        success = all([
            save_entity_registry(entity_registry),
            save_source_mentions(source_mentions),
            save_processed_sources(processed_sources),
        ])

        if success:
            logger.info(f"Indexes updated successfully for document {document_id}")
        else:
            logger.error("Failed to save one or more index files")

        return success

    except Exception as e:
        logger.error(f"Error updating indexes: {e}")
        return False


# =============================================================================
# QUEUE PROCESSING
# =============================================================================

def process_ingestion_queue(dry_run: bool = False) -> dict:
    """Process all pending items in the ingestion queue."""
    queue = load_ingestion_queue()
    pending = [item for item in queue if item.get("status") == "pending"]

    if not pending:
        logger.info("No pending items in ingestion queue")
        return {"processed": 0, "success": 0, "failed": 0}

    logger.info(f"Processing {len(pending)} pending items")

    # Initialize Paperless client
    client = PaperlessClient(
        base_url=settings.paperless_url,
        token=settings.paperless_token,
    )

    stats = {"processed": 0, "success": 0, "failed": 0}

    for item in pending:
        document_id = item.get("document_id")
        if not document_id:
            continue

        logger.info(f"Processing document {document_id}")
        item["status"] = "processing"
        item["started_at"] = datetime.utcnow().isoformat() + "Z"
        item["attempts"] = item.get("attempts", 0) + 1
        save_ingestion_queue(queue)

        try:
            # Fetch document content
            content = get_document_content(client, document_id)
            if not content:
                raise ValueError("Failed to fetch document content")

            # Process with Claude
            result = process_document_with_claude(
                document_id=document_id,
                document_title=item.get("title", f"Document {document_id}"),
                document_content=content,
                dry_run=dry_run,
            )

            if result.get("error"):
                raise ValueError(result["error"])

            # Update indexes
            if not dry_run:
                update_indexes(
                    document_id=document_id,
                    document_title=item.get("title", f"Document {document_id}"),
                    extraction_result=result,
                )

            item["status"] = "completed"
            item["completed_at"] = datetime.utcnow().isoformat() + "Z"
            item["entities_found"] = len(result.get("entities_extracted", []))
            stats["success"] += 1

        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}")
            item["status"] = "failed"
            item["error"] = str(e)
            item["failed_at"] = datetime.utcnow().isoformat() + "Z"
            stats["failed"] += 1

        stats["processed"] += 1
        save_ingestion_queue(queue)

        # Brief pause between documents
        time.sleep(2)

    logger.info(f"Queue processing complete: {stats}")
    return stats


def process_single_document(document_id: int, dry_run: bool = False) -> dict:
    """Process a single document by ID."""
    logger.info(f"Processing single document: {document_id}")

    # Initialize Paperless client
    client = PaperlessClient(
        base_url=settings.paperless_url,
        token=settings.paperless_token,
    )

    # Fetch document
    doc = client.get_document(document_id)
    if not doc:
        return {"error": f"Document {document_id} not found"}

    content = get_document_content(client, document_id)
    if not content:
        return {"error": "Failed to fetch document content"}

    # Process with Claude
    result = process_document_with_claude(
        document_id=document_id,
        document_title=doc.get("title", f"Document {document_id}"),
        document_content=content,
        dry_run=dry_run,
    )

    if result.get("error"):
        return result

    # Update indexes
    if not dry_run:
        update_indexes(
            document_id=document_id,
            document_title=doc.get("title", f"Document {document_id}"),
            extraction_result=result,
        )

    return result


# =============================================================================
# LOGGING
# =============================================================================

def log_stage1_event(event_type: str, data: dict) -> None:
    """Log Stage 1 events."""
    try:
        log_file = LOGS_DIR / "stage1_ingestion.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "stage": "stage1_ingestion",
            "event_type": event_type,
            **data,
        }

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    except Exception as e:
        logger.error(f"Error logging stage1 event: {e}")


# =============================================================================
# CLI
# =============================================================================

def main():
    """CLI interface for Stage 1 processing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Stage 1: Source Ingestion - Extract entities from documents"
    )
    parser.add_argument("--document-id", type=int,
                        help="Process specific document by ID")
    parser.add_argument("--dry-run", action="store_true",
                        help="Dry run without updating indexes")
    parser.add_argument("--queue-status", action="store_true",
                        help="Show ingestion queue status")

    args = parser.parse_args()

    print("=" * 60)
    print("The Continuum Report - Stage 1: Source Ingestion")
    print("=" * 60)

    if args.queue_status:
        queue = load_ingestion_queue()
        status_counts = {}
        for item in queue:
            status = item.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        print(f"Queue status: {status_counts}")
        print(f"Total items: {len(queue)}")
        return 0

    if args.document_id:
        result = process_single_document(args.document_id, dry_run=args.dry_run)
        print(json.dumps(result, indent=2))
        return 0 if not result.get("error") else 1

    # Process queue
    stats = process_ingestion_queue(dry_run=args.dry_run)
    print(f"\nProcessing complete:")
    print(f"  Processed: {stats['processed']}")
    print(f"  Success: {stats['success']}")
    print(f"  Failed: {stats['failed']}")

    return 0 if stats["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
