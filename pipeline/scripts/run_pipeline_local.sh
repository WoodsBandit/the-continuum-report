#!/bin/bash
# The Continuum Report - Pipeline Runner for WoodsDen (Linux/WSL)
# Run this on WoodsDen where Claude CLI is installed
#
# Prerequisites:
#   - Python 3.11+ with pip
#   - Claude CLI installed and authenticated
#   - Network share mounted at /mnt/continuum or via UNC path
#
# Usage:
#   ./run_pipeline_local.sh          - Start pipeline
#   ./run_pipeline_local.sh --dry-run - Dry run mode
#   ./run_pipeline_local.sh --status  - Check status

set -e

echo "============================================================"
echo "THE CONTINUUM REPORT - LOCAL PIPELINE RUNNER"
echo "============================================================"
echo

# Determine continuum path
if [ -d "/mnt/continuum/scripts" ]; then
    CONTINUUM_DIR="/mnt/continuum"
elif [ -d "//192.168.1.139/continuum/scripts" ]; then
    CONTINUUM_DIR="//192.168.1.139/continuum"
elif [ -d "$HOME/continuum/scripts" ]; then
    CONTINUUM_DIR="$HOME/continuum"
else
    echo "ERROR: Continuum directory not found"
    echo "Mount the share or set CONTINUUM_DIR environment variable"
    exit 1
fi

echo "Using continuum at: $CONTINUUM_DIR"

# Check Claude CLI
if ! command -v claude &> /dev/null; then
    echo "ERROR: Claude CLI not found in PATH"
    echo "Install with: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found"
    exit 1
fi

# Install dependencies if needed
echo "Checking Python dependencies..."
if ! python3 -c "import watchdog" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install watchdog pydantic-settings requests
fi

# Change to scripts directory
cd "$CONTINUUM_DIR/scripts"

# Export environment
export PYTHONPATH="$CONTINUUM_DIR/scripts:$CONTINUUM_DIR/scripts/lib"
export CONTINUUM_BASE_DIR="$CONTINUUM_DIR"

# Run pipeline watcher
echo
echo "Starting pipeline watcher..."
echo "Press Ctrl+C to stop"
echo

python3 pipeline_watcher.py "$@"
