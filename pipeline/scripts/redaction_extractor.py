#!/usr/bin/env python3
"""
Redaction Extractor Tool
The Continuum Report

Scans PDFs for "fake" redactions (black boxes with hidden text underneath).
Extracts and reports all hidden text found under visual redaction overlays.

Usage:
    python redaction_extractor.py [--dir PATH] [--output PATH] [--verbose]
"""

import fitz  # PyMuPDF
import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


class RedactionExtractor:
    def __init__(self, output_dir: str = None, verbose: bool = False):
        self.verbose = verbose
        self.output_dir = output_dir or "T:/reports/redaction-extraction"
        self.findings = []
        self.stats = {
            "files_scanned": 0,
            "files_with_hidden_text": 0,
            "total_hidden_segments": 0,
            "errors": 0
        }

    def log(self, msg: str):
        """Print if verbose mode enabled"""
        if self.verbose:
            print(msg)

    def is_black_fill(self, fill) -> bool:
        """Check if fill color is black or near-black"""
        if not fill:
            return False
        if not isinstance(fill, tuple) or len(fill) < 3:
            return False
        return all(c < 0.15 for c in fill[:3])

    def extract_hidden_text(self, pdf_path: str) -> dict:
        """
        Scan a single PDF for hidden text under black boxes.
        Returns dict with findings or None if no hidden text found.
        """
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            self.log(f"  ERROR opening {pdf_path}: {e}")
            self.stats["errors"] += 1
            return None

        file_findings = {
            "file": pdf_path,
            "pages": len(doc),
            "file_size_kb": os.path.getsize(pdf_path) / 1024,
            "hidden_text": []
        }

        try:
            for page_num in range(len(doc)):
                page = doc[page_num]

                # Get all drawings on the page
                try:
                    drawings = page.get_drawings()
                except:
                    continue

                for d in drawings:
                    fill = d.get("fill")
                    if self.is_black_fill(fill):
                        rect = d.get("rect")
                        if rect:
                            try:
                                clip = fitz.Rect(rect)
                                hidden_text = page.get_text("text", clip=clip).strip()

                                # Only record if there's meaningful text (> 2 chars)
                                if hidden_text and len(hidden_text) > 2:
                                    finding = {
                                        "page": page_num + 1,
                                        "rect": [round(x, 2) for x in rect],
                                        "hidden_text": hidden_text,
                                        "char_count": len(hidden_text)
                                    }
                                    file_findings["hidden_text"].append(finding)
                            except:
                                pass

            doc.close()

        except Exception as e:
            self.log(f"  ERROR processing {pdf_path}: {e}")
            self.stats["errors"] += 1
            try:
                doc.close()
            except:
                pass
            return None

        if file_findings["hidden_text"]:
            return file_findings
        return None

    def scan_directory(self, directory: str, recursive: bool = True):
        """Scan a directory for PDFs and extract hidden text"""
        directory = Path(directory)

        if not directory.exists():
            print(f"ERROR: Directory not found: {directory}")
            return

        print(f"Scanning: {directory}")
        print(f"Recursive: {recursive}")
        print("-" * 60)

        # Find all PDFs
        if recursive:
            pdf_files = list(directory.rglob("*.pdf")) + list(directory.rglob("*.PDF"))
        else:
            pdf_files = list(directory.glob("*.pdf")) + list(directory.glob("*.PDF"))

        pdf_files = list(set(pdf_files))  # Remove duplicates
        print(f"Found {len(pdf_files)} PDF files")
        print("-" * 60)

        for i, pdf_path in enumerate(pdf_files):
            self.stats["files_scanned"] += 1

            if self.verbose or (i + 1) % 10 == 0:
                print(f"[{i+1}/{len(pdf_files)}] {pdf_path.name}")

            result = self.extract_hidden_text(str(pdf_path))

            if result:
                self.findings.append(result)
                self.stats["files_with_hidden_text"] += 1
                self.stats["total_hidden_segments"] += len(result["hidden_text"])

                if self.verbose:
                    for h in result["hidden_text"][:3]:
                        print(f"    Page {h['page']}: \"{h['hidden_text'][:50]}...\"")
                    if len(result["hidden_text"]) > 3:
                        print(f"    ... and {len(result['hidden_text']) - 3} more")

    def generate_report(self) -> str:
        """Generate markdown report of findings"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""# Redaction Extraction Report
## The Continuum Report

**Generated:** {timestamp}
**Tool:** redaction_extractor.py

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Files Scanned | {self.stats['files_scanned']} |
| Files with Hidden Text | {self.stats['files_with_hidden_text']} |
| Total Hidden Segments | {self.stats['total_hidden_segments']} |
| Errors | {self.stats['errors']} |

---

## Findings by File

"""

        if not self.findings:
            report += "*No hidden text found under black boxes.*\n"
        else:
            for f in self.findings:
                rel_path = f["file"]
                if "continuum" in rel_path.lower():
                    rel_path = rel_path.split("continuum")[-1]

                report += f"### {os.path.basename(f['file'])}\n\n"
                report += f"**Path:** `{rel_path}`\n"
                report += f"**Pages:** {f['pages']} | **Size:** {f['file_size_kb']:.1f} KB\n"
                report += f"**Hidden segments:** {len(f['hidden_text'])}\n\n"

                report += "| Page | Hidden Text | Chars |\n"
                report += "|------|-------------|-------|\n"

                for h in f["hidden_text"]:
                    # Escape pipe characters and truncate
                    text = h["hidden_text"].replace("|", "\\|").replace("\n", " ")
                    if len(text) > 80:
                        text = text[:77] + "..."
                    report += f"| {h['page']} | {text} | {h['char_count']} |\n"

                report += "\n---\n\n"

        report += """
## Methodology

This tool scans PDF files for:
1. Drawing objects with black or near-black fill colors (RGB < 0.15)
2. Text content within the bounding rectangle of each black box
3. Any text found indicates a "fake" redaction (visual overlay only)

**Legal Note:** Extracted text was present in the original document.
The black boxes were visual overlays that did not actually remove the underlying text.

---

*The Continuum Report — Another Node in the Decentralized Intelligence Agency*
"""

        return report

    def save_results(self):
        """Save report and raw JSON data"""
        os.makedirs(self.output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save markdown report
        report_path = os.path.join(self.output_dir, f"redaction_report_{timestamp}.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(self.generate_report())
        print(f"\nReport saved: {report_path}")

        # Save raw JSON
        json_path = os.path.join(self.output_dir, f"redaction_data_{timestamp}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": timestamp,
                "stats": self.stats,
                "findings": self.findings
            }, f, indent=2)
        print(f"JSON data saved: {json_path}")

        return report_path, json_path


def main():
    parser = argparse.ArgumentParser(description="Extract hidden text from fake PDF redactions")
    parser.add_argument("--dir", "-d", type=str, default="T:/website/sources",
                        help="Directory to scan (default: T:/website/sources)")
    parser.add_argument("--output", "-o", type=str, default="T:/reports/redaction-extraction",
                        help="Output directory for reports")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    parser.add_argument("--no-recursive", action="store_true",
                        help="Don't scan subdirectories")

    args = parser.parse_args()

    print("=" * 60)
    print("REDACTION EXTRACTOR")
    print("The Continuum Report")
    print("=" * 60)
    print()

    extractor = RedactionExtractor(
        output_dir=args.output,
        verbose=args.verbose
    )

    extractor.scan_directory(
        args.dir,
        recursive=not args.no_recursive
    )

    print()
    print("=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"Files scanned: {extractor.stats['files_scanned']}")
    print(f"Files with hidden text: {extractor.stats['files_with_hidden_text']}")
    print(f"Total hidden segments: {extractor.stats['total_hidden_segments']}")
    print(f"Errors: {extractor.stats['errors']}")
    print()

    if extractor.findings:
        report_path, json_path = extractor.save_results()
        print()
        print("Top findings:")
        for f in extractor.findings[:5]:
            print(f"  - {os.path.basename(f['file'])}: {len(f['hidden_text'])} hidden segments")
    else:
        print("No hidden text found.")


if __name__ == "__main__":
    main()
