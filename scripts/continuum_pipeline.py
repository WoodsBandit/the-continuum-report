#!/usr/bin/env python3
"""
The Continuum Report - AI Document Pipeline
Version 4.0 - Refactored with Shared Library

CHANGES IN v4.0:
- Uses centralized configuration (lib.config)
- Uses PaperlessClient with retry logic (lib.paperless_client)
- Uses OllamaClient with memory management (lib.ollama_client)
- Structured logging with structlog (lib.logging_config)
- No hardcoded secrets - uses environment variables
- Path handling with pathlib

CHANGES IN v3.1:
- Memory-safe processing with forced garbage collection
- Delays between documents to prevent RAM exhaustion
- Checkpoint system - saves progress after each document
- Auto-resume from checkpoint on restart
- Reduced Ollama context window to lower memory footprint
- All documents still processed - just paced safely

CHANGES IN v3.0:
- Uses ALL matching source documents (configurable limit)
- EXCLUDES previously generated dossiers from sources
- Streaming progress indicators
"""

import json
import sys
import re
import gc
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Import shared library
from lib import settings, get_logger, PaperlessClient, OllamaClient
from lib import PaperlessError, OllamaError

# Initialize logger
logger = get_logger(__name__)

# =============================================================================
# CONFIGURATION (from centralized config)
# =============================================================================

MODEL_NAME = settings.ollama_model

# Where to save outputs (using pathlib)
OUTPUT_DIR = Path(settings.continuum_base_dir) / "documents" / "inbox"
DOSSIER_DIR = settings.reports_dir
CHECKPOINT_DIR = settings.checkpoints_dir

# Website URL for source links
WEBSITE_BASE_URL = "https://thecontinuumreport.com"

# DOCUMENT LIMITS
MAX_DOCUMENTS_TO_SEARCH = 9999    # No artificial cap - get everything
MAX_DOCUMENTS_FOR_ENTITIES = 9999 # Extract from ALL matching docs
MAX_DOCUMENTS_FOR_DOSSIER = 9999  # Include ALL in dossier generation
MAX_CHUNK_SIZE = 1500             # Characters per chunk (reduced for memory)

# MEMORY SAFETY SETTINGS - AGGRESSIVE FOR 16GB RAM
DELAY_BETWEEN_DOCS = 10           # Seconds to wait between processing docs
DELAY_BETWEEN_BATCHES = 30        # Seconds to wait every 5 docs
OLLAMA_CONTEXT_SIZE = 1024        # Minimal context window
OLLAMA_TIMEOUT = 600              # 10 minutes per request
UNLOAD_MODEL_EVERY = 10           # Unload Ollama model every N docs to clear memory

# Ensure directories exist
settings.ensure_directories()
DOSSIER_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# CHECKPOINT SYSTEM
# =============================================================================

def get_checkpoint_path(subject: str) -> Path:
    """Get checkpoint file path for a subject."""
    safe_subject = re.sub(r'[^\w\s-]', '', subject).replace(' ', '_')
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    return CHECKPOINT_DIR / f"checkpoint_{safe_subject}.json"


def load_checkpoint(subject: str) -> Optional[Dict]:
    """Load checkpoint if it exists."""
    path = get_checkpoint_path(subject)
    if path.exists():
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.warning("Failed to load checkpoint", path=str(path), error=str(e))
    return None


def save_checkpoint(subject: str, data: Dict):
    """Save checkpoint data."""
    path = get_checkpoint_path(subject)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    logger.debug("Checkpoint saved", path=str(path))


def clear_checkpoint(subject: str):
    """Remove checkpoint after successful completion."""
    path = get_checkpoint_path(subject)
    if path.exists():
        path.unlink()
        logger.info("Checkpoint cleared", path=str(path))


# =============================================================================
# PROGRESS INDICATORS
# =============================================================================

def print_progress_bar(current: int, total: int, prefix: str = "", suffix: str = "", length: int = 40):
    """Print a progress bar to the console."""
    if total == 0:
        return
    percent = current / total
    filled = int(length * percent)
    bar = "█" * filled + "░" * (length - filled)
    print(f"\r  {prefix} |{bar}| {current}/{total} {suffix}", end="", flush=True)
    if current >= total:
        print()


