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
Consumption Folder: /mnt/user/appdata/paperless/consume/
```

### Network Share (for direct file drops)
```
SMB Path: \\192.168.1.139\continuum\documents\inbox\
Mount Point: /mnt/continuum/documents/inbox/
```

### Working Directory
```
Download Staging: ~/continuum_downloads/
Processed Archive: ~/continuum_processed/
Error Log: ~/continuum_errors.log
Progress Log: ~/continuum_progress.json
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
1. Download the document(s)
2. Rename with standardized naming convention
3. Apply appropriate tags
4. Upload to Paperless via API or consumption folder
5. Log progress to checkpoint file
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
```python
# Download from Internet Archive
urls = [
    "https://archive.org/download/EpsteinFlightLogsLolitaExpress/Jeffrey%20Epstein%20Flight%20Logs.pdf",
    "https://ia801606.us.archive.org/30/items/epstein-flight-logs-unredacted_202304/EPSTEIN%20FLIGHT%20LOGS%20UNREDACTED.pdf"
]

# Tags to apply:
tags = [
    "TYPE:FLIGHT-LOG",
    "PERSON:JEFFREY-EPSTEIN",
    "NETWORK:EPSTEIN",
    "LAYER:1-EPSTEIN-CORE",
    "PRIORITY:CRITICAL",
    "VERIFIED:COURT-RECORD"
]

# Naming:
# 1995-2005-EPSTEIN-FLIGHT-LOGS-LOLITA-EXPRESS.pdf
# 1995-2005-EPSTEIN-FLIGHT-LOGS-UNREDACTED.pdf
```

### 1.2 DocumentCloud Flight Logs
```python
url = "https://www.documentcloud.org/documents/6404379-Epstein-Flight-Logs-Lolita-Express.pdf"
# Same tags as above
```

---

## TASK 2: EPSTEIN BLACK BOOK

### 2.1 Unredacted Version
```python
# Internet Archive
url = "https://archive.org/download/jeffrey-epstein-39s-little-black-book-unredacted/Jeffrey%20Epstein%27s%20Little%20Black%20Book%20unredacted.pdf"

tags = [
    "TYPE:ADDRESS-BOOK",
    "PERSON:JEFFREY-EPSTEIN",
    "NETWORK:EPSTEIN",
    "LAYER:1-EPSTEIN-CORE",
    "PRIORITY:CRITICAL",
    "VERIFIED:COURT-RECORD"
]

# Naming: 2004-EPSTEIN-ADDRESS-BOOK-BLACK-BOOK-UNREDACTED.pdf
```

### 2.2 Redacted Court Version
```python
url = "https://www.documentcloud.org/documents/1508273-jeffrey-epsteins-little-black-book-redacted.pdf"
# Naming: 2004-EPSTEIN-ADDRESS-BOOK-BLACK-BOOK-REDACTED.pdf
```

---

## TASK 3: 2008 NON-PROSECUTION AGREEMENT

### 3.1 NPA Document
```python
url = "https://www.documentcloud.org/documents/6184602-Jeffrey-Epstein-non-prosecution-agreement.pdf"

tags = [
    "TYPE:COURT-FILING",
    "CASE:EPSTEIN-FLORIDA-2008",
    "PERSON:JEFFREY-EPSTEIN",
    "PERSON:ALEXANDER-ACOSTA",
    "ORG:DOJ",
    "NETWORK:EPSTEIN",
    "LAYER:1-EPSTEIN-CORE",
    "PRIORITY:CRITICAL",
    "VERIFIED:COURT-RECORD"
]

# Naming: 2008-EPSTEIN-FLORIDA-NPA-NON-PROSECUTION-AGREEMENT.pdf
```

### 3.2 Alternative NPA Source
```python
url = "https://reason.com/wp-content/uploads/2021/08/Non-Prosecution-Agreement-1433.pdf"
```

### 3.3 DOJ OPR Investigation Report
```python
url = "https://www.justice.gov/opr/page/file/1336471/dl"

tags = [
    "TYPE:INVESTIGATION-REPORT",
    "TYPE:GOVERNMENT-REPORT",
    "CASE:EPSTEIN-FLORIDA-2008",
    "PERSON:JEFFREY-EPSTEIN",
    "PERSON:ALEXANDER-ACOSTA",
    "ORG:DOJ",
    "LAYER:1-EPSTEIN-CORE",
    "PRIORITY:CRITICAL",
    "VERIFIED:GOVERNMENT-OFFICIAL"
]

# Naming: 2020-DOJ-OPR-REPORT-EPSTEIN-NPA-INVESTIGATION.pdf
```

