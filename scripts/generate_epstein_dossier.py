#!/usr/bin/env python3
"""
Generate Jeffrey Epstein dossier from prep file
"""

import json
import sys
from datetime import datetime

def load_prep_file(filepath):
    """Load the JSON prep file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_document_metadata(prep_data):
    """Extract document metadata for source table"""
    documents = prep_data.get('documents', [])

    doc_metadata = []
    for doc in documents:
        # Extract ECF number from title
        title = doc.get('title', '')

        # Parse date
        created = doc.get('created', '')

        # Build metadata entry
        doc_metadata.append({
            'ecf_no': title,
            'date': created,
            'title': title,
            'content_preview': doc.get('content', '')[:500] if doc.get('content') else ''
        })

    return doc_metadata

def extract_key_information(prep_data):
    """Extract key information about Epstein from the documents"""

    # This will hold categorized information
    info = {
        'criminal_conduct': [],
        'npa_2008': [],
        'network': [],
        'properties': [],
        'victims_testimony': [],
        'death': [],
        'other': []
    }

    documents = prep_data.get('documents', [])

    for doc in documents:
        content = doc.get('content', '')
        title = doc.get('title', '')

        # Look for key themes in content
        content_lower = content.lower()

        # Criminal conduct
        if any(term in content_lower for term in ['sexual', 'abuse', 'minor', 'trafficking', 'massage', 'victim']):
            info['criminal_conduct'].append({
                'doc': title,
                'content_snippet': content[:2000]
            })

        # NPA references
        if 'npa' in content_lower or 'non-prosecution' in content_lower or '2008' in content:
            info['npa_2008'].append({
                'doc': title,
                'content_snippet': content[:2000]
            })

        # Network/associates
        if any(name in content for name in ['Maxwell', 'Ghislaine', 'Clinton', 'Prince Andrew', 'Dershowitz']):
            info['network'].append({
                'doc': title,
                'content_snippet': content[:2000]
            })

        # Properties
        if any(term in content for term in ['island', 'Palm Beach', 'Manhattan', 'New Mexico', 'Paris']):
            info['properties'].append({
                'doc': title,
                'content_snippet': content[:2000]
            })

    return info

def main():
    prep_file = '/continuum/entity_data/dossier_prep_Jeffrey_Epstein.json'

    print("Loading prep file...")
    prep_data = load_prep_file(prep_file)

    print(f"Entity: {prep_data.get('entity_name')}")
    print(f"Document count: {prep_data.get('document_count')}")
    print(f"Total documents in data: {len(prep_data.get('documents', []))}")

    # Extract metadata
    print("\nExtracting document metadata...")
    doc_metadata = extract_document_metadata(prep_data)
    print(f"Found {len(doc_metadata)} documents")

    # Extract key information
    print("\nExtracting key information...")
    info = extract_key_information(prep_data)

    print(f"Criminal conduct references: {len(info['criminal_conduct'])}")
    print(f"NPA references: {len(info['npa_2008'])}")
    print(f"Network references: {len(info['network'])}")
    print(f"Property references: {len(info['properties'])}")

    # Save extracted info for review
    output = {
        'metadata': doc_metadata,
        'extracted_info': info
    }

    with open('/continuum/reports/epstein_extracted_info.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("\nExtracted info saved to /continuum/reports/epstein_extracted_info.json")

if __name__ == '__main__':
    main()
