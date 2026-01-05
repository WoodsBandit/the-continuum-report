# CLAUDE CODE PROMPT: Continuum Report Document Acquisition System

## MISSION
You are a document acquisition agent for The Continuum Report, an independent OSINT journalism platform. Your task is to systematically download primary source documents from the web and ingest them into a Paperless-ngx document management system with appropriate tagging and metadata.

---

## SYSTEM CONFIGURATION

### Paperless-ngx Server
```
Host: 192.168.1.139
Port: 8040
API Endpoint: http://192.168.1.139:8040/api/
Auth Token: da99fe6aa0b8d021689126cf72b91986abbbd283
```

### Working Directory (IMPORTANT: Use /continuum/ - it has 12TB of space)
```
Download Staging: /continuum/downloads/
Processed Archive: /continuum/processed/
Error Log: /continuum/errors.log
Progress Log: /continuum/progress.json
```

---

## TAGGING TAXONOMY

### Create these tags in Paperless if they don't exist:

#### Document Type Tags (PREFIX: TYPE:)
```
TYPE:COURT-FILING
TYPE:DEPOSITION
TYPE:INDICTMENT
TYPE:SETTLEMENT
TYPE:CONGRESSIONAL-REPORT
TYPE:CONGRESSIONAL-HEARING
TYPE:FBI-FILE
TYPE:CIA-DOCUMENT
TYPE:FOIA-RELEASE
TYPE:SEC-FILING
TYPE:FINANCIAL-RECORD
TYPE:FLIGHT-LOG
TYPE:ADDRESS-BOOK
TYPE:MEDIA-REPORT
TYPE:BOOK-CHAPTER
TYPE:GOVERNMENT-REPORT
TYPE:INVESTIGATION-REPORT
```

#### Case Tags (PREFIX: CASE:)
```
CASE:GIUFFRE-V-MAXWELL
CASE:MAXWELL-CRIMINAL
CASE:EPSTEIN-SDNY-2019
CASE:EPSTEIN-FLORIDA-2008
CASE:USVI-V-JPMORGAN
CASE:JANE-DOE-V-JPMORGAN
CASE:INSLAW-V-DOJ
CASE:IRAN-CONTRA
CASE:BCCI-INVESTIGATION
CASE:CHURCH-COMMITTEE
CASE:NXIVM-RANIERE
```

#### Person Tags (PREFIX: PERSON:)
```
PERSON:JEFFREY-EPSTEIN
PERSON:GHISLAINE-MAXWELL
PERSON:VIRGINIA-GIUFFRE
PERSON:LESLIE-WEXNER
PERSON:ALAN-DERSHOWITZ
PERSON:PRINCE-ANDREW
PERSON:BILL-CLINTON
PERSON:DONALD-TRUMP
PERSON:ROBERT-MAXWELL
PERSON:ROY-COHN
PERSON:KEITH-RANIERE
PERSON:ALEXANDER-ACOSTA
PERSON:SARAH-KELLEN
PERSON:NADIA-MARCINKOVA
```

#### Organization Tags (PREFIX: ORG:)
```
ORG:MOSSAD
ORG:CIA
ORG:FBI
ORG:DOJ
ORG:JPMORGAN
ORG:DEUTSCHE-BANK
ORG:L-BRANDS
ORG:BCCI
ORG:NXIVM
ORG:INSLAW
ORG:NSA
```

#### Network Tags (PREFIX: NETWORK:)
```
NETWORK:EPSTEIN
NETWORK:INTELLIGENCE
NETWORK:FINANCIAL
NETWORK:POLITICAL
NETWORK:BLACKMAIL-OPS
```

#### Layer Tags (PREFIX: LAYER:)
```
LAYER:1-EPSTEIN-CORE
LAYER:2-INTELLIGENCE
LAYER:3-FINANCIAL
LAYER:4-POLITICAL
LAYER:5-PARALLEL-CASES
LAYER:6-DECLASSIFIED
```

#### Priority Tags
```
PRIORITY:CRITICAL
PRIORITY:HIGH
PRIORITY:MEDIUM
PRIORITY:LOW
```

#### Verification Tags
```
VERIFIED:PRIMARY-SOURCE
VERIFIED:COURT-RECORD
VERIFIED:GOVERNMENT-OFFICIAL
UNVERIFIED:SECONDARY-SOURCE
UNVERIFIED:LEAKED
```

---

## DOCUMENT ACQUISITION TASKS

Execute these tasks in order. For each task:
1. Download the document(s) to /continuum/downloads/
2. Rename with standardized naming convention
3. Apply appropriate tags
4. Upload to Paperless via API
5. Log progress to /continuum/progress.json
6. Handle errors gracefully and continue

