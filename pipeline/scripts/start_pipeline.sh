#!/bin/bash
# The Continuum Report - Pipeline Startup Script for Tower (Unraid)
#
# Run this on Tower to start the full autonomous pipeline.
# Requires: Nerd Tools with python3, python-pip enabled
#
# Usage:
#   ./start_pipeline.sh           # Start full pipeline
#   ./start_pipeline.sh --dry-run # Dry run mode
#   ./start_pipeline.sh --status  # Check status

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONTINUUM_DIR="/mnt/user/continuum"

echo "============================================================"
echo "THE CONTINUUM REPORT - AUTONOMOUS PIPELINE"
echo "============================================================"
echo "Running on: $(hostname)"
echo "Directory: $CONTINUUM_DIR"
echo "============================================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found"
    echo "Install via Unraid Nerd Tools plugin:"
    echo "  Settings -> Nerd Tools -> Enable python3, python-pip"
    exit 1
fi

# Check Claude CLI
if ! command -v claude &> /dev/null; then
    echo "ERROR: Claude CLI not found"
    echo "Install with: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

echo "Python: $(python3 --version)"
echo "Claude: $(claude --version 2>/dev/null || echo 'installed')"

# Install Python dependencies if needed
echo ""
echo "Checking dependencies..."
pip3 install --quiet flask watchdog pydantic-settings requests 2>/dev/null || {
    echo "Installing Python packages..."
    pip3 install flask watchdog pydantic-settings requests
}

# Set environment
export CONTINUUM_BASE_DIR="$CONTINUUM_DIR"
export PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/lib"

cd "$SCRIPT_DIR"

# Handle arguments
case "${1:-}" in
    --status)
        echo ""
        python3 pipeline_daemon.py --status
        exit 0
        ;;
    --health)
        echo ""
        python3 pipeline_daemon.py --health
        exit 0
        ;;
    --dry-run)
        echo ""
        echo "Starting in DRY RUN mode..."
        python3 pipeline_daemon.py --dry-run
        ;;
    --webhook-only)
        echo ""
        echo "Starting webhook listener only..."
        python3 webhook_listener.py
        ;;
    --watchers-only)
        echo ""
        echo "Starting file watchers only..."
        python3 pipeline_watcher.py
        ;;
    *)
        echo ""
        echo "Starting full pipeline daemon..."
        echo "Press Ctrl+C to stop"
        echo ""
        python3 pipeline_daemon.py
        ;;
esac
