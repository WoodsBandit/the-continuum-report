# Paperless Tagging Instructions — Financial Enabler & Florida Case Documents

> **Task for WoodsBandit:** Apply these tags to newly ingested documents in Paperless
> **Date:** 2025-12-23
> **Updated:** With additional regulatory documents

---

## Documents Added to Inbox

14 documents copied to `/continuum/documents/inbox/` for Paperless consumption:

### Financial Enabler Documents (Original 6)

| Filename | Type | Suggested Tags |
|----------|------|----------------|
| `nysdfs-consent-order-2020-07-06.pdf` | Regulatory Action | `CASE: Deutsche-Bank-Epstein`, `SOURCE: NYSDFS`, `TYPE: Consent Order` |
| `doe-v-deutsche-bank-complaint-2022-11-24.pdf` | Court Filing | `CASE: Deutsche-Bank-Epstein`, `TYPE: Complaint`, `CASE: SDNY-1-22-cv-10018` |
| `usvi-v-jpmorgan-complaint-2022-12-27.pdf` | Court Filing | `CASE: JPMorgan-Epstein`, `TYPE: Complaint`, `CASE: SDNY-1-22-cv-10904` |
| `usvi-v-jpmorgan-second-amended-complaint-2023-04-12.pdf` | Court Filing | `CASE: JPMorgan-Epstein`, `TYPE: Complaint`, `CASE: SDNY-1-22-cv-10904` |
| `jpmorgan-v-staley-third-party-complaint-2023-03-08.pdf` | Court Filing | `CASE: JPMorgan-Epstein`, `TYPE: Third-Party Complaint`, `PERSON: Jes Staley` |
| `jane-doe-v-jpmorgan-complaint-2022-11-24.pdf` | Court Filing | `CASE: JPMorgan-Epstein`, `TYPE: Complaint`, `CASE: SDNY-1-22-cv-10019` |

### NEW: Additional Regulatory Documents (8)

| Filename | Type | Suggested Tags |
|----------|------|----------------|
| `nysdfs-consent-order-2017-01-30-mirror-trades.pdf` | Regulatory Action | `ORG: Deutsche Bank`, `SOURCE: NYSDFS`, `TYPE: Consent Order`, `TOPIC: AML`, `TOPIC: Mirror Trades` |
| `fca-final-notice-2017-01-30.pdf` | Regulatory Action | `ORG: Deutsche Bank`, `SOURCE: FCA`, `TYPE: Final Notice`, `TOPIC: AML` |
| `occ-consent-order-2013-01-14.pdf` | Regulatory Action | `ORG: JP Morgan Chase`, `SOURCE: OCC`, `TYPE: Consent Order`, `TOPIC: BSA-AML` |
| `occ-penalty-order-2014-01-07.pdf` | Regulatory Action | `ORG: JP Morgan Chase`, `SOURCE: OCC`, `TYPE: Penalty Order`, `TOPIC: BSA-AML` |
| `wexner-foundation-independent-review.pdf` | Report | `PERSON: Les Wexner`, `PERSON: Jeffrey Epstein`, `ORG: Wexner Foundation`, `TYPE: Independent Review` |
| `2008-EPSTEIN-FLORIDA-NPA-NON-PROSECUTION-AGREEMENT.pdf` | Legal Document | `CASE: Epstein-Florida`, `TYPE: NPA`, `PERSON: Jeffrey Epstein`, `SOURCE: SDFL` |
| `2020-DOJ-OPR-REPORT-EPSTEIN-NPA-INVESTIGATION.pdf` | Government Report | `CASE: Epstein-Florida`, `SOURCE: DOJ-OPR`, `TYPE: Investigation Report` |
| `2020-WILD-V-DOJ-11TH-CIRCUIT-EPSTEIN-CVRA.pdf` | Court Filing | `CASE: Wild-v-DOJ`, `TYPE: Appeals Decision`, `TOPIC: CVRA` |

---

## NEW Tags to Create

### Source Tags
- `SOURCE: FCA` (UK Financial Conduct Authority)
- `SOURCE: OCC` (Office of the Comptroller of the Currency)
- `SOURCE: DOJ-OPR` (DOJ Office of Professional Responsibility)
- `SOURCE: SDFL` (Southern District of Florida)

### Topic Tags
- `TOPIC: AML` (Anti-Money Laundering)
- `TOPIC: BSA-AML` (Bank Secrecy Act violations)
- `TOPIC: Mirror Trades` (Russian mirror trading scheme)
- `TOPIC: CVRA` (Crime Victims' Rights Act)
- `TOPIC: NPA` (Non-Prosecution Agreement)

### Document Type Tags
- `TYPE: Final Notice` (UK regulatory)
- `TYPE: Penalty Order`
- `TYPE: Independent Review`
- `TYPE: NPA` (Non-Prosecution Agreement)
- `TYPE: Investigation Report`
- `TYPE: Appeals Decision`

### Organization Tags
- `ORG: Wexner Foundation`

---

## Document Type Assignment

| Document | Paperless Document Type |
|----------|------------------------|
| Consent Orders, Penalty Orders, Final Notices | `Regulatory Action` |
| Complaints, Third-Party Complaints | `Court Filing` |
| NPA | `Legal Document` |
| DOJ OPR Report, Independent Review | `Government Report` |
| Appeals Decisions | `Court Filing` |

---

## Verification Steps

After Paperless ingests the documents:

1. Check inbox is empty (documents consumed)
2. Search for "Deutsche Bank" — should find 4 docs
3. Search for "JPMorgan" — should find 6 docs
4. Search for "Wexner" — should find 1 doc
5. Search for "Florida" or "NPA" — should find 3 docs
6. Apply tags as listed above
7. Set Document Type for each

---

## Also Hosted At

These documents are now publicly accessible at:
```
https://thecontinuumreport.com/sources/
├── financial-enablers/
│   ├── deutsche-bank/
│   │   ├── nysdfs-consent-order-2020-07-06.pdf
│   │   ├── nysdfs-consent-order-2017-01-30-mirror-trades.pdf
│   │   ├── fca-final-notice-2017-01-30.pdf
│   │   └── doe-v-deutsche-bank-complaint-2022-11-24.pdf
│   ├── jpmorgan/
│   │   ├── usvi-v-jpmorgan-complaint-2022-12-27.pdf
│   │   ├── usvi-v-jpmorgan-second-amended-complaint-2023-04-12.pdf
│   │   ├── jpmorgan-v-staley-third-party-complaint-2023-03-08.pdf
│   │   ├── jane-doe-v-jpmorgan-complaint-2022-11-24.pdf
│   │   ├── occ-consent-order-2013-01-14.pdf
│   │   └── occ-penalty-order-2014-01-07.pdf
│   └── wexner/
│       ├── wexner-foundation-letter-2019-08-08.md
│       └── wexner-foundation-independent-review.pdf
└── florida-case/
    ├── 2008-EPSTEIN-FLORIDA-NPA-NON-PROSECUTION-AGREEMENT.pdf
    ├── 2020-DOJ-OPR-REPORT-EPSTEIN-NPA-INVESTIGATION.pdf
    └── 2020-WILD-V-DOJ-11TH-CIRCUIT-EPSTEIN-CVRA.pdf
```

---

*Task created by ClaudeCode Overseer — 2025-12-23*
*Updated: 2025-12-23 with 8 additional documents*
