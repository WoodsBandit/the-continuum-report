# SOP-005: Document Acquisition Standard

**Version:** 1.0
**Created:** 2026-01-05
**Purpose:** Mandatory standard for ALL Claude Code sessions performing document acquisition
**Classification:** Core Operational Procedure

---

## CRITICAL: READ THIS FIRST

**This SOP is MANDATORY for any Claude session tasked with acquiring documents.**

When you receive a document acquisition request:
1. Read this entire SOP before taking any action
2. Follow the decision tree in Section 2
3. If acquiring secondary sources, you MUST extract and acquire all primary sources cited
4. All outputs must follow the formats in Section 6
5. All documents must be verified per Section 5

**NO EXCEPTIONS. NO SHORTCUTS.**

---

## 1. SCOPE & DEFINITIONS

### 1.1 What This Covers

This SOP applies whenever you are asked to:
- Find documents about a topic/person/case
- Download court filings
- Acquire regulatory documents
- Get source materials for briefs
- Research and document a subject
- "Get everything you can find on X"

### 1.2 Definitions

| Term | Definition |
|------|------------|
| **Primary Source** | Original document from authoritative source (court filing, government report, corporate filing, official record) |
| **Secondary Source** | Document that references/analyzes primary sources (news article, book, investigative report, blog post) |
| **Acquisition** | The complete process: identify → download → verify → name → store → log |
| **Citation Extraction** | Parsing a secondary source to identify all primary sources it references |

### 1.3 The Cardinal Rule

```
┌─────────────────────────────────────────────────────────────────────────┐
│  WHEN YOU ACQUIRE A SECONDARY SOURCE, YOU MUST AUTOMATICALLY           │
│  EXTRACT AND ACQUIRE ALL PRIMARY SOURCES IT CITES.                     │
│                                                                         │
│  A news article is NOT complete without its underlying court filings,  │
│  regulatory documents, and official records.                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. DECISION TREE

When you receive an acquisition request, follow this logic:

```
START: Acquisition Request Received
    │
    ▼
┌─────────────────────────────────────────┐
│ STEP 1: Classify the request            │
│ Is target a PRIMARY or SECONDARY source?│
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
   PRIMARY           SECONDARY
        │                 │
        ▼                 ▼
┌───────────────┐  ┌────────────────────────────────┐
│ Go to         │  │ STEP 2A: Acquire the secondary │
│ Section 3     │  │ source first                   │
│ (Primary      │  └────────────────┬───────────────┘
│  Acquisition) │                   │
└───────────────┘                   ▼
                   ┌────────────────────────────────┐
                   │ STEP 2B: MANDATORY - Extract   │
                   │ ALL citations from secondary   │
                   │ Go to Section 4                │
                   └────────────────┬───────────────┘
                                    │
                                    ▼
                   ┌────────────────────────────────┐
                   │ STEP 2C: For EACH primary      │
                   │ source citation found:         │
                   │ Execute Section 3              │
                   └────────────────────────────────┘
