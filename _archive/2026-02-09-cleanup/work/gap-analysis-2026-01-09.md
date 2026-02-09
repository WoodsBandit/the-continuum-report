# Gap Analysis: Source Documentation vs. Entities & Connections
**Generated:** 2026-01-09
**Purpose:** Identify missing entities and connections based on source document review

---

## CURRENT INVENTORY

| Category | Count |
|----------|-------|
| Source Documents | 153 files (135 PDF, 14 MD, 4 JSON) |
| Entities | 40 |
| Connections | 99 |
| Connection Briefs | 113 files |

---

## PART 1: MISSING ENTITIES

### A. FINANCIAL ENABLERS - PERSONS

| Entity Slug | Name | Type | Source Documents | Priority |
|-------------|------|------|------------------|----------|
| `jes-staley` | James "Jes" Staley | Person | FCA Decision Notice, FCA Final Notice, Staley-Epstein Emails (707 lines), JPMorgan complaints | **HIGH** |
| `alexander-acosta` | Alexander Acosta | Person | DOJ OPR Report, 2008 NPA, Florida Case Index | **HIGH** |
| `darren-indyke` | Darren Indyke | Person | Epstein Estate Probate, Wexner emails, DOJ docs | **MEDIUM** |
| `richard-kahn` | Richard Kahn | Person | Epstein Estate Probate Report | **MEDIUM** |
| `mary-erdoes` | Mary Erdoes | Person | JPMorgan 33k search, USVI complaints | **MEDIUM** |
| `jamie-dimon` | Jamie Dimon | Person | JPMorgan complaints, regulatory orders | **MEDIUM** |
| `ann-marie-villafana` | Ann Marie Villafaña | Person | DOJ OPR Report, Florida Case docs | **LOW** |

**Source Index:**
- `T:/website/sources/regulatory-actions/fca-decision-notice-staley.md`
- `T:/website/sources/regulatory-actions/fca-final-notice-staley.md`
- `T:/website/sources/regulatory-actions/staley-epstein-email-extracts.md`
- `T:/website/sources/financial-enablers/jpmorgan/doj-33k-jpmorgan-search.md`
- `T:/website/sources/florida-case/doj-opr-investigation-report.pdf`

---

### B. FINANCIAL ENABLERS - ORGANIZATIONS

| Entity Slug | Name | Type | Source Documents | Priority |
|-------------|------|------|------------------|----------|
| `mc2-model-management` | MC2 Model Management | Organization | Epstein Modeling Agency Network (1,330 lines) | **HIGH** |
| `wexner-foundation` | Wexner Foundation | Organization | Wexner docs (3 files), Dropsite leaked emails | **HIGH** |
| `limited-brands` | Limited Brands/L Brands | Organization | Wexner Foundation docs | **MEDIUM** |
| `ylk-charitable-fund` | YLK Charitable Fund | Organization | Wexner/Epstein financial docs | **LOW** |
| `couq-foundation` | C.O.U.Q. Foundation | Organization | Wexner/Epstein financial docs | **LOW** |

**Source Index:**
- `T:/website/sources/financial-enablers/deutsche-bank/epstein-modeling-agency-network.md`
- `T:/website/sources/financial-enablers/wexner/wexner-foundation-letter.md`
- `T:/website/sources/financial-enablers/wexner/dropsite-news-leaked-emails.md`
- `T:/website/sources/financial-enablers/wexner/wexner-foundation-independent-review.pdf`

---

### C. REGULATORY BODIES

| Entity Slug | Name | Type | Source Documents | Priority |
|-------------|------|------|------------------|----------|
| `fca-uk` | Financial Conduct Authority (UK) | Organization | FCA notices on Staley, Deutsche Bank | **MEDIUM** |
| `nysdfs` | NY State Dept of Financial Services | Organization | Deutsche Bank consent orders | **MEDIUM** |
| `occ` | Office of Comptroller of Currency | Organization | JPMorgan consent orders | **LOW** |
| `fincen` | Financial Crimes Enforcement Network | Organization | FinCEN 311 notices | **LOW** |
| `doj-opr` | DOJ Office of Professional Responsibility | Organization | OPR Investigation Report | **LOW** |

**Source Index:**
- `T:/website/sources/regulatory-actions/fca-*.md`
- `T:/website/sources/financial-enablers/deutsche-bank/nysdfs-consent-order-*.pdf`
- `T:/website/sources/financial-enablers/jpmorgan/occ-*.pdf`

---

### D. CASES - MISSING

| Entity Slug | Name | Type | Source Documents | Priority |
|-------------|------|------|------------------|----------|
| `usa-v-maxwell` | United States v. Maxwell | Case | Maxwell Case Documents (574 lines), trial docs | **HIGH** |
| `usvi-v-jpmorgan` | USVI v. JPMorgan Chase | Case | USVI complaints, settlement docs | **HIGH** |
| `jane-doe-v-jpmorgan` | Jane Doe 1 v. JPMorgan | Case | Class action complaint, $290M settlement | **MEDIUM** |
| `doe-v-deutsche-bank` | Doe v. Deutsche Bank | Case | TVPA class action complaint | **MEDIUM** |
| `wild-v-doj` | Wild v. DOJ (CVRA) | Case | 11th Circuit Opinion | **MEDIUM** |

