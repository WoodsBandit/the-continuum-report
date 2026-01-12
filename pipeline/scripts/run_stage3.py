"""
The Continuum Report - Stage 3: Brief Generation

Generates/updates analytical briefs for entities and connections.
Runs legal compliance check before outputting to pending_approval/.

Trigger: Change to connection_contexts.json
Output: Briefs in pending_approval/entities/ and pending_approval/connections/

Usage:
    # Process all entities/connections needing briefs
    python run_stage3.py

    # Generate brief for specific entity
    python run_stage3.py --entity "Jeffrey Epstein"

    # Generate brief for specific connection
    python run_stage3.py --connection "Jeffrey Epstein" "Ghislaine Maxwell"

    # Dry run
    python run_stage3.py --dry-run
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Tuple

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from logging_config import get_logger
from config import settings

logger = get_logger("stage3_briefs")


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(os.environ.get("CONTINUUM_BASE_DIR", "/mnt/user/continuum"))
INDEXES_DIR = BASE_DIR / "indexes"
BRIEFS_DIR = BASE_DIR / "briefs"
PENDING_DIR = BASE_DIR / "pending_approval"
TEMPLATES_DIR = BASE_DIR / "templates"
LOGS_DIR = BASE_DIR / "logs"

# Index files
ENTITY_REGISTRY = INDEXES_DIR / "entity_registry.json"
SOURCE_MENTIONS = INDEXES_DIR / "source_mentions.json"
CO_OCCURRENCE = INDEXES_DIR / "co_occurrence.json"
CONNECTION_CONTEXTS = INDEXES_DIR / "connection_contexts.json"

# Threshold for connection briefs
MIN_CO_MENTIONS_FOR_BRIEF = 2


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
    """Save JSON file safely."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
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


def load_connection_contexts() -> dict:
    return load_json_file(CONNECTION_CONTEXTS, {})


# =============================================================================
# TEMPLATE LOADING
# =============================================================================

def load_template(template_name: str) -> str:
    """Load a template file."""
    template_path = TEMPLATES_DIR / template_name
    try:
        if template_path.exists():
            return template_path.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Error loading template {template_name}: {e}")

    # Return minimal default template
    if "entity" in template_name:
        return """# {entity_name}

## Summary
{summary}

## Sources
{sources}

## Analysis
{analysis}
"""
    else:
        return """# Connection: {entity1} ↔ {entity2}

## Summary
{summary}

## Evidence
{evidence}

## Analysis
{analysis}
"""


# =============================================================================
# LEGAL COMPLIANCE CHECK
# =============================================================================

LEGAL_CHECKLIST = [
    ("factual_basis", "All claims have documented source citations"),
    ("no_defamation", "No defamatory statements without factual basis"),
    ("public_figure", "Subject is public figure or matter of public concern"),
    ("fair_reporting", "Fair and accurate reporting of public records"),
    ("no_private_facts", "No disclosure of private facts without public interest"),
    ("neutral_tone", "Neutral, objective journalistic tone"),
    ("source_attribution", "All quotes and claims attributed to sources"),
    ("no_speculation", "No unsubstantiated speculation presented as fact"),
    ("context_provided", "Adequate context for potentially damaging claims"),
    ("corrections_noted", "Any known corrections or retractions noted"),
    ("time_relevance", "Information is current or historical context provided"),
    ("proportionality", "Detail proportional to public interest"),
    ("no_malice", "No evidence of actual malice in presentation"),
    ("verified_sources", "Sources are verifiable and documented"),
    ("balanced_view", "Multiple perspectives included where relevant"),
    ("no_harassment", "Content does not constitute harassment"),
    ("legal_proceedings", "Ongoing legal matters noted as such"),
    ("privacy_balance", "Privacy interests balanced against public interest"),
]