---

## TASK 4: GIUFFRE V. MAXWELL UNSEALED DOCUMENTS

### 4.1 Public Intelligence Batches
```python
# Scrape and download all batches
base_urls = [
    "https://publicintelligence.net/epstein-docs-batch-1/",
    "https://publicintelligence.net/epstein-docs-batch-2/",
    "https://publicintelligence.net/epstein-docs-batch-3/",
    "https://publicintelligence.net/epstein-docs-batch-4/",
    "https://publicintelligence.net/epstein-docs-batch-5/",
    "https://publicintelligence.net/epstein-docs-batch-6/",
    "https://publicintelligence.net/epstein-docs-batch-7/",
    "https://publicintelligence.net/epstein-docs-batch-8/"
]

# For each batch, download all PDF attachments

tags = [
    "TYPE:COURT-FILING",
    "CASE:GIUFFRE-V-MAXWELL",
    "PERSON:VIRGINIA-GIUFFRE",
    "PERSON:GHISLAINE-MAXWELL",
    "NETWORK:EPSTEIN",
    "LAYER:1-EPSTEIN-CORE",
    "PRIORITY:CRITICAL",
    "VERIFIED:COURT-RECORD"
]

# Naming: 2024-GIUFFRE-V-MAXWELL-UNSEALED-BATCH-[N]-[DESCRIPTION].pdf
```

### 4.2 Epstein Archive Collection
```python
# Scrape https://www.epsteinarchive.org/docs/giuffre-v-maxwell-unsealed/
# Download all available documents
```

---

## TASK 5: JP MORGAN LAWSUIT DOCUMENTS

### 5.1 Original USVI Complaint
```python
url = "https://static.foxbusiness.com/foxbusiness.com/content/uploads/2022/12/U.S.-Virgin-Islands-v-JP-Morgan.pdf"

tags = [
    "TYPE:COURT-FILING",
    "CASE:USVI-V-JPMORGAN",
    "PERSON:JEFFREY-EPSTEIN",
    "ORG:JPMORGAN",
    "NETWORK:EPSTEIN",
    "NETWORK:FINANCIAL",
    "LAYER:1-EPSTEIN-CORE",
    "LAYER:3-FINANCIAL",
    "PRIORITY:CRITICAL",
    "VERIFIED:COURT-RECORD"
]

# Naming: 2022-USVI-V-JPMORGAN-COMPLAINT-EPSTEIN-TRAFFICKING.pdf
```

### 5.2 CourtListener Docket Scrape
```python
# Scrape all available documents from:
# https://www.courtlistener.com/docket/66683865/government-of-the-united-states-virgin-islands-v-jpmorgan-chase-bank-na/

# Use RECAP/CourtListener API if available
# Download all free documents from docket
```

---

## TASK 6: INSLAW / PROMIS DOCUMENTS

### 6.1 The Black Vault Collection
```python
url = "https://www.theblackvault.com/documentarchive/nsa-surveillance-program-promis/"
# Download the Bua Report and related documents

tags = [
    "TYPE:INVESTIGATION-REPORT",
    "TYPE:GOVERNMENT-REPORT",
    "CASE:INSLAW-V-DOJ",
    "ORG:DOJ",
    "ORG:NSA",
    "ORG:INSLAW",
    "NETWORK:INTELLIGENCE",
    "LAYER:2-INTELLIGENCE",
    "PRIORITY:CRITICAL",
    "VERIFIED:GOVERNMENT-OFFICIAL"
]

# Naming: 1993-INSLAW-BUA-REPORT-PROMIS-SPECIAL-COUNSEL.pdf
```

### 6.2 Internet Archive Chapter
```python
url = "https://ia601309.us.archive.org/23/items/TheInslawAffair/Chapter%2017%20-%20The%20Inslaw%20Affair.pdf"

# Naming: 1992-INSLAW-AFFAIR-CHAPTER-17-ANALYSIS.pdf
```

---

## TASK 7: IRAN-CONTRA DOCUMENTS

### 7.1 Main Congressional Report
```python
# Internet Archive collection
collection_url = "https://archive.org/details/Iran-ContraReport"

# Download main report:
url = "https://archive.org/download/Iran-ContraReport/Report%20of%20the%20Congressional%20Committees%20Investigating%20the%20Iran-Contra%20Affair.pdf"

tags = [
    "TYPE:CONGRESSIONAL-REPORT",
    "CASE:IRAN-CONTRA",
    "ORG:CIA",
    "NETWORK:INTELLIGENCE",
    "LAYER:2-INTELLIGENCE",
    "PRIORITY:CRITICAL",
    "VERIFIED:GOVERNMENT-OFFICIAL"
]

# Naming: 1987-IRAN-CONTRA-CONGRESSIONAL-REPORT-MAIN.pdf
```

