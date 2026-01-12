# SOURCES ARCHIVE — Landing Page Project

**Project ID:** sources-archive
**Created:** 2025-12-25
**Status:** ACTIVE
**Priority:** HIGH

---

## Mission

Create a professional, curated **Sources Archive** landing page at `/sources/index.html` that:

1. Displays all hosted primary source documents
2. Matches The Continuum Report's visual identity perfectly
3. Provides intuitive navigation and categorization
4. Establishes credibility through professional presentation
5. Makes verification easy for journalists and researchers

**This page represents our commitment to transparency and verifiability.**

---

## Design Requirements

### Visual Identity (MUST MATCH)

**Color Palette:**
```css
--void-black: #0a0a0b;      /* Background */
--deep-purple: #1a1025;     /* Section backgrounds */
--royal-purple: #2d1f3d;    /* Card backgrounds */
--mystic-purple: #4a3660;   /* Accents */
--ancient-gold: #c9a227;    /* Primary accent */
--light-gold: #e8d48b;      /* Highlights */
--pale-gold: #f5e6b3;       /* Subtle accents */
--smoke: #a8a8a8;           /* Secondary text */
--mist: #d4d4d4;            /* Body text */
--pure: #f8f8f8;            /* Headlines */
```

**Typography:**
```css
font-family: 'Cinzel', serif;              /* Headlines, titles */
font-family: 'Cormorant Garamond', serif;  /* Subheadings, quotes */
font-family: 'Source Sans 3', sans-serif;  /* Body, navigation */
```

**Design Elements:**
- Dark backgrounds with subtle gradients
- Gold accents for interactive elements
- Thin gold borders on cards
- Subtle glow effects on hover
- Professional, intelligence-agency aesthetic
- Cathedral gravitas, not flashy

### Page Structure

```
┌─────────────────────────────────────────┐
│  NAVIGATION BAR (same as main site)     │
├─────────────────────────────────────────┤
│                                         │
│  HERO SECTION                           │
│  "Source Archive"                       │
│  "Primary documents. Independently      │
│   verifiable. Open to all."             │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│  CATEGORY FILTERS                       │
│  [All] [Court Filings] [FOIA]           │
│  [Regulatory] [Financial] [Other]       │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│  SEARCH BAR                             │
│  "Search documents..."                  │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│  DOCUMENT GRID                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ Doc 1   │ │ Doc 2   │ │ Doc 3   │   │
│  │ Type    │ │ Type    │ │ Type    │   │
│  │ Size    │ │ Size    │ │ Size    │   │
│  └─────────┘ └─────────┘ └─────────┘   │
│                                         │
│  (Expandable sections by category)      │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│  METHODOLOGY SECTION                    │
│  How we source documents                │
│  Verification standards                 │
│                                         │
├─────────────────────────────────────────┤
│  FOOTER (same as main site)             │
└─────────────────────────────────────────┘
```

### Document Card Design

Each document card should display:
- Document title (descriptive name)
- Document type badge (Court Filing, FOIA, Regulatory, etc.)
- Case/Source attribution
- File size
- Download button (gold accent)
- Optional: Page count, date filed

**Card Interaction:**
- Hover: lift effect, gold border glow
- Click: Opens PDF in new tab OR triggers download

---

## Source Document Categories

### 1. Giuffre v. Maxwell (Civil Case)
Location: `/sources/giuffre-v-maxwell/`
- ECF filings from SDNY case
- Depositions, exhibits, sealed documents (now unsealed)

### 2. Florida Case
Location: `/sources/florida-case/`
- 2006 Grand Jury Transcripts
- 2008 NPA (Non-Prosecution Agreement)
- Palm Beach Police Records
- DOJ OPR Report (2020)

### 3. Maxwell Criminal Case
Location: `/sources/maxwell-criminal/`
- Indictments (original, superseding)
- Sentencing memoranda
- Trial exhibits

### 4. Financial Enablers
Location: `/sources/financial-enablers/`

**Deutsche Bank:**
- NYSDFS Consent Orders
- UK FCA Notices