### Naming Convention
```
[YEAR]-[CASE/SOURCE]-[DOCTYPE]-[DESCRIPTION].pdf
Examples:
2016-GIUFFRE-V-MAXWELL-DEPOSITION-GHISLAINE-MAXWELL.pdf
2008-EPSTEIN-FLORIDA-NPA-NON-PROSECUTION-AGREEMENT.pdf
1992-BCCI-CONGRESSIONAL-REPORT-KERRY-COMMITTEE.pdf
```

---

## TASK 1: EPSTEIN FLIGHT LOGS

### 1.1 Internet Archive - Main Collection
```
URL: https://archive.org/download/EpsteinFlightLogsLolitaExpress/Jeffrey%20Epstein%20Flight%20Logs.pdf
Filename: 1995-2005-EPSTEIN-FLIGHT-LOGS-LOLITA-EXPRESS.pdf
Title: Jeffrey Epstein Flight Logs - Lolita Express (1995-2005)
Tags: TYPE:FLIGHT-LOG, PERSON:JEFFREY-EPSTEIN, NETWORK:EPSTEIN, LAYER:1-EPSTEIN-CORE, PRIORITY:CRITICAL, VERIFIED:COURT-RECORD
```

### 1.2 Unredacted Flight Logs
```
URL: https://ia801606.us.archive.org/30/items/epstein-flight-logs-unredacted_202304/EPSTEIN%20FLIGHT%20LOGS%20UNREDACTED.pdf
Filename: 1995-2005-EPSTEIN-FLIGHT-LOGS-UNREDACTED.pdf
Title: Jeffrey Epstein Flight Logs - Unredacted Version
Tags: TYPE:FLIGHT-LOG, PERSON:JEFFREY-EPSTEIN, NETWORK:EPSTEIN, LAYER:1-EPSTEIN-CORE, PRIORITY:CRITICAL, VERIFIED:COURT-RECORD
```

---

## TASK 2: EPSTEIN BLACK BOOK

### 2.1 Unredacted Version
```
URL: https://archive.org/download/jeffrey-epstein-39s-little-black-book-unredacted/Jeffrey%20Epstein%27s%20Little%20Black%20Book%20unredacted.pdf
Filename: 2004-EPSTEIN-ADDRESS-BOOK-BLACK-BOOK-UNREDACTED.pdf
Title: Jeffrey Epstein's Black Book - Unredacted (2004)
Tags: TYPE:ADDRESS-BOOK, PERSON:JEFFREY-EPSTEIN, NETWORK:EPSTEIN, LAYER:1-EPSTEIN-CORE, PRIORITY:CRITICAL, VERIFIED:COURT-RECORD
```

### 2.2 Redacted Court Version
```
URL: https://www.documentcloud.org/documents/1508273-jeffrey-epsteins-little-black-book-redacted.pdf
Filename: 2004-EPSTEIN-ADDRESS-BOOK-BLACK-BOOK-REDACTED.pdf
Title: Jeffrey Epstein's Black Book - Redacted Court Version
Tags: TYPE:ADDRESS-BOOK, PERSON:JEFFREY-EPSTEIN, NETWORK:EPSTEIN, LAYER:1-EPSTEIN-CORE, PRIORITY:HIGH, VERIFIED:COURT-RECORD
```

---

## TASK 3: 2008 NON-PROSECUTION AGREEMENT

### 3.1 NPA Document
```
URL: https://www.documentcloud.org/documents/6184602-Jeffrey-Epstein-non-prosecution-agreement.pdf
Filename: 2008-EPSTEIN-FLORIDA-NPA-NON-PROSECUTION-AGREEMENT.pdf
Title: Epstein Non-Prosecution Agreement (2008)
Tags: TYPE:COURT-FILING, CASE:EPSTEIN-FLORIDA-2008, PERSON:JEFFREY-EPSTEIN, PERSON:ALEXANDER-ACOSTA, ORG:DOJ, NETWORK:EPSTEIN, LAYER:1-EPSTEIN-CORE, PRIORITY:CRITICAL, VERIFIED:COURT-RECORD
```

### 3.2 DOJ OPR Investigation Report
```
URL: https://www.justice.gov/opr/page/file/1336471/dl
Filename: 2020-DOJ-OPR-REPORT-EPSTEIN-NPA-INVESTIGATION.pdf
Title: DOJ Office of Professional Responsibility Report - Epstein NPA Investigation
Tags: TYPE:INVESTIGATION-REPORT, TYPE:GOVERNMENT-REPORT, CASE:EPSTEIN-FLORIDA-2008, PERSON:JEFFREY-EPSTEIN, PERSON:ALEXANDER-ACOSTA, ORG:DOJ, LAYER:1-EPSTEIN-CORE, PRIORITY:CRITICAL, VERIFIED:GOVERNMENT-OFFICIAL
```