def run_legal_compliance_check(brief_content: str) -> Dict:
    """
    Run legal compliance check on brief content.

    Returns compliance result with pass/fail for each checklist item.
    """
    from invoke_claude import invoke_claude_with_sop

    checklist_text = "\n".join([f"- {item[0]}: {item[1]}" for item in LEGAL_CHECKLIST])

    task_description = f"""
You are the legal-auditor agent. Review this analytical brief for legal compliance.

LEGAL COMPLIANCE CHECKLIST:
{checklist_text}

BRIEF CONTENT TO REVIEW:
{brief_content[:20000]}

YOUR TASK:
1. Evaluate each checklist item (PASS or FAIL)
2. Provide specific concerns for any FAIL items
3. Output JSON in this exact format:

```json
{{
    "overall_status": "APPROVED" or "ISSUES_FOUND",
    "checklist_results": {{
        "factual_basis": {{"status": "PASS" or "FAIL", "notes": "..."}},
        "no_defamation": {{"status": "PASS" or "FAIL", "notes": "..."}},
        ... (all 18 items)
    }},
    "issues": ["list of specific issues if any"],
    "recommendations": ["list of recommendations if any"]
}}
```

Be thorough but fair. PASS items that are adequately addressed.
"""

    result = invoke_claude_with_sop(
        sop_number=3,
        task_description=task_description,
        additional_context={"content_length": len(brief_content)},
        include_runbook=False,
        timeout=600,
    )

    if not result.success:
        logger.error(f"Legal check failed: {result.error}")
        return {
            "overall_status": "ERROR",
            "error": result.error,
            "issues": ["Legal compliance check could not be completed"],
        }

    # Parse response
    try:
        output = result.output
        json_start = output.find("{")
        json_end = output.rfind("}") + 1

        if json_start >= 0 and json_end > json_start:
            return json.loads(output[json_start:json_end])
    except json.JSONDecodeError:
        pass

    # Default if parsing fails
    return {
        "overall_status": "MANUAL_REVIEW",
        "issues": ["Could not parse legal check output"],
        "raw_output": result.output[:500],
    }


# =============================================================================
# BRIEF GENERATION
# =============================================================================

def generate_entity_brief(
    entity_name: str,
    entity_data: dict,
    mentions_data: dict,
    dry_run: bool = False,
) -> Optional[str]:
    """
    Generate analytical brief for an entity.

    Returns brief content or None on failure.
    """
    from invoke_claude import invoke_claude_raw

    # Gather all mentions and contexts
    mentions = mentions_data.get(entity_name, {}).get("mentions", [])

    sources_summary = []
    all_contexts = []
    for mention in mentions:
        sources_summary.append(f"- Document {mention['source_id']}: {mention.get('source_title', 'Unknown')}")
        all_contexts.extend(mention.get("contexts", []))

    task_description = f"""
Generate an analytical brief for the entity: {entity_name}

ENTITY DATA:
- Type: {entity_data.get('entity_type', 'unknown')}
- First seen: {entity_data.get('first_seen', 'unknown')}
- Source count: {entity_data.get('source_count', 0)}

SOURCES:
{chr(10).join(sources_summary[:20])}

CONTEXT MENTIONS:
{chr(10).join(all_contexts[:30])}

YOUR TASK:
Generate a comprehensive analytical brief following this structure:

1. SUMMARY (2-3 paragraphs)
   - Who/what is this entity
   - Why they are significant
   - Key facts established by sources

2. BACKGROUND
   - Known history and affiliations
   - Timeline of relevant events

3. SOURCE ANALYSIS
   - What the documents reveal
   - Key quotes and citations
   - Patterns identified

4. CONNECTIONS
   - Related entities (mention by name)
   - Nature of relationships

5. ASSESSMENT
   - Significance level
   - Information gaps
   - Areas requiring further investigation

OUTPUT FORMAT:
Use Markdown with proper headings.
Include source citations like [Source: doc_123]
Maintain neutral, factual tone.
"""

    if dry_run:
        return f"# {entity_name}\n\n[DRY RUN - Brief would be generated here]"

    # Use raw invocation without full SOP context to reduce prompt size
    result = invoke_claude_raw(task_description, timeout=120)

    if not result.success:
        logger.error(f"Brief generation failed for {entity_name}: {result.error}")
        return None

    return result.output


