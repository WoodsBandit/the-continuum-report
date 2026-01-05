"""
The Continuum Report - Pipeline File Watcher

Watches for file changes that trigger pipeline stages:
- entity_registry.json changes → Stage 2
- connection_contexts.json changes → Stage 3
- approved/ directory changes → Stage 4

Uses watchdog library for efficient file system monitoring.

Usage:
    # Start all watchers
    python pipeline_watcher.py

    # Watch specific index
    python pipeline_watcher.py --watch entity_registry

    # Dry run mode
    python pipeline_watcher.py --dry-run
"""

import json
import os
import sys
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Dict

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from logging_config import get_logger

logger = get_logger("pipeline_watcher")

# Try to import watchdog, provide fallback if not available
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    logger.warning("watchdog library not installed. Using polling fallback.")


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(os.environ.get("CONTINUUM_BASE_DIR", "/mnt/user/continuum"))
INDEXES_DIR = BASE_DIR / "indexes"
APPROVED_DIR = BASE_DIR / "approved"
LOGS_DIR = BASE_DIR / "logs"

# Files to watch and their triggers
WATCH_TARGETS = {
    "entity_registry": {
        "path": INDEXES_DIR / "entity_registry.json",
        "trigger_stage": 2,
        "debounce_seconds": 30,
    },
    "connection_contexts": {
        "path": INDEXES_DIR / "connection_contexts.json",
        "trigger_stage": 3,
        "debounce_seconds": 30,
    },
    "approved_entities": {
        "path": APPROVED_DIR / "entities",
        "trigger_stage": 4,
        "debounce_seconds": 10,
        "is_directory": True,
    },
    "approved_connections": {
        "path": APPROVED_DIR / "connections",
        "trigger_stage": 4,
        "debounce_seconds": 10,
        "is_directory": True,
    },
}

# Polling interval for fallback mode (seconds)
POLLING_INTERVAL = 30


# =============================================================================
# EVENT HANDLERS
# =============================================================================

class StageTriggeredError(Exception):
    """Raised when a stage fails to trigger."""
    pass


def trigger_stage(stage_number: int, context: dict, dry_run: bool = False) -> bool:
    """
    Trigger a pipeline stage.

    Args:
        stage_number: Stage to trigger (2, 3, or 4)
        context: Context about what triggered the stage
        dry_run: If True, don't actually run the stage

    Returns:
        True if stage was triggered successfully
    """
    logger.info(f"Triggering Stage {stage_number} with context: {context}")

    if dry_run:
        logger.info(f"[DRY RUN] Would trigger Stage {stage_number}")
        return True

    try:
        if stage_number == 2:
            from run_stage2 import process_context_extraction
            result = process_context_extraction()
            logger.info(f"Stage 2 result: {result}")
            return True

        elif stage_number == 3:
            from run_stage3 import process_brief_generation
            result = process_brief_generation(limit=5)  # Limit to avoid long runs
            logger.info(f"Stage 3 result: {result}")
            return True

        elif stage_number == 4:
            from run_stage4 import process_publication
            result = process_publication()
            logger.info(f"Stage 4 result: {result}")
            return True

        else:
            logger.error(f"Unknown stage number: {stage_number}")
            return False

    except ImportError as e:
        logger.error(f"Failed to import stage {stage_number} module: {e}")
        return False
    except Exception as e:
        logger.error(f"Error running stage {stage_number}: {e}")
        return False


