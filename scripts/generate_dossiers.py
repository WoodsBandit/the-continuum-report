#!/usr/bin/env python3
"""
Dossier Generation Pipeline for The Continuum Report
Version 2.0 - Refactored with Shared Library

This script prepares document content for dossier generation.
It collects all documents mentioning an entity and formats them
for AI processing.

Works with Claude Code for intelligent dossier generation.

Changes in v2.0:
- Uses centralized configuration (lib.config)
- Uses PaperlessClient with retry logic (lib.paperless_client)
- Structured logging with structlog (lib.logging_config)
- No hardcoded secrets - uses environment variables
- Path handling with pathlib
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Import shared library
from lib import settings, get_logger, PaperlessClient, PaperlessError

# Initialize logger
logger = get_logger(__name__)

# =============================================================================
# CONFIGURATION (from centralized config)
# =============================================================================

DATA_DIR = settings.data_dir
REPORTS_DIR = settings.reports_dir
ENTITY_DB_FILE = settings.entity_db_file
DOSSIER_QUEUE_FILE = settings.dossier_queue_file
DOSSIER_PROGRESS_FILE = DATA_DIR / "dossier_progress.json"

# Ensure directories exist
settings.ensure_directories()
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# API HELPERS (using PaperlessClient)
# =============================================================================

def get_paperless_client() -> PaperlessClient:
    """Get a configured Paperless client."""
    return PaperlessClient()


def get_document_content(doc_id: int) -> Optional[Dict]:
    """Get full document details."""
    try:
        with get_paperless_client() as client:
            return client.get_document(doc_id)
    except PaperlessError as e:
        logger.error("Failed to get document", doc_id=doc_id, error=str(e))
        return None


# =============================================================================
# DATA LOADERS
# =============================================================================

def load_entity_db() -> Dict:
    """Load entity database."""
    if ENTITY_DB_FILE.exists():
        try:
            with open(ENTITY_DB_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.warning("Failed to load entity database", error=str(e))
    return {}


def load_dossier_queue() -> List[Dict]:
    """Load dossier queue."""
    if DOSSIER_QUEUE_FILE.exists():
        try:
            with open(DOSSIER_QUEUE_FILE, 'r') as f:
                return json.load(f).get("queue", [])
        except json.JSONDecodeError as e:
            logger.warning("Failed to load dossier queue", error=str(e))
    return []


def load_progress() -> Dict:
    """Load dossier generation progress."""
    if DOSSIER_PROGRESS_FILE.exists():
        try:
            with open(DOSSIER_PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.warning("Failed to load progress", error=str(e))
    return {"completed": [], "in_progress": None}


def save_progress(progress: Dict):
    """Save progress."""
    with open(DOSSIER_PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)
    logger.debug("Progress saved", path=str(DOSSIER_PROGRESS_FILE))


def mark_dossier_complete(entity_name: str, entity_type: str, output_path: str):
    """Mark a dossier as completed."""
    progress = load_progress()
    progress["completed"].append({
        "name": entity_name,
        "type": entity_type,
        "output": output_path,
        "completed_at": datetime.now().isoformat()
    })
    progress["in_progress"] = None
    save_progress(progress)
    logger.info("Dossier marked complete", entity=entity_name, type=entity_type, path=output_path)


# =============================================================================
# DOSSIER PREPARATION
# =============================================================================

def prepare_entity_dossier(entity_name: str, entity_type: str, max_content_per_doc: int = 8000) -> Dict:
    """
    Prepare all materials for generating a dossier on an entity.
    Returns structured data with document contents and metadata.
    """
    logger.info("Preparing dossier", entity=entity_name, type=entity_type)
    db = load_entity_db()

    # Find entity in database
    entity_data = db.get(entity_type, {}).get(entity_name)
    if not entity_data:
        error_msg = f"Entity '{entity_name}' not found in {entity_type}"
        logger.error("Entity not found", entity=entity_name, type=entity_type)
        return {"error": error_msg}

    doc_ids = entity_data.get("docs", [])
    print(f"\nPreparing dossier for: {entity_name}")
    print(f"Entity type: {entity_type}")
    print(f"Documents: {len(doc_ids)}")
    print("-" * 60)

    # Collect document contents
    documents = []
    for i, doc_id in enumerate(doc_ids):
        print(f"  [{i+1}/{len(doc_ids)}] Fetching document {doc_id}...")
        doc = get_document_content(doc_id)
        if doc:
            content = doc.get("content", "")
            # Truncate very long documents
            if len(content) > max_content_per_doc:
                content = content[:max_content_per_doc//2] + \
                         "\n\n[...CONTENT TRUNCATED...]\n\n" + \
                         content[-max_content_per_doc//2:]
                logger.debug("Content truncated", doc_id=doc_id, original_length=len(doc.get("content", "")))

            documents.append({
                "id": doc_id,
                "title": doc.get("title", f"Document {doc_id}"),
                "created": doc.get("created", ""),
                "content": content,
                "content_length": len(doc.get("content", ""))
            })

    logger.info("Dossier preparation complete", entity=entity_name, documents=len(documents))

    return {
        "entity_name": entity_name,
        "entity_type": entity_type,
        "roles": entity_data.get("roles", []),
        "contexts": entity_data.get("contexts", []),
        "document_count": len(documents),
        "documents": documents,
        "prepared_at": datetime.now().isoformat()
    }


def save_dossier_prep(entity_name: str, prep_data: Dict) -> str:
    """Save prepared dossier data to a file."""
    safe_name = re.sub(r'[^\w\s-]', '', entity_name).replace(' ', '_')
    filename = f"dossier_prep_{safe_name}.json"
    filepath = DATA_DIR / filename

    with open(filepath, 'w') as f:
        json.dump(prep_data, f, indent=2)

    logger.info("Dossier preparation saved", entity=entity_name, path=str(filepath))
    print(f"\nSaved preparation to: {filepath}")
    return str(filepath)


def format_dossier_output(entity_name: str, entity_type: str, dossier_text: str,
                         documents: List[Dict]) -> str:
    """Format the final dossier as markdown."""
    type_labels = {
        "people": "Person",
        "organizations": "Organization",
        "events": "Event",
        "locations": "Location"
    }

    output = f"""---
