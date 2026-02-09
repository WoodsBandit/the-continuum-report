#!/usr/bin/env python3
import re

# Read a test file
filepath = r"C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum\work\epstein-extraction\findings\court-filings\ecf-1320-2.md"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 60)
print("FILE CONTENT (first 2000 chars):")
print("=" * 60)
print(content[:2000])
print("\n" + "=" * 60)
print("SEARCHING FOR ENTITIES SECTION")
print("=" * 60)

# Look for "Entities Found" or "Entities" section
entities_match = re.search(r'##+ Entities.*?\n(.*?)(?=\n##|$)', content, re.DOTALL | re.IGNORECASE)
if not entities_match:
    print("Pattern 1 failed, trying pattern 2...")
    entities_match = re.search(r'##+ Entities \(People.*?\n(.*?)(?=\n##|$)', content, re.DOTALL | re.IGNORECASE)

if entities_match:
    entities_section = entities_match.group(1)
    print(f"Found entities section ({len(entities_section)} chars):")
    print(entities_section[:1000])

    print("\n" + "=" * 60)
    print("SEARCHING FOR PEOPLE SUBSECTION")
    print("=" * 60)

    # Extract People
    people_match = re.search(r'###+ People.*?\n(.*?)(?=\n###|$)', entities_section, re.DOTALL | re.IGNORECASE)
    if people_match:
        people_text = people_match.group(1)
        print(f"Found people section ({len(people_text)} chars):")
        print(people_text[:500])

        print("\n" + "=" * 60)
        print("EXTRACTING NAMES")
        print("=" * 60)

        people_found = []
        for line in people_text.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                # Get name from "- Name" or "- Name (role) - context"
                name = line[2:].strip()
                print(f"Line: {line[:80]}")
                print(f"  Raw name: {name[:80]}")
                # If there's a dash after the name, take only the part before the dash
                if ' - ' in name:
                    name = name.split(' - ')[0].strip()
                    print(f"  After dash split: {name}")
                # Remove parentheses content but keep the base name
                name = re.sub(r'\s*\([^)]*\)\s*', ' ', name).strip()
                print(f"  After paren removal: {name}")
                if name and name.lower() not in ['none', 'n/a', '0']:
                    people_found.append(name)
                    print(f"  ✓ ADDED: {name}")
                print()

        print(f"\nTotal people found: {len(people_found)}")
        for p in people_found[:10]:
            print(f"  - {p}")
    else:
        print("NO PEOPLE SECTION FOUND")
else:
    print("NO ENTITIES SECTION FOUND")
