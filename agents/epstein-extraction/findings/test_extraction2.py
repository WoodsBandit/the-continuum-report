#!/usr/bin/env python3
import re

# Read a test file
filepath = r"\\192.168.1.139\continuum\agents\epstein-extraction\findings\court-filings\ecf-1320-2.md"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("Testing different regex patterns...")
print("=" * 60)

# Try pattern 1 - Entities section
pattern1 = r'##+ Entities.*?\n(.*?)(?=\n##|$)'
match1 = re.search(pattern1, content, re.DOTALL | re.IGNORECASE)
print(f"Pattern 1: {pattern1}")
if match1:
    print(f"  Matched! Length: {len(match1.group(1))}")
    print(f"  Content preview: {match1.group(1)[:200]}")
else:
    print("  No match")

print()

# Try pattern 2 - More specific for this file format
pattern2 = r'## Entities\s*\n(.*?)(?=\n## Timeline Events|$)'
match2 = re.search(pattern2, content, re.DOTALL | re.IGNORECASE)
print(f"Pattern 2: {pattern2}")
if match2:
    print(f"  Matched! Length: {len(match2.group(1))}")
    print(f"  Content preview: {match2.group(1)[:200]}")
else:
    print("  No match")

print()

# Try pattern 3 - Even broader
pattern3 = r'## Entities[^\n]*\n(.*?)(?=\n## [A-Z]|$)'
match3 = re.search(pattern3, content, re.DOTALL)
print(f"Pattern 3: {pattern3}")
if match3:
    print(f"  Matched! Length: {len(match3.group(1))}")
    print(f"  Content preview: {match3.group(1)[:200]}")

    # Now try to extract people
    entities_section = match3.group(1)
    people_pattern = r'### People\s*\n(.*?)(?=\n### |$)'
    people_match = re.search(people_pattern, entities_section, re.DOTALL)
    if people_match:
        print(f"\n  People section found! Length: {len(people_match.group(1))}")
        print(f"  People preview: {people_match.group(1)[:300]}")
    else:
        print("\n  No people section found")
else:
    print("  No match")
