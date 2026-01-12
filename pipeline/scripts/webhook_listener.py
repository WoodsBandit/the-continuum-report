"""
The Continuum Report - Paperless Webhook Listener

Flask-based webhook endpoint that triggers Stage 1 (Source Ingestion)
when documents are uploaded to Paperless-ngx.

Endpoint: POST /api/continuum/ingest
Trigger: Paperless document consumed webhook

Usage:
    # Run standalone
    python webhook_listener.py

    # Or import for integration
    from webhook_listener import app

Configuration:
    WEBHOOK_HOST - Host to bind to (default: 0.0.0.0)
    WEBHOOK_PORT - Port to listen on (default: 5000)
    WEBHOOK_SECRET - Optional shared secret for verification
"""

import json
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from flask import Flask, request, jsonify

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from logging_config import get_logger

logger = get_logger("webhook_listener")


# =============================================================================
# CONFIGURATION
# =============================================================================

# Network configuration
WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.environ.get("WEBHOOK_PORT", "5000"))
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")  # Optional shared secret

# Base directory
BASE_DIR = Path(os.environ.get("CONTINUUM_BASE_DIR", "/mnt/user/continuum"))
LOGS_DIR = BASE_DIR / "logs"

# Queue file for pending ingestion tasks
INGESTION_QUEUE_FILE = BASE_DIR / "indexes" / "ingestion_queue.json"


# =============================================================================
# FLASK APP
# =============================================================================

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


# =============================================================================
# QUEUE MANAGEMENT
# =============================================================================

_queue_lock = threading.Lock()


def load_queue() -> list:
    """Load the ingestion queue from disk."""
    try:
        if INGESTION_QUEUE_FILE.exists():
            return json.loads(INGESTION_QUEUE_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error(f"Error loading queue: {e}")
    return []


def save_queue(queue: list) -> None:
    """Save the ingestion queue to disk."""
    try:
        INGESTION_QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
        INGESTION_QUEUE_FILE.write_text(
            json.dumps(queue, indent=2),
            encoding="utf-8"
        )
    except Exception as e:
        logger.error(f"Error saving queue: {e}")


def add_to_queue(document_info: dict) -> bool:
    """Add a document to the ingestion queue."""
    with _queue_lock:
        queue = load_queue()

        # Check for duplicates
        doc_id = document_info.get("document_id")
        for item in queue:
            if item.get("document_id") == doc_id and item.get("status") == "pending":
                logger.warning(f"Document {doc_id} already in queue")
                return False

        # Add to queue
        queue_item = {
            **document_info,
            "status": "pending",
            "queued_at": datetime.utcnow().isoformat() + "Z",
            "attempts": 0,
        }
        queue.append(queue_item)
        save_queue(queue)

        logger.info(f"Added document {doc_id} to ingestion queue")
        return True


def get_pending_count() -> int:
    """Get count of pending items in queue."""
    queue = load_queue()
    return sum(1 for item in queue if item.get("status") == "pending")


# =============================================================================
# LOGGING
# =============================================================================

def log_webhook_event(event_type: str, data: dict, status: str) -> None:
    """Log webhook events to pipeline log."""
    try:
        log_file = LOGS_DIR / "webhook_events.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "status": status,
            "data": data,
        }

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    except Exception as e:
        logger.error(f"Error logging webhook event: {e}")


# =============================================================================
# ROUTES
# =============================================================================

@app.route("/", methods=["GET"])
def root():
    """Health check endpoint."""
    return jsonify({
        "service": "The Continuum Report - Webhook Listener",
        "status": "running",
        "endpoints": {
            "/api/continuum/ingest": "POST - Paperless document webhook",
            "/api/continuum/status": "GET - Queue status",
            "/api/continuum/queue": "GET - View pending queue",
        },
        "queue_pending": get_pending_count(),
    })


@app.route("/health", methods=["GET"])
def health():
    """Simple health check."""
    return jsonify({"status": "ok"})