---

## TASK 4: JP MORGAN LAWSUIT

### 4.1 Original USVI Complaint
```
URL: https://static.foxbusiness.com/foxbusiness.com/content/uploads/2022/12/U.S.-Virgin-Islands-v-JP-Morgan.pdf
Filename: 2022-USVI-V-JPMORGAN-COMPLAINT-EPSTEIN-TRAFFICKING.pdf
Title: USVI v. JP Morgan - Complaint (Epstein Trafficking)
Tags: TYPE:COURT-FILING, CASE:USVI-V-JPMORGAN, PERSON:JEFFREY-EPSTEIN, ORG:JPMORGAN, NETWORK:EPSTEIN, NETWORK:FINANCIAL, LAYER:1-EPSTEIN-CORE, LAYER:3-FINANCIAL, PRIORITY:CRITICAL, VERIFIED:COURT-RECORD
```

---

## TASK 5: INSLAW / PROMIS DOCUMENTS

### 5.1 Internet Archive Chapter
```
URL: https://ia601309.us.archive.org/23/items/TheInslawAffair/Chapter%2017%20-%20The%20Inslaw%20Affair.pdf
Filename: 1992-INSLAW-AFFAIR-CHAPTER-17-ANALYSIS.pdf
Title: The Inslaw Affair - Chapter 17 Analysis
Tags: TYPE:BOOK-CHAPTER, CASE:INSLAW-V-DOJ, ORG:DOJ, ORG:INSLAW, NETWORK:INTELLIGENCE, LAYER:2-INTELLIGENCE, PRIORITY:HIGH
```

---

## TASK 6: IRAN-CONTRA DOCUMENTS

### 6.1 Main Congressional Report
```
URL: https://archive.org/download/ReportOnTheIranContraAffair/Report-on-the-Iran-Contra-Affair.pdf
Filename: 1987-IRAN-CONTRA-CONGRESSIONAL-REPORT-MAIN.pdf
Title: Report of Congressional Committees Investigating Iran-Contra Affair
Tags: TYPE:CONGRESSIONAL-REPORT, CASE:IRAN-CONTRA, ORG:CIA, NETWORK:INTELLIGENCE, LAYER:2-INTELLIGENCE, PRIORITY:CRITICAL, VERIFIED:GOVERNMENT-OFFICIAL
```

### 6.2 Tower Commission Report
```
URL: https://archive.org/download/ReportOnTheIranContraAffair/The-Tower-Report-on-Iran-Contra-Affair.pdf
Filename: 1987-IRAN-CONTRA-TOWER-COMMISSION-REPORT.pdf
Title: Tower Commission Report on Iran-Contra Affair
Tags: TYPE:GOVERNMENT-REPORT, CASE:IRAN-CONTRA, ORG:CIA, NETWORK:INTELLIGENCE, LAYER:2-INTELLIGENCE, PRIORITY:HIGH, VERIFIED:GOVERNMENT-OFFICIAL
```

---

## TASK 7: BCCI INVESTIGATION

### 7.1 Kerry Committee Report
```
URL: https://info.publicintelligence.net/The-BCCI-Affair.pdf
Filename: 1992-BCCI-KERRY-COMMITTEE-REPORT-FULL.pdf
Title: The BCCI Affair - Kerry Committee Report
Tags: TYPE:CONGRESSIONAL-REPORT, CASE:BCCI-INVESTIGATION, ORG:BCCI, ORG:CIA, NETWORK:INTELLIGENCE, NETWORK:FINANCIAL, LAYER:2-INTELLIGENCE, LAYER:3-FINANCIAL, PRIORITY:CRITICAL, VERIFIED:GOVERNMENT-OFFICIAL
```

---

## TASK 8: CHURCH COMMITTEE REPORTS

### 8.1 Brennan Center Analysis
```
URL: https://www.brennancenter.org/sites/default/files/publications/Church_Committee_Report.pdf
Filename: 2015-CHURCH-COMMITTEE-BRENNAN-CENTER-ANALYSIS.pdf
Title: Church Committee - Brennan Center Analysis
Tags: TYPE:GOVERNMENT-REPORT, CASE:CHURCH-COMMITTEE, ORG:CIA, ORG:FBI, ORG:NSA, NETWORK:INTELLIGENCE, LAYER:2-INTELLIGENCE, PRIORITY:MEDIUM
```