**Source Index:**
- `T:/website/sources/financial-enablers/deutsche-bank/ghislaine-maxwell-case-documents.md`
- `T:/website/sources/financial-enablers/jpmorgan/usvi-v-jpmorgan-*.pdf`
- `T:/website/sources/financial-enablers/jpmorgan/jane-doe-v-jpmorgan-complaint.pdf`
- `T:/website/sources/florida-case/wild-v-doj-11th-circuit.pdf`

---

### E. INTELLIGENCE/HISTORICAL - ENTITIES

| Entity Slug | Name | Type | Source Documents | Priority |
|-------------|------|------|------------------|----------|
| `church-committee` | Church Committee | Case/Investigation | Church Committee Book II (77.6 MB) | **MEDIUM** |
| `operation-gladio` | Operation Gladio | Case/Operation | Ganser NATO Secret Armies (3 files) | **LOW** |
| `operation-paperclip` | Operation Paperclip | Case/Operation | CIA Review, FBI docs | **LOW** |
| `five-eyes` | Five Eyes/UKUSA | Organization | UKUSA docs (2 files) | **LOW** |
| `cointelpro` | COINTELPRO | Case/Program | Church Committee findings | **LOW** |

**Source Index:**
- `T:/website/sources/congressional/church-committee-book-ii.pdf`
- `T:/website/sources/intelligence/natos-secret-armies-ganser.pdf`
- `T:/website/sources/intelligence/operation-paperclip-*.pdf`
- `T:/website/sources/intelligence/ukusa-*.pdf`

---

### F. JUDGES & COURTS

| Entity Slug | Name | Type | Source Documents | Priority |
|-------------|------|------|------------------|----------|
| `judge-alison-nathan` | Judge Alison J. Nathan | Person | Giuffre v. Maxwell docket, Maxwell criminal | **LOW** |
| `judge-jed-rakoff` | Judge Jed S. Rakoff | Person | JPMorgan cases | **LOW** |
| `sdny` | Southern District of New York | Organization | Multiple case filings | **LOW** |
| `edny` | Eastern District of New York | Organization | Maxwell criminal, NXIVM | **LOW** |

---

## PART 2: MISSING CONNECTIONS

### A. JES STALEY NETWORK (if entity created)

| Source | Target | Type | Evidence | Source Doc |
|--------|--------|------|----------|------------|
| jes-staley | jeffrey-epstein | documented | 1,700+ emails | FCA notices |
| jes-staley | jpmorgan-epstein-case | documented | Executive responsibility | USVI complaints |
| jes-staley | jamie-dimon | referenced | CEO relationship | JPMorgan docs |
| jes-staley | ghislaine-maxwell | referenced | Email mentions | FCA extracts |

---

### B. WEXNER FOUNDATION NETWORK (if entity created)

| Source | Target | Type | Evidence | Source Doc |
|--------|--------|------|----------|------------|
| wexner-foundation | jeffrey-epstein | documented | Financial control | Dropsite emails |
| wexner-foundation | les-wexner | documented | Founder | Foundation letter |
| wexner-foundation | darren-indyke | documented | Intermediary | Leaked emails |

---

### C. MC2 MODEL MANAGEMENT (if entity created)

| Source | Target | Type | Evidence | Source Doc |
|--------|--------|------|----------|------------|
| mc2-model-management | jean-luc-brunel | documented | Founder/operator | Modeling network doc |
| mc2-model-management | jeffrey-epstein | documented | $1-2M funding | Modeling network doc |
| mc2-model-management | ghislaine-maxwell | referenced | Recruitment pipeline | Trial testimony |

---

### D. EXISTING ENTITIES - MISSING CONNECTIONS

| Source | Target | Type | Evidence | Source Doc |
|--------|--------|------|----------|------------|
| jean-luc-brunel | virginia-giuffre | documented | Deposition testimony | Giuffre depositions |
| les-wexner | ghislaine-maxwell | referenced | Social connection | Multiple docs |
| deutsche-bank | ghislaine-maxwell | referenced | Account relationship | NYSDFS order |
| robert-maxwell | jeffrey-epstein | referenced | Introduction narrative | Secondary sources |

---

## PART 3: SOURCE DOCUMENT INDEX

### Congressional Documents
```
T:/website/sources/congressional/
├── church-committee-book-ii.pdf (1976) - CIA/NSA/FBI operations
├── house-judiciary-inslaw-affair.pdf (1992) - PROMIS software
└── senate-bcci-affair.pdf (1992) - BCCI investigation
```

### Florida Case
```
T:/website/sources/florida-case/
├── Index.md - Case timeline and key participants
├── 2008-non-prosecution-agreement.pdf
├── doj-opr-investigation-report.pdf (Nov 2020)
├── wild-v-doj-11th-circuit.pdf (Apr 2020)
├── 2006-palm-beach-grand-jury-exhibit-4.pdf
├── 2019-federal-indictment-sdny.pdf
└── grand-jury-transcripts.pdf (2006)
```

