#!/usr/bin/env python3
"""
Entity Index Consolidator
Aggregates entities from multiple extraction markdown files
Performs deduplication and quality filtering
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class EntityConsolidator:
    def __init__(self):
        self.entities = {
            'people': defaultdict(lambda: {'mentions': 0, 'sources': set(), 'contexts': []}),
            'organizations': defaultdict(lambda: {'mentions': 0, 'sources': set(), 'contexts': []}),
            'locations': defaultdict(lambda: {'mentions': 0, 'sources': set(), 'contexts': []}),
            'cases': defaultdict(lambda: {'mentions': 0, 'sources': set(), 'contexts': []})
        }

        # Quality filters - patterns to exclude
        self.exclude_patterns = [
            r'^And\s',
            r'^At\s',
            r'^Between\s',
            r'^Besides\s',
            r'^But\s',
            r'^Did\s',
            r'^For\s',
            r'^From\s',
            r'^In\s',
            r'^On\s',
            r'^Only\s',
            r'^So\s',
            r'^That\s',
            r'^The\s',
            r'^To\s',
            r'^Was\s',
            r'^When\s',
            r'^Where\s',
            r'^Which\s',
            r'^Who\s',
            r'^With\s',
            r'^Would\s',
            r'^\s*$',
            r'^[0-9/]+$',  # Just dates
            r'Exhibit\s*\d+',
            r'Page\s*\d+',
            r'Document\s*\d+',
            r'Commission\s+(No|Expires)',
            r'Certified\s+',
            r'Deposition\s+',
            r'Case\s+\d+',
            r'^\w{1,2}$',  # Single/two letter entries
        ]

        # Known good entities (from existing briefs)
        self.verified_entities = {
            'people': {
                'Alan Dershowitz', 'Allison Mack', 'Bill Clinton', 'Clare Bronfman',
                'Donald Trump', 'Emmy Taylor', 'Ghislaine Maxwell', 'Glenn Dubin',
                'Jean Luc Brunel', 'Jean-Luc Brunel', 'Jeffrey Epstein', 'Johanna Sjoberg',
                'Juan Alessi', 'Keith Raniere', 'Lesley Groff', 'Les Wexner',
                'Leslie Wexner', 'Meyer Lansky', 'Nadia Marcinkova', 'Oliver North',
                'Prince Andrew', 'Robert Maxwell', 'Roy Cohn', 'Sarah Kellen',
                'Virginia Giuffre', 'Virginia Roberts', 'William Casey',
                'Al Gore', 'Bill Richardson', 'Brad Edwards', 'Cameron Diaz',
                'Cate Blanchett', 'David Copperfield', 'Detective Recarey',
                'Ehud Barak', 'George Lucas', 'John Connelly', 'Kevin Spacey',
                'Marvin Minsky', 'Michael Jackson', 'Naomi Campbell',
                'Paul Cassell', 'Tom Pritzker', 'Wendy Leigh',
                'Audrey Strauss', 'Jes Staley',
            },
            'organizations': {
                'BCCI', 'CIA', 'Deutsche Bank', 'FBI', 'JPMorgan', 'JPMorgan Chase',
                'Mossad', 'NXIVM', 'Terramar Project', 'Maxwell Family Network',
                'Boies Schiller', 'Palm Beach Police', 'United States District Court',
                'Southern District of New York', 'OCC', 'NYSDFS', 'FCA', 'DOJ',
                'Department of Justice',
            },
            'locations': {
                'Manhattan', 'New York', 'Palm Beach', 'Virgin Islands',
                'Little St. James', 'Santa Fe', 'New Mexico', 'London',
                'Florida', 'England', 'Paris', 'Little Saint James',
            }
        }

    def is_quality_entity(self, entity_name: str, entity_type: str) -> bool:
        """Filter out low-quality entity extractions"""

        # Check verified entities first
        if entity_name in self.verified_entities.get(entity_type, set()):
            return True

        # Apply exclusion patterns
        for pattern in self.exclude_patterns:
            if re.match(pattern, entity_name, re.IGNORECASE):
                return False

        # Must have at least one capital letter and be 3+ chars
        if len(entity_name) < 3:
            return False

        # Should start with capital letter or be all caps (acronym)
        if not (entity_name[0].isupper() or entity_name.isupper()):
            return False

        return True

    def normalize_entity_name(self, name: str) -> str:
        """Normalize entity names for deduplication"""
        # Common variations
        normalizations = {
            'Virginia Roberts': 'Virginia Giuffre',
            'Jeffrey E. Epstein': 'Jeffrey Epstein',
            'Jeffrey E Epstein': 'Jeffrey Epstein',
            'Ghislaine Noelle Marion Maxwell': 'Ghislaine Maxwell',
            'Prince Andrew Duke of York': 'Prince Andrew',
            'Jean Luc Brunel': 'Jean-Luc Brunel',
            'Leslie Wexner': 'Les Wexner',
            'Governor Bill Richardson': 'Bill Richardson',
            'Minister Ehud Barak': 'Ehud Barak',
            'JPMorgan Chase': 'JPMorgan',
            'JP Morgan': 'JPMorgan',
            'Little Saint James': 'Little St. James',
            'U.S. Virgin Islands': 'Virgin Islands',
            'USVI': 'Virgin Islands',
        }

        return normalizations.get(name, name)

    def parse_extraction_md(self, filepath: Path) -> Dict:
        """Parse a markdown extraction file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        result = {
            'source': '',
            'people': [],
            'organizations': [],
            'locations': []
        }

        # Extract source file path
        source_match = re.search(r'\*\*Source:\*\*\s*(.+)', content)
        if source_match:
            result['source'] = source_match.group(1).strip()

        # Extract people
        people_section = re.search(r'### People \((\d+)\)\n(.*?)(?=###|##|$)', content, re.DOTALL)
        if people_section:
            people_text = people_section.group(2)
            result['people'] = [p.strip('- ').strip() for p in people_text.split('\n') if p.strip().startswith('-')]

        # Extract organizations
        org_section = re.search(r'### Organizations \((\d+)\)\n(.*?)(?=###|##|$)', content, re.DOTALL)
        if org_section:
            org_text = org_section.group(2)
            result['organizations'] = [o.strip('- ').strip() for o in org_text.split('\n') if o.strip().startswith('-')]

        # Extract locations
        loc_section = re.search(r'### Locations \((\d+)\)\n(.*?)(?=###|##|$)', content, re.DOTALL)
        if loc_section:
            loc_text = loc_section.group(2)
            result['locations'] = [l.strip('- ').strip() for l in loc_text.split('\n') if l.strip().startswith('-')]

        return result

    def add_entity(self, entity_type: str, name: str, source: str):
        """Add entity to consolidated index"""
        # Normalize name
        normalized = self.normalize_entity_name(name)

        # Quality check
        if not self.is_quality_entity(normalized, entity_type):
            return

        # Add to index
        self.entities[entity_type][normalized]['mentions'] += 1
        self.entities[entity_type][normalized]['sources'].add(source)

    def process_directory(self, directory: Path):
        """Process all extraction markdown files in a directory"""
        md_files = list(directory.glob('*.md'))
        # Exclude _summary and other meta files
        md_files = [f for f in md_files if not f.name.startswith('_')]

        print(f"Processing {len(md_files)} files from {directory.name}...")

        for md_file in md_files:
            data = self.parse_extraction_md(md_file)
            source = data['source'] or str(md_file.name)

            for person in data['people']:
                self.add_entity('people', person, source)

            for org in data['organizations']:
                self.add_entity('organizations', org, source)

            for loc in data['locations']:
                self.add_entity('locations', loc, source)

    def get_sorted_entities(self, entity_type: str) -> List[Tuple[str, Dict]]:
        """Get sorted list of entities by mention count"""
        entities = []
        for name, data in self.entities[entity_type].items():
            entities.append((name, {
                'mentions': data['mentions'],
                'sources': sorted(list(data['sources'])),
                'source_count': len(data['sources'])
            }))

        # Sort by mention count descending
        entities.sort(key=lambda x: x[1]['mentions'], reverse=True)
        return entities

    def generate_report(self) -> str:
        """Generate consolidated entity report"""
        report = []
        report.append("# CONSOLIDATED ENTITY EXTRACTION REPORT")
        report.append(f"**Generated:** 2025-12-24")
        report.append("")

        for entity_type in ['people', 'organizations', 'locations']:
            entities = self.get_sorted_entities(entity_type)
            report.append(f"## {entity_type.upper()} ({len(entities)} unique)")
            report.append("")

            for name, data in entities:
                report.append(f"### {name}")
                report.append(f"- **Mentions:** {data['mentions']} across {data['source_count']} documents")
                if len(data['sources']) <= 5:
                    report.append(f"- **Sources:** {', '.join(data['sources'])}")
                else:
                    report.append(f"- **Sources:** {', '.join(data['sources'][:5])} ... (+{len(data['sources'])-5} more)")
                report.append("")

        return '\n'.join(report)

    def export_json(self, filepath: Path):
        """Export entities to JSON"""
        export_data = {}
        for entity_type in ['people', 'organizations', 'locations', 'cases']:
            export_data[entity_type] = {}
            for name, data in self.entities[entity_type].items():
                export_data[entity_type][name] = {
                    'mentions': data['mentions'],
                    'sources': sorted(list(data['sources'])),
                    'source_count': len(data['sources'])
                }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)

if __name__ == '__main__':
    consolidator = EntityConsolidator()

    # Process Phase 1 extractions
    base_path = Path('C:/Users/Xx LilMan xX/Documents/Claude Docs/Continuum/work/epstein-extraction/findings')

    # Court filings
    court_filings = base_path / 'court-filings'
    if court_filings.exists():
        consolidator.process_directory(court_filings)

    # Criminal case
    criminal_case = base_path / 'criminal-case'
    if criminal_case.exists():
        consolidator.process_directory(criminal_case)

    # Generate outputs
    output_dir = Path('C:/Users/Xx LilMan xX/Documents/Claude Docs/Continuum/work/tasks')

    # Markdown report
    report = consolidator.generate_report()
    with open(output_dir / 'consolidated_entities_phase1.md', 'w', encoding='utf-8') as f:
        f.write(report)

    # JSON export
    consolidator.export_json(output_dir / 'consolidated_entities_phase1.json')

    # Print summary
    print("\n=== CONSOLIDATION COMPLETE ===")
    for entity_type in ['people', 'organizations', 'locations']:
        count = len(consolidator.entities[entity_type])
        print(f"{entity_type.capitalize()}: {count} unique entities")