@app.route("/api/continuum/ingest", methods=["POST"])
def ingest_webhook():
    """
    Paperless webhook endpoint for document consumed events.

    Expected payload:
    {
        "document_id": 12345,
        "title": "Document Title",
        "created": "2025-12-25T10:00:00Z",
        "file_path": "/path/to/document.pdf",
        "tags": ["intelligence", "source"]
    }
    """
    # Verify secret if configured
    if WEBHOOK_SECRET:
        provided_secret = request.headers.get("X-Webhook-Secret", "")
        if provided_secret != WEBHOOK_SECRET:
            logger.warning("Webhook request with invalid secret")
            log_webhook_event("ingest", {}, "rejected_invalid_secret")
            return jsonify({"error": "Invalid webhook secret"}), 403

    # Parse payload
    try:
        if request.is_json:
            data = request.get_json()
        else:
            # Try to parse form data
            data = request.form.to_dict()
            if not data:
                data = {}
    except Exception as e:
        logger.error(f"Error parsing webhook payload: {e}")
        log_webhook_event("ingest", {}, "rejected_parse_error")
        return jsonify({"error": "Invalid payload"}), 400

    # Validate required fields
    document_id = data.get("document_id")
    if not document_id:
        logger.warning("Webhook missing document_id")
        log_webhook_event("ingest", data, "rejected_missing_document_id")
        return jsonify({"error": "Missing document_id"}), 400

    # Build document info
    document_info = {
        "document_id": document_id,
        "title": data.get("title", f"Document {document_id}"),
        "created": data.get("created"),
        "file_path": data.get("file_path"),
        "tags": data.get("tags", []),
        "source": "paperless_webhook",
    }

    # Add to queue
    added = add_to_queue(document_info)

    if added:
        log_webhook_event("ingest", document_info, "queued")
        logger.info(f"Document {document_id} queued for ingestion")

        # Trigger Stage 1 processor (non-blocking)
        trigger_stage1_processor()

        return jsonify({
            "status": "queued",
            "document_id": document_id,
            "message": "Document queued for Stage 1 processing",
        }), 202
    else:
        log_webhook_event("ingest", document_info, "duplicate")
        return jsonify({
            "status": "duplicate",
            "document_id": document_id,
            "message": "Document already in queue",
        }), 200


@app.route("/api/continuum/status", methods=["GET"])
def queue_status():
    """Get queue status."""
    queue = load_queue()

    status_counts = {}
    for item in queue:
        status = item.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

    return jsonify({
        "total_items": len(queue),
        "status_counts": status_counts,
        "queue_file": str(INGESTION_QUEUE_FILE),
    })


@app.route("/api/continuum/queue", methods=["GET"])
def view_queue():
    """View pending queue items."""
    queue = load_queue()

    # Filter by status if requested
    status_filter = request.args.get("status")
    if status_filter:
        queue = [item for item in queue if item.get("status") == status_filter]

    # Limit response size
    limit = int(request.args.get("limit", 50))
    queue = queue[-limit:]  # Most recent

    return jsonify({
        "items": queue,
        "count": len(queue),
    })


@app.route("/api/continuum/queue/clear", methods=["POST"])
def clear_queue():
    """Clear completed/failed items from queue."""
    with _queue_lock:
        queue = load_queue()
        original_count = len(queue)

        # Keep only pending items
        queue = [item for item in queue if item.get("status") == "pending"]
        save_queue(queue)

        removed = original_count - len(queue)
        logger.info(f"Cleared {removed} items from queue")

        return jsonify({
            "removed": removed,
            "remaining": len(queue),
        })


# =============================================================================
# STAGE 1 TRIGGER
# =============================================================================

_processor_lock = threading.Lock()
_processor_running = False


def trigger_stage1_processor():
    """
    Trigger the Stage 1 processor to run.

    This is a non-blocking call that starts processing in a background thread
    if not already running.
    """
    global _processor_running

    with _processor_lock:
        if _processor_running:
            logger.debug("Stage 1 processor already running")
            return

        _processor_running = True

    # Start processor in background thread
    thread = threading.Thread(target=_run_stage1_processor, daemon=True)
    thread.start()


def _run_stage1_processor():
    """Background thread to process ingestion queue."""
    global _processor_running

    try:
        # Import here to avoid circular imports
        from run_stage1 import process_ingestion_queue

        logger.info("Starting Stage 1 processor")
        process_ingestion_queue()
        logger.info("Stage 1 processor completed")

    except ImportError:
        logger.warning("run_stage1.py not available - queue will be processed by daemon")
    except Exception as e:
        logger.error(f"Stage 1 processor error: {e}")
    finally:
        with _processor_lock:
            _processor_running = False


# =============================================================================
# MANUAL TRIGGER ENDPOINT
# =============================================================================

@app.route("/api/continuum/trigger/stage1", methods=["POST"])
def manual_trigger_stage1():
    """Manually trigger Stage 1 processing."""
    trigger_stage1_processor()
    return jsonify({
        "status": "triggered",
        "message": "Stage 1 processor triggered",
    })


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({"error": "Internal server error"}), 500


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run the webhook listener."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Paperless webhook listener for The Continuum Report"
    )
    parser.add_argument("--host", default=WEBHOOK_HOST,
                        help=f"Host to bind to (default: {WEBHOOK_HOST})")
    parser.add_argument("--port", type=int, default=WEBHOOK_PORT,
                        help=f"Port to listen on (default: {WEBHOOK_PORT})")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug mode")

    args = parser.parse_args()

    print("=" * 60)
    print("The Continuum Report - Webhook Listener")
    print("=" * 60)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Queue file: {INGESTION_QUEUE_FILE}")
    print(f"Pending items: {get_pending_count()}")
    print()
    print("Endpoints:")
    print(f"  POST http://{args.host}:{args.port}/api/continuum/ingest")
    print(f"  GET  http://{args.host}:{args.port}/api/continuum/status")
    print("=" * 60)

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
