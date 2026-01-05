#!/usr/bin/env python3
"""
Consolidate all entities from Phase 1 extraction files
"""

import os
import re
from collections import defaultdict
from pathlib import Path

# Directories to process
COURT_FILINGS = r"\\192.168.1.139\continuum\agents\epstein-extraction\findings\court-filings"
CRIMINAL_CASE = r"\\192.168.1.139\continuum\agents\epstein-extraction\findings\criminal-case"

# Entity consolidation
entities = {
    'people': defaultdict(lambda: {'count': 0, 'files': [], 'contexts': set()}),
    'organizations': defaultdict(lambda: {'count': 0, 'files': [], 'contexts': set()}),
    'locations': defaultdict(lambda: {'count': 0, 'files': [], 'contexts': set()})
}

# Deduplication mapping
PERSON_ALIASES = {
    'leslie wexner': 'Les Wexner',
    'les wexner': 'Les Wexner',
    'wexner': 'Les Wexner',
    'ghislaine maxwell': 'Ghislaine Maxwell',
    'g. maxwell': 'Ghislaine Maxwell',
    'maxwell': 'Ghislaine Maxwell',
    'virginia roberts': 'Virginia Giuffre (Roberts)',
    'virginia giuffre': 'Virginia Giuffre (Roberts)',
    'virginia l. giuffre': 'Virginia Giuffre (Roberts)',
    'virginia lee roberts': 'Virginia Giuffre (Roberts)',
    'virginia l. giuffre / virginia': 'Virginia Giuffre (Roberts)',
    'ms. roberts': 'Virginia Giuffre (Roberts)',
    'giuffre': 'Virginia Giuffre (Roberts)',
    'jeffrey epstein': 'Jeffrey Epstein',
    'epstein': 'Jeffrey Epstein',
    'prince andrew': 'Prince Andrew',
    'andrew, prince': 'Prince Andrew',
    'duke of york': 'Prince Andrew',
    'jean luc brunel': 'Jean-Luc Brunel',
    'jean-luc brunel': 'Jean-Luc Brunel',
    'john luc brunel': 'Jean-Luc Brunel',
    'jon luc brunel': 'Jean-Luc Brunel',
}

def normalize_name(name, entity_type='people'):
    """Normalize entity names using deduplication rules"""
    if entity_type == 'people':
        normalized = name.lower().strip()
        return PERSON_ALIASES.get(normalized, name.strip())
    return name.strip()

