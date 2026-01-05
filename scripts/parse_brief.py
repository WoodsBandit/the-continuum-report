#!/usr/bin/env python3
"""
parse_brief.py - Parse an analytical brief markdown file and extract structured data
Version 2.0 - Refactored with Shared Library

Usage:
    python parse_brief.py <path_to_brief.md>

Output:
    JSON object with entity data suitable for the Continuum knowledge graph

Changes in v2.0:
- Structured logging with structlog (lib.logging_config)
- Better error handling
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Import shared library for logging
from lib import get_logger

# Initialize logger
logger = get_logger(__name__)

# Known entities for cross-referencing (built from existing briefs)
KNOWN_ENTITIES = {
    # Person names -> entity IDs
    "Jeffrey Epstein": "jeffrey-epstein",
    "Epstein": "jeffrey-epstein",
    "Jeffrey E. Epstein": "jeffrey-epstein",
    "Jeffrey Edward Epstein": "jeffrey-epstein",

    "Ghislaine Maxwell": "ghislaine-maxwell",
    "Maxwell": "ghislaine-maxwell",
    "Ms. Maxwell": "ghislaine-maxwell",
    "G. Maxwell": "ghislaine-maxwell",

    "Virginia Giuffre": "virginia-giuffre",
    "Virginia Roberts": "virginia-giuffre",
    "Giuffre": "virginia-giuffre",
    "Virginia L. Giuffre": "virginia-giuffre",
    "Virginia Roberts Giuffre": "virginia-giuffre",
    "Ms. Giuffre": "virginia-giuffre",

    "Bill Clinton": "bill-clinton",
    "President Clinton": "bill-clinton",
    "Clinton": "bill-clinton",
    "William Clinton": "bill-clinton",

    "Donald Trump": "donald-trump",
    "Trump": "donald-trump",
    "President Trump": "donald-trump",

    "Prince Andrew": "prince-andrew",
    "Duke of York": "prince-andrew",
    "Andrew": "prince-andrew",

    "Alan Dershowitz": "alan-dershowitz",
    "Dershowitz": "alan-dershowitz",
    "Professor Dershowitz": "alan-dershowitz",

    "Glenn Dubin": "glenn-dubin",
    "Dubin": "glenn-dubin",

    "Sarah Kellen": "sarah-kellen",
    "Kellen": "sarah-kellen",
    "Sarah Kensington": "sarah-kellen",

    "Nadia Marcinkova": "nadia-marcinkova",
    "Marcinkova": "nadia-marcinkova",
    "Nadia Marcinko": "nadia-marcinkova",

    "Lesley Groff": "lesley-groff",
    "Groff": "lesley-groff",
    "Les Groff": "lesley-groff",

    "Emmy Taylor": "emmy-taylor",
    "Taylor": "emmy-taylor",
    "Emmy Tayler": "emmy-taylor",

    # Organizations
    "The Terramar Project": "terramar-project",
    "Terramar Project": "terramar-project",
    "Terramar": "terramar-project",

    # Cases
    "Giuffre v. Maxwell": "giuffre-v-maxwell-case",
    "Giuffre v Maxwell": "giuffre-v-maxwell-case",
    "15-cv-07433": "giuffre-v-maxwell-case",

    "Epstein Florida Case": "epstein-florida-case",
    "Florida case": "epstein-florida-case",
    "2008 NPA": "epstein-florida-case",
    "non-prosecution agreement": "epstein-florida-case",
}

# Entity ID to canonical name mapping
ENTITY_NAMES = {
    "jeffrey-epstein": "Jeffrey Epstein",
    "ghislaine-maxwell": "Ghislaine Maxwell",
    "virginia-giuffre": "Virginia Giuffre",
    "bill-clinton": "Bill Clinton",
    "donald-trump": "Donald Trump",
    "prince-andrew": "Prince Andrew",
    "alan-dershowitz": "Alan Dershowitz",
    "glenn-dubin": "Glenn Dubin",
    "sarah-kellen": "Sarah Kellen",
    "nadia-marcinkova": "Nadia Marcinkova",
    "lesley-groff": "Lesley Groff",
    "emmy-taylor": "Emmy Taylor",
    "terramar-project": "The Terramar Project",
    "giuffre-v-maxwell-case": "Giuffre v. Maxwell Civil Case",
    "epstein-florida-case": "Epstein Florida Case",
}


def extract_entity_id_from_filename(filename: str) -> str:
    """Generate entity ID from filename like analytical_brief_jeffrey_epstein.md"""
    name = Path(filename).stem
    # Remove 'analytical_brief_' prefix
    name = re.sub(r'^analytical_brief_', '', name)
    # Convert underscores to hyphens
    return name.replace('_', '-')


def detect_entity_type(filename: str, content: str) -> str:
    """Detect entity type from filename pattern and content"""
    filename_lower = filename.lower()

    # Check filename patterns
    if '_case' in filename_lower or 'case' in filename_lower:
        return 'case'
    if 'project' in filename_lower or 'organization' in filename_lower:
        return 'organization'

    # Check content for organization indicators
    if '(nonprofit organization)' in content.lower():
        return 'organization'
    if 'Case No.' in content or 'civil case' in content.lower():
        # Check if subject line indicates a case
        subject_match = re.search(r'\*\*Subject\*\*\s*\|\s*\*([^*]+)\*', content)
        if subject_match and ' v. ' in subject_match.group(1):
            return 'case'

    return 'person'


def extract_title(content: str) -> str:
    """Extract the main title (# Heading)"""
    match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "Unknown"


def extract_document_classification(content: str) -> dict:
    """Extract fields from the Document Classification table"""
    classification = {
        'subject': None,
        'status': None,
        'document_type': None,
        'sources': None,
        'case_no': None,
    }

    # Find the Document Classification section
    section_match = re.search(
        r'## Document Classification\s*\n+\|[^\n]+\|[^\n]+\|\s*\n\|[-|]+\|\s*\n((?:\|[^\n]+\|\s*\n)+)',
        content
    )

    if not section_match:
        return classification

    table_content = section_match.group(1)

    # Parse each row
    for line in table_content.strip().split('\n'):
        # Clean up the line
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 2:
            key = cells[0].replace('**', '').lower().strip()
            value = cells[1].strip()

            if 'subject' in key:
                classification['subject'] = value
            elif 'status' in key:
                classification['status'] = value
            elif 'document type' in key:
                classification['document_type'] = value
            elif 'sources' in key or 'source' in key:
                classification['sources'] = value
            elif 'case no' in key:
                classification['case_no'] = value

    return classification


def extract_executive_summary(content: str) -> str:
    """Extract the Executive Summary section"""
    # Find Executive Summary section
    match = re.search(
        r'## Executive Summary\s*\n+\*\*Editorial Assessment:\*\*\s*(.+?)(?=\n---|\n## )',
        content,
        re.DOTALL
    )

    if match:
        summary = match.group(1).strip()
        # Clean up markdown formatting
        summary = re.sub(r'\s+', ' ', summary)
        return summary

    return ""


def extract_source_documents(content: str) -> list:
    """Extract source document citations from Source Documents table"""
    sources = []

    # Find Source Documents section
    section_match = re.search(
        r'## Source Documents\s*\n+.*?\n\|[^\n]+\|\s*\n\|[-|]+\|\s*\n((?:\|[^\n]+\|\s*\n)+)',
        content,
        re.DOTALL
    )

    if not section_match:
        return sources

    table_content = section_match.group(1)

    for line in table_content.strip().split('\n'):
        cells = [c.strip() for c in line.split('|') if c.strip()]
        if len(cells) >= 2:
            ecf_num = cells[0].strip()

            # Handle different table formats
            if len(cells) >= 3:
                # Format: ECF # | Filed | Description
                filed_date = cells[1] if len(cells) > 2 else None
                description = cells[2] if len(cells) > 2 else cells[1]
            else:
                # Format: Document | Description
                filed_date = None
                description = cells[1]

            # Extract ECF document number
            ecf_match = re.search(r'(?:ECF\s*)?(?:Doc\.?\s*)?(\d+(?:-\d+)?)', ecf_num)
            if ecf_match:
                sources.append({
                    'ecf': ecf_match.group(1),
                    'description': description,
                    'filed': filed_date,
                })

    return sources


def extract_ecf_citations(content: str) -> list:
    """Find all ECF document citations in the content"""
    # Pattern for ECF Doc. XXXX-XX citations
    pattern = r'ECF\s+Doc\.?\s*(\d+(?:-\d+)?)'

    matches = re.findall(pattern, content, re.IGNORECASE)
    return list(set(matches))  # Remove duplicates


def find_entity_mentions(content: str, self_id: str) -> dict:
    """Find mentions of other known entities in the content"""
    mentions = {}

    # Sections for weighting
    public_record_match = re.search(
        r'## The Public Record\s*\n(.+?)(?=\n## )',
        content,
        re.DOTALL
    )
    editorial_match = re.search(
        r'## Editorial Analysis\s*\n(.+?)(?=\n## )',
        content,
        re.DOTALL
    )

    public_record = public_record_match.group(1) if public_record_match else ""
    editorial = editorial_match.group(1) if editorial_match else ""
    other_content = content

    for name, entity_id in KNOWN_ENTITIES.items():
        # Skip self-references
        if entity_id == self_id:
            continue

        # Skip very short names that could cause false positives
        if len(name) <= 4 and name.lower() in ['trump', 'dubin']:
            # Use word boundary matching for short names
            pattern = r'\b' + re.escape(name) + r'\b'
        else:
            pattern = re.escape(name)

        # Count mentions in different sections
        public_count = len(re.findall(pattern, public_record, re.IGNORECASE))
        editorial_count = len(re.findall(pattern, editorial, re.IGNORECASE))
        total_count = len(re.findall(pattern, content, re.IGNORECASE))
        other_count = total_count - public_count - editorial_count

        if total_count > 0:
            # Calculate weighted score
            # Public Record = 3x weight, Editorial = 2x, Other = 1x
            weight = (public_count * 3) + (editorial_count * 2) + (other_count * 1)

            if entity_id not in mentions or mentions[entity_id]['weight'] < weight:
                mentions[entity_id] = {
                    'count': total_count,
                    'weight': weight,
                    'in_public_record': public_count > 0,
                    'in_editorial': editorial_count > 0,
                }

    return mentions


def determine_connection_strength_DEPRECATED(mention_data: dict) -> str:
    """
    DEPRECATED: Determine connection strength based on mention context.

    DEPRECATED as of 2026-01:
    The binary connection model eliminates subjective strength scoring.
    Connections exist (in a brief) or they don't. No scoring.

    Use: python scripts/build_connections_from_briefs.py

    Keeping this code for backwards compatibility only.
    """
    if mention_data['in_public_record']:
        return 'documented'
    elif mention_data['in_editorial']:
        return 'interpreted'
    else:
        return 'referenced'


def parse_brief(filepath: str) -> dict:
    """Main function to parse an analytical brief and return structured JSON"""

    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Brief not found: {filepath}")

    content = path.read_text(encoding='utf-8')
    filename = path.name

    # Extract basic info
    entity_id = extract_entity_id_from_filename(filename)
    title = extract_title(content)
    entity_type = detect_entity_type(filename, content)

    # Extract document classification
    classification = extract_document_classification(content)

    # Extract summary
    summary = extract_executive_summary(content)

    # Extract source documents
    sources = extract_source_documents(content)

    # Find all ECF citations
    ecf_citations = extract_ecf_citations(content)

    # Find mentions of other entities
    mentions_data = find_entity_mentions(content, entity_id)

    # Build mentions list (sorted by weight)
    mentions = sorted(mentions_data.keys(), key=lambda x: -mentions_data[x]['weight'])

    # Build output structure
    result = {
        'id': entity_id,
        'name': title,
        'type': entity_type,
        'status': classification.get('status') or 'Unknown',
        'summary': summary[:500] + '...' if len(summary) > 500 else summary,
        'full_summary': summary,
        'brief_file': filename,
        'brief_url': f'/briefs/{entity_id}.html',
        'document_type': classification.get('document_type'),
        'primary_sources': classification.get('sources'),
        'sources': sources,
        'ecf_citations': ecf_citations,
        'mentions': mentions,
        'mention_details': {
            eid: {
                'count': data['count'],
                'in_public_record': data.get('in_public_record', False),
                'in_editorial': data.get('in_editorial', False),
                # NOTE: No 'strength' field - binary model only
            }
            for eid, data in mentions_data.items()
        },
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'parsed_from': str(path.absolute()),
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_brief.py <path_to_brief.md>")
        print("\nExample:")
        print("  python parse_brief.py /continuum/briefs/analytical_brief_jeffrey_epstein.md")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        result = parse_brief(filepath)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error parsing brief: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
