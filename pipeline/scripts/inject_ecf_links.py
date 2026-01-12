#!/usr/bin/env python3
"""
CC1 Brief Link Injection Script
Injects clickable source URLs into analytical briefs for ECF citations.
"""

import re
import os
from pathlib import Path
from datetime import datetime

# Configuration
BRIEFS_DIR = Path("/continuum/briefs")
SOURCES_DIR = Path("/continuum/website/sources/giuffre-v-maxwell")
BASE_URL = "https://thecontinuumreport.com/sources/giuffre-v-maxwell"
REPORT_PATH = Path("/continuum/reports/brief_link_injection_2025-12-23.md")

# Get available PDFs
available_pdfs = set()
for pdf in SOURCES_DIR.glob("*.pdf"):
    # Extract ecf-XXXX-XX from filename
    name = pdf.stem  # e.g., "ecf-1331-12"
    available_pdfs.add(name)

print(f"Found {len(available_pdfs)} available PDFs")

# Pattern to match ECF Doc. XXXX-XX that is NOT already a link
# Matches: ECF Doc. 1331-12 (various formats)
# Excludes: [ECF Doc. 1331-12](...) (already linked)
ECF_PATTERN = re.compile(
    r'(?<!\[)'  # Not preceded by [
    r'(ECF Doc\.?\s*(\d+-\d+))'  # Match ECF Doc. XXXX-XX, capture doc number
    r'(?!\])'  # Not followed by ]
)

# Also match table format: | 1331-12 | (doc number only in tables)
TABLE_ECF_PATTERN = re.compile(
    r'\|\s*(?<!\[)'  # After pipe, not preceded by [
    r'((\d{4}-\d+))'  # Doc number like 1331-12
    r'(?!\])\s*\|'  # Not followed by ], then pipe
)

# Statistics
stats = {
    "briefs_scanned": 0,
    "briefs_modified": 0,
    "links_injected": 0,
    "links_skipped_no_pdf": 0,
    "per_brief": {}
}

def inject_links(content, brief_name):
    """Inject clickable links into ECF citations."""
    modified = False
    injected_count = 0
    skipped_count = 0

    def replace_ecf(match):
        nonlocal modified, injected_count, skipped_count
        full_match = match.group(1)  # ECF Doc. 1331-12
        doc_num = match.group(2)     # 1331-12
        pdf_name = f"ecf-{doc_num}"

        if pdf_name in available_pdfs:
            modified = True
            injected_count += 1
            url = f"{BASE_URL}/{pdf_name}.pdf"
            return f"[{full_match}]({url})"
        else:
            skipped_count += 1
            return full_match

    # Apply ECF Doc. pattern replacement
    new_content = ECF_PATTERN.sub(replace_ecf, content)

    return new_content, modified, injected_count, skipped_count

# Process each analytical brief
briefs = sorted(BRIEFS_DIR.glob("analytical_brief_*.md"))
results = []

for brief_path in briefs:
    brief_name = brief_path.name
    stats["briefs_scanned"] += 1

    content = brief_path.read_text(encoding="utf-8")

    new_content, modified, injected, skipped = inject_links(content, brief_name)

    if modified:
        brief_path.write_text(new_content, encoding="utf-8")
        stats["briefs_modified"] += 1
        stats["links_injected"] += injected
        stats["per_brief"][brief_name] = {"injected": injected, "skipped": skipped}
        results.append(f"  - {brief_name}: {injected} links injected")
        print(f"Modified: {brief_name} ({injected} links)")

    stats["links_skipped_no_pdf"] += skipped

# Generate report
report = f"""# Brief Link Injection Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Instance:** CC1

---

## Summary

| Metric | Value |
|--------|-------|
| Briefs Scanned | {stats['briefs_scanned']} |
| Briefs Modified | {stats['briefs_modified']} |
| Links Injected | {stats['links_injected']} |
| Skipped (no PDF) | {stats['links_skipped_no_pdf']} |

---

## Modified Briefs

"""

if stats['per_brief']:
    report += "| Brief | Links Injected | Skipped |\n"
    report += "|-------|----------------|--------|\n"
    for brief, data in sorted(stats['per_brief'].items()):
        report += f"| {brief} | {data['injected']} | {data['skipped']} |\n"
else:
    report += "*No briefs required modification.*\n"

report += """
---

## What Was Done

1. Scanned all `analytical_brief_*.md` files in `/continuum/briefs/`
2. Found ECF citation patterns like `ECF Doc. 1331-12`
3. Checked if corresponding PDF exists in `/continuum/website/sources/giuffre-v-maxwell/`
4. If PDF exists, converted to clickable link:
   - Before: `ECF Doc. 1331-12`
   - After: `[ECF Doc. 1331-12](https://thecontinuumreport.com/sources/giuffre-v-maxwell/ecf-1331-12.pdf)`

---

## URL Pattern

All links point to:
```
https://thecontinuumreport.com/sources/giuffre-v-maxwell/ecf-XXXX-XX.pdf
```

---

*CC1 — Citation Systems*
"""

REPORT_PATH.write_text(report, encoding="utf-8")
print(f"\nReport saved to: {REPORT_PATH}")
print(f"\nSUMMARY:")
print(f"  Briefs scanned: {stats['briefs_scanned']}")
print(f"  Briefs modified: {stats['briefs_modified']}")
print(f"  Links injected: {stats['links_injected']}")