def stream_progress(char_count: int, start_time: float):
    """Display streaming progress during AI generation."""
    elapsed = time.time() - start_time
    rate = char_count / elapsed if elapsed > 0 else 0
    print(f"\r  Generating... {char_count:,} chars | {elapsed:.1f}s | {rate:.0f} chars/s", end="", flush=True)


def clear_memory():
    """Force garbage collection to free memory."""
    gc.collect()


def unload_ollama_model():
    """Unload model from Ollama to free memory."""
    logger.info("Unloading model to free memory")
    try:
        with OllamaClient() as client:
            client.unload_model()
        time.sleep(10)  # Wait for memory to clear
        logger.info("Model unloaded successfully")
    except OllamaError as e:
        logger.warning("Could not unload model", error=str(e))


# =============================================================================
# PAPERLESS API FUNCTIONS (using PaperlessClient)
# =============================================================================

def get_paperless_client() -> PaperlessClient:
    """Get a configured Paperless client."""
    return PaperlessClient()


def get_all_tags() -> Dict[str, int]:
    """Fetch all tags from Paperless."""
    try:
        with get_paperless_client() as client:
            return client.get_all_tags()
    except PaperlessError as e:
        logger.error("Failed to fetch tags", error=str(e))
        return {}


def get_all_document_types() -> Dict[str, int]:
    """Fetch all document types from Paperless."""
    try:
        with get_paperless_client() as client:
            return client.get_all_document_types()
    except PaperlessError as e:
        logger.error("Failed to fetch document types", error=str(e))
        return {}


def search_paperless(query: str, limit: int = MAX_DOCUMENTS_TO_SEARCH) -> List[Dict]:
    """Search Paperless for documents matching query with pagination."""
    logger.info("Searching Paperless", query=query, limit=limit)

    try:
        with get_paperless_client() as client:
            def progress(fetched, total):
                print_progress_bar(fetched, min(total, limit), prefix="Fetching", suffix="docs")

            results = client.search_documents(query, progress_callback=progress)
            logger.info("Search complete", found=len(results))
            return results[:limit]
    except PaperlessError as e:
        logger.error("Search failed", query=query, error=str(e))
        return []


def filter_out_dossiers(documents: List[Dict]) -> List[Dict]:
    """Filter out previously generated dossiers from source list."""
    filtered = []
    excluded_count = 0

    all_tags = get_all_tags()
    all_doctypes = get_all_document_types()

    dossier_tag_ids = set()
    for tag_name, tag_id in all_tags.items():
        if "dossier" in tag_name.lower() or "ai generated" in tag_name.lower():
            dossier_tag_ids.add(tag_id)

    dossier_doctype_ids = set()
    for dt_name, dt_id in all_doctypes.items():
        if "dossier" in dt_name.lower() or "ai generated" in dt_name.lower():
            dossier_doctype_ids.add(dt_id)

    for doc in documents:
        title = doc.get("title", "").upper()

        if title.startswith("DOSSIER:") or title.startswith("DOSSIER_"):
            excluded_count += 1
            continue

        doc_tags = doc.get("tags", [])
        if any(tag_id in dossier_tag_ids for tag_id in doc_tags):
            excluded_count += 1
            continue

        doc_type = doc.get("document_type")
        if doc_type in dossier_doctype_ids:
            excluded_count += 1
            continue

        filtered.append(doc)

    if excluded_count > 0:
        logger.info("Excluded AI-generated dossiers", count=excluded_count)
        print(f"  Excluded {excluded_count} previously generated dossier(s) from sources")

    return filtered


def get_document_content(doc_id: int) -> Optional[Dict]:
    """Get full document details including content."""
    try:
        with get_paperless_client() as client:
            return client.get_document(doc_id)
    except PaperlessError as e:
        logger.error("Failed to get document", doc_id=doc_id, error=str(e))
        return None