title: "DOSSIER: {entity_name}"
date: {datetime.now().strftime("%Y-%m-%d")}
type: AI Dossier
subject_type: {type_labels.get(entity_type, entity_type)}
classification: OPEN SOURCE
sources: {len(documents)} documents analyzed
generated_by: The Continuum Report - Claude Code Pipeline
---

# DOSSIER: {entity_name}

**Generated:** {datetime.now().strftime("%B %d, %Y at %H:%M")}
**Subject Type:** {type_labels.get(entity_type, entity_type)}
**Sources Analyzed:** {len(documents)} documents
**Classification:** Open Source Intelligence

---

{dossier_text}

---

## Source Documents ({len(documents)} total)

| # | Document Title | Paperless ID |
|---|----------------|--------------|
"""

    for i, doc in enumerate(documents, 1):
        title = doc.get("title", "Untitled")[:55]
        doc_id = doc["id"]
        output += f"| {i} | {title} | [{doc_id}]({settings.paperless_url}/documents/{doc_id}/) |\n"

    output += f"""

---

*Generated by The Continuum Report - Claude Code Pipeline*
*Another Node in the Decentralized Intelligence Agency*
"""

    return output


def save_dossier(entity_name: str, entity_type: str, markdown_content: str) -> str:
    """Save the final dossier."""
    safe_name = re.sub(r'[^\w\s-]', '', entity_name).replace(' ', '_')
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"DOSSIER_{safe_name}_{timestamp}.md"
    filepath = REPORTS_DIR / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    logger.info("Dossier saved", entity=entity_name, type=entity_type, path=str(filepath))
    print(f"Saved dossier: {filepath}")
    return str(filepath)


# =============================================================================
# CLI COMMANDS
# =============================================================================

def cmd_queue():
    """Show the dossier queue."""
    queue = load_dossier_queue()
    progress = load_progress()
    completed_names = [c["name"] for c in progress.get("completed", [])]

    print(f"\n{'='*60}")
    print("DOSSIER GENERATION QUEUE")
    print(f"{'='*60}")
    print(f"\nTotal entities: {len(queue)}")
    print(f"Completed: {len(completed_names)}")
    print(f"Remaining: {len(queue) - len(completed_names)}")
    print(f"\n{'Type':<15} {'Name':<35} {'Docs':<6} {'Status'}")
    print("-" * 70)

    for item in queue:
        name = item["name"]
        status = "DONE" if name in completed_names else "pending"
        print(f"{item['type']:<15} {name[:33]:<35} {item['doc_count']:<6} {status}")


def cmd_prep(entity_name: str):
    """Prepare dossier materials for an entity."""
    queue = load_dossier_queue()

    # Find entity in queue
    entity = None
    for item in queue:
        if item["name"].lower() == entity_name.lower():
            entity = item
            break

    if not entity:
        print(f"Entity '{entity_name}' not found in queue")
        return

    prep_data = prepare_entity_dossier(entity["name"], entity["type"])
    if "error" in prep_data:
        print(prep_data["error"])
        return

    save_dossier_prep(entity["name"], prep_data)

    # Summary
    print(f"\n{'='*60}")
    print("DOSSIER PREPARATION COMPLETE")
    print(f"{'='*60}")
    print(f"Entity: {entity['name']}")
    print(f"Type: {entity['type']}")
    print(f"Documents: {prep_data['document_count']}")

    # Show document list
    print(f"\nSource documents:")
    for doc in prep_data["documents"][:10]:
        print(f"  [{doc['id']}] {doc['title'][:50]}")
    if len(prep_data["documents"]) > 10:
        print(f"  ... and {len(prep_data['documents']) - 10} more")


def cmd_show_prep(entity_name: str):
    """Show prepared dossier data (truncated for display)."""
    safe_name = re.sub(r'[^\w\s-]', '', entity_name).replace(' ', '_')
    filepath = DATA_DIR / f"dossier_prep_{safe_name}.json"

    if not filepath.exists():
        print(f"No preparation found for '{entity_name}'")
        print(f"Run: python generate_dossiers.py prep \"{entity_name}\"")
        logger.warning("Preparation file not found", entity=entity_name, path=str(filepath))
        return

    with open(filepath, 'r') as f:
        data = json.load(f)

    print(f"\n{'='*60}")
    print(f"PREPARED DATA: {data['entity_name']}")
    print(f"{'='*60}")
    print(f"Type: {data['entity_type']}")
    print(f"Documents: {data['document_count']}")
    print(f"Prepared: {data['prepared_at']}")

    if data.get("roles"):
        print(f"Known roles: {', '.join(data['roles'][:5])}")

    print(f"\nDocument previews:")
    for doc in data["documents"][:3]:
        print(f"\n--- [{doc['id']}] {doc['title']} ---")
        preview = doc["content"][:1000].replace('\n', ' ')
        print(preview)
        if len(doc["content"]) > 1000:
            print(f"[...{len(doc['content']) - 1000} more chars...]")


def cmd_next():
    """Show the next entity to process."""
    queue = load_dossier_queue()
    progress = load_progress()
    completed_names = [c["name"] for c in progress.get("completed", [])]

    for item in queue:
        if item["name"] not in completed_names:
            print(f"\nNext entity to process:")
            print(f"  Name: {item['name']}")
            print(f"  Type: {item['type']}")
            print(f"  Documents: {item['doc_count']}")
            print(f"\nTo prepare: python generate_dossiers.py prep \"{item['name']}\"")
            return

    print("All entities have been processed!")


def cmd_complete(entity_name: str, output_path: str = ""):
    """Mark an entity as complete."""
    queue = load_dossier_queue()

    for item in queue:
        if item["name"].lower() == entity_name.lower():
            if not output_path:
                safe_name = re.sub(r'[^\w\s-]', '', entity_name).replace(' ', '_')
                output_path = str(REPORTS_DIR / f"DOSSIER_{safe_name}*.md")

            mark_dossier_complete(item["name"], item["type"], output_path)
            print(f"Marked '{item['name']}' as complete")
            return

    logger.warning("Entity not found in queue", entity=entity_name)
    print(f"Entity '{entity_name}' not found in queue")


def print_usage():
    print("""
