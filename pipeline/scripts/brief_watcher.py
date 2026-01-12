#!/usr/bin/env python3
"""
Simple file watcher - no external dependencies
Version 2.0 - Refactored with Shared Library

Checks for new .md files every 5 seconds

Changes in v2.0:
- Uses centralized configuration (lib.config)
- Structured logging with structlog (lib.logging_config)
- No hardcoded paths - uses environment variables
- Path handling with pathlib
"""

import time
import subprocess
from pathlib import Path
from datetime import datetime

# Import shared library
from lib import settings, get_logger

# Initialize logger
logger = get_logger(__name__)

BRIEFS_DIR = settings.briefs_dir
LOG_FILE = settings.logs_dir / "watcher.log"
SEEN_FILES = set()

# Ensure directories exist
settings.ensure_directories()
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def trigger_rebuild(new_file: Path):
    filename = new_file.name
    logger.info("Triggering rebuild for new brief", filename=filename)

    prompt = f"""New analytical brief added: {new_file}

TASK: Update the knowledge graph.

1. Read the new brief at {new_file}
2. Extract all entities (people, organizations, cases)
3. Scan ALL briefs in {BRIEFS_DIR} for cross-references
4. Update {settings.data_dir}/entities.json
5. Update {settings.data_dir}/connections.json
6. Update {settings.data_dir}/manifest.json with timestamp
"""
    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=600
        )
        logger.info("Claude Code completed", exit_code=result.returncode)
    except subprocess.TimeoutExpired:
        logger.error("Claude Code timed out")
    except Exception as e:
        logger.error("Error triggering Claude Code", error=str(e))

def get_md_files():
    if not BRIEFS_DIR.exists():
        return set()
    return {f.name for f in BRIEFS_DIR.glob("*.md")}

def main():
    global SEEN_FILES

    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    logger.info("Brief watcher started", briefs_dir=str(BRIEFS_DIR), check_interval=5)
    print("Starting brief watcher (pure Python)...")
    print(f"Watching: {BRIEFS_DIR}")
    print("Checking every 5 seconds...")

    # Initialize with existing files
    SEEN_FILES = get_md_files()
    logger.info("Initial scan complete", existing_briefs=len(SEEN_FILES))
    print(f"Found {len(SEEN_FILES)} existing briefs")

    while True:
        try:
            current_files = get_md_files()
            new_files = current_files - SEEN_FILES

            for new_file in new_files:
                full_path = BRIEFS_DIR / new_file
                logger.info("New brief detected", filename=new_file)
                print(f"New brief detected: {new_file}")
                time.sleep(2)  # Wait for file to finish writing
                trigger_rebuild(full_path)

            SEEN_FILES = current_files
            time.sleep(5)

        except KeyboardInterrupt:
            logger.info("Watcher stopped by user")
            print("Watcher stopped by user")
            break
        except Exception as e:
            logger.error("Error in main loop", error=str(e))
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
