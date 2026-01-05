#!/usr/bin/env python3
"""
Epstein Document Extraction Script
Extracts entities, dates, quotes from PDF documents
"""

import fitz  # PyMuPDF
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = Path(pdf_path)
        self.doc = None
        self.text = ""
        self.entities = {
            'people': set(),
            'organizations': set(),
            'locations': set()
        }
        self.dates = []
        self.quotes = []

    def extract_text(self):
        """Extract all text from PDF"""
        try:
            self.doc = fitz.open(str(self.pdf_path))
            pages_text = []
            for page_num, page in enumerate(self.doc, 1):
                text = page.get_text()
                pages_text.append({
                    'page': page_num,
                    'text': text
                })
            self.text = "\n".join([p['text'] for p in pages_text])
            return pages_text
        except Exception as e:
            print(f"Error extracting text: {e}", file=sys.stderr)
            return []

    def extract_entities(self):
        """Extract named entities"""
        # Common Epstein-related names to look for
        known_names = [
            'Jeffrey Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre', 'Virginia Roberts',
            'Prince Andrew', 'Alan Dershowitz', 'Bill Clinton', 'Donald Trump',
            'Jean-Luc Brunel', 'Sarah Kellen', 'Nadia Marcinkova', 'Lesley Groff',
            'Adriana Ross', 'Emmy Tayler', 'Haley Robson', 'Rachel Chandler',
            'Eva Dubin', 'Glenn Dubin', 'Les Wexner', 'Marvin Minsky',
            'Bill Richardson', 'George Mitchell', 'Ron Burkle', 'Ehud Barak',
            'Leslie Wexner', 'Steven Hoffenberg', 'Jes Staley', 'JPMorgan',
            'Deutsche Bank', 'Southern Trust Company', 'JEGE', 'Hyperion Air',
            'Little St. James', 'Great St. James', 'Palm Beach', 'New York',
            'New Mexico', 'Paris', 'London', 'Virgin Islands', 'Manhattan',
            'Lolita Express', 'Mar-a-Lago', 'Interlochen', 'Zorro Ranch'
        ]

        # Find all instances
        for name in known_names:
            if re.search(r'\b' + re.escape(name) + r'\b', self.text, re.IGNORECASE):
                if any(org_word in name for org_word in ['Bank', 'Company', 'Trust', 'Air', 'JEGE']):
                    self.entities['organizations'].add(name)
                elif any(loc_word in name for loc_word in ['Island', 'Beach', 'York', 'Paris', 'London', 'Mexico', 'Express', 'Mar-a-Lago', 'Ranch', 'Manhattan']):
                    self.entities['locations'].add(name)
                else:
                    self.entities['people'].add(name)

        # Find capitalized names (potential people)
        name_pattern = r'\b([A-Z][a-z]+ [A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\b'
        found_names = re.findall(name_pattern, self.text)
        for name in found_names:
            if len(name.split()) >= 2 and name not in self.entities['people']:
                # Filter out common false positives
                if not any(word in name for word in ['United States', 'New York', 'Southern District']):
                    self.entities['people'].add(name)

    def extract_dates(self):
        """Extract dates and associated events"""
        # Date patterns
        patterns = [
            r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b',  # MM/DD/YYYY or M/D/YY
            r'\b(\d{1,2}-\d{1,2}-\d{2,4})\b',  # MM-DD-YYYY
            r'\b([A-Z][a-z]+ \d{1,2},? \d{4})\b',  # Month DD, YYYY
            r'\b(\d{4}-\d{2}-\d{2})\b'  # YYYY-MM-DD
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, self.text)
            for match in matches:
                date_str = match.group(1)
                # Get context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(self.text), match.end() + 50)
                context = self.text[start:end].replace('\n', ' ')
                self.dates.append({
                    'date': date_str,
                    'context': context.strip()
                })

    def extract_quotes(self, pages_text):
        """Extract significant quotes"""
        quote_pattern = r'"([^"]{20,300})"'

        for page_info in pages_text:
            matches = re.finditer(quote_pattern, page_info['text'])
            for match in matches:
                quote_text = match.group(1)
                # Filter out form text and boilerplate
                if not any(skip in quote_text.lower() for skip in ['page', 'exhibit', 'plaintiff', 'defendant']):
                    self.quotes.append({
                        'quote': quote_text,
                        'page': page_info['page']
                    })

    def generate_report(self, output_path):
        """Generate markdown report"""
        report = f"""# {self.pdf_path.name}

**Source:** {self.pdf_path}
**Pages:** {len(self.doc) if self.doc else 0}
**Processed:** {datetime.now().isoformat()}

## Entities Found

### People ({len(self.entities['people'])})
"""
        for person in sorted(self.entities['people']):
            report += f"- {person}\n"

        report += f"\n### Organizations ({len(self.entities['organizations'])})\n"
        for org in sorted(self.entities['organizations']):
            report += f"- {org}\n"

        report += f"\n### Locations ({len(self.entities['locations'])})\n"
        for loc in sorted(self.entities['locations']):
            report += f"- {loc}\n"

        report += f"\n## Timeline Events ({len(self.dates)})\n"
        for date_info in self.dates[:50]:  # Limit to first 50
            report += f"- **{date_info['date']}**: {date_info['context']}\n"

        report += f"\n## Key Quotes ({len(self.quotes)})\n"
        for quote_info in self.quotes[:20]:  # Limit to first 20
            report += f"> \"{quote_info['quote']}\" — Page {quote_info['page']}\n\n"

        report += "\n## Summary\n"
        report += f"Document contains {len(self.entities['people'])} unique people, "
        report += f"{len(self.entities['organizations'])} organizations, "
        report += f"{len(self.entities['locations'])} locations, "
        report += f"{len(self.dates)} dated events, and {len(self.quotes)} quotes.\n"

        # Write report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return report

    def process(self, output_path):
        """Main processing pipeline"""
        print(f"Processing: {self.pdf_path.name}")
        pages_text = self.extract_text()
        if not pages_text:
            print(f"Failed to extract text from {self.pdf_path.name}")
            return None

        self.extract_entities()
        self.extract_dates()
        self.extract_quotes(pages_text)

        report = self.generate_report(output_path)
        print(f"[OK] Completed: {self.pdf_path.name} -> {output_path}")

        return {
            'file': str(self.pdf_path),
            'pages': len(self.doc),
            'people': len(self.entities['people']),
            'orgs': len(self.entities['organizations']),
            'locations': len(self.entities['locations']),
            'dates': len(self.dates),
            'quotes': len(self.quotes)
        }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_pdf.py <input_pdf> <output_md>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    extractor = PDFExtractor(input_file)
    result = extractor.process(output_file)

    if result:
        print(json.dumps(result, indent=2))