Dossier Generation Pipeline - The Continuum Report
===================================================

Commands:
  queue               Show all entities in the queue with status
  next                Show the next entity to process
  prep "<name>"       Prepare document materials for an entity
  show "<name>"       Show prepared data for an entity
  complete "<name>"   Mark an entity's dossier as complete

Workflow:
  1. Run 'queue' to see all entities
  2. Run 'next' to see what to work on
  3. Run 'prep "Entity Name"' to collect documents
  4. Generate dossier with Claude (read the prep file)
  5. Run 'complete "Entity Name"' when done

Example:
  python generate_dossiers.py queue
  python generate_dossiers.py prep "Ghislaine Maxwell"
  python generate_dossiers.py show "Ghislaine Maxwell"
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)

    command = sys.argv[1].lower()

    try:
        if command == "queue":
            cmd_queue()
        elif command == "next":
            cmd_next()
        elif command == "prep" and len(sys.argv) > 2:
            cmd_prep(sys.argv[2])
        elif command == "show" and len(sys.argv) > 2:
            cmd_show_prep(sys.argv[2])
        elif command == "complete" and len(sys.argv) > 2:
            output = sys.argv[3] if len(sys.argv) > 3 else ""
            cmd_complete(sys.argv[2], output)
        else:
            print_usage()
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\nCancelled.")
    except PaperlessError as e:
        logger.error("Paperless error", error=str(e))
        print(f"\nError: {e}")
        print("Check your PAPERLESS_TOKEN in .env file")
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error", error=str(e))
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