def generate_connection_brief(
    entity1: str,
    entity2: str,
    co_occurrence_data: dict,
    contexts_data: dict,
    dry_run: bool = False,
) -> Optional[str]:
    """
    Generate analytical brief for a connection between two entities.

    Returns brief content or None on failure.
    """
    from invoke_claude import invoke_claude_raw

    pair_key = f"{entity1.lower()}___{entity2.lower()}"
    if pair_key not in co_occurrence_data:
        # Try reversed order
        pair_key = f"{entity2.lower()}___{entity1.lower()}"

    co_occ = co_occurrence_data.get(pair_key, {})
    contexts = contexts_data.get(pair_key, {})

    context_snippets = contexts.get("context_snippets", [])
    relationship_summary = contexts.get("relationship_summary", {})

    task_description = f"""
Generate an analytical brief for the connection between: {entity1} and {entity2}

CONNECTION DATA:
- Co-mention count: {co_occ.get('co_mention_count', 0)}
- Sources: {len(co_occ.get('sources', []))}
- First documented: {co_occ.get('first_seen', 'unknown')}

RELATIONSHIP SIGNALS:
- Interaction verbs: {relationship_summary.get('interaction_verbs', [])}
- Relationship terms: {relationship_summary.get('relationship_terms', [])}
- Confidence: {relationship_summary.get('overall_confidence', 0):.2f}

CONTEXT SNIPPETS (showing up to 10):
{chr(10).join([f"[{s.get('source_id')}]: {s.get('text', '')[:300]}..." for s in context_snippets[:10]])}

YOUR TASK:
Generate an analytical brief documenting this connection:

1. CONNECTION SUMMARY
   - Nature of the relationship
   - How they are connected
   - Significance of the connection

2. EVIDENCE
   - Documented interactions
   - Source citations
   - Timeline of connection

3. CONTEXT
   - Circumstances of connection
   - Third parties involved
   - Locations/events

4. ANALYSIS
   - Strength of evidence
   - Gaps in documentation
   - Questions remaining

OUTPUT FORMAT:
Use Markdown with proper headings.
Include source citations like [Source: doc_123]
Focus on documented facts, not speculation.
"""

    if dry_run:
        return f"# Connection: {entity1} ↔ {entity2}\n\n[DRY RUN - Brief would be generated here]"

    # Use raw invocation without full SOP context to reduce prompt size
    result = invoke_claude_raw(task_description, timeout=120)

    if not result.success:
        logger.error(f"Connection brief failed for {entity1}-{entity2}: {result.error}")
        return None

    return result.output


# =============================================================================
# BRIEF OUTPUT
# =============================================================================

def write_brief_to_pending(
    brief_content: str,
    brief_type: str,  # "entity" or "connection"
    name: str,  # entity name or "entity1_entity2"
    legal_result: dict,
    reason: str,
) -> bool:
    """Write brief to pending_approval directory with metadata."""
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Build filename
    safe_name = re.sub(r'[^\w\-]', '_', name.lower())
    filename = f"{safe_name}.md"

    # Determine output directory
    if brief_type == "entity":
        output_dir = PENDING_DIR / "entities"
    else:
        output_dir = PENDING_DIR / "connections"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename

    # Build frontmatter
    frontmatter = f"""---
title: "{name}"
type: {brief_type}
generated: "{timestamp}"
legal_review: "{legal_result.get('overall_status', 'PENDING')}"
review_date: "{timestamp}"
reviewer: "legal-auditor-agent"
reason: "{reason}"
"""

    if legal_result.get("issues"):
        frontmatter += f"issues:\n"
        for issue in legal_result["issues"]:
            frontmatter += f'  - "{issue}"\n'

    frontmatter += "---\n\n"

    # Write file
    try:
        full_content = frontmatter + brief_content
        output_path.write_text(full_content, encoding="utf-8")
        logger.info(f"Brief written to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error writing brief: {e}")
        return False


def update_review_log(entries: List[Dict]) -> bool:
    """Update REVIEW_LOG.md with new entries."""
    log_path = PENDING_DIR / "REVIEW_LOG.md"

    try:
        # Load existing log
        existing = ""
        if log_path.exists():
            existing = log_path.read_text(encoding="utf-8")

        # Add new entries
        timestamp = datetime.utcnow().isoformat() + "Z"
        new_entries = f"\n## {timestamp}\n\n"

        for entry in entries:
            new_entries += f"- **{entry['type']}**: {entry['name']}\n"
            new_entries += f"  - Reason: {entry['reason']}\n"
            new_entries += f"  - Legal: {entry['legal_status']}\n"
            if entry.get('issues'):
                new_entries += f"  - Issues: {', '.join(entry['issues'])}\n"
            new_entries += "\n"

        # Write updated log
        if not existing:
            existing = "# Pending Approval Review Log\n\nAutomatically generated by Stage 3 Brief Generation.\n"

        log_path.write_text(existing + new_entries, encoding="utf-8")
        return True

    except Exception as e:
        logger.error(f"Error updating review log: {e}")
        return False


# =============================================================================
# MAIN PROCESSING
# =============================================================================