def extract_entities_from_file(filepath):
    """Extract entities from a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    filename = os.path.basename(filepath)

    # Find entities section
    entities_found = {
        'people': [],
        'organizations': [],
        'locations': []
    }

    # Look for "Entities Found" or "Entities" section
    entities_match = re.search(r'## Entities[^\n]*\n(.*?)(?=\n## [A-Z]|$)', content, re.DOTALL)
    if not entities_match:
        # Try alternative format "## Entities (People, Organizations, Locations with page refs)"
        entities_match = re.search(r'##+ Entities \(People.*?\n(.*?)(?=\n## [A-Z]|$)', content, re.DOTALL)

    if entities_match:
        entities_section = entities_match.group(1)

        # Extract People
        people_match = re.search(r'###+ People.*?\n(.*?)(?=\n###|$)', entities_section, re.DOTALL | re.IGNORECASE)
        if people_match:
            people_text = people_match.group(1)
            # Extract from list format "- Name" or "**Name**"
            for line in people_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    # Get name from "- Name" or "- Name (role) - context"
                    name = line[2:].strip()
                    # Remove bold markdown **text**
                    name = re.sub(r'\*\*(.*?)\*\*', r'\1', name)
                    # If there's a dash (regular or em-dash) after the name, take only before it
                    if ' - ' in name or ' — ' in name or ' – ' in name:
                        name = re.split(r'\s+[-—–]\s+', name)[0].strip()
                    # Remove parentheses content but keep the base name
                    name = re.sub(r'\s*\([^)]*\)\s*', ' ', name).strip()
                    # Clean up multiple spaces
                    name = ' '.join(name.split())
                    # Filter out non-names
                    if name and name.lower() not in ['none', 'n/a', '0']:
                        entities_found['people'].append(name)
                elif line.startswith('**') and '**' in line[2:]:
                    name = line.split('**')[1].strip()
                    if name and name.lower() not in ['none', 'n/a', '0']:
                        entities_found['people'].append(name)

        # Extract Organizations
        org_match = re.search(r'###+ Organizations.*?\n(.*?)(?=\n###|$)', entities_section, re.DOTALL | re.IGNORECASE)
        if org_match:
            org_text = org_match.group(1)
            for line in org_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    name = line[2:].strip()
                    # Remove bold markdown
                    name = re.sub(r'\*\*(.*?)\*\*', r'\1', name)
                    # If there's a dash after the name, take only the part before the dash
                    if ' - ' in name or ' — ' in name or ' – ' in name:
                        name = re.split(r'\s+[-—–]\s+', name)[0].strip()
                    # Remove parentheses content
                    name = re.sub(r'\s*\([^)]*\)\s*', ' ', name).strip()
                    # Clean up multiple spaces
                    name = ' '.join(name.split())
                    if name and name.lower() not in ['none', 'n/a', '0']:
                        entities_found['organizations'].append(name)
                elif line.startswith('**') and '**' in line[2:]:
                    name = line.split('**')[1].strip()
                    if name and name.lower() not in ['none', 'n/a', '0']:
                        entities_found['organizations'].append(name)

        # Extract Locations
        loc_match = re.search(r'###+ (?:Locations|Organizations/Locations).*?\n(.*?)(?=\n##|$)', entities_section, re.DOTALL | re.IGNORECASE)
        if loc_match:
            loc_text = loc_match.group(1)
            for line in loc_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    name = line[2:].strip()
                    # Remove bold markdown
                    name = re.sub(r'\*\*(.*?)\*\*', r'\1', name)
                    # If there's a dash after the name, take only the part before the dash
                    if ' - ' in name or ' — ' in name or ' – ' in name:
                        name = re.split(r'\s+[-—–]\s+', name)[0].strip()
                    # Remove parentheses content
                    name = re.sub(r'\s*\([^)]*\)\s*', ' ', name).strip()
                    # Clean up multiple spaces
                    name = ' '.join(name.split())
                    if name and name.lower() not in ['none', 'n/a', '0']:
                        entities_found['locations'].append(name)
                elif line.startswith('**') and '**' in line[2:]:
                    name = line.split('**')[1].strip()
                    if name and name.lower() not in ['none', 'n/a', '0']:
                        entities_found['locations'].append(name)

    return filename, entities_found

def process_directory(directory):
    """Process all markdown files in a directory"""
    files_processed = 0
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            result = extract_entities_from_file(filepath)
            if result:
                fname, found = result
                files_processed += 1

                # Add to consolidated entities
                for person in found['people']:
                    normalized = normalize_name(person, 'people')
                    entities['people'][normalized]['count'] += 1
                    entities['people'][normalized]['files'].append(fname)

                for org in found['organizations']:
                    normalized = normalize_name(org, 'organizations')
                    entities['organizations'][normalized]['count'] += 1
                    entities['organizations'][normalized]['files'].append(fname)

                for loc in found['locations']:
                    normalized = normalize_name(loc, 'locations')
                    entities['locations'][normalized]['count'] += 1
                    entities['locations'][normalized]['files'].append(fname)

    return files_processed

# Process both directories
print("Processing court-filings directory...")
count1 = process_directory(COURT_FILINGS)
print(f"Processed {count1} files from court-filings")

print("Processing criminal-case directory...")
count2 = process_directory(CRIMINAL_CASE)
print(f"Processed {count2} files from criminal-case")

total_files = count1 + count2
print(f"\nTotal files processed: {total_files}")

# Generate output
output_lines = []
output_lines.append("# Consolidated Entity Index — Phase 1 Extractions\n")
output_lines.append(f"**Processed:** 2025-12-24\n")
output_lines.append(f"**Source Files:** {total_files} extraction documents\n")

total_people = len(entities['people'])
total_orgs = len(entities['organizations'])
total_locs = len(entities['locations'])
total_entities = total_people + total_orgs + total_locs

output_lines.append(f"**Total Entities:** {total_entities}\n")
output_lines.append("\n---\n\n")

# Sort people alphabetically and group by first letter
output_lines.append("## PERSONS (Alphabetical)\n\n")
people_sorted = sorted(entities['people'].items(), key=lambda x: x[0].lower())

current_letter = ''
for name, data in people_sorted:
    first_letter = name[0].upper()
    if first_letter != current_letter:
        current_letter = first_letter
        output_lines.append(f"### {current_letter}\n\n")

    output_lines.append(f"#### {name}\n")
    output_lines.append(f"- **Mention Count:** {data['count']}\n")
    output_lines.append(f"- **Found In:** \n")

    # List files (limit to first 10 to avoid huge lists)
    files_to_show = sorted(set(data['files']))[:10]
    for f in files_to_show:
        output_lines.append(f"  - {f}\n")

    if len(data['files']) > 10:
        output_lines.append(f"  - ...and {len(data['files']) - 10} more files\n")

    output_lines.append("\n")

# Organizations
output_lines.append("\n---\n\n")
output_lines.append("## ORGANIZATIONS\n\n")
orgs_sorted = sorted(entities['organizations'].items(), key=lambda x: x[0].lower())

for name, data in orgs_sorted:
    output_lines.append(f"### {name}\n")
    output_lines.append(f"- **Mention Count:** {data['count']}\n")
    output_lines.append(f"- **Found In:** \n")

    files_to_show = sorted(set(data['files']))[:10]
    for f in files_to_show:
        output_lines.append(f"  - {f}\n")

    if len(data['files']) > 10:
        output_lines.append(f"  - ...and {len(data['files']) - 10} more files\n")

    output_lines.append("\n")

# Locations
output_lines.append("\n---\n\n")
output_lines.append("## PLACES\n\n")
locs_sorted = sorted(entities['locations'].items(), key=lambda x: x[0].lower())

for name, data in locs_sorted:
    output_lines.append(f"### {name}\n")
    output_lines.append(f"- **Mention Count:** {data['count']}\n")
    output_lines.append(f"- **Found In:** \n")

    files_to_show = sorted(set(data['files']))[:10]
    for f in files_to_show:
        output_lines.append(f"  - {f}\n")

    if len(data['files']) > 10:
        output_lines.append(f"  - ...and {len(data['files']) - 10} more files\n")

    output_lines.append("\n")

# Statistics
output_lines.append("\n---\n\n")
output_lines.append("## STATISTICS\n\n")
output_lines.append("| Category | Count |\n")
output_lines.append("|----------|-------|\n")
output_lines.append(f"| Total Persons | {total_people} |\n")
output_lines.append(f"| Total Organizations | {total_orgs} |\n")
output_lines.append(f"| Total Places | {total_locs} |\n")
output_lines.append(f"| Total Documents Processed | {total_files} |\n")

# Write output
output_content = ''.join(output_lines)
print("\n" + "="*60)
print(output_content[:2000])  # Preview
print("="*60)
print(f"\nGenerated {len(output_content)} characters")
print(f"People: {total_people}, Organizations: {total_orgs}, Locations: {total_locs}")

# Save to file
output_path = r"\\192.168.1.139\continuum\agents\epstein-extraction\findings\synthesis\CONSOLIDATED_ENTITIES.md"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(output_content)

print(f"\nSaved to: {output_path}")