```

### 2.1 How to Classify Sources

**PRIMARY SOURCES (acquire directly):**
- Court filings (complaints, motions, orders, depositions, exhibits)
- Government documents (DOJ reports, FBI records, Congressional testimony)
- Regulatory filings (SEC, OCC, NYSDFS consent orders, enforcement actions)
- Corporate records (10-K, 8-K, proxy statements, articles of incorporation)
- Tax records (IRS Form 990, 990-PF)
- Property records (deeds, tax assessments)
- Official correspondence (letters, memos with letterhead)
- FOIA releases
- Police reports
- Autopsy/medical examiner reports

**SECONDARY SOURCES (require citation extraction):**
- News articles (NYT, WSJ, Washington Post, local papers)
- Investigative journalism (ProPublica, The Intercept, etc.)
- Magazine features
- Books
- Academic papers
- Blog posts
- Wikipedia articles
- Podcasts/transcripts
- Documentary films
- Social media threads analyzing documents

---

## 3. PRIMARY SOURCE ACQUISITION

### 3.1 Source Hierarchy

Always prefer sources in this order:

| Priority | Source Type | Examples |
|----------|-------------|----------|
| 1 | Official government database | PACER, SEC EDGAR, FBI Vault, OCC.gov |
| 2 | Official agency website | DOJ.gov, NYSDFS.ny.gov, state court sites |
| 3 | Verified legal database | CourtListener, UniCourt, Justia |
| 4 | Verified archive | Internet Archive, DocumentCloud |
| 5 | News outlet hosting | NYT, WSJ (only if they host the actual document) |
| 6 | Other | Only with explicit verification |

### 3.2 Primary Source Database Reference

#### Federal Courts (PACER)
- **URL:** https://pacer.uscourts.gov
- **Access:** Requires PACER account ($0.10/page, $3 cap per document)
- **Free Alternative:** https://www.courtlistener.com (limited coverage)
- **Naming:** `{court}-{case_number}-{ecf_number}-{description}.pdf`
- **Example:** `sdny-15-cv-07433-ecf-1328-giuffre-deposition.pdf`

#### SEC Filings (EDGAR)
- **URL:** https://www.sec.gov/cgi-bin/browse-edgar
- **Access:** Free
- **Naming:** `{ticker}-{form_type}-{date}-{description}.pdf`
- **Example:** `LB-10K-2019-annual-report.pdf`

#### IRS Tax-Exempt Organizations (990s)
- **URL:** https://projects.propublica.org/nonprofits
- **Backup:** https://www.irs.gov/charities-non-profits/tax-exempt-organization-search
- **Access:** Free (ProPublica), or IRS Form 4506-A for older records
- **Naming:** `{org_name}-990PF-{year}.pdf`
- **Example:** `wexner-foundation-990PF-2018.pdf`

#### State Corporate Records
- **Ohio:** https://businesssearch.ohiosos.gov
- **Delaware:** https://icis.corp.delaware.gov
- **New York:** https://apps.dos.ny.gov/publicInquiry
- **Naming:** `{state}-{entity_name}-{document_type}.pdf`
- **Example:** `ohio-wexner-foundation-articles-of-incorporation.pdf`

#### NYC Property Records (ACRIS)
- **URL:** https://a836-acris.nyc.gov/CP/
- **Access:** Free
- **Naming:** `nyc-acris-{address_short}-{document_type}-{date}.pdf`
- **Example:** `nyc-acris-9e71st-deed-transfer-1996.pdf`

#### Federal Regulatory Agencies
- **OCC:** https://www.occ.gov/topics/laws-and-regulations/enforcement-actions/index-enforcement-actions.html
- **NYSDFS:** https://www.dfs.ny.gov/reports_and_publications/enforcement_actions
- **FCA (UK):** https://www.fca.org.uk/news/news-stories
- **Naming:** `{agency}-{action_type}-{entity}-{date}.pdf`
- **Example:** `nysdfs-consent-order-deutsche-bank-2020-07-06.pdf`

#### FBI Records
- **FBI Vault:** https://vault.fbi.gov
- **FOIA Portal:** https://vault.fbi.gov/foia-request
- **Naming:** `fbi-{subject}-{release_date}-{part_number}.pdf`
- **Example:** `fbi-epstein-foia-2020-part1.pdf`

#### Congressional Records
- **URL:** https://www.congress.gov
- **Hearing Transcripts:** GPO.gov
- **Naming:** `congress-{session}-{committee}-{subject}-{date}.pdf`
- **Example:** `congress-116th-judiciary-epstein-oversight-2019-07-12.pdf`

### 3.3 Acquisition Steps

For EACH primary source document:

```
STEP 1: IDENTIFY
    - Confirm document exists
    - Identify authoritative source
    - Note any access requirements (login, fees)
    - Record source URL

STEP 2: DOWNLOAD
    - Download from highest-priority available source
    - Use appropriate method:
        * Direct download for freely available
        * WebFetch for web-hosted PDFs
        * Note if manual download required (e.g., PACER login)
    - Verify download completed successfully

STEP 3: VERIFY
    - Check file integrity (not corrupted, opens correctly)
    - Verify content matches expected document
    - Check page count if known
    - Confirm it's the correct version (final, not draft)
    - Look for official headers/stamps/signatures