def update_document_metadata(doc_id: int, tags: List[int] = None,
                             document_type: int = None, title: str = None) -> bool:
    """Update a document's tags, type, or title in Paperless."""
    payload = {}
    if tags is not None:
        payload["tags"] = tags
    if document_type is not None:
        payload["document_type"] = document_type
    if title is not None:
        payload["title"] = title

    if not payload:
        return True

    try:
        with get_paperless_client() as client:
            return client.update_document(doc_id, **payload)
    except PaperlessError as e:
        logger.error("Failed to update document", doc_id=doc_id, error=str(e))
        return False


def create_tag_if_missing(tag_name: str) -> Optional[int]:
    """Create a tag in Paperless if it doesn't exist."""
    tags = get_all_tags()
    if tag_name in tags:
        return tags[tag_name]

    try:
        with get_paperless_client() as client:
            tag_id = client.create_tag(tag_name)
            logger.info("Created tag", name=tag_name, tag_id=tag_id)
            return tag_id
    except PaperlessError as e:
        logger.error("Failed to create tag", name=tag_name, error=str(e))
        return None


# =============================================================================
# OLLAMA / AI FUNCTIONS - MEMORY OPTIMIZED (using OllamaClient)
# =============================================================================

def query_ollama(prompt: str, system_prompt: str = None, show_progress: bool = True) -> str:
    """Send a prompt to Ollama with streaming and reduced memory footprint."""
    try:
        with OllamaClient() as client:
            full_response = ""
            start_time = time.time()

            for chunk in client.generate_stream(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=2048,
                context_size=OLLAMA_CONTEXT_SIZE
            ):
                full_response += chunk
                if show_progress:
                    stream_progress(len(full_response), start_time)

            if show_progress:
                print()

            return full_response

    except OllamaError as e:
        logger.error("Ollama generation failed", error=str(e))
        print(f"\n  [ERROR] Ollama request failed: {e}")
        return ""


def query_ollama_simple(prompt: str, system_prompt: str = None) -> str:
    """Non-streaming version for quick queries with memory optimization."""
    try:
        with OllamaClient() as client:
            return client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=1024,
                context_size=OLLAMA_CONTEXT_SIZE
            )
    except OllamaError as e:
        logger.error("Ollama generation failed", error=str(e))
        print(f"  [ERROR] {e}")
        return ""


# =============================================================================
# ENTITY EXTRACTION
# =============================================================================

ENTITY_EXTRACTION_PROMPT = """You are an intelligence analyst extracting structured data from documents.

Extract ALL mentioned entities. Return ONLY valid JSON:
{
  "people": [{"name": "Full Name", "role": "role if mentioned", "context": "brief context"}],
  "organizations": [{"name": "Org Name", "type": "type", "context": "brief context"}],
  "locations": [{"name": "Location", "type": "type", "context": "brief context"}],
  "dates": [{"date": "YYYY-MM-DD or description", "event": "what happened"}],
  "key_claims": [{"claim": "factual claim", "evidence_type": "type"}]
}

DOCUMENT TEXT:
"""


def extract_entities(text: str, doc_title: str = "") -> Dict:
    """Extract entities with memory-safe chunking."""
    # Aggressive truncation for memory safety
    if len(text) > MAX_CHUNK_SIZE * 2:
        text = text[:MAX_CHUNK_SIZE] + "\n\n[...TRUNCATED...]\n\n" + text[-MAX_CHUNK_SIZE:]
        logger.debug("Text truncated for memory safety", original_length=len(text))

    prompt = ENTITY_EXTRACTION_PROMPT + text
    response = query_ollama_simple(prompt)

    # Clear memory after each extraction
    clear_memory()

    try:
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            entities = json.loads(json_match.group())
            logger.debug("Entities extracted", doc_title=doc_title,
                        people=len(entities.get("people", [])),
                        orgs=len(entities.get("organizations", [])))
            return entities
    except json.JSONDecodeError as e:
        logger.warning("Failed to parse entity JSON", doc_title=doc_title, error=str(e))

    return {"people": [], "organizations": [], "locations": [], "dates": [], "key_claims": []}


# =============================================================================
# DOSSIER GENERATION
# =============================================================================