### Giuffre v. Maxwell
```
T:/website/sources/giuffre-v-maxwell/
├── manifest.json - Document index
└── [45 ECF documents across multiple docket series]
    ├── ECF-1320-* (40 docs)
    ├── ECF-1325-* (3 docs)
    ├── ECF-1327-* (8 docs)
    ├── ECF-1328-* (15 docs)
    ├── ECF-1330-* (9 docs)
    └── ECF-1331-* (11 docs)
```

### Financial Enablers - Deutsche Bank
```
T:/website/sources/financial-enablers/deutsche-bank/
├── nysdfs-consent-order-russian-mirror-trades.pdf ($425M, 2017)
├── fca-final-notice-deutsche-bank.pdf (2017)
├── nysdfs-consent-order-epstein.pdf ($150M, 2020)
├── doe-v-deutsche-bank-complaint.pdf (2022)
├── epstein-modeling-agency-network.md (1,330 lines) **KEY**
├── jes-staley-fca-timeline.md (1,130 lines) **KEY**
├── jeffrey-epstein-estate-probate-report.md (1,027 lines)
├── epstein-settlement-agreements-research.md
├── ghislaine-maxwell-case-documents.md
└── maxwell-case-summary.md
```

### Financial Enablers - JPMorgan
```
T:/website/sources/financial-enablers/jpmorgan/
├── occ-consent-order-bsa-aml.pdf (2013)
├── occ-350m-penalty-order.pdf (2014)
├── usvi-v-jpmorgan-complaint.pdf (Dec 2022)
├── usvi-v-jpmorgan-second-amended-complaint.pdf (Apr 2023) **KEY**
├── jpmorgan-v-staley-third-party-complaint.pdf (Mar 2023)
├── jane-doe-v-jpmorgan-complaint.pdf (Nov 2022)
├── settlement-2023-09.pdf ($75M)
└── doj-33k-jpmorgan-search.md (240 lines)
```

### Financial Enablers - Wexner
```
T:/website/sources/financial-enablers/wexner/
├── wexner-foundation-letter.md (Aug 2019)
├── wexner-foundation-independent-review.pdf (2020)
├── dropsite-news-leaked-emails.md (Dec 2025) **KEY**
└── doj-co-conspirator-email.md (Dec 2025)
```

### Regulatory Actions
```
T:/website/sources/regulatory-actions/
├── fca-decision-notice-staley.md (May 2023)
├── fca-final-notice-staley.md (July 2025)
├── staley-epstein-email-extracts.md (707 lines) **KEY**
└── fincen-311-fbme.pdf (2014)
```

### Intelligence
```
T:/website/sources/intelligence/
├── cia-angleton-phenomenon.pdf
├── cia-studies-intelligence-2024.pdf
├── dni-counterintelligence-reader-vol3.pdf
├── gladio-approach-ganser.pdf
├── nato-secret-armies-eth.pdf
├── natos-secret-armies-ganser.pdf (3.0 MB) **KEY**
├── operation-paperclip-cia-review.pdf
├── operation-paperclip-fbi.pdf
├── parallel-history-nato-warsaw.pdf
├── ukusa-highlights-guide.pdf
└── ukusa-history-harvard.pdf
```

---

## PART 4: PRIORITY RECOMMENDATIONS

### Tier 1 - HIGH PRIORITY (Create These First)
1. **jes-staley** - Central to financial enabler narrative, extensive source docs
2. **usa-v-maxwell** - Major case, distinct from civil Giuffre case
3. **mc2-model-management** - Trafficking front operation
4. **alexander-acosta** - Key to prosecutorial failure narrative
5. **usvi-v-jpmorgan** - Major institutional accountability case

### Tier 2 - MEDIUM PRIORITY
6. **wexner-foundation** - Institutional enabler
7. **darren-indyke** - Key intermediary figure
8. **jane-doe-v-jpmorgan** - $290M settlement case
9. **doe-v-deutsche-bank** - TVPA precedent
10. **fca-uk** - Regulatory body with enforcement actions

### Tier 3 - LOWER PRIORITY (Background/Context)
11. Intelligence historical entities (Church Committee, Gladio, etc.)
12. Additional regulatory bodies (OCC, NYSDFS, FinCEN)
13. Judges and court entities

---

## USAGE NOTES

**To create entities from this list:**
1. Reference the Source Index paths to locate primary documents
2. Use source documents to populate entity briefs
3. Create connection briefs for documented relationships
4. Update entities.json and connections.json

**Key Source Documents (Most Valuable):**
- `staley-epstein-email-extracts.md` (707 lines) - Direct evidence
- `epstein-modeling-agency-network.md` (1,330 lines) - MC2 operation
- `dropsite-news-leaked-emails.md` - Wexner continued control
- `usvi-v-jpmorgan-second-amended-complaint.pdf` - Unredacted emails
- `doj-opr-investigation-report.pdf` - Prosecutorial misconduct

---

*This document serves as an index for future sessions to identify gaps and locate source materials.*
