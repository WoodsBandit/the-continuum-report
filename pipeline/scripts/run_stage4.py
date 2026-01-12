"""
The Continuum Report - Stage 4: Publication

Publishes approved briefs to the website, updates data files,
and archives published content.

Trigger: Files detected in approved/
Output: Updated website/data/, website/briefs/, archive/published/

Usage:
    # Process all approved briefs
    python run_stage4.py

    # Dry run (show what would be published)
    python run_stage4.py --dry-run

    # Force republish specific brief
    python run_stage4.py --republish path/to/brief.md
"""

import json
import os
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from logging_config import get_logger

logger = get_logger("stage4_publication")


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(os.environ.get("CONTINUUM_BASE_DIR", "/mnt/user/continuum"))
APPROVED_DIR = BASE_DIR / "approved"
WEBSITE_DIR = BASE_DIR / "website"
ARCHIVE_DIR = BASE_DIR / "archive" / "published"
LOGS_DIR = BASE_DIR / "logs"

# Website paths
WEBSITE_DATA_DIR = WEBSITE_DIR / "data"
WEBSITE_BRIEFS_DIR = WEBSITE_DIR / "briefs"
WEBSITE_SOURCES_DIR = WEBSITE_DIR / "sources"

# Data files
ENTITIES_JSON = WEBSITE_DATA_DIR / "entities.json"
CONNECTIONS_JSON = WEBSITE_DATA_DIR / "connections.json"


# =============================================================================
# UTILITIES
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
            shutil.copy2(path, backup_path)

        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    except Exception as e:
        logger.error(f"Error saving {path}: {e}")
        return False


def parse_frontmatter(content: str) -> Dict:
    """Parse YAML frontmatter from markdown content."""
    frontmatter = {}

    if content.startswith("---"):
        end_idx = content.find("---", 3)
        if end_idx > 0:
            fm_content = content[3:end_idx].strip()
            for line in fm_content.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"')
                    frontmatter[key] = value

    return frontmatter