def should_generate_entity_brief(entity_name: str, entity_data: dict) -> Tuple[bool, str]:
    """Determine if entity brief should be generated/updated."""
    # Check if brief already exists
    safe_name = re.sub(r'[^\w\-]', '_', entity_name.lower())
    brief_path = BRIEFS_DIR / "entity" / f"analytical_brief_{safe_name}.md"

    if not brief_path.exists():
        return True, "New entity discovered"

    # Check if new sources exist
    # (In full implementation, compare sources in brief vs registry)
    if entity_data.get("source_count", 0) >= 2:
        return True, f"Entity has {entity_data.get('source_count')} sources"

    return False, "No update needed"


def should_generate_connection_brief(
    pair_key: str,
    co_occ_data: dict,
) -> Tuple[bool, str]:
    """Determine if connection brief should be generated/updated."""
    co_mention_count = co_occ_data.get("co_mention_count", 0)

    if co_mention_count < MIN_CO_MENTIONS_FOR_BRIEF:
        return False, f"Insufficient co-mentions ({co_mention_count} < {MIN_CO_MENTIONS_FOR_BRIEF})"

    # Check if brief exists
    entity1 = co_occ_data.get("entity1", "").lower().replace(" ", "_")
    entity2 = co_occ_data.get("entity2", "").lower().replace(" ", "_")
    filename = f"{entity1}_{entity2}.md"

    brief_path = BRIEFS_DIR / "connections" / filename
    if not brief_path.exists():
        return True, f"New connection discovered ({co_mention_count} co-mentions)"

    return True, f"Connection update ({co_mention_count} co-mentions)"


def process_brief_generation(dry_run: bool = False, limit: int = 10) -> dict:
    """
    Main brief generation process.

    Generates briefs for entities and connections that meet criteria.
    """
    logger.info("Starting Stage 3: Brief Generation")

    # Load indexes
    entity_registry = load_entity_registry()
    source_mentions = load_source_mentions()
    co_occurrence = load_co_occurrence()
    connection_contexts = load_connection_contexts()

    stats = {
        "entities_checked": 0,
        "entity_briefs_generated": 0,
        "connections_checked": 0,
        "connection_briefs_generated": 0,
        "legal_approved": 0,
        "legal_issues": 0,
    }

    review_log_entries = []

    # Process entities
    entities_dict = entity_registry.get("entities", entity_registry)
    total_entities = len(entities_dict)
    logger.info(f"Checking {total_entities} entities")
    entity_count = 0
    briefs_attempted = 0

    for entity_key, entity_data in entities_dict.items():
        if not isinstance(entity_data, dict):
            continue  # Skip metadata keys
        if entity_count >= limit:
            break

        entity_name = entity_data.get("canonical_name", entity_key)
        should_generate, reason = should_generate_entity_brief(entity_name, entity_data)

        stats["entities_checked"] += 1
        entity_count += 1

        if not should_generate:
            continue

        # Skip entities with no source mentions - can't generate brief without context
        # Try multiple lookup keys: canonical_name, name field, entity_key
        lookup_keys = [
            entity_name,  # canonical_name or entity_key
            entity_data.get("canonical_name", ""),
            entity_data.get("name", ""),
            entity_key,
        ]
        entity_mentions = []
        matched_key = None
        for key in lookup_keys:
            if key and key in source_mentions:
                mentions_data = source_mentions.get(key, {})
                if isinstance(mentions_data, dict):
                    entity_mentions = mentions_data.get("mentions", [])
                    if entity_mentions:
                        matched_key = key
                        break

        if not entity_mentions:
            logger.debug(f"Skipping {entity_name}: no source mentions (tried: {[k for k in lookup_keys if k]})")
            continue

        briefs_attempted += 1
        logger.info(f"[{briefs_attempted}/{limit}] [{entity_count}/{total_entities} checked] Generating brief for entity: {entity_name} ({len(entity_mentions)} mentions)")

        brief_content = generate_entity_brief(
            entity_name=entity_name,
            entity_data=entity_data,
            mentions_data=source_mentions,
            dry_run=dry_run,
        )

        if not brief_content:
            continue

        # Run legal check
        if dry_run:
            legal_result = {"overall_status": "DRY_RUN"}
        else:
            legal_result = run_legal_compliance_check(brief_content)

        # Write to pending
        if not dry_run:
            write_brief_to_pending(
                brief_content=brief_content,
                brief_type="entity",
                name=entity_name,
                legal_result=legal_result,
                reason=reason,
            )

        # Track results
        stats["entity_briefs_generated"] += 1
        if legal_result.get("overall_status") == "APPROVED":
            stats["legal_approved"] += 1
        else:
            stats["legal_issues"] += 1

        review_log_entries.append({
            "type": "entity",
            "name": entity_name,
            "reason": reason,
            "legal_status": legal_result.get("overall_status", "UNKNOWN"),
            "issues": legal_result.get("issues", []),
        })

        entity_count += 1
        time.sleep(2)

    # Process connections
    co_occ_dict = co_occurrence.get("connections", co_occurrence)
    logger.info(f"Checking {len(co_occ_dict)} connections")
    connection_count = 0

    for pair_key, co_occ_data in co_occ_dict.items():
        if not isinstance(co_occ_data, dict):
            continue  # Skip metadata keys
        if connection_count >= limit:
            break

        should_generate, reason = should_generate_connection_brief(pair_key, co_occ_data)

        stats["connections_checked"] += 1

        if not should_generate:
            continue

        entity1 = co_occ_data.get("entity1", "")
        entity2 = co_occ_data.get("entity2", "")

        logger.info(f"Generating brief for connection: {entity1} <-> {entity2}")

        brief_content = generate_connection_brief(
            entity1=entity1,
            entity2=entity2,
            co_occurrence_data=co_occurrence,
            contexts_data=connection_contexts,
            dry_run=dry_run,
        )

        if not brief_content:
            continue

        # Run legal check
        if dry_run:
            legal_result = {"overall_status": "DRY_RUN"}
        else:
            legal_result = run_legal_compliance_check(brief_content)

        # Write to pending
        connection_name = f"{entity1}_{entity2}"
        if not dry_run:
            write_brief_to_pending(
                brief_content=brief_content,
                brief_type="connection",
                name=connection_name,
                legal_result=legal_result,
                reason=reason,
            )

        # Track results
        stats["connection_briefs_generated"] += 1
        if legal_result.get("overall_status") == "APPROVED":
            stats["legal_approved"] += 1
        else:
            stats["legal_issues"] += 1

        review_log_entries.append({
            "type": "connection",
            "name": connection_name,
            "reason": reason,
            "legal_status": legal_result.get("overall_status", "UNKNOWN"),
            "issues": legal_result.get("issues", []),
        })

        connection_count += 1
        time.sleep(2)

    # Update review log
    if review_log_entries and not dry_run:
        update_review_log(review_log_entries)

    logger.info(f"Stage 3 complete: {stats}")
    return stats


