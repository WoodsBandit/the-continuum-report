# Source Link Structure Audit

**Generated:** 2025-12-21
**Purpose:** Document current source link implementation to standardize connection brief methodology

---

## 1. In-Text Link Examples

### Current Format in Analytical Briefs

In-text references use plain text citation format with no hyperlinks:

```markdown
Flight logs entered as exhibits document extensive travel between these locations on private aircraft. (ECF Doc. 1331-32, filed 01/05/24)
```

```markdown
**ECF Doc. 1331-12, filed 01/05/24:**

Sarah Ransome provided a sworn affidavit dated January 5, 2017, stating:

> "In the summer of 2006, when I was twenty-two years old..."
```

```markdown
According to court filings in *Jane Doe #1 and #2 v. United States*:

> "the U.S. Attorney's Office for the Southern District of Florida had concealed from Epstein's victims a non-prosecution agreement..."

(ECF Doc. 1330-1, filed 01/05/24)
```

### Connection Brief Format

Connection briefs use similar plain-text references:

```markdown
**ECF Doc. 1331-11** (Rodriguez Deposition Testimony, filed None):

> Document references connection context. See primary source for full details.
```

**Note:** Connection briefs currently have `filed None` — this is a bug that should be fixed.

---

## 2. Source List Examples

### Analytical Brief Footer Tables

Simple table with ECF number, date, and description:

```markdown
## Source Documents

| ECF Doc. No. | Filed | Document Description |
|--------------|-------|---------------------|
| 1320-12 | 01/03/24 | Court Filing |
| 1320-19 | 01/03/24 | Court Filing |
| 1320-40 | 01/03/24 | Maxwell's Rule 26 Disclosures |
| 1325-1 | 01/04/24 | Motion to Quash Trial Subpoena |
| 1327-12 | 01/05/24 | Defendant's Submission Regarding Search Terms |
```

### Key Source Documents List

Some briefs also include a "Key documents" list:

```markdown
Key documents include:

| Document | Description |
|----------|-------------|
| ECF Doc. 1331-11 | Rodriguez Deposition Testimony |
| ECF Doc. 1331-12 | Ransome Affidavit |
| ECF Doc. 1331-32 | Flight Log References |
| ECF Doc. 1330-1 | CVRA Case Background |
| ECF Doc. 1325-3 | Jane Doe Joinder Motion |
```

---

## 3. URL Structure

### PDF Access Pattern

```
/sources/{case-folder}/ecf-{ecf-number}.pdf
```

**Examples:**
- `/sources/giuffre-v-maxwell/ecf-1328-44.pdf`
- `/sources/giuffre-v-maxwell/ecf-1331-12.pdf`
- `/sources/epstein-sdny/ecf-{number}.pdf` (future)
- `/sources/maxwell-criminal/ecf-{number}.pdf` (future)

### Full URL

```
https://thecontinuumreport.com/sources/giuffre-v-maxwell/ecf-1328-44.pdf
```

---

## 4. PDF Storage Location

### Directory Structure

```
/continuum/website/sources/
├── index.json                    # Master index of all available documents
├── export_report.json            # Export metadata
├── giuffre-v-maxwell/            # Case folder
│   ├── ecf-1320-1.pdf
│   ├── ecf-1320-10.pdf
│   ├── ecf-1328-44.pdf
│   └── ... (68 documents currently)
├── epstein-sdny/                 # Placeholder for future
└── maxwell-criminal/             # Placeholder for future
```

### sources/index.json Structure

```json
{
  "generated": "2025-12-16T02:20:46.405030Z",
  "cases": {
    "giuffre-v-maxwell": {
      "case_citation": "Giuffre v. Maxwell, No. 15-cv-07433-LAP (S.D.N.Y.)",
      "documents": [
        {
          "ecf": "1328-44",
          "filename": "ecf-1328-44.pdf",
          "available": true,
          "paperless_id": 116
        }
      ]
    }
  }
}
```

---

## 5. Website Handler (continuum.html)

### ECF Link Processing Flow

The website auto-converts ECF text references into clickable links via JavaScript:

1. **Detection** — `linkifyECFReferences()` scans rendered content for ECF patterns
2. **Pattern Matching** — Uses regex to find variations:
   - `ECF Doc. 1328-44`
   - `ECF Document 1328-44`
   - `ECF #1328-44`
   - `Document 1328-44`
   - `Doc. 1328-44`
3. **Link Creation** — Wraps matches in `<span class="ecf-link">` elements
4. **Click Handler** — Calls `openECFDocument(ecf)` on click

### Relevant Code Patterns

```javascript
// ECF link styling
.ecf-link {
    color: var(--gold);
    cursor: pointer;
    text-decoration: underline;
    text-decoration-style: dotted;
}

// Pattern to match ECF references
const combinedPattern = /(?:ECF\s+(?:Doc(?:ument)?\.?\s*)?#?\s*|Document\s+|Doc\.\s*)(\d{3,4}(?:-\d{1,3})?)/gi;

// Opening document
openECFDocument(ecf) {
    PDFViewer.open({
        ecf: ecf,
        description: description
    });
}
```

### PDF Viewer Behavior

1. **Checks `sources/index.json`** for document availability
2. **If available:**
   - Loads PDF with pdf.js
   - Shows download link
   - Provides page navigation and zoom controls
3. **If NOT available:**
   - Shows placeholder with PACER verification instructions
   - Displays case citation for manual lookup
   - Links to pacer.uscourts.gov