STEP 4: NAME
    - Apply naming convention from Section 3.2
    - Use lowercase, hyphens, no spaces
    - Include date where applicable
    - Be descriptive but concise

STEP 5: STORE
    - Place in appropriate category directory:
        /continuum/website/sources/{category}/{subcategory}/
    - Categories:
        * court-filings/giuffre-v-maxwell/
        * court-filings/jpmorgan-litigation/
        * regulatory/sec/
        * regulatory/nysdfs/
        * regulatory/occ/
        * financial-enablers/jpmorgan/
        * financial-enablers/deutsche-bank/
        * financial-enablers/wexner/
        * florida-case/
        * estate/
        * fbi/
        * congressional/

STEP 6: LOG
    - Add entry to acquisition report (Section 6)
    - Update relevant manifest.json if exists
    - Note any issues or anomalies
```

### 3.4 Handling Paywalled/Gated Sources

When a source requires payment or special access:

```
IF source requires PACER account:
    → Note in report: "PACER document - requires login"
    → Provide exact URL and search parameters
    → Estimate cost ($0.10/page, $3 cap)
    → Mark as PENDING_MANUAL_DOWNLOAD

IF source requires subscription (NYT, WSJ, etc.):
    → Try Internet Archive Wayback Machine first
    → Try CourtListener for court docs
    → If unavailable, note in report with exact URL
    → Mark as PENDING_MANUAL_DOWNLOAD

IF source requires FOIA request:
    → Draft FOIA request letter (see templates in /continuum/research/foia/)
    → Note estimated wait time (3-12 months)
    → Mark as FOIA_REQUIRED
    → Add to FOIA tracking list

IF source requires state records request:
    → Note specific agency and contact
    → Estimate cost if fees apply
    → Mark as RECORDS_REQUEST_REQUIRED
```

---

## 4. SECONDARY SOURCE PROCESSING

### 4.1 The Mandatory Extraction Requirement

**THIS IS NOT OPTIONAL.**

When you acquire ANY secondary source (news article, investigative piece, book chapter, etc.), you MUST:

1. Read/parse the entire document
2. Extract EVERY citation to a primary source
3. Create acquisition tasks for each primary source
4. Execute those acquisition tasks
5. Document the citation chain

### 4.2 Citation Extraction Process

```
FOR each secondary source acquired:

    STEP 1: FULL TEXT ANALYSIS
        - Read the entire document
        - Identify all references to:
            * Court cases (by name or docket number)
            * Government reports
            * Regulatory filings
            * Official documents
            * Testimony/depositions
            * Corporate filings
            * Tax records
            * Any document that could be independently obtained

    STEP 2: CREATE CITATION LIST
        - Document each citation with:
            * What document is referenced
            * Where in secondary source it appears
            * Any identifying info (case number, date, parties)
            * Whether it appears to be publicly available

    STEP 3: CLASSIFY EACH CITATION
        - PRIMARY_OBTAINABLE: Can be downloaded from public source
        - PRIMARY_GATED: Exists but requires access/payment
        - PRIMARY_UNKNOWN: Referenced but unclear if obtainable
        - NOT_PRIMARY: Reference to another secondary source

    STEP 4: ACQUIRE PRIMARY_OBTAINABLE
        - For each obtainable primary source:
        - Execute Section 3 (Primary Source Acquisition)
        - Link acquisition to originating secondary source

    STEP 5: DOCUMENT GATED/UNKNOWN
        - For each gated or unknown source:
        - Document in acquisition report
        - Note access requirements
        - Flag for manual follow-up

    STEP 6: CREATE CITATION MAP
        - Output artifact linking:
            * Secondary source → All primary sources it cites
            * Which were acquired
            * Which are pending
            * Which are unobtainable
```

### 4.3 Citation Patterns to Recognize

Look for these patterns in secondary sources:

```
COURT FILINGS:
    - "according to court documents"
    - "the complaint alleges"
    - "in a motion filed"
    - "docket number 15-cv-07433"
    - "ECF No. 1328"
    - "filed in [Court Name]"
    - "Judge [Name] ruled"

