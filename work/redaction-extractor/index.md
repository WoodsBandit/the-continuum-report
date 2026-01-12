# Redaction Extractor Agent

## Purpose

Scan PDF files for "fake" redactions — black visual overlays that don't actually remove underlying text. Extract and document all hidden text found.

## Context

**Discovery:** December 24, 2025
- Found hidden text under black boxes in `ecf-1328-44.pdf` (Giuffre v. Maxwell)
- "Jane Doe 2" (redacted victim identity) was fully extractable
- Black boxes are visual overlays only — text layer preserved underneath

## Tool Location

**Script:** `T:\scripts\redaction_extractor.py`

## Usage

```bash
# Full scan of website sources (default)
python T:\scripts\redaction_extractor.py --verbose

# Scan specific directory
python T:\scripts\redaction_extractor.py --dir "T:\website\sources\giuffre-v-maxwell" --verbose

# Scan without recursion
python T:\scripts\redaction_extractor.py --dir "T:\website\sources" --no-recursive --verbose
```

## Output

Reports saved to: `T:\reports\redaction-extraction\`
- `redaction_report_YYYYMMDD_HHMMSS.md` — Human-readable markdown report
- `redaction_data_YYYYMMDD_HHMMSS.json` — Raw JSON data for further processing

## Target Directories

Priority scan order:
1. `T:\website\sources\giuffre-v-maxwell\` — Court filings with known redactions
2. `T:\website\sources\maxwell-criminal\` — Criminal case documents
3. `T:\website\sources\florida-case\` — Florida prosecution documents
4. `T:\website\sources\` — All other hosted sources

## Known Findings

| File | Hidden Text | Significance |
|------|-------------|--------------|
| ecf-1328-44.pdf | "Jane Doe 2" (4x) | Redacted victim identity |

## Technical Notes

- Tool uses PyMuPDF (fitz) library
- Detects black fills with RGB < 0.15
- Extracts text within bounding rectangles of black boxes
- Only reports text segments > 2 characters

## Cross-References

- Parent agent: `/agents/document-acquisition.md`
- Related: Legal audit concerns for extracted information
- Output feeds: Entity extraction, connection discovery

---

*Created: 2025-12-24*
*The Continuum Report*