### 7.2 Appendix A - Source Documents
```python
urls = [
    "https://archive.org/download/Iran-ContraReport/Report%20of%20the%20Congressional%20Committees%20Investigating%20the%20Iran-Contra%20Affair%2C%20Appendix%20A%2C%20Volume%201-%20Source%20Documents.pdf",
    "https://archive.org/download/Iran-ContraReport/Report%20of%20the%20Congressional%20Committees%20Investigating%20the%20Iran-Contra%20Affair%2C%20Appendix%20A%2C%20Volume%202-%20Source%20Documents.pdf"
]
```

### 7.3 Appendix B - Depositions (All 27 Volumes)
```python
# Download all deposition volumes
# Pattern: Report of the Congressional Committees Investigating the Iran-Contra Affair, Appendix B, Volume [N]; Depositions_ [Names].pdf

# Priority depositions:
priority_volumes = [13, 15, 24, 25]  # Hakim, Koch-Ledeen, Rugg-Secord, Shackley-Singlaub
```

### 7.4 Tower Commission Report
```python
url = "https://archive.org/download/ReportOnTheIranContraAffair/The-Tower-Report-on-Iran-Contra-Affair.pdf"

# Naming: 1987-IRAN-CONTRA-TOWER-COMMISSION-REPORT.pdf
```

### 7.5 Independent Counsel Final Report
```python
# From Internet Archive: IranContraInvestigationFinalReport
url = "https://archive.org/details/IranContraInvestigationFinalReport"
# Download video/transcript materials

# Naming: 1993-IRAN-CONTRA-WALSH-FINAL-REPORT.pdf
```

---

## TASK 8: BCCI INVESTIGATION

### 8.1 Kerry Committee Report
```python
urls = [
    "https://info.publicintelligence.net/The-BCCI-Affair.pdf",
    "https://archive.org/details/TheBCCIAffair"
]

tags = [
    "TYPE:CONGRESSIONAL-REPORT",
    "CASE:BCCI-INVESTIGATION",
    "ORG:BCCI",
    "ORG:CIA",
    "NETWORK:INTELLIGENCE",
    "NETWORK:FINANCIAL",
    "LAYER:2-INTELLIGENCE",
    "LAYER:3-FINANCIAL",
    "PRIORITY:CRITICAL",
    "VERIFIED:GOVERNMENT-OFFICIAL"
]

# Naming: 1992-BCCI-KERRY-COMMITTEE-REPORT-FULL.pdf
```

---

## TASK 9: CHURCH COMMITTEE REPORTS

### 9.1 Book II - Intelligence Activities and Rights of Americans
```python
url = "https://repositories.lib.utexas.edu/bitstream/handle/2152/13804/ChurchCommittee_BookII.pdf"

tags = [
    "TYPE:CONGRESSIONAL-REPORT",
    "CASE:CHURCH-COMMITTEE",
    "ORG:CIA",
    "ORG:FBI",
    "ORG:NSA",
    "NETWORK:INTELLIGENCE",
    "LAYER:2-INTELLIGENCE",
    "PRIORITY:CRITICAL",
    "VERIFIED:GOVERNMENT-OFFICIAL"
]

# Naming: 1976-CHURCH-COMMITTEE-BOOK-II-INTELLIGENCE-RIGHTS.pdf
```

### 9.2 Book III - Supplementary Staff Reports
```python
url = "https://repositories.lib.utexas.edu/bitstream/handle/2152/13804/ChurchCommittee_BookIII.pdf"

# Naming: 1976-CHURCH-COMMITTEE-BOOK-III-SUPPLEMENTARY-REPORTS.pdf
```

### 9.3 Additional Books (I, IV, V, VI)
```python
# Source from Senate Intelligence Committee:
# https://www.intelligence.senate.gov/resources/intelligence-related-commissions/
# Download each book
```

---

## TASK 10: ROY COHN FBI FILES

### 10.1 Internet Archive Complete Collection
```python
collection_url = "https://archive.org/details/RoyCohn"

tags = [
    "TYPE:FBI-FILE",
    "TYPE:FOIA-RELEASE",
    "PERSON:ROY-COHN",
    "ORG:FBI",
    "NETWORK:POLITICAL",
    "NETWORK:BLACKMAIL-OPS",
    "LAYER:4-POLITICAL",
    "PRIORITY:HIGH",
    "VERIFIED:GOVERNMENT-OFFICIAL"
]

# Download all PDF files from collection
# Naming: [YEAR]-ROY-COHN-FBI-FILE-PART-[N].pdf
```

