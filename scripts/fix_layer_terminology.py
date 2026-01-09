#!/usr/bin/env python3
"""
fix_layer_terminology.py - Remove 'Layer' terminology from all briefs

Changes:
1. Remove "Continuum Layer" row from Document Classification tables
2. Remove "Layer" column from Cross-Network Connections tables
3. Replace body text Layer references with network names
"""

import re
from pathlib import Path

BRIEFS_DIR = Path(r"T:\website\briefs\entity")

# Mapping of Layer numbers to network names
LAYER_MAPPING = {
    "Layer 0": "The Continuum",
    "Layer 1": "Epstein Network",
    "Layer 2": "Intelligence Operations",
    "Layer 2-3": "Intelligence-Financial Networks",
    "Layer 3": "Financial Networks",
    "Layer 4": "Political Networks",
    "Layer 5": "Media Networks",
    "Layers": "Networks"
}

def fix_document_classification(content: str) -> str:
    """Remove Continuum Layer row from Document Classification table."""
    # Match the entire Continuum Layer row including various formats
    patterns = [
        r'\| \*\*Continuum Layer[s]?\*\* \|[^\n]+\n',
        r'\| \*\*Continuum Layers\*\* \|[^\n]+\n',
    ]
    for pattern in patterns:
        content = re.sub(pattern, '', content)
    return content

def fix_cross_network_connections(content: str) -> str:
    """Remove Layer column from Cross-Network Connections tables."""

    # Fix table header: "| Connected Entity | Layer | Connection Type | Source |"
    # Should become: "| Connected Entity | Connection Type | Source |"
    content = re.sub(
        r'\| Connected Entity \| Layer \| Connection Type \| Source \|',
        '| Connected Entity | Connection Type | Source |',
        content
    )

    # Fix separator line: "|-----------------|-------|-----------------|--------|"
    # Should become: "|-----------------|-----------------|--------|"
    content = re.sub(
        r'\|[-]+\|[-]+\|[-]+\|[-]+\|',
        '|-----------------|-----------------|--------|',
        content
    )

    # Fix data rows: "| BCCI Affair | 2-3 | Knowledge/relationship | Senate Report |"
    # Should become: "| BCCI Affair | Knowledge/relationship | Senate Report |"
    # Pattern: | text | layer-number | text | text |
    content = re.sub(
        r'\| ([^|]+) \| (\d+(?:-\d+)?) \| ([^|]+) \| ([^|]+) \|',
        r'| \1 | \3 | \4 |',
        content
    )

    return content

