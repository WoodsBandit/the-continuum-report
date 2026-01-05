"""
The Continuum Report - Claude CLI Invoker

Wrapper for invoking Claude Code CLI with SOP context and task descriptions.
Used by all pipeline stage runners for AI-powered processing.

Usage:
    from invoke_claude import invoke_claude_with_sop

    result = invoke_claude_with_sop(
        sop_number=1,
        task_description="Extract entities from document X",
        additional_context={"source_id": 123, "title": "Document"}
    )

    if result.success:
        print(result.output)
    else:
        print(f"Error: {result.error}")

Environment:
    CONTINUUM_BASE_DIR - Base directory (default: //192.168.1.139/continuum)
"""

import json
import os
import subprocess
import sys
import time
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from logging_config import get_logger

logger = get_logger("invoke_claude")


# =============================================================================
# CONFIGURATION
# =============================================================================

# Base directory for continuum
# Use environment variable or default to Unraid path
BASE_DIR = Path(os.environ.get("CONTINUUM_BASE_DIR", "/mnt/user/continuum"))

# SOP file mapping
SOP_FILES = {
    0: "SOP-000-master-pipeline.md",
    1: "SOP-001-source-ingestion.md",
    2: "SOP-002-context-extraction.md",
    3: "SOP-003-brief-generation.md",
    4: "SOP-004-publication.md",
}

# Claude CLI settings
# Use docker exec to call claude inside the claude-code container
CLAUDE_CONTAINER = os.environ.get("CLAUDE_CONTAINER", "claude-code")
CLAUDE_CLI = ["docker", "exec", "-i", "--user", "node", CLAUDE_CONTAINER, "claude"]
DEFAULT_TIMEOUT = 600  # 10 minutes


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ClaudeResult:
    """Result from Claude CLI invocation."""
    success: bool
    output: str = ""
    error: str = ""
    exit_code: int = 0
    duration_seconds: float = 0.0
    sop_used: str = ""
    task_description: str = ""


@dataclass
class InvocationContext:
    """Context for Claude invocation."""
    sop_content: str = ""
    runbook_content: str = ""
    index_states: dict = field(default_factory=dict)
    additional_context: dict = field(default_factory=dict)


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def read_file_safe(path: Path) -> str:
    """Read file contents safely, return empty string on error."""
    try:
        if path.exists():
            return path.read_text(encoding="utf-8")
        logger.warning(f"File not found: {path}")
        return ""
    except Exception as e:
        logger.error(f"Error reading {path}: {e}")
        return ""


def get_sop_content(sop_number: int) -> str:
    """Load SOP file content by number."""
    if sop_number not in SOP_FILES:
        raise ValueError(f"Invalid SOP number: {sop_number}. Valid: {list(SOP_FILES.keys())}")

    sop_path = BASE_DIR / "sops" / SOP_FILES[sop_number]
    content = read_file_safe(sop_path)

    if not content:
        raise FileNotFoundError(f"SOP file not found or empty: {sop_path}")

    return content


def get_runbook_content() -> str:
    """Load RUNBOOK.md content."""
    runbook_path = BASE_DIR / "sops" / "RUNBOOK.md"
    return read_file_safe(runbook_path)


def get_index_states() -> dict:
    """Get current state of all index files."""
    indexes_dir = BASE_DIR / "indexes"
    index_files = [
        "entity_registry.json",
        "source_mentions.json",
        "co_occurrence.json",
        "connection_contexts.json",
        "processed_sources.json",
    ]

    states = {}
    for filename in index_files:
        path = indexes_dir / filename
        if path.exists():
            stat = path.stat()
            states[filename] = {
                "exists": True,
                "size_bytes": stat.st_size,
                "modified": stat.st_mtime,
            }
            # For smaller files, include entry count
            if stat.st_size < 1_000_000:  # < 1MB
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    if isinstance(data, dict):
                        states[filename]["entry_count"] = len(data)
                    elif isinstance(data, list):
                        states[filename]["entry_count"] = len(data)
                except Exception:
                    pass
        else:
            states[filename] = {"exists": False}

    return states