def remove_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from markdown content."""
    if content.startswith("---"):
        end_idx = content.find("---", 3)
        if end_idx > 0:
            return content[end_idx + 3:].strip()
    return content


def sanitize_filename(name: str) -> str:
    """Convert name to safe filename."""
    return re.sub(r'[^\w\-]', '_', name.lower())


# =============================================================================
# VALIDATION
# =============================================================================

def validate_brief_metadata(filepath: Path) -> Dict:
    """Validate brief has required metadata for publication."""
    try:
        content = filepath.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)

        errors = []

        # Required fields
        if not frontmatter.get("title"):
            errors.append("Missing title")
        if not frontmatter.get("type"):
            errors.append("Missing type (entity/connection)")
        if not frontmatter.get("legal_review"):
            errors.append("Missing legal_review status")

        # Check legal approval
        legal_status = frontmatter.get("legal_review", "")
        if legal_status not in ["AUTO-APPROVED", "APPROVED", "MANUAL_APPROVED"]:
            if legal_status == "ISSUES_FOUND":
                errors.append(f"Legal issues not resolved: {frontmatter.get('issues', 'unspecified')}")
            else:
                errors.append(f"Unknown legal status: {legal_status}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "frontmatter": frontmatter,
            "content": content,
        }

    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Error reading file: {e}"],
            "frontmatter": {},
            "content": "",
        }


# =============================================================================
# PUBLICATION
# =============================================================================

def publish_entity_brief(
    filepath: Path,
    frontmatter: Dict,
    content: str,
    dry_run: bool = False,
) -> bool:
    """Publish entity brief to website."""
    entity_name = frontmatter.get("title", "unknown")
    safe_name = sanitize_filename(entity_name)

    # Destination path
    dest_path = WEBSITE_BRIEFS_DIR / "entity" / f"analytical_brief_{safe_name}.md"

    logger.info(f"Publishing entity brief: {entity_name}")

    if dry_run:
        logger.info(f"[DRY RUN] Would copy to {dest_path}")
        return True

    try:
        # Create directory
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy brief
        brief_content = remove_frontmatter(content)
        dest_path.write_text(brief_content, encoding="utf-8")

        # Update entities.json
        entities_data = load_json_file(ENTITIES_JSON, {"entities": []})

        # Find or create entity entry
        entity_entry = None
        for entry in entities_data.get("entities", []):
            if entry.get("name", "").lower() == entity_name.lower():
                entity_entry = entry
                break

        if not entity_entry:
            entity_entry = {"name": entity_name}
            entities_data.setdefault("entities", []).append(entity_entry)

        # Update entry
        entity_entry["brief_path"] = f"briefs/entity/analytical_brief_{safe_name}.md"
        entity_entry["entity_type"] = frontmatter.get("entity_type", "unknown")
        entity_entry["last_updated"] = datetime.utcnow().isoformat() + "Z"
        entity_entry["has_brief"] = True

        save_json_file(ENTITIES_JSON, entities_data)

        logger.info(f"Entity brief published: {dest_path}")
        return True

    except Exception as e:
        logger.error(f"Error publishing entity brief: {e}")
        return False


def publish_connection_brief(
    filepath: Path,
    frontmatter: Dict,
    content: str,
    dry_run: bool = False,
) -> bool:
    """Publish connection brief to website."""
    title = frontmatter.get("title", "unknown")

    # Parse entity names from title (format: "Entity1_Entity2")
    parts = title.split("_")
    if len(parts) >= 2:
        entity1 = parts[0].replace("_", " ").title()
        entity2 = "_".join(parts[1:]).replace("_", " ").title()
    else:
        entity1 = title
        entity2 = "Unknown"

    safe_name = sanitize_filename(title)
    dest_path = WEBSITE_BRIEFS_DIR / "connections" / f"{safe_name}.md"

    logger.info(f"Publishing connection brief: {entity1} <-> {entity2}")

    if dry_run:
        logger.info(f"[DRY RUN] Would copy to {dest_path}")
        return True

    try:
        # Create directory
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy brief
        brief_content = remove_frontmatter(content)
        dest_path.write_text(brief_content, encoding="utf-8")

        # Update connections.json
        connections_data = load_json_file(CONNECTIONS_JSON, {"connections": []})

        # Find or create connection entry
        conn_entry = None
        for entry in connections_data.get("connections", []):
            if (entry.get("entity1", "").lower() == entity1.lower() and
                entry.get("entity2", "").lower() == entity2.lower()):
                conn_entry = entry
                break
            if (entry.get("entity1", "").lower() == entity2.lower() and
                entry.get("entity2", "").lower() == entity1.lower()):
                conn_entry = entry
                break

        if not conn_entry:
            conn_entry = {"entity1": entity1, "entity2": entity2}
            connections_data.setdefault("connections", []).append(conn_entry)

        # Update entry
        conn_entry["brief_path"] = f"briefs/connections/{safe_name}.md"
        conn_entry["last_updated"] = datetime.utcnow().isoformat() + "Z"
        conn_entry["has_brief"] = True

        save_json_file(CONNECTIONS_JSON, connections_data)

        logger.info(f"Connection brief published: {dest_path}")
        return True

    except Exception as e:
        logger.error(f"Error publishing connection brief: {e}")
        return False


def archive_published_brief(
    filepath: Path,
    brief_type: str,
    dry_run: bool = False,
) -> bool:
    """Move published brief to archive."""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    archive_subdir = ARCHIVE_DIR / brief_type

    if dry_run:
        logger.info(f"[DRY RUN] Would archive {filepath}")
        return True

    try:
        archive_subdir.mkdir(parents=True, exist_ok=True)

        # Add timestamp to filename
        new_name = f"{timestamp}_{filepath.name}"
        dest_path = archive_subdir / new_name

        shutil.move(str(filepath), str(dest_path))
        logger.info(f"Archived: {dest_path}")
        return True

    except Exception as e:
        logger.error(f"Error archiving brief: {e}")
        return False


# =============================================================================
# MAIN PROCESSING
# =============================================================================

def get_approved_briefs() -> Dict[str, List[Path]]:
    """Get all briefs in approved directories."""
    briefs = {
        "entities": [],
        "connections": [],
    }

    entities_dir = APPROVED_DIR / "entities"
    if entities_dir.exists():
        briefs["entities"] = list(entities_dir.glob("*.md"))

    connections_dir = APPROVED_DIR / "connections"
    if connections_dir.exists():
        briefs["connections"] = list(connections_dir.glob("*.md"))

    return briefs


def process_publication(dry_run: bool = False) -> dict:
    """
    Main publication process.

    Publishes all approved briefs to website.
    """
    logger.info("Starting Stage 4: Publication")

    approved_briefs = get_approved_briefs()

    stats = {
        "entities_found": len(approved_briefs["entities"]),
        "connections_found": len(approved_briefs["connections"]),
        "entities_published": 0,
        "connections_published": 0,
        "validation_errors": 0,
        "publication_errors": 0,
    }

    if stats["entities_found"] == 0 and stats["connections_found"] == 0:
        logger.info("No approved briefs to publish")
        return stats

    # Process entity briefs
    for filepath in approved_briefs["entities"]:
        logger.info(f"Processing entity brief: {filepath.name}")

        validation = validate_brief_metadata(filepath)
        if not validation["valid"]:
            logger.warning(f"Validation failed for {filepath}: {validation['errors']}")
            stats["validation_errors"] += 1
            continue

        success = publish_entity_brief(
            filepath=filepath,
            frontmatter=validation["frontmatter"],
            content=validation["content"],
            dry_run=dry_run,
        )

        if success:
            stats["entities_published"] += 1
            archive_published_brief(filepath, "entities", dry_run=dry_run)
        else:
            stats["publication_errors"] += 1

        time.sleep(0.5)

    # Process connection briefs
    for filepath in approved_briefs["connections"]:
        logger.info(f"Processing connection brief: {filepath.name}")

        validation = validate_brief_metadata(filepath)
        if not validation["valid"]:
            logger.warning(f"Validation failed for {filepath}: {validation['errors']}")
            stats["validation_errors"] += 1
            continue

        success = publish_connection_brief(
            filepath=filepath,
            frontmatter=validation["frontmatter"],
            content=validation["content"],
            dry_run=dry_run,
        )

        if success:
            stats["connections_published"] += 1
            archive_published_brief(filepath, "connections", dry_run=dry_run)
        else:
            stats["publication_errors"] += 1

        time.sleep(0.5)

    logger.info(f"Stage 4 complete: {stats}")
    return stats


def publish_single_brief(filepath: Path, dry_run: bool = False) -> bool:
    """Publish a single brief by path."""
    if not filepath.exists():
        logger.error(f"File not found: {filepath}")
        return False

    validation = validate_brief_metadata(filepath)
    if not validation["valid"]:
        logger.error(f"Validation failed: {validation['errors']}")
        return False

    brief_type = validation["frontmatter"].get("type", "")

    if brief_type == "entity":
        return publish_entity_brief(
            filepath=filepath,
            frontmatter=validation["frontmatter"],
            content=validation["content"],
            dry_run=dry_run,
        )
    elif brief_type == "connection":
        return publish_connection_brief(
            filepath=filepath,
            frontmatter=validation["frontmatter"],
            content=validation["content"],
            dry_run=dry_run,
        )
    else:
        logger.error(f"Unknown brief type: {brief_type}")
        return False


# =============================================================================
# LOGGING
# =============================================================================

def log_publication_event(event_type: str, data: dict) -> None:
    """Log Stage 4 events."""
    try:
        log_file = LOGS_DIR / "stage4_publication.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "stage": "stage4_publication",
            "event_type": event_type,
            **data,
        }

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    except Exception as e:
        logger.error(f"Error logging publication event: {e}")


# =============================================================================
# CLI
# =============================================================================

def main():
    """CLI interface for Stage 4 processing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Stage 4: Publication - Publish approved briefs to website"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Dry run without publishing")
    parser.add_argument("--republish", type=str,
                        help="Force republish specific brief by path")
    parser.add_argument("--status", action="store_true",
                        help="Show publication status")

    args = parser.parse_args()

    print("=" * 60)
    print("The Continuum Report - Stage 4: Publication")
    print("=" * 60)

    if args.status:
        approved = get_approved_briefs()
        print(f"Approved entities pending: {len(approved['entities'])}")
        print(f"Approved connections pending: {len(approved['connections'])}")

        # Count published
        published_entities = len(list((WEBSITE_BRIEFS_DIR / "entity").glob("*.md"))) if (WEBSITE_BRIEFS_DIR / "entity").exists() else 0
        published_connections = len(list((WEBSITE_BRIEFS_DIR / "connections").glob("*.md"))) if (WEBSITE_BRIEFS_DIR / "connections").exists() else 0
        print(f"Published entity briefs: {published_entities}")
        print(f"Published connection briefs: {published_connections}")
        return 0

    if args.republish:
        filepath = Path(args.republish)
        success = publish_single_brief(filepath, dry_run=args.dry_run)
        return 0 if success else 1

    stats = process_publication(dry_run=args.dry_run)
    print(f"\nPublication complete:")
    print(f"  Entities found: {stats['entities_found']}")
    print(f"  Entities published: {stats['entities_published']}")
    print(f"  Connections found: {stats['connections_found']}")
    print(f"  Connections published: {stats['connections_published']}")
    print(f"  Validation errors: {stats['validation_errors']}")
    print(f"  Publication errors: {stats['publication_errors']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