---

## 6. JSON Data Structures

### connections.json

**Note:** `connections.json` is DERIVED from connection briefs. No subjective strength scoring.

Stores entity-to-entity connections with evidence array:

```json
{
  "source": "bill-clinton",
  "target": "virginia-giuffre",
  "sources_count": 5,
  "type": "SOC",
  "evidence": [
    "ECF 1328-44",
    "ECF 1320-28",
    "ECF 1331-18",
    "ECF 1331-19",
    "ECF 1320-6"
  ],
  "bidirectional": true,
  "brief_file": "bill-clinton_virginia-giuffre.md"
}
```

**Note:** Evidence uses abbreviated format `ECF 1328-44` (no "Doc.")

### connection_briefs.json

Stores connection details with structured source objects:

```json
{
  "entityId": "virginia-giuffre",
  "summary": "One-sentence description of connection nature based on source documents.",
  "sources_count": 3,
  "sources": [
    {
      "id": "1320-9",
      "title": "ECF Doc. 1320-9",
      "date": "01/03/24"
    },
    {
      "id": "1320-40",
      "title": "ECF Doc. 1320-40",
      "date": "01/03/24"
    }
  ]
}
```

**Note:** No "strength" field - binary model only. Connections exist (in a brief) or they don't.

### entities.json (referenced, not shown)

Stores entity metadata including analytical brief paths and source references.

---

## 7. Recommended Standard Format

### For Connection Briefs (Markdown)

#### In-Text Citations

Use consistent format that will be auto-linked by website:

```markdown
**ECF Doc. 1328-44** (Marcinkova Deposition, filed 01/05/24):

> Direct quote from document...
```

Or inline:

```markdown
This connection is documented in court filings (ECF Doc. 1328-44, filed 01/05/24).
```

#### Source Tables

Include both ECF number and description:

```markdown
## Source Documents

| ECF # | Filed | Description | Case |
|-------|-------|-------------|------|
| 1328-44 | 01/05/24 | Nadia Marcinkova Deposition (April 13, 2010) | Giuffre v. Maxwell |
| 1331-12 | 01/05/24 | Sarah Ransome Sworn Affidavit (Jan 5, 2017) | Giuffre v. Maxwell |
| 1330-1 | 01/05/24 | CVRA Case Background | Giuffre v. Maxwell |
```

### For JSON (connection_briefs.json)

Ensure all source objects include:

```json
{
  "id": "1328-44",
  "title": "ECF Doc. 1328-44",
  "date": "01/05/24",
  "description": "Marcinkova Deposition"  // NEW: Add description field
}
```

### ECF Number Format Standards

| Context | Format | Example |
|---------|--------|---------|
| Inline text | `ECF Doc. {number}` | ECF Doc. 1328-44 |
| JSON id field | `{number}` | 1328-44 |
| JSON title | `ECF Doc. {number}` | ECF Doc. 1328-44 |
| Filename | `ecf-{number}.pdf` | ecf-1328-44.pdf |
| URL path | `/sources/{case}/ecf-{number}.pdf` | /sources/giuffre-v-maxwell/ecf-1328-44.pdf |

---

## 8. Identified Issues

### Bugs to Fix

1. **`filed None` in connection briefs** — Date field not populated
2. **Generic descriptions** — Many source tables show "Court Filing" instead of descriptive titles
3. **Missing case context** — Some briefs don't specify which case (assumes Giuffre v. Maxwell)

### Gaps in Current Implementation

1. **No direct hyperlinks in markdown** — Relies on JavaScript post-processing
2. **Inconsistent evidence formats** — `ECF 1328-44` vs `ECF Doc. 1328-44`
3. **Limited source metadata** — JSON lacks description field for meaningful display

---

## 9. Source Access Flow Diagram

```
User clicks ECF reference in brief
         │
         ▼
┌─────────────────────────────┐
│  linkifyECFReferences()     │
│  detects ECF pattern        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  openECFDocument(ecf)       │
│  called with ECF number     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  PDFViewer.open()           │
│  checks sources/index.json  │
└──────────────┬──────────────┘
               │
       ┌───────┴───────┐
       │               │
       ▼               ▼
  Available?      Not Available
       │               │
       ▼               ▼
┌─────────────┐  ┌─────────────────┐
│ Load PDF    │  │ Show PACER      │
│ from        │  │ fallback with   │
│ /sources/   │  │ case citation   │
└─────────────┘  └─────────────────┘
```

---

## 10. Recommendations for CONNECTION_METHODOLOGY.md

Add the following to the methodology document:

### Source Citation Standards

1. **Always use full ECF format:** `ECF Doc. {number}` (e.g., `ECF Doc. 1328-44`)
2. **Include filing date when known:** `(ECF Doc. 1328-44, filed 01/05/24)`
3. **Include case citation for multi-case briefs**
4. **Use descriptive titles in source tables, not "Court Filing"**

### JSON Data Requirements

When generating connection_briefs.json:
- Populate `date` field (currently shows `None`)
- Add `description` field to sources array
- Use consistent `ECF Doc. {number}` format in `title`

### Source Document Naming

Follow the established pattern:
- Filename: `ecf-{number}.pdf` (lowercase, hyphenated)
- Path: `/sources/{case-slug}/ecf-{number}.pdf`
- Case slugs: `giuffre-v-maxwell`, `epstein-sdny`, `maxwell-criminal`

---

*This audit was generated to support standardization of source linking in The Continuum Report.*