REGULATORY DOCUMENTS:
    - "consent order"
    - "enforcement action"
    - "regulatory filing"
    - "SEC disclosure"
    - "[Agency] found that"
    - "penalty of $X million"

GOVERNMENT REPORTS:
    - "DOJ investigation"
    - "FBI records show"
    - "Congressional testimony"
    - "Inspector General report"
    - "according to [Agency]"

CORPORATE FILINGS:
    - "SEC filing"
    - "10-K"
    - "proxy statement"
    - "disclosed in"

TAX RECORDS:
    - "Form 990"
    - "tax filings show"
    - "IRS records"

DEPOSITIONS/TESTIMONY:
    - "testified that"
    - "in a deposition"
    - "under oath"
    - "sworn statement"
```

### 4.4 Example: Processing a News Article

**Input:** NYT article "JPMorgan Agrees to Pay $290 Million to Settle Epstein Claims"

**Citation Extraction Output:**

```markdown
## Citation Extraction Report
**Source:** NYT article "JPMorgan Agrees to Pay $290 Million..."
**Date Acquired:** 2026-01-05
**Analyst:** Claude Code Session

### Citations Found

1. **Jane Doe v. JPMorgan Chase (S.D.N.Y.)**
   - Reference: "class-action lawsuit filed in November 2022"
   - Case Number: 1:22-cv-10019
   - Status: PRIMARY_OBTAINABLE
   - Action: Acquire complaint from PACER/CourtListener

2. **Settlement Agreement**
   - Reference: "the settlement, announced Tuesday"
   - Case Number: Same as above
   - Status: PRIMARY_OBTAINABLE (if filed publicly)
   - Action: Check PACER for stipulation of settlement

3. **USVI v. JPMorgan**
   - Reference: "separate lawsuit by the U.S. Virgin Islands"
   - Case Number: 1:22-cv-10904
   - Status: PRIMARY_OBTAINABLE
   - Action: Acquire complaint from PACER/CourtListener

4. **OCC Consent Order (2013)**
   - Reference: "the bank was under a consent order related to anti-money laundering"
   - Document: OCC enforcement action
   - Status: PRIMARY_OBTAINABLE
   - Action: Acquire from OCC.gov

5. **Epstein's 2008 Plea Deal**
   - Reference: "after Epstein pleaded guilty in Florida"
   - Document: NPA/plea agreement
   - Status: PRIMARY_OBTAINABLE
   - Action: Verify we have this in /florida-case/

### Acquisition Actions

| Document | Source | Status | File |
|----------|--------|--------|------|
| Jane Doe complaint | CourtListener | ACQUIRED | jane-doe-v-jpmorgan-complaint-2022-11-24.pdf |
| Settlement stipulation | PACER | PENDING_MANUAL | (requires PACER login) |
| USVI complaint | CourtListener | ACQUIRED | usvi-v-jpmorgan-complaint-2022-12-27.pdf |
| OCC consent order | OCC.gov | ACQUIRED | occ-consent-order-2013-01-14.pdf |
| Florida NPA | Already in corpus | VERIFIED | 2008-EPSTEIN-FLORIDA-NPA.pdf |
```

---

## 5. VERIFICATION REQUIREMENTS

### 5.1 Mandatory Verification Checklist

For EVERY document acquired, verify:

```
□ FILE INTEGRITY
    - File opens without errors
    - Not corrupted or truncated
    - Correct file format (PDF, etc.)
    - Reasonable file size (not 0 bytes, not suspiciously small)

□ CONTENT AUTHENTICITY
    - Content matches expected document
    - Official headers/letterhead present (where expected)
    - Correct parties/names/dates
    - Page count matches expectations (if known)
    - No obvious alterations or redactions beyond official ones

□ SOURCE VERIFICATION
    - Downloaded from authoritative source
    - URL recorded
    - Access date recorded
    - Any intermediary sources noted

□ VERSION CONFIRMATION
    - This is the final version (not draft)
    - Most recent version (if multiple exist)
    - Correct exhibit/attachment (if part of larger filing)