DOSSIER_SYSTEM_PROMPT = """You are an intelligence analyst writing a detailed dossier. Your writing style:
- Precise and factual
- Every claim must reference a source document
- Use format: "According to [Document Title], ..."
- Include specific quotes when available
- Note contradictions or gaps in evidence
- Separate confirmed facts from allegations
- Professional tone, no speculation beyond evidence"""


DOSSIER_PROMPT_TEMPLATE = """Write a comprehensive intelligence dossier on {subject}.

You have access to {doc_count} source documents. Here are summaries:

{document_summaries}

REQUIREMENTS:
1. Brief summary (2-3 sentences) of who/what {subject} is
2. Organize by theme (Connections, Timeline, Financial Ties, etc.)
3. Every claim MUST cite source: "According to [Doc Title]..."
4. Include dates, names, locations from documents
5. Note strong vs. circumstantial evidence
6. End with "Gaps in Evidence" section
7. Use AS MANY sources as possible

Write the dossier now:"""


def generate_dossier(subject: str, documents: List[Dict], entities_by_doc: Dict[int, Dict]) -> str:
    """Generate dossier with adaptive compression for large document sets."""
    doc_summaries = []
    docs_to_use = documents  # Use ALL documents
    
    print(f"  Building summaries from {len(docs_to_use)} source documents...")
    
    # Adaptive compression: fewer details per doc when there are many
    if len(docs_to_use) > 100:
        max_people = 3
        max_claims = 1
        max_dates = 1
    elif len(docs_to_use) > 50:
        max_people = 5
        max_claims = 2
        max_dates = 2
    else:
        max_people = 8
        max_claims = 3
        max_dates = 3
    
    for i, doc in enumerate(docs_to_use):
        doc_id = doc["id"]
        title = doc.get("title", f"Document {doc_id}")
        entities = entities_by_doc.get(doc_id, {})
        
        summary = f"\n### SOURCE {i+1}: {title}\n"
        
        if entities.get("people"):
            people_list = ", ".join([p["name"] for p in entities["people"][:max_people]])
            summary += f"People: {people_list}\n"
        
        if entities.get("key_claims"):
            summary += "Claims:\n"
            for claim in entities["key_claims"][:max_claims]:
                summary += f"  - {claim['claim']}\n"
        
        if entities.get("dates"):
            for d in entities["dates"][:max_dates]:
                summary += f"  - {d['date']}: {d['event']}\n"
        
        if not any([entities.get("people"), entities.get("key_claims"), entities.get("dates")]):
            summary += "(Content available, entities not extracted)\n"
        
        doc_summaries.append(summary)
    
    # Clear memory before big generation
    clear_memory()
    
    prompt = DOSSIER_PROMPT_TEMPLATE.format(
        subject=subject,
        doc_count=len(docs_to_use),
        document_summaries="\n".join(doc_summaries)
    )
    
    print(f"\n  Generating dossier for {subject} using {len(docs_to_use)} sources...")
    print("  (This may take several minutes)\n")
    
    dossier_text = query_ollama(prompt, DOSSIER_SYSTEM_PROMPT, show_progress=True)
    
    # Clear memory after generation
    clear_memory()
    
    return dossier_text


# =============================================================================
# AUTO-TAGGING
# =============================================================================

def auto_tag_document(doc_id: int, entities: Dict, doc_info: Dict) -> List[str]:
    """Automatically apply tags based on extracted entities."""
    tags_to_apply = []
    current_tag_ids = doc_info.get("tags", [])
    
    content = doc_info.get("content", "").lower()
    
    # Case detection
    if "15-cv-07433" in content or "15-cv-7433" in content or "giuffre" in content:
        tag_id = create_tag_if_missing("CASE: Giuffre-v-Maxwell")
        if tag_id and tag_id not in current_tag_ids:
            tags_to_apply.append("CASE: Giuffre-v-Maxwell")
            current_tag_ids.append(tag_id)
    
    if "20-cr-330" in content or "united states v. maxwell" in content:
        tag_id = create_tag_if_missing("CASE: Maxwell-Criminal")
        if tag_id and tag_id not in current_tag_ids:
            tags_to_apply.append("CASE: Maxwell-Criminal")
            current_tag_ids.append(tag_id)
    
    # Key figures
    key_figures = ["jeffrey epstein", "ghislaine maxwell", "bill clinton", 
                   "prince andrew", "les wexner", "alan dershowitz", "virginia giuffre"]
    
    for person in entities.get("people", []):
        name_lower = person["name"].lower()
        for figure in key_figures:
            if figure in name_lower or name_lower in figure:
                tag_name = f"PERSON: {person['name'].title()}"
                tag_id = create_tag_if_missing(tag_name)
                if tag_id and tag_id not in current_tag_ids:
                    tags_to_apply.append(tag_name)
                    current_tag_ids.append(tag_id)
                break
    
    if tags_to_apply:
        print(f"    Auto-tagging: {', '.join(tags_to_apply)}")
        update_document_metadata(doc_id, tags=current_tag_ids)
    
    return tags_to_apply


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