def build_prompt(
    sop_number: int,
    task_description: str,
    context: InvocationContext,
) -> str:
    """Build the full prompt for Claude CLI."""

    parts = []

    # Header
    parts.append("=" * 70)
    parts.append("THE CONTINUUM REPORT - AUTONOMOUS PIPELINE TASK")
    parts.append("=" * 70)
    parts.append("")

    # SOP Context
    parts.append("## STANDARD OPERATING PROCEDURE")
    parts.append("")
    parts.append(context.sop_content)
    parts.append("")

    # Quick Reference (if available)
    if context.runbook_content:
        parts.append("## RUNBOOK QUICK REFERENCE")
        parts.append("")
        parts.append(context.runbook_content[:5000])  # Truncate to avoid too much context
        parts.append("")
        if len(context.runbook_content) > 5000:
            parts.append("(Runbook truncated - full version in sops/RUNBOOK.md)")
            parts.append("")

    # Current System State
    parts.append("## CURRENT INDEX STATES")
    parts.append("")
    parts.append("```json")
    parts.append(json.dumps(context.index_states, indent=2))
    parts.append("```")
    parts.append("")

    # Additional Context
    if context.additional_context:
        parts.append("## TASK CONTEXT")
        parts.append("")
        parts.append("```json")
        parts.append(json.dumps(context.additional_context, indent=2))
        parts.append("```")
        parts.append("")

    # Task Description
    parts.append("## YOUR TASK")
    parts.append("")
    parts.append(task_description)
    parts.append("")

    # Footer
    parts.append("=" * 70)
    parts.append("Execute this task following the SOP procedures exactly.")
    parts.append("Update index files as required.")
    parts.append("Log all actions to the pipeline log.")
    parts.append("=" * 70)

    return "\n".join(parts)


def invoke_claude_cli(
    prompt: str,
    timeout: int = DEFAULT_TIMEOUT,
    working_dir: Optional[Path] = None,
) -> ClaudeResult:
    """
    Invoke Claude CLI with the given prompt.

    Uses `claude --dangerously-skip-permissions --print` for fully autonomous operation.
    """
    start_time = time.time()

    if working_dir is None:
        working_dir = BASE_DIR

    # Progress indicator thread
    stop_progress = threading.Event()
    def progress_indicator():
        interval = 30  # Log every 30 seconds
        while not stop_progress.wait(interval):
            elapsed = int(time.time() - start_time)
            logger.info(f"  ...waiting for Claude response ({elapsed}s elapsed, timeout={timeout}s)")

    progress_thread = threading.Thread(target=progress_indicator, daemon=True)
    progress_thread.start()

    try:
        # Build command: docker exec -i claude-code claude --dangerously-skip-permissions --print
        # --dangerously-skip-permissions: Auto-approve all tool uses
        # --print: Non-interactive output mode
        cmd = CLAUDE_CLI + ["--dangerously-skip-permissions", "--print"]

        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # Note: working_dir doesn't apply to docker exec, container uses /continuum
            text=True,
        )

        stdout, stderr = process.communicate(input=prompt, timeout=timeout)
        stop_progress.set()  # Stop progress indicator
        duration = time.time() - start_time

        if process.returncode == 0:
            return ClaudeResult(
                success=True,
                output=stdout,
                error=stderr,
                exit_code=0,
                duration_seconds=duration,
            )
        else:
            return ClaudeResult(
                success=False,
                output=stdout,
                error=stderr or f"Claude CLI exited with code {process.returncode}",
                exit_code=process.returncode,
                duration_seconds=duration,
            )

    except subprocess.TimeoutExpired:
        stop_progress.set()  # Stop progress indicator
        process.kill()
        duration = time.time() - start_time
        return ClaudeResult(
            success=False,
            error=f"Claude CLI timed out after {timeout} seconds",
            exit_code=-1,
            duration_seconds=duration,
        )
    except FileNotFoundError:
        stop_progress.set()  # Stop progress indicator
        return ClaudeResult(
            success=False,
            error=f"Claude CLI not found. Ensure '{CLAUDE_CLI}' is in PATH.",
            exit_code=-1,
        )
    except Exception as e:
        stop_progress.set()  # Stop progress indicator
        duration = time.time() - start_time
        return ClaudeResult(
            success=False,
            error=f"Error invoking Claude CLI: {e}",
            exit_code=-1,
            duration_seconds=duration,
        )