def fix_body_text_layer_references(content: str) -> str:
    """Replace Layer references in body text with network names."""

    # Replace "Layer X: Name" format with just the name
    content = re.sub(r'Layer 0: The Continuum', 'The Continuum', content)
    content = re.sub(r'Layer 1: Epstein (Core|Network)', 'Epstein Network', content)
    content = re.sub(r'Layer 2: Intelligence Operations', 'Intelligence Operations', content)
    content = re.sub(r'Layer 3: Financial Networks?', 'Financial Networks', content)
    content = re.sub(r'Layer 4: Political Networks?', 'Political Networks', content)
    content = re.sub(r'Layer 5: Media Networks?', 'Media Networks', content)

    # Replace standalone "Layer X" references
    # Be careful with context - some need the network name, some should just be removed

    # "Layer 1" -> "Epstein Network"
    content = re.sub(r'\bLayer 1\b(?! \()', 'the Epstein Network', content)
    content = re.sub(r'\bLayer 1 \(Epstein[^)]+\)', 'the Epstein Network', content)

    # "Layer 2" -> "Intelligence Operations"
    content = re.sub(r'\bLayer 2\b(?! \()', 'Intelligence Operations', content)
    content = re.sub(r'\bLayer 2 \(Intelligence[^)]+\)', 'Intelligence Operations', content)

    # "Layer 3" -> "Financial Networks"
    content = re.sub(r'\bLayer 3\b(?! \()', 'Financial Networks', content)
    content = re.sub(r'\bLayer 3 \(Financial[^)]+\)', 'Financial Networks', content)
    content = re.sub(r'\(Layer 3\)', '(Financial Networks)', content)

    # "Layer 5" -> "Parallel Cases" or remove
    content = re.sub(r'\bLayer 5 classification\b', 'parallel case classification', content)
    content = re.sub(r'\bLayer 5\b', 'Parallel Cases', content)

    # "Layer 2-3" -> "Intelligence-Financial nexus"
    content = re.sub(r'\bLayer 2-3\b', 'Intelligence-Financial networks', content)

    # Fix compound forms
    content = re.sub(r'Intelligence Operations-Layer 3', 'Intelligence Operations-Financial Networks', content)

    # Fix "multiple Layer 2 congressional" -> "multiple Intelligence Operations congressional"
    content = re.sub(r'multiple Layer 2 congressional', 'multiple Intelligence Operations-related congressional', content)

    # Fix "Layer 1-Layer 2" -> "Epstein Network-Intelligence Operations"
    content = re.sub(r'Layer 1-Layer 2', 'Epstein Network to Intelligence Operations', content)

    # Fix "Layer 1 ↔ Layer 2" -> "Epstein Network ↔ Intelligence Operations"
    content = re.sub(r'Layer 1 ↔ Layer 2', 'Epstein Network ↔ Intelligence Operations', content)

    # Fix remaining "Layer X" references in parentheses
    content = re.sub(r'\(Layer 1\)', '(Epstein Network)', content)
    content = re.sub(r'\(Layer 2\)', '(Intelligence Operations)', content)

    # Fix "cross-layer" -> "cross-network"
    content = re.sub(r'cross-layer', 'cross-network', content, flags=re.IGNORECASE)
    content = re.sub(r'Cross-Layer', 'Cross-Network', content)

    # Fix "layers" in other contexts
    content = re.sub(r"The Continuum's Layer 1", "The Continuum's Epstein Network", content)
    content = re.sub(r"The Continuum's Layer 2", "The Continuum's Intelligence Operations network", content)
    content = re.sub(r"The Continuum's hierarchical framework", "The Continuum's network framework", content)

    # Fix "multiple layers" -> "multiple networks"
    content = re.sub(r'multiple layers', 'multiple networks', content, flags=re.IGNORECASE)
    content = re.sub(r'span multiple layers', 'span multiple networks', content)

    return content

def fix_ascii_diagrams(content: str) -> str:
    """Fix Layer references in ASCII diagrams."""
    content = re.sub(r'LAYER 1: Epstein Core', 'EPSTEIN NETWORK', content)
    content = re.sub(r'LAYER 2: Intelligence Operations', 'INTELLIGENCE OPERATIONS', content)
    return content

def process_brief(filepath: Path) -> tuple[bool, str]:
    """Process a single brief file. Returns (changed, summary)."""
    content = filepath.read_text(encoding='utf-8')
    original = content

    # Apply all fixes
    content = fix_document_classification(content)
    content = fix_cross_network_connections(content)
    content = fix_body_text_layer_references(content)
    content = fix_ascii_diagrams(content)

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return True, f"Fixed: {filepath.name}"
    return False, f"No changes: {filepath.name}"

def main():
    print("=" * 60)
    print("FIX LAYER TERMINOLOGY IN BRIEFS")
    print("=" * 60)

    briefs = list(BRIEFS_DIR.glob("*.md"))
    print(f"\nFound {len(briefs)} brief files")

    changed = 0
    unchanged = 0

    for brief in sorted(briefs):
        was_changed, msg = process_brief(brief)
        if was_changed:
            changed += 1
            print(f"  [FIXED] {msg}")
        else:
            unchanged += 1

    print(f"\n{'=' * 60}")
    print(f"SUMMARY: {changed} files modified, {unchanged} unchanged")
    print("=" * 60)

if __name__ == '__main__':
    main()
