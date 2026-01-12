"""
The Continuum Report - Master Pipeline Daemon

Single command to start the entire autonomous pipeline:
- Webhook listener for Paperless integration
- File watchers for index changes
- Automatic stage triggering

Usage:
    # Start the full pipeline
    python pipeline_daemon.py

    # Start with dry run (no actual processing)
    python pipeline_daemon.py --dry-run

    # Start specific components only
    python pipeline_daemon.py --webhook-only
    python pipeline_daemon.py --watchers-only

    # Show status
    python pipeline_daemon.py --status
"""

import json
import os
import signal
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from logging_config import get_logger

logger = get_logger("pipeline_daemon")


# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(os.environ.get("CONTINUUM_BASE_DIR", "/mnt/user/continuum"))
LOGS_DIR = BASE_DIR / "logs"
INDEXES_DIR = BASE_DIR / "indexes"

# Daemon configuration
WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.environ.get("WEBHOOK_PORT", "5000"))

# Status file for daemon state
DAEMON_STATUS_FILE = LOGS_DIR / "daemon_status.json"


# =============================================================================
# STATUS MANAGEMENT
# =============================================================================

def write_daemon_status(status: dict) -> None:
    """Write daemon status to file."""
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        status["updated_at"] = datetime.utcnow().isoformat() + "Z"
        DAEMON_STATUS_FILE.write_text(json.dumps(status, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Error writing daemon status: {e}")


def read_daemon_status() -> dict:
    """Read daemon status from file."""
    try:
        if DAEMON_STATUS_FILE.exists():
            return json.loads(DAEMON_STATUS_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error(f"Error reading daemon status: {e}")
    return {}


def get_pipeline_status() -> dict:
    """Get comprehensive pipeline status."""
    status = {
        "daemon": read_daemon_status(),
        "indexes": {},
        "queues": {},
        "pending_approval": {},
    }

    # Check index files
    index_files = [
        "entity_registry.json",
        "source_mentions.json",
        "co_occurrence.json",
        "connection_contexts.json",
        "processed_sources.json",
        "ingestion_queue.json",
    ]

    for filename in index_files:
        path = INDEXES_DIR / filename
        if path.exists():
            stat = path.stat()
            status["indexes"][filename] = {
                "exists": True,
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            }
        else:
            status["indexes"][filename] = {"exists": False}

    # Check ingestion queue
    queue_path = INDEXES_DIR / "ingestion_queue.json"
    if queue_path.exists():
        try:
            queue = json.loads(queue_path.read_text(encoding="utf-8"))
            pending = sum(1 for item in queue if item.get("status") == "pending")
            processing = sum(1 for item in queue if item.get("status") == "processing")
            completed = sum(1 for item in queue if item.get("status") == "completed")
            failed = sum(1 for item in queue if item.get("status") == "failed")
            status["queues"]["ingestion"] = {
                "pending": pending,
                "processing": processing,
                "completed": completed,
                "failed": failed,
                "total": len(queue),
            }
        except Exception:
            pass

    # Check pending approval
    pending_dir = BASE_DIR / "pending_approval"
    for subdir in ["entities", "connections"]:
        subpath = pending_dir / subdir
        if subpath.exists():
            files = list(subpath.glob("*.md"))
            status["pending_approval"][subdir] = len(files)
        else:
            status["pending_approval"][subdir] = 0

    return status


# =============================================================================
# COMPONENT MANAGERS
# =============================================================================

class WebhookManager:
    """Manages the webhook listener server."""

    def __init__(self, host: str = WEBHOOK_HOST, port: int = WEBHOOK_PORT):
        self.host = host
        self.port = port
        self._thread: Optional[threading.Thread] = None
        self._running = False

    def start(self):
        """Start the webhook server in a thread."""
        from webhook_listener import app

        def run_server():
            # Use werkzeug server directly for thread safety
            from werkzeug.serving import make_server
            self.server = make_server(self.host, self.port, app, threaded=True)
            logger.info(f"Webhook server starting on {self.host}:{self.port}")
            self._running = True
            self.server.serve_forever()

        self._thread = threading.Thread(target=run_server, daemon=True)
        self._thread.start()
        logger.info("Webhook manager started")

    def stop(self):
        """Stop the webhook server."""
        self._running = False
        if hasattr(self, 'server'):
            self.server.shutdown()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Webhook manager stopped")

    @property
    def is_running(self) -> bool:
        return self._running


class WatcherManager:
    """Manages file watchers."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self._watcher_manager = None
        self._running = False

    def start(self):
        """Start file watchers."""
        from pipeline_watcher import create_watchers

        self._watcher_manager = create_watchers(dry_run=self.dry_run)
        self._watcher_manager.start_all()
        self._running = True
        logger.info("Watcher manager started")

    def stop(self):
        """Stop file watchers."""
        if self._watcher_manager:
            self._watcher_manager.stop_all()
        self._running = False
        logger.info("Watcher manager stopped")

    @property
    def is_running(self) -> bool:
        return self._running


# =============================================================================
# MAIN DAEMON
# =============================================================================

class PipelineDaemon:
    """Master daemon that orchestrates all pipeline components."""

    def __init__(
        self,
        enable_webhook: bool = True,
        enable_watchers: bool = True,
        dry_run: bool = False,
        webhook_host: str = WEBHOOK_HOST,
        webhook_port: int = WEBHOOK_PORT,
    ):
        self.enable_webhook = enable_webhook
        self.enable_watchers = enable_watchers
        self.dry_run = dry_run

        self.webhook_manager = WebhookManager(host=webhook_host, port=webhook_port) if enable_webhook else None
        self.watcher_manager = WatcherManager(dry_run=dry_run) if enable_watchers else None

        self._running = False
        self._shutdown_event = threading.Event()

    def start(self):
        """Start all enabled components."""
        logger.info("=" * 60)
        logger.info("THE CONTINUUM REPORT - PIPELINE DAEMON")
        logger.info("=" * 60)
        logger.info(f"Dry run: {self.dry_run}")
        logger.info(f"Webhook enabled: {self.enable_webhook}")
        logger.info(f"Watchers enabled: {self.enable_watchers}")
        logger.info("=" * 60)

        self._running = True

        # Update status
        write_daemon_status({
            "status": "starting",
            "pid": os.getpid(),
            "started_at": datetime.utcnow().isoformat() + "Z",
            "dry_run": self.dry_run,
            "components": {
                "webhook": self.enable_webhook,
                "watchers": self.enable_watchers,
            },
        })

        # Start components
        if self.webhook_manager:
            self.webhook_manager.start()
            time.sleep(1)  # Give server time to start

        if self.watcher_manager:
            self.watcher_manager.start()

        # Update status
        write_daemon_status({
            "status": "running",
            "pid": os.getpid(),
            "started_at": datetime.utcnow().isoformat() + "Z",
            "dry_run": self.dry_run,
            "components": {
                "webhook": self.webhook_manager.is_running if self.webhook_manager else False,
                "watchers": self.watcher_manager.is_running if self.watcher_manager else False,
            },
        })

        logger.info("Pipeline daemon started successfully")
        self._print_endpoints()

    def _print_endpoints(self):
        """Print available endpoints."""
        print("\n" + "=" * 60)
        print("PIPELINE DAEMON RUNNING")
        print("=" * 60)

        if self.webhook_manager and self.webhook_manager.is_running:
            print(f"\nWebhook Endpoints:")
            print(f"  POST http://{WEBHOOK_HOST}:{WEBHOOK_PORT}/api/continuum/ingest")
            print(f"  GET  http://{WEBHOOK_HOST}:{WEBHOOK_PORT}/api/continuum/status")
            print(f"  GET  http://{WEBHOOK_HOST}:{WEBHOOK_PORT}/api/continuum/queue")

        if self.watcher_manager and self.watcher_manager.is_running:
            print(f"\nFile Watchers Active:")
            print(f"  - entity_registry.json → Stage 2")
            print(f"  - connection_contexts.json → Stage 3")
            print(f"  - approved/entities/ → Stage 4")
            print(f"  - approved/connections/ → Stage 4")

        print("\n" + "=" * 60)
        print("Press Ctrl+C to stop")
        print("=" * 60 + "\n")

    def stop(self):
        """Stop all components."""
        logger.info("Stopping pipeline daemon...")
        self._running = False

        if self.watcher_manager:
            self.watcher_manager.stop()

        if self.webhook_manager:
            self.webhook_manager.stop()

        write_daemon_status({
            "status": "stopped",
            "stopped_at": datetime.utcnow().isoformat() + "Z",
        })

        logger.info("Pipeline daemon stopped")

    def wait(self):
        """Wait for shutdown signal."""
        try:
            while self._running and not self._shutdown_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        finally:
            self.stop()

    def handle_signal(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}")
        self._shutdown_event.set()


# =============================================================================
# HEALTH CHECK
# =============================================================================

def run_health_check() -> dict:
    """Run health check on pipeline components."""
    results = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": {},
        "overall": "healthy",
    }

    # Check indexes directory
    results["checks"]["indexes_dir"] = {
        "status": "ok" if INDEXES_DIR.exists() else "error",
        "path": str(INDEXES_DIR),
    }

    # Check Paperless connection
    try:
        from lib.config import settings
        from lib.paperless_client import PaperlessClient

        client = PaperlessClient(
            base_url=settings.paperless_url,
            token=settings.paperless_token,
        )
        docs = client.get_documents(page_size=1)
        results["checks"]["paperless"] = {
            "status": "ok",
            "url": settings.paperless_url,
        }
    except Exception as e:
        results["checks"]["paperless"] = {
            "status": "error",
            "error": str(e),
        }
        results["overall"] = "degraded"

    # Check daemon status
    daemon_status = read_daemon_status()
    if daemon_status.get("status") == "running":
        results["checks"]["daemon"] = {"status": "ok"}
    else:
        results["checks"]["daemon"] = {
            "status": "warning",
            "message": f"Daemon status: {daemon_status.get('status', 'unknown')}",
        }

    # Set overall status
    if any(c.get("status") == "error" for c in results["checks"].values()):
        results["overall"] = "unhealthy"
    elif any(c.get("status") == "warning" for c in results["checks"].values()):
        results["overall"] = "degraded"

    return results


# =============================================================================
# CLI
# =============================================================================

def main():
    """CLI interface for pipeline daemon."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Master Pipeline Daemon - Orchestrates the full Continuum pipeline"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Dry run mode (stages won't execute)")
    parser.add_argument("--webhook-only", action="store_true",
                        help="Start webhook listener only")
    parser.add_argument("--watchers-only", action="store_true",
                        help="Start file watchers only")
    parser.add_argument("--host", type=str, default=WEBHOOK_HOST,
                        help=f"Webhook host (default: {WEBHOOK_HOST})")
    parser.add_argument("--port", type=int, default=WEBHOOK_PORT,
                        help=f"Webhook port (default: {WEBHOOK_PORT})")
    parser.add_argument("--status", action="store_true",
                        help="Show pipeline status and exit")
    parser.add_argument("--health", action="store_true",
                        help="Run health check and exit")

    args = parser.parse_args()

    # Status mode
    if args.status:
        status = get_pipeline_status()
        print(json.dumps(status, indent=2))
        return 0

    # Health check mode
    if args.health:
        health = run_health_check()
        print(json.dumps(health, indent=2))
        return 0 if health["overall"] == "healthy" else 1

    # Determine which components to enable
    enable_webhook = not args.watchers_only
    enable_watchers = not args.webhook_only

    # Create and start daemon
    daemon = PipelineDaemon(
        enable_webhook=enable_webhook,
        enable_watchers=enable_watchers,
        dry_run=args.dry_run,
        webhook_host=args.host,
        webhook_port=args.port,
    )

    # Register signal handlers
    signal.signal(signal.SIGINT, daemon.handle_signal)
    signal.signal(signal.SIGTERM, daemon.handle_signal)

    daemon.start()
    daemon.wait()

    return 0


if __name__ == "__main__":
    sys.exit(main())