□ NAMING COMPLIANCE
    - Follows naming convention in Section 3.2
    - Descriptive and unique
    - Lowercase with hyphens
    - Date included where applicable
```

### 5.2 Red Flags

Stop and investigate if you encounter:

- Document size is 0 bytes or < 1KB
- PDF won't open or is corrupted
- Content doesn't match filename
- Source URL is suspicious or unofficial
- Document appears altered
- Dates don't match expected timeline
- Names are misspelled or different from other sources
- Document claims to be "leaked" without verification
- File hosted on unknown or untrusted domain

### 5.3 Verification Failures

If verification fails:

```
1. DO NOT store the document in sources/
2. Note the issue in acquisition report
3. Attempt to find alternate source
4. If no alternate available:
    - Document the problem
    - Mark as VERIFICATION_FAILED
    - Include what went wrong
5. Move to next document
```

---

## 6. OUTPUT ARTIFACTS

### 6.1 Acquisition Report Format

Every acquisition session MUST produce an acquisition report:

```markdown
# Document Acquisition Report

**Session ID:** {unique_id}
**Date:** {YYYY-MM-DD}
**Analyst:** Claude Code
**Request:** {original user request}

---

## Summary

| Metric | Count |
|--------|-------|
| Documents Requested | X |
| Primary Sources Acquired | X |
| Secondary Sources Acquired | X |
| Primary Sources Extracted from Secondary | X |
| Pending Manual Download | X |
| Failed/Unavailable | X |
| **Total Documents Acquired** | **X** |

---

## Primary Sources Acquired

### 1. {Document Title}
- **File:** `{filename.pdf}`
- **Source:** {URL}
- **Category:** {category/subcategory}
- **Date Acquired:** {date}
- **File Size:** {size}
- **Verification:** ✓ PASSED
- **Notes:** {any relevant notes}

### 2. {Next Document}
...

---

## Secondary Sources Processed

### 1. {Article/Report Title}
- **File:** `{filename.pdf}` (or saved as markdown)
- **Source:** {URL}
- **Citations Found:** {count}
- **Primary Sources Extracted:** {count}
- **Citation Map:** See Section X

---

## Pending Manual Download

| Document | Source | Reason | Estimated Cost |
|----------|--------|--------|----------------|
| {doc} | PACER | Requires login | ~$3 |
| {doc} | NYT | Paywall | Subscription |

---

## Failed/Unavailable

| Document | Reason | Attempted Sources |
|----------|--------|-------------------|
| {doc} | 404 Not Found | URL1, URL2 |
| {doc} | Access Denied | URL1 |

---

## Citation Map

### From: {Secondary Source Title}

```
{Secondary Source}
    ├── {Primary Source 1} ✓ ACQUIRED
    ├── {Primary Source 2} ✓ ACQUIRED
    ├── {Primary Source 3} ⏳ PENDING
    └── {Primary Source 4} ✗ UNAVAILABLE
```

---

## File Manifest Updates

Files added to:
- `/continuum/website/sources/{path}/`: {count} files
- Manifest updated: {yes/no}

---

## Recommendations

{Any follow-up actions, FOIA requests needed, etc.}

---

**Report Generated:** {timestamp}
```

### 6.2 File Placement

```
ACQUIRED DOCUMENTS GO TO:
    /continuum/website/sources/{category}/{subcategory}/

ACQUISITION REPORTS GO TO:
    /continuum/reports/acquisition/acquisition-report-{YYYY-MM-DD}-{session_id}.md

CITATION MAPS GO TO:
    /continuum/reports/acquisition/citation-maps/{source_name}-citations.md

FAILED/PENDING LOGS GO TO:
    /continuum/reports/acquisition/pending/{YYYY-MM-DD}-pending.md