**JPMorgan:**
- OCC Consent Orders
- Civil Litigation Documents
- FCA Jes Staley Action

**Wexner:**
- Foundation documents
- DOJ co-conspirator email (Dec 2025)
- Leaked emails (Dropsite News)

### 5. Regulatory Actions
Location: `/sources/regulatory-actions/`
- FinCEN designations
- FCA Final Notices

### 6. FOIA Releases
Location: `/sources/foia/`
- FBI Vault releases
- DOJ document releases

---

## Technical Requirements

### File: `/continuum/website/sources/index.html`

**Must include:**
- Same meta tags pattern as index.html
- Same font loading (Google Fonts preconnect)
- Same navigation structure
- Responsive design (mobile-first)
- JavaScript for filtering/search (vanilla JS, no frameworks)

**Data source options:**
1. Static HTML with all documents listed
2. JSON file (`/sources/sources.json`) loaded dynamically
3. Hybrid: categories static, items from JSON

**Recommended:** Option 2 or 3 for maintainability

### sources.json Schema

```json
{
  "generated": "2025-12-25T00:00:00Z",
  "count": 68,
  "categories": [
    {
      "id": "giuffre-v-maxwell",
      "name": "Giuffre v. Maxwell",
      "description": "Civil case documents from SDNY",
      "icon": "court"
    }
  ],
  "documents": [
    {
      "id": "ecf-1328-44",
      "title": "Exhibit 44 to Motion to Unseal",
      "filename": "ecf-1328-44.pdf",
      "path": "/sources/giuffre-v-maxwell/ecf-1328-44.pdf",
      "category": "giuffre-v-maxwell",
      "type": "court-filing",
      "case": "Giuffre v. Maxwell, 15-cv-07433 (SDNY)",
      "filed": "2024-01-05",
      "size_bytes": 2456789,
      "pages": 45,
      "description": "Deposition excerpts discussing...",
      "verification_url": "https://pacer.uscourts.gov/..."
    }
  ]
}
```

---

## Agent Resources

### Custom Agents to Utilize

| Agent | Role in This Project |
|-------|---------------------|
| **visualization-expert** | CSS styling, responsive design, animations |
| **file-organizer** | Inventory existing sources, verify paths |
| **citation-mapper** | Map ECF numbers to files, verify completeness |

### Reference Files

| File | Purpose |
|------|---------|
| `/website/index.html` | Design patterns, CSS variables, structure |
| `/website/about.html` | Secondary page patterns |
| `/website/continuum.html` | Interactive component patterns |
| `/data/entities.json` | JSON structure example |

---

## Deliverables

1. **`/sources/index.html`** — Complete landing page
2. **`/sources/sources.json`** — Document inventory data
3. **Updated navigation** — Add Sources link to all pages
4. **Progress log** — Session-persistent documentation

---

## Success Criteria

The Sources Archive succeeds if:

1. **Professional appearance** — Matches site identity perfectly
2. **Complete inventory** — All 68+ hosted documents listed
3. **Easy navigation** — Filter by category, search by name
4. **Clear attribution** — Every document has source/case info
5. **Verification links** — PACER URLs where applicable
6. **Mobile responsive** — Works on all devices
7. **Fast loading** — Under 2 seconds initial load
8. **Accessible** — WCAG 2.1 AA compliant

---

## Timeline

| Phase | Tasks | Est. Time |
|-------|-------|-----------|
| 1 | Inventory sources, create JSON | 1-2 hours |
| 2 | Design HTML structure | 1 hour |
| 3 | Implement CSS styling | 2-3 hours |
| 4 | Add filtering/search JS | 1-2 hours |
| 5 | Testing & refinement | 1 hour |
| **Total** | | **6-9 hours** |

---

## Notes

- This page is critical for credibility
- Every journalist who wants to verify claims will come here
- It should feel like accessing a professional archive, not a file dump
- Consider future expansion: more categories, more documents
- The Continuum Report's tagline applies: "Another Node in the Decentralized Intelligence Agency"

---

*Task brief created: 2025-12-25*