def format_dossier_markdown(subject: str, dossier_text: str, 
                           documents: List[Dict], entities_by_doc: Dict) -> str:
    """Format dossier as publication-ready markdown."""
    
    all_people = {}
    all_orgs = {}
    all_dates = []
    
    for doc_id, entities in entities_by_doc.items():
        for person in entities.get("people", []):
            name = person["name"]
            if name not in all_people:
                all_people[name] = person
        for org in entities.get("organizations", []):
            name = org["name"]
            if name not in all_orgs:
                all_orgs[name] = org
        all_dates.extend(entities.get("dates", []))
    
    all_dates.sort(key=lambda x: x.get("date", ""))
    
    output = f"""---
title: "DOSSIER: {subject}"
date: {datetime.now().strftime("%Y-%m-%d")}
type: AI Dossier
classification: OPEN SOURCE
sources: {len(documents)} documents analyzed
generated_by: The Continuum Report AI Pipeline v3.1
---

# DOSSIER: {subject}

**Generated:** {datetime.now().strftime("%B %d, %Y at %H:%M")}  
**Sources Analyzed:** {len(documents)} documents  
**Classification:** Open Source Intelligence  

---

{dossier_text}

---

## Source Documents ({len(documents)} total)

| # | Title | Paperless ID |
|---|-------|--------------|
"""
    
    for i, doc in enumerate(documents, 1):
        title = doc.get("title", "Untitled")[:60]
        doc_id = doc["id"]
        output += f"| {i} | {title} | [{doc_id}]({settings.paperless_url}/documents/{doc_id}/) |\n"
    
    output += f"""

---

## Extracted Entities

### People ({len(all_people)})
"""
    for name, info in list(all_people.items())[:50]:
        role = info.get("role", "")
        output += f"- **{name}**{f' - {role}' if role else ''}\n"
    
    output += f"""

### Organizations ({len(all_orgs)})
"""
    for name, info in list(all_orgs.items())[:30]:
        org_type = info.get("type", "")
        output += f"- **{name}**{f' ({org_type})' if org_type else ''}\n"
    
    if all_dates:
        output += """

### Key Dates
"""
        for d in all_dates[:30]:
            output += f"- **{d.get('date', 'Unknown')}**: {d.get('event', '')}\n"
    
    output += f"""

---

*Generated by The Continuum Report AI Pipeline v3.1 (Memory Safe Edition)*
*Another Node in the Decentralized Intelligence Agency*
"""
    
    return output


# =============================================================================
# MAIN PIPELINE - MEMORY SAFE WITH CHECKPOINTS
# =============================================================================