### 10.2 FBI Vault Direct
```python
# Scrape from: https://vault.fbi.gov/roy-cohn
# Download all available parts
```

---

## TASK 11: ROBERT MAXWELL DOCUMENTS

### 11.1 Book - Robert Maxwell Israel's Superspy
```python
url = "https://archive.org/details/thomas_gordon_dillon_martin_robert_maxwell_israels_superspy"

tags = [
    "TYPE:BOOK-CHAPTER",
    "PERSON:ROBERT-MAXWELL",
    "ORG:MOSSAD",
    "NETWORK:INTELLIGENCE",
    "LAYER:2-INTELLIGENCE",
    "PRIORITY:HIGH",
    "UNVERIFIED:SECONDARY-SOURCE"
]

# Naming: 2002-ROBERT-MAXWELL-ISRAELS-SUPERSPY-THOMAS.pdf
```

---

## TASK 12: NXIVM CASE DOCUMENTS

### 12.1 DOJ Press Release Documents
```python
urls = [
    "https://www.justice.gov/usao-edny/press-release/file/1046381/download",  # Indictment
]

tags = [
    "TYPE:INDICTMENT",
    "CASE:NXIVM-RANIERE",
    "PERSON:KEITH-RANIERE",
    "ORG:NXIVM",
    "NETWORK:BLACKMAIL-OPS",
    "LAYER:5-PARALLEL-CASES",
    "PRIORITY:HIGH",
    "VERIFIED:COURT-RECORD"
]

# Naming: 2018-NXIVM-RANIERE-SUPERSEDING-INDICTMENT.pdf
```

### 12.2 Sentencing Memo
```python
url = "https://www.courthousenews.com/wp-content/uploads/2020/10/Raniere-Sentencing-Memo.pdf"

# Naming: 2020-NXIVM-RANIERE-GOVERNMENT-SENTENCING-MEMO.pdf
```

### 12.3 CourtListener Docket
```python
# Scrape: https://www.courtlistener.com/docket/6374665/united-states-v-raniere/
```

---

## TASK 13: ADDITIONAL COURT APPEALS

### 13.1 Wild v. DOJ (11th Circuit - Epstein Victims)
```python
url = "https://media.ca11.uscourts.gov/opinions/pub/files/201913843.pdf"

tags = [
    "TYPE:COURT-FILING",
    "CASE:EPSTEIN-FLORIDA-2008",
    "PERSON:JEFFREY-EPSTEIN",
    "ORG:DOJ",
    "LAYER:1-EPSTEIN-CORE",
    "PRIORITY:HIGH",
    "VERIFIED:COURT-RECORD"
]

# Naming: 2020-WILD-V-DOJ-11TH-CIRCUIT-EPSTEIN-CVRA.pdf
```

### 13.2 Brown v. Maxwell (2nd Circuit - Unsealing)
```python
# From CourtListener: https://www.courtlistener.com/opinion/4636326/brown-v-maxwell-dershowitz-v-giuffre/

# Naming: 2019-BROWN-V-MAXWELL-2ND-CIRCUIT-UNSEALING.pdf
```

---

## IMPLEMENTATION SCRIPT STRUCTURE