---

## TASK 9: ROY COHN FBI FILES

### 9.1 Note: Download from Internet Archive collection
```
URL: https://archive.org/details/RoyCohn
Action: Download all PDF files from this collection
Filename Pattern: [YEAR]-ROY-COHN-FBI-FILE-PART-[N].pdf
Tags: TYPE:FBI-FILE, TYPE:FOIA-RELEASE, PERSON:ROY-COHN, ORG:FBI, NETWORK:POLITICAL, NETWORK:BLACKMAIL-OPS, LAYER:4-POLITICAL, PRIORITY:HIGH, VERIFIED:GOVERNMENT-OFFICIAL
```

---

## TASK 10: ROBERT MAXWELL DOCUMENTS

### 10.1 Book - Robert Maxwell Israel's Superspy
```
URL: https://archive.org/download/thomas_gordon_dillon_martin_robert_maxwell_israels_superspy/thomas_gordon_dillon_martin_robert_maxwell_israels_superspy.pdf
Filename: 2002-ROBERT-MAXWELL-ISRAELS-SUPERSPY-THOMAS.pdf
Title: Robert Maxwell, Israel's Superspy - Gordon Thomas
Tags: TYPE:BOOK-CHAPTER, PERSON:ROBERT-MAXWELL, ORG:MOSSAD, NETWORK:INTELLIGENCE, LAYER:2-INTELLIGENCE, PRIORITY:HIGH, UNVERIFIED:SECONDARY-SOURCE
```

---

## TASK 11: NXIVM CASE DOCUMENTS

### 11.1 Superseding Indictment
```
URL: https://www.justice.gov/usao-edny/press-release/file/1046381/download
Filename: 2018-NXIVM-RANIERE-SUPERSEDING-INDICTMENT.pdf
Title: NXIVM - Keith Raniere Superseding Indictment
Tags: TYPE:INDICTMENT, CASE:NXIVM-RANIERE, PERSON:KEITH-RANIERE, ORG:NXIVM, NETWORK:BLACKMAIL-OPS, LAYER:5-PARALLEL-CASES, PRIORITY:HIGH, VERIFIED:COURT-RECORD
```

### 11.2 Sentencing Memo
```
URL: https://www.courthousenews.com/wp-content/uploads/2020/10/Raniere-Sentencing-Memo.pdf
Filename: 2020-NXIVM-RANIERE-GOVERNMENT-SENTENCING-MEMO.pdf
Title: NXIVM - Keith Raniere Government Sentencing Memorandum
Tags: TYPE:COURT-FILING, CASE:NXIVM-RANIERE, PERSON:KEITH-RANIERE, ORG:NXIVM, NETWORK:BLACKMAIL-OPS, LAYER:5-PARALLEL-CASES, PRIORITY:HIGH, VERIFIED:COURT-RECORD
```

---

## TASK 12: COURT APPEALS

### 12.1 Wild v. DOJ (11th Circuit - Epstein Victims)
```
URL: https://media.ca11.uscourts.gov/opinions/pub/files/201913843.pdf
Filename: 2020-WILD-V-DOJ-11TH-CIRCUIT-EPSTEIN-CVRA.pdf
Title: Wild v. DOJ - 11th Circuit Opinion (Epstein CVRA)
Tags: TYPE:COURT-FILING, CASE:EPSTEIN-FLORIDA-2008, PERSON:JEFFREY-EPSTEIN, ORG:DOJ, LAYER:1-EPSTEIN-CORE, PRIORITY:HIGH, VERIFIED:COURT-RECORD
```

---

## EXECUTION INSTRUCTIONS

1. Create directory: `mkdir -p /continuum/downloads`
2. For each task above, download the file using curl or wget
3. Upload to Paperless using this API call format:

```bash
curl -X POST "http://192.168.1.139:8040/api/documents/post_document/" \
  -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
  -F "document=@/continuum/downloads/FILENAME.pdf" \
  -F "title=TITLE" \
  -F "tags=TAG_ID1,TAG_ID2"
```

4. First create any tags that don't exist using:
```bash
curl -X POST "http://192.168.1.139:8040/api/tags/" \
  -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
  -H "Content-Type: application/json" \
  -d '{"name": "TAG_NAME"}'
```

5. Save progress after each successful upload to /continuum/progress.json
6. If a download fails, log the error and continue to the next document
7. Add 2 second delay between downloads to avoid rate limiting

---

## START EXECUTION NOW

Begin with Task 1 and work through all tasks sequentially. Report progress as you go.
