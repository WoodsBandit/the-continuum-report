"""
The Continuum Report - Stage 2: Context Extraction

Reads context windows around entity mentions, identifies co-occurring entities,
and extracts relationship signals.

Trigger: Change to entity_registry.json
Output: Updates connection_contexts.json, co_occurrence.json

Usage:
    # Process all entities with new mentions
    python run_stage2.py

    # Process specific entity
    python run_stage2.py --entity "Jeffrey Epstein"

    # Dry run
    python run_stage2.py --dry-run
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Tuple

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from logging_config import get_logger
from config import settings
from paperless_client import PaperlessClient

logger = get_logger("stage2_context")


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(os.environ.get("CONTINUUM_BASE_DIR", "/mnt/user/continuum"))
INDEXES_DIR = BASE_DIR / "indexes"
LOGS_DIR = BASE_DIR / "logs"

# Index files
ENTITY_REGISTRY = INDEXES_DIR / "entity_registry.json"
SOURCE_MENTIONS = INDEXES_DIR / "source_mentions.json"
CO_OCCURRENCE = INDEXES_DIR / "co_occurrence.json"
CONNECTION_CONTEXTS = INDEXES_DIR / "connection_contexts.json"

# Context extraction settings
CONTEXT_WINDOW_CHARS = 500  # Characters before/after mention


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

        if path.exists():
            backup_path = path.with_suffix(".json.bak")
            path.rename(backup_path)

        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    except Exception as e:
        logger.error(f"Error saving {path}: {e}")
        return False


def load_entity_registry() -> dict:
    return load_json_file(ENTITY_REGISTRY, {})


def load_source_mentions() -> dict:
    return load_json_file(SOURCE_MENTIONS, {})


def load_co_occurrence() -> dict:
    return load_json_file(CO_OCCURRENCE, {})


def save_co_occurrence(data: dict) -> bool:
    return save_json_file(CO_OCCURRENCE, data)


def load_connection_contexts() -> dict:
    return load_json_file(CONNECTION_CONTEXTS, {})


def save_connection_contexts(data: dict) -> bool:
    return save_json_file(CONNECTION_CONTEXTS, data)


# =============================================================================
# CO-OCCURRENCE ANALYSIS
# =============================================================================

def get_entity_pair_key(entity1: str, entity2: str) -> str:
    """Generate consistent key for entity pair (sorted alphabetically)."""
    sorted_pair = sorted([entity1.lower(), entity2.lower()])
    return f"{sorted_pair[0]}___{sorted_pair[1]}"


def find_co_occurring_entities(
    document_content: str,
    entity_mentions: Dict[str, List[str]],
    context_window: int = CONTEXT_WINDOW_CHARS,
) -> List[Dict]:
    """
    Find entities that co-occur within context windows.

    Returns list of co-occurrence records with context snippets.
    """
    co_occurrences = []
    content_lower = document_content.lower()

    # Build position index for all entity mentions
    entity_positions = {}
    for entity_name, mentions in entity_mentions.items():
        entity_positions[entity_name] = []
        for mention in mentions:
            mention_lower = mention.lower()
            start = 0
            while True:
                pos = content_lower.find(mention_lower, start)
                if pos == -1:
                    break
                entity_positions[entity_name].append({
                    "start": pos,
                    "end": pos + len(mention),
                    "text": mention,
                })
                start = pos + 1

    # Find co-occurrences within context windows
    entity_names = list(entity_positions.keys())
    seen_pairs = set()

    for i, entity1 in enumerate(entity_names):
        for entity2 in entity_names[i + 1:]:
            pair_key = get_entity_pair_key(entity1, entity2)
            if pair_key in seen_pairs:
                continue

            # Check if they co-occur within window
            for pos1 in entity_positions[entity1]:
                for pos2 in entity_positions[entity2]:
                    distance = abs(pos1["start"] - pos2["start"])
                    if distance <= context_window * 2:
                        # Extract context around both mentions
                        min_pos = min(pos1["start"], pos2["start"])
                        max_pos = max(pos1["end"], pos2["end"])
                        context_start = max(0, min_pos - context_window)
                        context_end = min(len(document_content), max_pos + context_window)
                        context = document_content[context_start:context_end]

                        co_occurrences.append({
                            "entity1": entity1,
                            "entity2": entity2,
                            "pair_key": pair_key,
                            "distance_chars": distance,
                            "context": context.strip(),
                            "entity1_mention": pos1["text"],
                            "entity2_mention": pos2["text"],
                        })
                        seen_pairs.add(pair_key)
                        break
                if pair_key in seen_pairs:
                    break

    return co_occurrences


def analyze_relationship_signals(context: str, entity1: str, entity2: str) -> Dict:
    """
    Analyze context for relationship signals between entities.

    Returns relationship indicators and confidence.
    """
    context_lower = context.lower()

    signals = {
        "interaction_verbs": [],
        "relationship_terms": [],
        "temporal_indicators": [],
        "location_indicators": [],
        "financial_indicators": [],
    }

    # Interaction verbs
    interaction_verbs = [
        "met", "spoke", "called", "emailed", "visited", "traveled",
        "attended", "hosted", "introduced", "accompanied", "discussed",
        "negotiated", "agreed", "arranged", "coordinated", "contacted"
    ]
    for verb in interaction_verbs:
        if verb in context_lower:
            signals["interaction_verbs"].append(verb)

    # Relationship terms
    relationship_terms = [
        "friend", "associate", "partner", "colleague", "employee",
        "employer", "client", "customer", "investor", "donor",
        "attorney", "lawyer", "agent", "representative", "adviser"
    ]
    for term in relationship_terms:
        if term in context_lower:
            signals["relationship_terms"].append(term)

    # Temporal indicators
    temporal_words = [
        "year", "month", "day", "week", "time", "date",
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december",
        "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007",
        "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"
    ]
    for word in temporal_words:
        if word in context_lower:
            signals["temporal_indicators"].append(word)

    # Financial indicators
    financial_words = [
        "paid", "payment", "money", "fund", "invest", "donation",
        "transfer", "account", "bank", "wire", "cash", "$", "dollar"
    ]
    for word in financial_words:
        if word in context_lower:
            signals["financial_indicators"].append(word)

    # Calculate confidence based on signal density
    total_signals = sum(len(v) for v in signals.values())
    confidence = min(1.0, total_signals / 10)

    return {
        "signals": signals,
        "signal_count": total_signals,
        "confidence": confidence,
        "relationship_likely": confidence > 0.3,
    }


# =============================================================================
# CONTEXT EXTRACTION
# =============================================================================

def process_source_for_context(
    source_id: str,
    document_content: str,
    entity_mentions: Dict[str, List[str]],
) -> Dict:
    """
    Process a single source document for entity context extraction.

    Returns co-occurrences and relationship signals.
    """
    logger.info(f"Processing source {source_id} for context")

    # Find co-occurrences
    co_occurrences = find_co_occurring_entities(
        document_content=document_content,
        entity_mentions=entity_mentions,
    )

    logger.info(f"Found {len(co_occurrences)} co-occurrences in {source_id}")

    # Analyze relationship signals for each co-occurrence
    for co_occ in co_occurrences:
        signals = analyze_relationship_signals(
            context=co_occ["context"],
            entity1=co_occ["entity1"],
            entity2=co_occ["entity2"],
        )
        co_occ["relationship_analysis"] = signals

    return {
        "source_id": source_id,
        "co_occurrences": co_occurrences,
        "entity_count": len(entity_mentions),
        "processed_at": datetime.utcnow().isoformat() + "Z",
    }


def update_co_occurrence_index(
    co_occurrence_data: dict,
    new_co_occurrences: List[Dict],
    source_id: str,
) -> dict:
    """Update co-occurrence index with new data."""
    timestamp = datetime.utcnow().isoformat() + "Z"

    for co_occ in new_co_occurrences:
        pair_key = co_occ["pair_key"]

        if pair_key not in co_occurrence_data:
            co_occurrence_data[pair_key] = {
                "entity1": co_occ["entity1"],
                "entity2": co_occ["entity2"],
                "co_mention_count": 0,
                "sources": [],
                "first_seen": timestamp,
                "contexts": [],
            }

        entry = co_occurrence_data[pair_key]

        # Add source if not already present
        if source_id not in entry["sources"]:
            entry["sources"].append(source_id)
            entry["co_mention_count"] = len(entry["sources"])

        # Add context snippet
        entry["contexts"].append({
            "source_id": source_id,
            "context": co_occ["context"][:500],  # Truncate
            "relationship_analysis": co_occ.get("relationship_analysis", {}),
            "extracted_at": timestamp,
        })

        entry["last_updated"] = timestamp

    return co_occurrence_data


def update_connection_contexts_index(
    contexts_data: dict,
    new_co_occurrences: List[Dict],
    source_id: str,
) -> dict:
    """Update connection contexts index with detailed context snippets."""
    timestamp = datetime.utcnow().isoformat() + "Z"

    for co_occ in new_co_occurrences:
        pair_key = co_occ["pair_key"]

        if pair_key not in contexts_data:
            contexts_data[pair_key] = {
                "entity1": co_occ["entity1"],
                "entity2": co_occ["entity2"],
                "context_snippets": [],
                "relationship_summary": {
                    "interaction_verbs": [],
                    "relationship_terms": [],
                    "temporal_indicators": [],
                    "overall_confidence": 0,
                },
            }

        entry = contexts_data[pair_key]

        # Add context snippet
        entry["context_snippets"].append({
            "source_id": source_id,
            "text": co_occ["context"],
            "entity1_mention": co_occ.get("entity1_mention", ""),
            "entity2_mention": co_occ.get("entity2_mention", ""),
            "distance_chars": co_occ.get("distance_chars", 0),
            "extracted_at": timestamp,
        })

        # Aggregate relationship signals
        analysis = co_occ.get("relationship_analysis", {})
        signals = analysis.get("signals", {})

        for verb in signals.get("interaction_verbs", []):
            if verb not in entry["relationship_summary"]["interaction_verbs"]:
                entry["relationship_summary"]["interaction_verbs"].append(verb)

        for term in signals.get("relationship_terms", []):
            if term not in entry["relationship_summary"]["relationship_terms"]:
                entry["relationship_summary"]["relationship_terms"].append(term)

        for indicator in signals.get("temporal_indicators", []):
            if indicator not in entry["relationship_summary"]["temporal_indicators"]:
                entry["relationship_summary"]["temporal_indicators"].append(indicator)

        # Update overall confidence (average)
        new_confidence = analysis.get("confidence", 0)
        old_confidence = entry["relationship_summary"]["overall_confidence"]
        snippet_count = len(entry["context_snippets"])
        entry["relationship_summary"]["overall_confidence"] = (
            (old_confidence * (snippet_count - 1) + new_confidence) / snippet_count
        )

        entry["last_updated"] = timestamp

    return contexts_data


# =============================================================================
# MAIN PROCESSING
# =============================================================================

def process_context_extraction(dry_run: bool = False) -> dict:
    """
    Main context extraction process.

    Processes entity registry to find co-occurrences and extract contexts.
    """
    logger.info("Starting Stage 2: Context Extraction")

    # Load indexes
    entity_registry = load_entity_registry()
    source_mentions = load_source_mentions()
    co_occurrence_data = load_co_occurrence()
    contexts_data = load_connection_contexts()

    # Initialize Paperless client
    client = PaperlessClient(
        base_url=settings.paperless_url,
        token=settings.paperless_token,
    )

    stats = {
        "sources_processed": 0,
        "co_occurrences_found": 0,
        "connections_updated": 0,
    }

    # Get all unique sources from entity registry
    processed_sources = set()
    entities_dict = entity_registry.get("entities", entity_registry)
    for entity_key, entity_data in entities_dict.items():
        if not isinstance(entity_data, dict):
            continue  # Skip metadata keys like "generated", "count"
        for source_ref in entity_data.get("sources", []):
            processed_sources.add(source_ref)

    logger.info(f"Found {len(processed_sources)} sources to process")

    for source_ref in processed_sources:
        # Extract document ID from source ref
        # Supports both "doc_123" format and "ecf-1320-11" format
        doc_id = None
        if source_ref.startswith("doc_"):
            try:
                doc_id = int(source_ref.replace("doc_", ""))
            except ValueError:
                logger.warning(f"Invalid doc_ format: {source_ref}")
                continue
        else:
            # For ecf-* format, use the full string as identifier
            # These won't have Paperless document IDs, skip for now
            logger.debug(f"Skipping non-Paperless source: {source_ref}")
            continue

        # Get entities mentioned in this source
        source_entities = {}
        for entity_name, mentions_data in source_mentions.items():
            if not isinstance(mentions_data, dict):
                continue
            for mention in mentions_data.get("mentions", []):
                if mention.get("source_id") == doc_id:
                    source_entities[entity_name] = mention.get("contexts", [entity_name])
                    break

        logger.debug(f"Source {source_ref}: found {len(source_entities)} entities in source_mentions")

        if len(source_entities) < 2:
            # Need at least 2 entities for co-occurrence
            continue

        # Fetch document content
        try:
            content = client.get_document_content(doc_id)
            if not content:
                logger.warning(f"No content for document {doc_id}")
                continue
        except Exception as e:
            logger.error(f"Error fetching document {doc_id}: {e}")
            continue

        # Process for context
        result = process_source_for_context(
            source_id=source_ref,
            document_content=content,
            entity_mentions=source_entities,
        )

        # Update indexes
        if result["co_occurrences"] and not dry_run:
            co_occurrence_data = update_co_occurrence_index(
                co_occurrence_data=co_occurrence_data,
                new_co_occurrences=result["co_occurrences"],
                source_id=source_ref,
            )
            contexts_data = update_connection_contexts_index(
                contexts_data=contexts_data,
                new_co_occurrences=result["co_occurrences"],
                source_id=source_ref,
            )
            stats["connections_updated"] += len(result["co_occurrences"])

        stats["sources_processed"] += 1
        stats["co_occurrences_found"] += len(result["co_occurrences"])

        # Brief pause
        time.sleep(0.5)

    # Save indexes
    if not dry_run:
        save_co_occurrence(co_occurrence_data)
        save_connection_contexts(contexts_data)
        logger.info("Context indexes saved")

    logger.info(f"Stage 2 complete: {stats}")
    return stats


# =============================================================================
# CLI
# =============================================================================

def main():
    """CLI interface for Stage 2 processing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Stage 2: Context Extraction - Find entity co-occurrences"
    )
    parser.add_argument("--entity", type=str,
                        help="Process specific entity")
    parser.add_argument("--dry-run", action="store_true",
                        help="Dry run without updating indexes")
    parser.add_argument("--status", action="store_true",
                        help="Show co-occurrence index status")

    args = parser.parse_args()

    print("=" * 60)
    print("The Continuum Report - Stage 2: Context Extraction")
    print("=" * 60)

    if args.status:
        co_occ = load_co_occurrence()
        contexts = load_connection_contexts()
        print(f"Co-occurrence pairs: {len(co_occ)}")
        print(f"Connection contexts: {len(contexts)}")

        # Top co-occurrences
        sorted_pairs = sorted(
            co_occ.items(),
            key=lambda x: x[1].get("co_mention_count", 0),
            reverse=True
        )[:10]
        print("\nTop 10 co-occurring entity pairs:")
        for pair_key, data in sorted_pairs:
            print(f"  {data['entity1']} <-> {data['entity2']}: {data['co_mention_count']} sources")
        return 0

    stats = process_context_extraction(dry_run=args.dry_run)
    print(f"\nProcessing complete:")
    print(f"  Sources processed: {stats['sources_processed']}")
    print(f"  Co-occurrences found: {stats['co_occurrences_found']}")
    print(f"  Connections updated: {stats['connections_updated']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