```

### 6.3 Manifest Updates

If the target directory has a `manifest.json`, update it:

```json
{
  "last_updated": "2026-01-05",
  "document_count": 15,
  "documents": [
    {
      "filename": "example-document.pdf",
      "title": "Example Document Title",
      "source": "https://source.url",
      "date_acquired": "2026-01-05",
      "date_original": "2020-07-06",
      "type": "consent_order",
      "verified": true
    }
  ]
}
```

---

## 7. SPECIAL CASES

### 7.1 Bulk Court Filings (Full Docket)

When acquiring all filings from a case:

```
1. Start with the docket sheet (list of all filings)
2. Prioritize:
    - Complaints/initial filings
    - Key motions and responses
    - Court orders and opinions
    - Depositions and exhibits
    - Settlement documents
3. Skip:
    - Routine scheduling orders
    - Notice of appearance
    - Duplicate filings
    - Sealed documents (note their existence)
4. Create case-specific subdirectory
5. Create case README.md with timeline
```

### 7.2 FOIA-Only Documents

When a document is only available via FOIA:

```
1. Note document in acquisition report as FOIA_REQUIRED
2. Draft FOIA request (use template in /continuum/research/foia/)
3. Add to FOIA tracking list at /continuum/research/foia/tracking.md
4. Estimate wait time (typically 3-12 months)
5. Set calendar reminder to follow up
6. Document what we expect to receive
```

### 7.3 Multimedia Sources

When a secondary source is video/audio:

```
1. Find transcript if available (official or auto-generated)
2. If no transcript, note key timestamps with citations
3. Extract document references as you would from text
4. Note the multimedia source for reference
5. Prioritize acquiring any documents shown on screen
```

### 7.4 Foreign Language Documents

```
1. Acquire the original document
2. Note the language
3. If critical, find official translation or note translation needed
4. Tag as TRANSLATION_NEEDED in manifest
5. Original always takes precedence
```

### 7.5 Redacted Documents

```
1. Acquire the redacted version
2. Note extent of redactions
3. Check if unredacted version exists (different source, later release)
4. If unredacted found, acquire both and note relationship
5. Naming: add "-redacted" or "-unredacted" suffix
```

---

## 8. QUALITY GATES

### 8.1 Before Completing Session

Before ending an acquisition session, verify:

```
□ All requested documents addressed (acquired, pending, or documented as unavailable)
□ All secondary sources had citations extracted
□ All obtainable primary sources acquired
□ All files follow naming conventions
□ All files passed verification
□ Acquisition report is complete
□ Files are in correct directories
□ Manifests updated (if applicable)
□ Pending items clearly documented
□ No orphaned or misplaced files
```

### 8.2 Minimum Acceptable Output

An acquisition session is NOT complete unless it produces:

1. **Acquisition Report** - Always required
2. **At least one acquired document OR clear documentation of why none available**
3. **Citation map for every secondary source acquired**
4. **Pending/failed list if applicable**

---

## 9. INTEGRATION WITH PIPELINE

### 9.1 After Acquisition

Once documents are acquired:

```
1. Source files in /continuum/website/sources/ are served directly by website
2. Copy source PDFs to Paperless inbox for OCR and indexing:
    - /continuum/paperless-inbox/ OR
    - Paperless web upload
3. Paperless webhook triggers Stage 1 of pipeline
4. Pipeline handles entity extraction, brief generation automatically
```

### 9.2 Updating Existing Briefs

If acquired documents relate to existing briefs:

```
1. Note in acquisition report which briefs may need updating
2. The pipeline (Stage 3) will auto-detect new sources and update briefs
3. Updated briefs go to pending_approval/ for review
```

---

## 10. TEMPLATES

### 10.1 Quick Acquisition Checklist

```markdown
## Quick Acquisition Checklist

**Target:** {what are you acquiring}
**Date:** {date}

### Classification
- [ ] This is a PRIMARY source → Go to Section 3
- [ ] This is a SECONDARY source → Also do Section 4

### Primary Source Acquisition
- [ ] Source identified
- [ ] Downloaded from authoritative source
- [ ] Verification passed
- [ ] Naming convention applied
- [ ] Stored in correct directory
- [ ] Logged in report

### Secondary Source Processing (if applicable)
- [ ] Full text analyzed
- [ ] All citations extracted
- [ ] Citation list created
- [ ] Each citation classified
- [ ] PRIMARY_OBTAINABLE items acquired
- [ ] GATED/UNKNOWN items documented
- [ ] Citation map created