class PipelineEventHandler(FileSystemEventHandler):
    """Watchdog event handler for pipeline triggers."""

    def __init__(
        self,
        target_name: str,
        trigger_stage: int,
        debounce_seconds: float = 30,
        dry_run: bool = False,
    ):
        super().__init__()
        self.target_name = target_name
        self.trigger_stage = trigger_stage
        self.debounce_seconds = debounce_seconds
        self.dry_run = dry_run
        self.last_trigger = 0
        self._lock = threading.Lock()

    def _should_trigger(self) -> bool:
        """Check if enough time has passed since last trigger."""
        with self._lock:
            now = time.time()
            if now - self.last_trigger >= self.debounce_seconds:
                self.last_trigger = now
                return True
            return False

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        if self._should_trigger():
            logger.info(f"Change detected: {event.src_path}")
            self._trigger_stage(event.src_path)

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        if self._should_trigger():
            logger.info(f"New file detected: {event.src_path}")
            self._trigger_stage(event.src_path)

    def _trigger_stage(self, src_path: str):
        """Trigger the associated pipeline stage."""
        context = {
            "target": self.target_name,
            "changed_file": src_path,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        # Run in separate thread to avoid blocking watcher
        thread = threading.Thread(
            target=trigger_stage,
            args=(self.trigger_stage, context, self.dry_run),
            daemon=True,
        )
        thread.start()


# =============================================================================
# POLLING FALLBACK
# =============================================================================

class PollingWatcher:
    """Fallback watcher using file modification time polling."""

    def __init__(
        self,
        target_name: str,
        path: Path,
        trigger_stage: int,
        debounce_seconds: float = 30,
        is_directory: bool = False,
        dry_run: bool = False,
    ):
        self.target_name = target_name
        self.path = path
        self.trigger_stage = trigger_stage
        self.debounce_seconds = debounce_seconds
        self.is_directory = is_directory
        self.dry_run = dry_run

        self.last_mtime = self._get_mtime()
        self.last_file_count = self._get_file_count() if is_directory else 0
        self.last_trigger = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def _get_mtime(self) -> float:
        """Get modification time of path."""
        try:
            if self.path.exists():
                return self.path.stat().st_mtime
        except Exception:
            pass
        return 0

    def _get_file_count(self) -> int:
        """Get file count in directory."""
        try:
            if self.path.exists() and self.path.is_dir():
                return len(list(self.path.glob("*.md")))
        except Exception:
            pass
        return 0

    def _check_for_changes(self) -> bool:
        """Check if target has changed."""
        if self.is_directory:
            current_count = self._get_file_count()
            if current_count > self.last_file_count:
                self.last_file_count = current_count
                return True
            self.last_file_count = current_count
            return False
        else:
            current_mtime = self._get_mtime()
            if current_mtime > self.last_mtime:
                self.last_mtime = current_mtime
                return True
            return False

    def _poll_loop(self):
        """Main polling loop."""
        logger.info(f"Starting polling watcher for {self.target_name}")

        while self._running:
            try:
                if self._check_for_changes():
                    now = time.time()
                    if now - self.last_trigger >= self.debounce_seconds:
                        self.last_trigger = now
                        logger.info(f"Change detected in {self.target_name}")

                        context = {
                            "target": self.target_name,
                            "path": str(self.path),
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                        }

                        trigger_stage(self.trigger_stage, context, self.dry_run)

            except Exception as e:
                logger.error(f"Error in polling loop for {self.target_name}: {e}")

            time.sleep(POLLING_INTERVAL)

    def start(self):
        """Start the polling watcher."""
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the polling watcher."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)


# =============================================================================
# WATCHER MANAGER
# =============================================================================

class WatcherManager:
    """Manages all file watchers for the pipeline."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.observers = []
        self.polling_watchers = []
        self._running = False

    def add_watchdog_watcher(
        self,
        target_name: str,
        path: Path,
        trigger_stage: int,
        debounce_seconds: float,
        is_directory: bool = False,
    ):
        """Add a watchdog-based watcher."""
        if not WATCHDOG_AVAILABLE:
            logger.warning("watchdog not available, using polling instead")
            self.add_polling_watcher(
                target_name, path, trigger_stage, debounce_seconds, is_directory
            )
            return

        handler = PipelineEventHandler(
            target_name=target_name,
            trigger_stage=trigger_stage,
            debounce_seconds=debounce_seconds,
            dry_run=self.dry_run,
        )

        observer = Observer()

        if is_directory:
            watch_path = str(path)
        else:
            watch_path = str(path.parent)

        observer.schedule(handler, watch_path, recursive=False)
        self.observers.append((target_name, observer))

        logger.info(f"Added watchdog watcher for {target_name}: {path}")

    def add_polling_watcher(
        self,
        target_name: str,
        path: Path,
        trigger_stage: int,
        debounce_seconds: float,
        is_directory: bool = False,
    ):
        """Add a polling-based watcher."""
        watcher = PollingWatcher(
            target_name=target_name,
            path=path,
            trigger_stage=trigger_stage,
            debounce_seconds=debounce_seconds,
            is_directory=is_directory,
            dry_run=self.dry_run,
        )
        self.polling_watchers.append((target_name, watcher))

        logger.info(f"Added polling watcher for {target_name}: {path}")

    def start_all(self):
        """Start all watchers."""
        self._running = True

        # Start watchdog observers
        for name, observer in self.observers:
            observer.start()
            logger.info(f"Started watchdog observer for {name}")

        # Start polling watchers
        for name, watcher in self.polling_watchers:
            watcher.start()
            logger.info(f"Started polling watcher for {name}")

    def stop_all(self):
        """Stop all watchers."""
        self._running = False

        # Stop watchdog observers
        for name, observer in self.observers:
            observer.stop()
            observer.join()
            logger.info(f"Stopped watchdog observer for {name}")

        # Stop polling watchers
        for name, watcher in self.polling_watchers:
            watcher.stop()
            logger.info(f"Stopped polling watcher for {name}")

    def wait(self):
        """Wait for all watchers (blocking)."""
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            self.stop_all()


# =============================================================================
# MAIN
# =============================================================================

def create_watchers(dry_run: bool = False, targets: Optional[list] = None) -> WatcherManager:
    """Create watcher manager with configured watchers."""
    manager = WatcherManager(dry_run=dry_run)

    for target_name, config in WATCH_TARGETS.items():
        if targets and target_name not in targets:
            continue

        path = config["path"]
        is_directory = config.get("is_directory", False)

        # Ensure directory exists
        if is_directory:
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)

        # Use watchdog for files, polling for network directories
        if is_directory or str(path).startswith("//"):
            # Network paths work better with polling
            manager.add_polling_watcher(
                target_name=target_name,
                path=path,
                trigger_stage=config["trigger_stage"],
                debounce_seconds=config["debounce_seconds"],
                is_directory=is_directory,
            )
        else:
            manager.add_watchdog_watcher(
                target_name=target_name,
                path=path,
                trigger_stage=config["trigger_stage"],
                debounce_seconds=config["debounce_seconds"],
                is_directory=is_directory,
            )

    return manager


def main():
    """CLI interface for pipeline watcher."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Pipeline file watcher - triggers stages on file changes"
    )
    parser.add_argument("--watch", type=str, choices=list(WATCH_TARGETS.keys()),
                        help="Watch specific target only")
    parser.add_argument("--dry-run", action="store_true",
                        help="Dry run mode (don't trigger stages)")
    parser.add_argument("--status", action="store_true",
                        help="Show current file states and exit")

    args = parser.parse_args()

    print("=" * 60)
    print("The Continuum Report - Pipeline File Watcher")
    print("=" * 60)

    if args.status:
        print("\nWatch targets:")
        for name, config in WATCH_TARGETS.items():
            path = config["path"]
            exists = path.exists()
            mtime = path.stat().st_mtime if exists else 0
            mtime_str = datetime.fromtimestamp(mtime).isoformat() if mtime else "N/A"

            print(f"\n  {name}:")
            print(f"    Path: {path}")
            print(f"    Exists: {exists}")
            print(f"    Modified: {mtime_str}")
            print(f"    Triggers: Stage {config['trigger_stage']}")

        print(f"\nWatchdog available: {WATCHDOG_AVAILABLE}")
        return 0

    targets = [args.watch] if args.watch else None
    manager = create_watchers(dry_run=args.dry_run, targets=targets)

    print(f"\nWatching for changes...")
    print(f"Dry run: {args.dry_run}")
    print(f"Watchdog: {WATCHDOG_AVAILABLE}")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)

    manager.start_all()
    manager.wait()

    return 0


if __name__ == "__main__":
    sys.exit(main())
