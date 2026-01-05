#!/usr/bin/env python3
"""
Build comprehensive Jeffrey Epstein dossier from prep file
"""

import json
import re
from datetime import datetime
from collections import defaultdict

def load_prep_file(filepath):
    """Load the JSON prep file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def parse_ecf_number(title):
    """Parse ECF document number from title"""
    # Handle formats like "1331-11", "gov.uscourts.nysd.447706.1327.12", etc.
    if title.startswith('gov.uscourts'):
        parts = title.split('.')
        if len(parts) >= 5:
            return f"Doc. {parts[-2]}-{parts[-1]}"
        return title
    elif '-' in title:
        return f"Doc. {title}"
    return title

def extract_date_from_content(content):
    """Try to extract filing date from document content"""
    # Look for "Filed MM/DD/YY" pattern
    match = re.search(r'Filed\s+(\d{1,2}/\d{1,2}/\d{2,4})', content)
    if match:
        return match.group(1)

    # Look for other date patterns
    match = re.search(r'Date[d]?:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', content, re.IGNORECASE)
    if match:
        return match.group(1)

    return None

def extract_page_numbers(content, search_term):
    """Extract page numbers where a term appears"""
    pages = set()
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if search_term.lower() in line.lower():
            # Look backwards for page number
            for j in range(max(0, i-10), i):
                page_match = re.search(r'Page\s+(\d+)', lines[j], re.IGNORECASE)
                if page_match:
                    pages.add(page_match.group(1))
                    break

    return sorted(pages, key=int) if pages else []

def build_source_table(documents):
    """Build the source document table"""
    table_rows = []

    for doc in documents:
        title = doc['title']
        created = doc['created']
        content = doc['content'][:1000]  # Preview

        ecf_no = parse_ecf_number(title)
        filed_date = extract_date_from_content(content) or created

        # Try to determine document description
        if 'deposition' in content.lower():
            desc = "Deposition"
        elif 'affidavit' in content.lower():
            desc = "Affidavit"
        elif 'exhibit' in content.lower():
            desc = "Exhibit"
        elif 'flight' in content.lower() and 'log' in content.lower():
            desc = "Flight Logs"
        elif 'motion' in content.lower():
            desc = "Motion"
        else:
            desc = "Court Filing"

        # Determine Epstein reference type
        content_lower = content.lower()
        if 'testimony' in content_lower or 'deposition' in content_lower:
            epstein_ref = "Testimony regarding Epstein"
        elif 'victim' in content_lower or 'abuse' in content_lower:
            epstein_ref = "Allegations of abuse"
        elif 'flight' in content_lower:
            epstein_ref = "Travel records"
        else:
            epstein_ref = "Direct reference"

        table_rows.append({
            'ecf_no': ecf_no,
            'filed': filed_date,
            'description': desc,
            'reference': epstein_ref,
            'raw_title': title
        })

    return table_rows

def extract_criminal_conduct_info(documents):
    """Extract information about Epstein's criminal conduct"""
    findings = []

    for doc in documents:
        content = doc['content']
        title = doc['title']

        # Look for criminal allegations
        if 'sexual' in content.lower() and ('minor' in content.lower() or 'underage' in content.lower()):
            # Extract relevant passages
            lines = content.split('\n')
            for i, line in enumerate(lines):
                line_lower = line.lower()
                if ('epstein' in line_lower and
                    any(term in line_lower for term in ['sexual', 'massage', 'abuse', 'victim', 'minor'])):

                    # Get context (5 lines before and after)
                    context_start = max(0, i-5)
                    context_end = min(len(lines), i+6)
                    context = '\n'.join(lines[context_start:context_end])

                    findings.append({
                        'doc': title,
                        'snippet': context[:500],
                        'category': 'criminal_conduct'
                    })
                    break  # One per document

    return findings

