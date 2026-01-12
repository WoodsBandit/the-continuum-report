#!/usr/bin/env python3
"""
Master script to rebuild all indexes

Runs the complete pipeline:
1. entity_registry.json
2. source_mentions.json
3. co_occurrence.json
4. Gap analysis report
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone


def run_script(script_name, description):
    """Run a Python script and report status"""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}")

    script_path = Path(__file__).parent / script_name

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Print output
        if result.stdout:
            print(result.stdout)

        # Check for errors
        if result.returncode != 0:
            print(f"\nERROR: Script failed with exit code {result.returncode}")
            if result.stderr:
                print(f"STDERR: {result.stderr}")
            return False

        print(f"\n[OK] {description} completed successfully")
        return True

    except Exception as e:
        print(f"\nERROR: Failed to run {script_name}: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("CONTINUUM REPORT - INDEX REBUILD PIPELINE")
    print("="*60)
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("="*60)

    # Define pipeline steps
    steps = [
        ('build_entity_registry.py', 'Build Entity Registry'),
        ('build_source_mentions.py', 'Build Source Mentions Index'),
        ('build_co_occurrence.py', 'Build Co-occurrence Matrix'),
        ('analyze_gaps.py', 'Generate Gap Analysis Report')
    ]

    # Run pipeline
    results = []
    for script, description in steps:
        success = run_script(script, description)
        results.append((description, success))

        if not success:
            print(f"\n[X] Pipeline halted due to error in: {description}")
            break

    # Summary
    print("\n" + "="*60)
    print("PIPELINE SUMMARY")
    print("="*60)

    for description, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status}: {description}")

    # Final status
    all_success = all(success for _, success in results)

    print("="*60)
    if all_success:
        print("[OK] ALL INDEXES REBUILT SUCCESSFULLY")
    else:
        print("[X] PIPELINE FAILED - CHECK ERRORS ABOVE")

    print(f"Completed: {datetime.now(timezone.utc).isoformat()}")
    print("="*60)

    # Exit with appropriate code
    sys.exit(0 if all_success else 1)


if __name__ == '__main__':
    main()