# =============================================================================
# PUBLIC API
# =============================================================================

def invoke_claude_with_sop(
    sop_number: int,
    task_description: str,
    additional_context: Optional[dict] = None,
    include_runbook: bool = True,
    timeout: int = DEFAULT_TIMEOUT,
) -> ClaudeResult:
    """
    Invoke Claude with SOP context for pipeline task execution.

    Args:
        sop_number: SOP number (0-4)
        task_description: What Claude should do
        additional_context: Extra context (source data, trigger info, etc.)
        include_runbook: Whether to include RUNBOOK.md quick reference
        timeout: Timeout in seconds

    Returns:
        ClaudeResult with success status and output
    """
    logger.info(f"Invoking Claude with SOP-{sop_number:03d}")
    logger.info(f"Task: {task_description[:100]}...")

    try:
        # Build context
        context = InvocationContext(
            sop_content=get_sop_content(sop_number),
            runbook_content=get_runbook_content() if include_runbook else "",
            index_states=get_index_states(),
            additional_context=additional_context or {},
        )

        # Build prompt
        prompt = build_prompt(sop_number, task_description, context)
        logger.debug(f"Prompt length: {len(prompt)} chars")

        # Invoke Claude
        result = invoke_claude_cli(prompt, timeout=timeout)
        result.sop_used = SOP_FILES[sop_number]
        result.task_description = task_description

        if result.success:
            logger.info(f"Claude completed in {result.duration_seconds:.1f}s")
        else:
            logger.error(f"Claude failed: {result.error}")

        return result

    except Exception as e:
        logger.error(f"Error preparing Claude invocation: {e}")
        return ClaudeResult(
            success=False,
            error=str(e),
            sop_used=SOP_FILES.get(sop_number, "unknown"),
            task_description=task_description,
        )


def invoke_claude_raw(
    prompt: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> ClaudeResult:
    """
    Invoke Claude with a raw prompt (no SOP context).

    For ad-hoc tasks that don't fit the SOP pipeline.
    """
    logger.info("Invoking Claude with raw prompt")
    return invoke_claude_cli(prompt, timeout=timeout)


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """CLI interface for testing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Invoke Claude CLI with SOP context",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Test with SOP-001
    python invoke_claude.py --sop 1 --task "List entities from test document"

    # Raw prompt
    python invoke_claude.py --raw "What is 2+2?"

    # Check system state
    python invoke_claude.py --status
        """
    )

    parser.add_argument("--sop", type=int, choices=[0, 1, 2, 3, 4],
                        help="SOP number to use")
    parser.add_argument("--task", type=str,
                        help="Task description for Claude")
    parser.add_argument("--raw", type=str,
                        help="Raw prompt (no SOP context)")
    parser.add_argument("--status", action="store_true",
                        help="Show current index states")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT})")

    args = parser.parse_args()

    if args.status:
        print("Index States:")
        print(json.dumps(get_index_states(), indent=2))
        return 0

    if args.raw:
        result = invoke_claude_raw(args.raw, timeout=args.timeout)
    elif args.sop is not None and args.task:
        result = invoke_claude_with_sop(
            sop_number=args.sop,
            task_description=args.task,
            timeout=args.timeout,
        )
    else:
        parser.print_help()
        return 1

    print("\n" + "=" * 60)
    print(f"Success: {result.success}")
    print(f"Duration: {result.duration_seconds:.1f}s")
    print(f"Exit Code: {result.exit_code}")
    print("=" * 60)

    if result.output:
        print("\nOutput:")
        print(result.output)

    if result.error:
        print("\nError:")
        print(result.error)

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
