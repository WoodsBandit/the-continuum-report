#!/usr/bin/env python3
"""
BNIS v2 - Main Orchestrator

Single entry point for the Breaking News Intelligence System.
Runs the full pipeline: Fetch → Match → Generate → Queue for Approval

Usage:
    python run_bnis.py                    # Full pipeline
    python run_bnis.py --fetch-only       # Just fetch and match
    python run_bnis.py --generate-only    # Just generate narratives
    python run_bnis.py --dry-run          # Preview without changes
    python run_bnis.py --hours 48         # Custom time window
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from intelligence_pipeline import IntelligencePipeline
from narrative_generator import main as generate_narratives


def print_banner():
    """Print startup banner."""
    print()
    print("=" * 70)
    print("  BNIS v2 - Breaking News Intelligence System")
    print("  The Continuum Report")
    print("=" * 70)
    print(f"  Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f"  Host: WoodsDen (Local)")
    print("=" * 70)
    print()


def run_fetch_and_match(hours: int = 24, dry_run: bool = False) -> dict:
    """
    Run the fetch and entity matching pipeline.

    Args:
        hours: Time window for fetching
        dry_run: If True, don't save outputs

    Returns:
        Pipeline results dict
    """
    print("[PHASE 1] Fetch & Match")
    print("-" * 40)

    pipeline = IntelligencePipeline()
    results = pipeline.run(since_hours=hours, save_all=not dry_run)

    return results


def run_narrative_generation(dry_run: bool = False, limit: int = 5):
    """
    Run narrative generation on pending items.

    Args:
        dry_run: If True, don't generate
        limit: Max items to process
    """
    print()
    print("[PHASE 2] Narrative Generation")
    print("-" * 40)

    if dry_run:
        print("  [DRY RUN] Would generate narratives for pending items")
        return

    # Import and run
    import subprocess
    script = Path(__file__).parent / "scripts" / "narrative_generator.py"

    args = ["python", str(script), "--limit", str(limit)]
    if dry_run:
        args.append("--dry-run")

    subprocess.run(args)


def main():
    parser = argparse.ArgumentParser(
        description="BNIS v2 - Breaking News Intelligence System"
    )
    parser.add_argument(
        "--fetch-only",
        action="store_true",
        help="Only run fetch and match phase"
    )
    parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Only run narrative generation"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without making changes"
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Time window for fetching (default: 24)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Max narratives to generate (default: 5)"
    )
    args = parser.parse_args()

    print_banner()

    if args.dry_run:
        print("*** DRY RUN MODE - No changes will be saved ***")
        print()

    try:
        # Phase 1: Fetch and Match
        if not args.generate_only:
            results = run_fetch_and_match(args.hours, args.dry_run)

            # Check if we have high-value items
            high_value = results.get("stats", {}).get("high_value_items", 0)
            print(f"\nHigh-value items found: {high_value}")

            if high_value == 0 and not args.fetch_only:
                print("No high-value items to process. Skipping narrative generation.")
                args.fetch_only = True

        # Phase 2: Narrative Generation
        if not args.fetch_only:
            run_narrative_generation(args.dry_run, args.limit)

        # Summary
        print()
        print("=" * 70)
        print("  BNIS Run Complete")
        print("=" * 70)
        print()
        print("  Next Steps:")
        print("  1. Review narratives in pending_approval/")
        print("  2. Approved briefs → website/briefs/breaking_news/")
        print("  3. Run again to fetch new items")
        print()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        raise


if __name__ == "__main__":
    main()