### Completion
- [ ] Acquisition report written
- [ ] All files in correct locations
- [ ] Manifests updated
- [ ] Pending items documented
```

### 10.2 FOIA Request Template

See `/continuum/research/foia/templates/` for FOIA request templates.

---

## 11. REFERENCE TABLES

### 11.1 Source Priority Matrix

| Document Type | Primary Source | Backup Source |
|--------------|----------------|---------------|
| Federal court filings | PACER | CourtListener |
| State court filings | State court website | UniCourt |
| SEC filings | SEC EDGAR | Company IR page |
| 990 tax forms | ProPublica | IRS (via 4506-A) |
| Regulatory orders | Agency website | Archive.org |
| Property records | County assessor | ACRIS (NYC) |
| Corporate records | State SOS | OpenCorporates |
| FBI records | FBI Vault | FOIA request |
| Congressional records | Congress.gov | GPO.gov |

### 11.2 Directory Structure Quick Reference

```
/continuum/website/sources/
├── court-filings/
│   ├── giuffre-v-maxwell/
│   ├── jpmorgan-litigation/
│   ├── maxwell-criminal/
│   └── wild-v-doj/
├── regulatory/
│   ├── sec/
│   ├── occ/
│   ├── nysdfs/
│   └── fca-uk/
├── financial-enablers/
│   ├── jpmorgan/
│   ├── deutsche-bank/
│   └── wexner/
├── florida-case/
├── estate/
├── fbi/
├── congressional/
└── misc/
```

### 11.3 File Naming Quick Reference

| Document Type | Pattern | Example |
|--------------|---------|---------|
| Court filing | `{court}-{case}-{ecf}-{desc}.pdf` | `sdny-15cv07433-ecf1328-giuffre-depo.pdf` |
| SEC filing | `{ticker}-{form}-{date}.pdf` | `LB-10K-2019-12-31.pdf` |
| Regulatory order | `{agency}-{type}-{entity}-{date}.pdf` | `nysdfs-consent-order-db-2020-07-06.pdf` |
| Tax form | `{org}-990PF-{year}.pdf` | `wexner-foundation-990PF-2018.pdf` |
| Property record | `{jurisdiction}-{address}-{type}-{date}.pdf` | `nyc-9e71st-deed-1996.pdf` |

---

## 12. ESCALATION

### 12.1 When to Escalate

Escalate to human operator when:

- Document requires payment > $50
- FOIA request needed for critical document
- Legal concerns about acquiring document
- Document appears to be leaked/unofficial
- Access requires creating account with personal info
- Unsure about document authenticity
- Conflicting versions of same document exist

### 12.2 How to Escalate

```markdown
## ESCALATION NOTICE

**Issue:** {brief description}
**Document:** {what document}
**Reason for Escalation:** {why human decision needed}
**Options:**
1. {option 1}
2. {option 2}
**Recommendation:** {your recommendation if any}
**Blocking:** {yes/no - can we continue with other work?}
```

---

## APPENDIX A: Common Mistakes to Avoid

1. **Acquiring secondary source without extracting citations** - NEVER do this
2. **Skipping verification** - Every document must be verified
3. **Wrong naming convention** - Follow patterns exactly
4. **Wrong directory** - Check directory structure
5. **No acquisition report** - Every session needs a report
6. **Incomplete citation extraction** - Get ALL citations, not just obvious ones
7. **Assuming document doesn't exist** - Try multiple sources before giving up
8. **Not noting pending items** - Document what couldn't be acquired
9. **Overwriting existing files** - Check before placing, version if needed
10. **Ignoring file size/integrity** - Always verify the download

---

## APPENDIX B: Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-05 | Initial release |

---

**Document Control**
- **Owner:** The Continuum Report
- **Next Review:** 2026-02-05
- **Change Authority:** Pipeline Administrator
- **Distribution:** All Claude Code sessions performing document acquisition

---

*End of SOP-005: Document Acquisition Standard*