def run_pipeline(subject: str, auto_tag: bool = True, extract_entities_flag: bool = True):
    """Run the full pipeline with checkpointing and memory management."""

    logger.info("Pipeline started", subject=subject, auto_tag=auto_tag, extract_entities=extract_entities_flag)

    print(f"\n{'='*60}")
    print(f"THE CONTINUUM REPORT - AI PIPELINE v4.0")
    print(f"Subject: {subject}")
    print(f"{'='*60}\n")

    # Check for existing checkpoint
    checkpoint = load_checkpoint(subject)
    entities_by_doc = {}
    processed_doc_ids = set()

    if checkpoint:
        print(f"  Found checkpoint - resuming from previous run")
        entities_by_doc = checkpoint.get("entities_by_doc", {})
        # Convert string keys back to int
        entities_by_doc = {int(k): v for k, v in entities_by_doc.items()}
        processed_doc_ids = set(checkpoint.get("processed_doc_ids", []))
        logger.info("Resuming from checkpoint", processed=len(processed_doc_ids))
        print(f"     Already processed: {len(processed_doc_ids)} documents\n")
    
    # Step 1: Search for documents
    print(f"[1/6] Searching Paperless for '{subject}'...")
    all_documents = search_paperless(subject, limit=MAX_DOCUMENTS_TO_SEARCH)
    print(f"      Found {len(all_documents)} total documents\n")
    
    if not all_documents:
        print("No documents found. Exiting.")
        return
    
    # Step 2: Filter out dossiers
    print(f"[2/6] Filtering out previously generated dossiers...")
    documents = filter_out_dossiers(all_documents)
    print(f"      {len(documents)} source documents remaining\n")
    
    if not documents:
        print("No source documents found after filtering.")
        return
    
    # List documents
    print(f"Source documents to analyze ({len(documents)} total):")
    for i, doc in enumerate(documents[:25], 1):
        status = "✓" if doc["id"] in processed_doc_ids else " "
        print(f"  {status} {i}. {doc.get('title', 'Untitled')[:55]}")
    if len(documents) > 25:
        print(f"  ... and {len(documents) - 25} more")
    print()
    
    # Step 3: Extract entities with memory-safe pacing
    if extract_entities_flag:
        docs_for_entities = documents  # ALL documents, no cap
        remaining = [d for d in docs_for_entities if d["id"] not in processed_doc_ids]
        
        print(f"[3/6] Extracting entities from {len(remaining)} documents...")
        print(f"      (Memory-safe mode: {DELAY_BETWEEN_DOCS}s delay between docs)\n")
        
        for i, doc in enumerate(remaining):
            doc_id = doc["id"]
            doc_title = doc.get('title', '')[:35]
            
            print(f"  [{i+1}/{len(remaining)}] {doc_title}...")
            
            full_doc = get_document_content(doc_id)
            if full_doc and full_doc.get("content"):
                entities = extract_entities(
                    full_doc["content"], 
                    doc.get("title", f"Doc {doc_id}")
                )
                entities_by_doc[doc_id] = entities
                
                if auto_tag:
                    auto_tag_document(doc_id, entities, full_doc)
                
                processed_doc_ids.add(doc_id)
                
                # Save checkpoint after each document
                save_checkpoint(subject, {
                    "entities_by_doc": {str(k): v for k, v in entities_by_doc.items()},
                    "processed_doc_ids": list(processed_doc_ids),
                    "last_updated": datetime.now().isoformat()
                })
                
                # Memory management
                clear_memory()
                
                # Unload model periodically to prevent memory buildup
                if (i + 1) % UNLOAD_MODEL_EVERY == 0:
                    unload_ollama_model()
                # Pacing delays
                elif (i + 1) % 5 == 0:
                    print(f"  💤 Batch pause ({DELAY_BETWEEN_BATCHES}s)...")
                    time.sleep(DELAY_BETWEEN_BATCHES)
                else:
                    time.sleep(DELAY_BETWEEN_DOCS)
            else:
                print(f"    [SKIP] No content")
        
        print(f"\n  ✓ Entity extraction complete\n")
    else:
        print(f"[3/6] Skipping entity extraction\n")
    
    # Step 4: Generate dossier
    print(f"[4/6] Generating dossier with {MODEL_NAME}...")
    dossier_text = generate_dossier(subject, documents, entities_by_doc)
    
    if not dossier_text:
        print("Failed to generate dossier. Exiting.")
        return
    
    # Step 5: Format and save
    print(f"\n[5/6] Formatting output...")
    logger.info("Formatting dossier output", subject=subject)
    markdown_output = format_dossier_markdown(subject, dossier_text, documents, entities_by_doc)

    safe_subject = re.sub(r'[^\w\s-]', '', subject).replace(' ', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    md_filename = f"DOSSIER_{safe_subject}_{timestamp}.md"
    md_path = DOSSIER_DIR / md_filename

    print(f"\n[6/6] Saving outputs...")

    try:
        DOSSIER_DIR.mkdir(parents=True, exist_ok=True)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        logger.info("Dossier saved", path=str(md_path))
        print(f"      Markdown saved: {md_path}")
    except Exception as e:
        logger.error("Failed to save dossier", path=str(md_path), error=str(e))
        fallback_path = Path(md_filename)
        with open(fallback_path, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        md_path = fallback_path
        print(f"      Saved to: {md_filename}")
    
    # Clear checkpoint on success
    clear_checkpoint(subject)

    logger.info("Pipeline completed successfully",
                subject=subject,
                documents=len(documents),
                entities_extracted=len(entities_by_doc),
                dossier_path=str(md_path))

    print(f"\n{'='*60}")
    print(f"PIPELINE COMPLETE")
    print(f"  Subject: {subject}")
    print(f"  Sources: {len(documents)} documents")
    print(f"  Entities extracted: {len(entities_by_doc)} documents")
    print(f"{'='*60}\n")

    # Preview
    print("DOSSIER PREVIEW:")
    print("-"*40)
    print(dossier_text[:2000])
    if len(dossier_text) > 2000:
        print("\n[...truncated...]")

    return {
        "subject": subject,
        "documents_analyzed": len(documents),
        "entities_extracted": len(entities_by_doc),
        "dossier_path": str(md_path)
    }


# =============================================================================
# CLI
# =============================================================================

def print_usage():
    print("""
The Continuum Report - AI Pipeline v3.1 (Memory Safe Edition)

Features:
  - Memory-safe processing with delays between documents
  - Checkpoint system - resume if interrupted
  - Reduced memory footprint for stable operation

Usage:
  python continuum_pipeline.py dossier "Subject Name"
  python continuum_pipeline.py test
  python continuum_pipeline.py resume "Subject Name"   Resume from checkpoint

Examples:
  python continuum_pipeline.py dossier "Bill Clinton"
  python continuum_pipeline.py dossier "Jeffrey Epstein"
""")


def test_connections():
    """Test connectivity."""
    logger.info("Testing system connections")
    print("\nTesting connections...\n")

    print(f"Paperless ({settings.paperless_url})...")
    try:
        with get_paperless_client() as client:
            if client.health_check():
                print("  Connected")
                logger.info("Paperless connection successful")
            else:
                print("  Health check failed")
                logger.error("Paperless health check failed")
    except PaperlessError as e:
        print(f"  Failed: {e}")
        logger.error("Paperless connection failed", error=str(e))

    print(f"\nOllama ({settings.ollama_url})...")
    try:
        with OllamaClient() as client:
            models = client.list_models()
            print(f"  Connected")
            print(f"  Models: {models}")
            logger.info("Ollama connection successful", models=models)
    except OllamaError as e:
        print(f"  Failed: {e}")
        logger.error("Ollama connection failed", error=str(e))

    print(f"\nMemory settings (aggressive for 16GB RAM):")
    print(f"  Context window: {OLLAMA_CONTEXT_SIZE}")
    print(f"  Delay between docs: {DELAY_BETWEEN_DOCS}s")
    print(f"  Batch pause: {DELAY_BETWEEN_BATCHES}s every 5 docs")
    print(f"  Model unload: every {UNLOAD_MODEL_EVERY} docs")
    print(f"  Chunk size: {MAX_CHUNK_SIZE} chars")

    print(f"\nFetching Paperless taxonomy...")
    tags = get_all_tags()
    doctypes = get_all_document_types()
    print(f"  Tags: {list(tags.keys())[:10]}{'...' if len(tags) > 10 else ''}")
    print(f"  Document Types: {list(doctypes.keys())}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == "dossier":
        if len(sys.argv) < 3:
            print("Error: Please provide a subject name")
            sys.exit(1)
        subject = " ".join(sys.argv[2:])
        run_pipeline(subject)
    
    elif command == "resume":
        if len(sys.argv) < 3:
            print("Error: Please provide a subject name")
            sys.exit(1)
        subject = " ".join(sys.argv[2:])
        run_pipeline(subject)  # Will auto-detect checkpoint
    
    elif command == "test":
        test_connections()
    
    else:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)