```python
#!/usr/bin/env python3
"""
Continuum Report Document Acquisition System
Downloads and ingests documents into Paperless-ngx
"""

import os
import json
import requests
import hashlib
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, unquote
import logging

# Configuration
PAPERLESS_URL = "http://192.168.1.139:8040/api"
PAPERLESS_TOKEN = "da99fe6aa0b8d021689126cf72b91986abbbd283"
DOWNLOAD_DIR = Path.home() / "continuum_downloads"
PROGRESS_FILE = Path.home() / "continuum_progress.json"
ERROR_LOG = Path.home() / "continuum_errors.log"

# Rate limiting
DOWNLOAD_DELAY = 2  # seconds between downloads
API_DELAY = 1  # seconds between API calls

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(ERROR_LOG),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PaperlessAPI:
    """Interface to Paperless-ngx API"""
    
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {"Authorization": f"Token {token}"}
        self.tag_cache = {}
    
    def get_or_create_tag(self, tag_name):
        """Get existing tag or create new one"""
        if tag_name in self.tag_cache:
            return self.tag_cache[tag_name]
        
        # Search for existing tag
        response = requests.get(
            f"{self.base_url}/tags/",
            headers=self.headers,
            params={"name__iexact": tag_name}
        )
        
        if response.ok and response.json()["count"] > 0:
            tag_id = response.json()["results"][0]["id"]
            self.tag_cache[tag_name] = tag_id
            return tag_id
        
        # Create new tag
        response = requests.post(
            f"{self.base_url}/tags/",
            headers=self.headers,
            json={"name": tag_name}
        )
        
        if response.ok:
            tag_id = response.json()["id"]
            self.tag_cache[tag_name] = tag_id
            logger.info(f"Created tag: {tag_name}")
            return tag_id
        
        logger.error(f"Failed to create tag {tag_name}: {response.text}")
        return None
    
    def upload_document(self, filepath, title, tags):
        """Upload document to Paperless"""
        tag_ids = [self.get_or_create_tag(t) for t in tags if self.get_or_create_tag(t)]
        
        with open(filepath, 'rb') as f:
            files = {'document': (filepath.name, f, 'application/pdf')}
            data = {
                'title': title,
                'tags': tag_ids
            }
            
            response = requests.post(
                f"{self.base_url}/documents/post_document/",
                headers=self.headers,
                files=files,
                data=data
            )
        
        if response.ok:
            logger.info(f"Uploaded: {title}")
            return True
        else:
            logger.error(f"Upload failed for {title}: {response.text}")
            return False


class DocumentDownloader:
    """Handles document downloads with checkpointing"""
    
    def __init__(self, download_dir, progress_file):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.progress_file = Path(progress_file)
        self.progress = self.load_progress()
    
    def load_progress(self):
        """Load progress from checkpoint file"""
        if self.progress_file.exists():
            with open(self.progress_file) as f:
                return json.load(f)
        return {"downloaded": [], "failed": [], "uploaded": []}
    
    def save_progress(self):
        """Save progress to checkpoint file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def download_file(self, url, filename=None):
        """Download file with retry logic"""
        if url in self.progress["downloaded"]:
            logger.info(f"Already downloaded: {url}")
            return self.get_filepath(url, filename)
        
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            if not filename:
                # Extract filename from URL or Content-Disposition
                if 'Content-Disposition' in response.headers:
                    filename = response.headers['Content-Disposition'].split('filename=')[-1].strip('"')
                else:
                    filename = unquote(urlparse(url).path.split('/')[-1])
            
            filepath = self.download_dir / filename
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.progress["downloaded"].append(url)
            self.save_progress()
            logger.info(f"Downloaded: {filename}")
            
            time.sleep(DOWNLOAD_DELAY)
            return filepath
            
        except Exception as e:
            logger.error(f"Download failed for {url}: {e}")
            self.progress["failed"].append({"url": url, "error": str(e)})
            self.save_progress()
            return None
    
    def get_filepath(self, url, filename):
        """Get filepath for already downloaded file"""
        if not filename:
            filename = unquote(urlparse(url).path.split('/')[-1])
        return self.download_dir / filename


def process_task(downloader, paperless, task):
    """Process a single acquisition task"""
    url = task["url"]
    filename = task.get("filename")
    title = task["title"]
    tags = task["tags"]
    
    # Download
    filepath = downloader.download_file(url, filename)
    if not filepath or not filepath.exists():
        return False
    
    # Upload to Paperless
    success = paperless.upload_document(filepath, title, tags)
    
    if success:
        downloader.progress["uploaded"].append(url)
        downloader.save_progress()
    
    time.sleep(API_DELAY)
    return success


# Define all tasks
TASKS = [
    # TASK 1: Flight Logs
    {
        "url": "https://archive.org/download/EpsteinFlightLogsLolitaExpress/Jeffrey%20Epstein%20Flight%20Logs.pdf",
        "filename": "1995-2005-EPSTEIN-FLIGHT-LOGS-LOLITA-EXPRESS.pdf",
        "title": "Jeffrey Epstein Flight Logs - Lolita Express (1995-2005)",
        "tags": ["TYPE:FLIGHT-LOG", "PERSON:JEFFREY-EPSTEIN", "NETWORK:EPSTEIN", 
                 "LAYER:1-EPSTEIN-CORE", "PRIORITY:CRITICAL", "VERIFIED:COURT-RECORD"]
    },
    {
        "url": "https://ia801606.us.archive.org/30/items/epstein-flight-logs-unredacted_202304/EPSTEIN%20FLIGHT%20LOGS%20UNREDACTED.pdf",
        "filename": "1995-2005-EPSTEIN-FLIGHT-LOGS-UNREDACTED.pdf",
        "title": "Jeffrey Epstein Flight Logs - Unredacted Version",
        "tags": ["TYPE:FLIGHT-LOG", "PERSON:JEFFREY-EPSTEIN", "NETWORK:EPSTEIN",
                 "LAYER:1-EPSTEIN-CORE", "PRIORITY:CRITICAL", "VERIFIED:COURT-RECORD"]
    },
    
    # TASK 2: Black Book
    {
        "url": "https://archive.org/download/jeffrey-epstein-39s-little-black-book-unredacted/Jeffrey%20Epstein%27s%20Little%20Black%20Book%20unredacted.pdf",
        "filename": "2004-EPSTEIN-ADDRESS-BOOK-BLACK-BOOK-UNREDACTED.pdf",
        "title": "Jeffrey Epstein's Black Book - Unredacted (2004)",
        "tags": ["TYPE:ADDRESS-BOOK", "PERSON:JEFFREY-EPSTEIN", "NETWORK:EPSTEIN",
                 "LAYER:1-EPSTEIN-CORE", "PRIORITY:CRITICAL", "VERIFIED:COURT-RECORD"]
    },
    {
        "url": "https://www.documentcloud.org/documents/1508273-jeffrey-epsteins-little-black-book-redacted.pdf",
        "filename": "2004-EPSTEIN-ADDRESS-BOOK-BLACK-BOOK-REDACTED.pdf",
        "title": "Jeffrey Epstein's Black Book - Redacted Court Version",
        "tags": ["TYPE:ADDRESS-BOOK", "PERSON:JEFFREY-EPSTEIN", "NETWORK:EPSTEIN",
                 "LAYER:1-EPSTEIN-CORE", "PRIORITY:HIGH", "VERIFIED:COURT-RECORD"]
    },
    
    # TASK 3: NPA Documents
    {
        "url": "https://www.documentcloud.org/documents/6184602-Jeffrey-Epstein-non-prosecution-agreement.pdf",
        "filename": "2008-EPSTEIN-FLORIDA-NPA-NON-PROSECUTION-AGREEMENT.pdf",
        "title": "Epstein Non-Prosecution Agreement (2008)",
        "tags": ["TYPE:COURT-FILING", "CASE:EPSTEIN-FLORIDA-2008", "PERSON:JEFFREY-EPSTEIN",
                 "PERSON:ALEXANDER-ACOSTA", "ORG:DOJ", "LAYER:1-EPSTEIN-CORE",
                 "PRIORITY:CRITICAL", "VERIFIED:COURT-RECORD"]
    },
    {
        "url": "https://www.justice.gov/opr/page/file/1336471/dl",
        "filename": "2020-DOJ-OPR-REPORT-EPSTEIN-NPA-INVESTIGATION.pdf",
        "title": "DOJ Office of Professional Responsibility Report - Epstein NPA Investigation",
        "tags": ["TYPE:INVESTIGATION-REPORT", "TYPE:GOVERNMENT-REPORT", "CASE:EPSTEIN-FLORIDA-2008",
                 "PERSON:JEFFREY-EPSTEIN", "ORG:DOJ", "LAYER:1-EPSTEIN-CORE",
                 "PRIORITY:CRITICAL", "VERIFIED:GOVERNMENT-OFFICIAL"]
    },
    
    # TASK 5: JP Morgan
    {
        "url": "https://static.foxbusiness.com/foxbusiness.com/content/uploads/2022/12/U.S.-Virgin-Islands-v-JP-Morgan.pdf",
        "filename": "2022-USVI-V-JPMORGAN-COMPLAINT-EPSTEIN-TRAFFICKING.pdf",
        "title": "USVI v. JP Morgan - Complaint (Epstein Trafficking)",
        "tags": ["TYPE:COURT-FILING", "CASE:USVI-V-JPMORGAN", "PERSON:JEFFREY-EPSTEIN",
                 "ORG:JPMORGAN", "NETWORK:EPSTEIN", "NETWORK:FINANCIAL",
                 "LAYER:1-EPSTEIN-CORE", "LAYER:3-FINANCIAL", "PRIORITY:CRITICAL", "VERIFIED:COURT-RECORD"]
    },
    
    # TASK 6: INSLAW
    {
        "url": "https://ia601309.us.archive.org/23/items/TheInslawAffair/Chapter%2017%20-%20The%20Inslaw%20Affair.pdf",
        "filename": "1992-INSLAW-AFFAIR-CHAPTER-17-ANALYSIS.pdf",
        "title": "The Inslaw Affair - Chapter 17 Analysis",
        "tags": ["TYPE:BOOK-CHAPTER", "CASE:INSLAW-V-DOJ", "ORG:DOJ", "ORG:INSLAW",
                 "NETWORK:INTELLIGENCE", "LAYER:2-INTELLIGENCE", "PRIORITY:HIGH"]
    },
    
    # TASK 7: Iran-Contra
    {
        "url": "https://archive.org/download/ReportOnTheIranContraAffair/Report-on-the-Iran-Contra-Affair.pdf",
        "filename": "1987-IRAN-CONTRA-CONGRESSIONAL-REPORT-MAIN.pdf",
        "title": "Report of Congressional Committees Investigating Iran-Contra Affair",
        "tags": ["TYPE:CONGRESSIONAL-REPORT", "CASE:IRAN-CONTRA", "ORG:CIA",
                 "NETWORK:INTELLIGENCE", "LAYER:2-INTELLIGENCE", "PRIORITY:CRITICAL",
                 "VERIFIED:GOVERNMENT-OFFICIAL"]
    },
    {
        "url": "https://archive.org/download/ReportOnTheIranContraAffair/The-Tower-Report-on-Iran-Contra-Affair.pdf",
        "filename": "1987-IRAN-CONTRA-TOWER-COMMISSION-REPORT.pdf",
        "title": "Tower Commission Report on Iran-Contra Affair",
        "tags": ["TYPE:GOVERNMENT-REPORT", "CASE:IRAN-CONTRA", "ORG:CIA",
                 "NETWORK:INTELLIGENCE", "LAYER:2-INTELLIGENCE", "PRIORITY:HIGH",
                 "VERIFIED:GOVERNMENT-OFFICIAL"]
    },
    
    # TASK 8: BCCI
    {
        "url": "https://info.publicintelligence.net/The-BCCI-Affair.pdf",
        "filename": "1992-BCCI-KERRY-COMMITTEE-REPORT-FULL.pdf",
        "title": "The BCCI Affair - Kerry Committee Report",
        "tags": ["TYPE:CONGRESSIONAL-REPORT", "CASE:BCCI-INVESTIGATION", "ORG:BCCI",
                 "ORG:CIA", "NETWORK:INTELLIGENCE", "NETWORK:FINANCIAL",
                 "LAYER:2-INTELLIGENCE", "LAYER:3-FINANCIAL", "PRIORITY:CRITICAL",
                 "VERIFIED:GOVERNMENT-OFFICIAL"]
    },
    
    # TASK 9: Church Committee
    {
        "url": "https://www.brennancenter.org/sites/default/files/publications/Church_Committee_Report.pdf",
        "filename": "2015-CHURCH-COMMITTEE-BRENNAN-CENTER-ANALYSIS.pdf",
        "title": "Church Committee - Brennan Center Analysis",
        "tags": ["TYPE:GOVERNMENT-REPORT", "CASE:CHURCH-COMMITTEE", "ORG:CIA", "ORG:FBI",
                 "ORG:NSA", "NETWORK:INTELLIGENCE", "LAYER:2-INTELLIGENCE", "PRIORITY:MEDIUM"]
    },
    
    # TASK 11: Robert Maxwell
    {
        "url": "https://archive.org/download/thomas_gordon_dillon_martin_robert_maxwell_israels_superspy/thomas_gordon_dillon_martin_robert_maxwell_israels_superspy.pdf",
        "filename": "2002-ROBERT-MAXWELL-ISRAELS-SUPERSPY-THOMAS.pdf",
        "title": "Robert Maxwell, Israel's Superspy - Gordon Thomas",
        "tags": ["TYPE:BOOK-CHAPTER", "PERSON:ROBERT-MAXWELL", "ORG:MOSSAD",
                 "NETWORK:INTELLIGENCE", "LAYER:2-INTELLIGENCE", "PRIORITY:HIGH",
                 "UNVERIFIED:SECONDARY-SOURCE"]
    },
    
    # TASK 12: NXIVM
    {
        "url": "https://www.justice.gov/usao-edny/press-release/file/1046381/download",
        "filename": "2018-NXIVM-RANIERE-SUPERSEDING-INDICTMENT.pdf",
        "title": "NXIVM - Keith Raniere Superseding Indictment",
        "tags": ["TYPE:INDICTMENT", "CASE:NXIVM-RANIERE", "PERSON:KEITH-RANIERE",
                 "ORG:NXIVM", "NETWORK:BLACKMAIL-OPS", "LAYER:5-PARALLEL-CASES",
                 "PRIORITY:HIGH", "VERIFIED:COURT-RECORD"]
    },
    {
        "url": "https://www.courthousenews.com/wp-content/uploads/2020/10/Raniere-Sentencing-Memo.pdf",
        "filename": "2020-NXIVM-RANIERE-GOVERNMENT-SENTENCING-MEMO.pdf",
        "title": "NXIVM - Keith Raniere Government Sentencing Memorandum",
        "tags": ["TYPE:COURT-FILING", "CASE:NXIVM-RANIERE", "PERSON:KEITH-RANIERE",
                 "ORG:NXIVM", "NETWORK:BLACKMAIL-OPS", "LAYER:5-PARALLEL-CASES",
                 "PRIORITY:HIGH", "VERIFIED:COURT-RECORD"]
    },
    
    # TASK 13: Appeals
    {
        "url": "https://media.ca11.uscourts.gov/opinions/pub/files/201913843.pdf",
        "filename": "2020-WILD-V-DOJ-11TH-CIRCUIT-EPSTEIN-CVRA.pdf",
        "title": "Wild v. DOJ - 11th Circuit Opinion (Epstein CVRA)",
        "tags": ["TYPE:COURT-FILING", "CASE:EPSTEIN-FLORIDA-2008", "PERSON:JEFFREY-EPSTEIN",
                 "ORG:DOJ", "LAYER:1-EPSTEIN-CORE", "PRIORITY:HIGH", "VERIFIED:COURT-RECORD"]
    },
]


def main():
    """Main execution"""
    logger.info("Starting Continuum Document Acquisition System")
    
    # Initialize
    downloader = DocumentDownloader(DOWNLOAD_DIR, PROGRESS_FILE)
    paperless = PaperlessAPI(PAPERLESS_URL, PAPERLESS_TOKEN)
    
    # Process all tasks
    success_count = 0
    fail_count = 0
    
    for i, task in enumerate(TASKS, 1):
        logger.info(f"Processing task {i}/{len(TASKS)}: {task['title']}")
        
        if process_task(downloader, paperless, task):
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    logger.info(f"Acquisition complete: {success_count} succeeded, {fail_count} failed")
    logger.info(f"Progress saved to: {PROGRESS_FILE}")


if __name__ == "__main__":
    main()
```