# =============================================================================
# CLI
# =============================================================================

def main():
    """CLI interface for Stage 3 processing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Stage 3: Brief Generation - Create analytical products"
    )
    parser.add_argument("--entity", type=str,
                        help="Generate brief for specific entity")
    parser.add_argument("--connection", nargs=2, metavar=("ENTITY1", "ENTITY2"),
                        help="Generate brief for specific connection")
    parser.add_argument("--dry-run", action="store_true",
                        help="Dry run without generating briefs")
    parser.add_argument("--limit", type=int, default=10,
                        help="Maximum briefs to generate (default: 10)")
    parser.add_argument("--status", action="store_true",
                        help="Show pending approval status")

    args = parser.parse_args()

    print("=" * 60)
    print("The Continuum Report - Stage 3: Brief Generation")
    print("=" * 60)

    if args.status:
        pending_entities = list((PENDING_DIR / "entities").glob("*.md")) if (PENDING_DIR / "entities").exists() else []
        pending_connections = list((PENDING_DIR / "connections").glob("*.md")) if (PENDING_DIR / "connections").exists() else []
        print(f"Pending entity briefs: {len(pending_entities)}")
        print(f"Pending connection briefs: {len(pending_connections)}")
        return 0

    stats = process_brief_generation(dry_run=args.dry_run, limit=args.limit)
    print(f"\nProcessing complete:")
    print(f"  Entities checked: {stats['entities_checked']}")
    print(f"  Entity briefs generated: {stats['entity_briefs_generated']}")
    print(f"  Connections checked: {stats['connections_checked']}")
    print(f"  Connection briefs generated: {stats['connection_briefs_generated']}")
    print(f"  Legal approved: {stats['legal_approved']}")
    print(f"  Legal issues: {stats['legal_issues']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