def extract_npa_info(documents):
    """Extract information about 2008 NPA"""
    findings = []

    for doc in documents:
        content = doc['content']
        title = doc['title']

        if any(term in content.lower() for term in ['non-prosecution', 'npa', 'plea deal', 'acosta']):
            lines = content.split('\n')
            for i, line in enumerate(lines):
                line_lower = line.lower()
                if any(term in line_lower for term in ['non-prosecution', 'npa', 'plea']):
                    context_start = max(0, i-5)
                    context_end = min(len(lines), i+6)
                    context = '\n'.join(lines[context_start:context_end])

                    findings.append({
                        'doc': title,
                        'snippet': context[:500],
                        'category': 'npa'
                    })
                    break

    return findings

def extract_network_info(documents):
    """Extract information about Epstein's network"""
    findings = defaultdict(list)

    key_associates = {
        'Ghislaine Maxwell': ['maxwell', 'ghislaine'],
        'Prince Andrew': ['prince andrew', 'andrew'],
        'Bill Clinton': ['clinton', 'bill clinton'],
        'Alan Dershowitz': ['dershowitz', 'alan dershowitz'],
        'Jean-Luc Brunel': ['brunel', 'jean-luc'],
        'Sarah Kellen': ['kellen', 'sarah kellen'],
        'Nadia Marcinkova': ['marcinkova', 'nadia']
    }

    for doc in documents:
        content = doc['content']
        title = doc['title']
        content_lower = content.lower()

        for person, terms in key_associates.items():
            if any(term in content_lower for term in terms):
                # Find relevant passage
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    line_lower = line.lower()
                    if any(term in line_lower for term in terms):
                        context_start = max(0, i-3)
                        context_end = min(len(lines), i+4)
                        context = '\n'.join(lines[context_start:context_end])

                        findings[person].append({
                            'doc': title,
                            'snippet': context[:400]
                        })
                        break

    return findings

def extract_death_info(documents):
    """Extract information about Epstein's death"""
    findings = []

    for doc in documents:
        content = doc['content']
        title = doc['title']

        if any(term in content.lower() for term in ['death', 'died', 'suicide', 'mcc', 'autopsy']):
            lines = content.split('\n')
            for i, line in enumerate(lines):
                line_lower = line.lower()
                if 'epstein' in line_lower and any(term in line_lower for term in ['death', 'died', 'suicide']):
                    context_start = max(0, i-5)
                    context_end = min(len(lines), i+6)
                    context = '\n'.join(lines[context_start:context_end])

                    findings.append({
                        'doc': title,
                        'snippet': context[:500]
                    })
                    break

    return findings

def main():
    prep_file = '/continuum/entity_data/dossier_prep_Jeffrey_Epstein.json'
    output_file = '/continuum/reports/epstein_dossier_data.json'

    print("Loading prep file...")
    prep_data = load_prep_file(prep_file)

    documents = prep_data.get('documents', [])
    print(f"Processing {len(documents)} documents...")

    # Build source table
    print("\nBuilding source table...")
    source_table = build_source_table(documents)

    # Extract criminal conduct info
    print("Extracting criminal conduct information...")
    criminal_info = extract_criminal_conduct_info(documents)

    # Extract NPA info
    print("Extracting NPA information...")
    npa_info = extract_npa_info(documents)

    # Extract network info
    print("Extracting network information...")
    network_info = extract_network_info(documents)

    # Extract death info
    print("Extracting death information...")
    death_info = extract_death_info(documents)

    # Compile all data
    dossier_data = {
        'entity_name': prep_data.get('entity_name'),
        'document_count': len(documents),
        'source_table': source_table,
        'criminal_conduct': criminal_info[:20],  # Top 20
        'npa': npa_info[:10],  # Top 10
        'network': {k: v[:5] for k, v in network_info.items()},  # Top 5 per person
        'death': death_info[:5]
    }

    # Save extracted data
    with open(output_file, 'w') as f:
        json.dump(dossier_data, f, indent=2)

    print(f"\nDossier data saved to {output_file}")
    print(f"\nSummary:")
    print(f"  Source documents: {len(source_table)}")
    print(f"  Criminal conduct refs: {len(criminal_info)}")
    print(f"  NPA refs: {len(npa_info)}")
    print(f"  Network associates: {len(network_info)}")
    print(f"  Death refs: {len(death_info)}")

if __name__ == '__main__':
    main()