---

## EXECUTION INSTRUCTIONS

### Step 1: Setup Environment
```bash
# Create working directories
mkdir -p ~/continuum_downloads
mkdir -p ~/continuum_processed

# Install dependencies
pip install requests beautifulsoup4 lxml
```

### Step 2: Verify Paperless Connection
```bash
# Test API connection
curl -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
     http://192.168.1.139:8040/api/documents/
```

### Step 3: Run Acquisition
```bash
# Execute the script
python3 continuum_acquisition.py

# Monitor progress
tail -f ~/continuum_errors.log
cat ~/continuum_progress.json | jq .
```

### Step 4: Verify Ingestion
```bash
# Check Paperless for new documents
curl -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
     "http://192.168.1.139:8040/api/documents/?query=EPSTEIN"
```

---

## ERROR HANDLING

### Common Issues

1. **Rate Limiting**: Increase `DOWNLOAD_DELAY` if sources block requests
2. **Large Files**: Some Iran-Contra volumes are 50MB+; increase timeout
3. **Authentication**: Some DocumentCloud links may require direct PDF URLs
4. **Paperless Queue**: Monitor consumption folder for stuck files

### Recovery
```bash
# Resume from checkpoint
python3 continuum_acquisition.py  # Will skip already-downloaded files

# Clear failed downloads to retry
jq '.failed = []' ~/continuum_progress.json > temp.json && mv temp.json ~/continuum_progress.json
```

---

## EXPANSION TASKS

After core tasks complete, add these additional acquisitions:

### Internet Archive Bulk Downloads
```bash
# Download entire collections
ia download EpsteinFlightLogsLolitaExpress --glob="*.pdf"
ia download Iran-ContraReport --glob="*.pdf"
ia download RoyCohn --glob="*.pdf"
```

### CourtListener RECAP Scraping
```python
# Use CourtListener API to download all free documents from key dockets
dockets = [
    "4355835",   # Giuffre v. Maxwell
    "66683865",  # USVI v. JP Morgan
    "6374665",   # United States v. Raniere
]
```

### Public Intelligence Batch Scraper
```python
# Scrape all PDF links from Public Intelligence Epstein batches
# Extract document links and download each
```

---

## MAINTENANCE

### Weekly Tasks
- Check for new court filings on active dockets
- Monitor MuckRock for new FOIA releases
- Update progress checkpoint

### Monthly Tasks
- Verify document integrity (checksums)
- Remove duplicates in Paperless
- Update tag taxonomy as needed

---

*Prompt Version: 1.0*
*Created: December 16, 2025*
*For: The Continuum Report Document Acquisition System*
