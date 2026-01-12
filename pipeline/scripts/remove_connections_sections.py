#!/usr/bin/env python3
"""
remove_connections_sections.py - Remove Connections sections from entity briefs
that reference connections without brief files.
"""

import re
from pathlib import Path

BRIEFS_DIR = Path(r"T:\website\briefs\entity")

def remove_connections_section(filepath):
    """Remove the ## Connections section from a brief."""
    content = filepath.read_text(encoding='utf-8')
    original = content

    # Remove Connections section (## Connections through next ## or ---)
    # Pattern: ## Connections followed by everything until next section
    new_content = re.sub(
        r'\n## Connections\s*\n\n.*?(?=\n---|\n## [A-Z]|\Z)',
        '',
        content,
        flags=re.DOTALL
    )

    if new_content != original:
        filepath.write_text(new_content, encoding='utf-8')
        return True
    return False

def main():
    print("=" * 60)
    print("REMOVE CONNECTIONS SECTIONS FROM ENTITY BRIEFS")
    print("=" * 60)

    # Find all briefs with Connections sections
    briefs = list(BRIEFS_DIR.glob("analytical_brief_*.md"))

    count = 0
    for brief in sorted(briefs):
        content = brief.read_text(encoding='utf-8')
        if '## Connections' in content:
            if remove_connections_section(brief):
                count += 1
                print(f"  Removed: {brief.name}")

    print(f"\n{'=' * 60}")
    print(f"Total: {count} files updated")
    print("=" * 60)

if __name__ == '__main__':
    main()
