# The Continuum Report - Modernization Migration Guide

**Version:** 1.0
**Last Updated:** December 24, 2024
**Status:** Complete

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [What Changed](#what-changed)
3. [Migration Overview](#migration-overview)
4. [Step-by-Step Migration](#step-by-step-migration)
5. [Before & After Examples](#before--after-examples)
6. [Breaking Changes](#breaking-changes)
7. [Troubleshooting](#troubleshooting)
8. [Rollback Plan](#rollback-plan)

---

## Executive Summary

The Continuum Report has been modernized with a **shared library architecture** that eliminates code duplication, improves reliability, and prepares the codebase for containerization and cloud deployment.

### Key Improvements

| Aspect | Before | After | Benefit |
|--------|--------|-------|---------|
| **Configuration** | Hardcoded URLs/tokens | Environment variables | Security & flexibility |
| **API Clients** | Custom code in each script | Shared clients with retry logic | Reliability & DRY |
| **Logging** | Print statements | Structured JSON logging | Observability |
| **Error Handling** | Basic try/catch | Typed exceptions & retries | Resilience |
| **Code Reuse** | ~500 lines duplicated | Shared library | Maintainability |
| **Memory Safety** | Manual management | Automated unloading | Stability |

### Migration Effort

- **Time Required:** 1-2 hours per script
- **Complexity:** Low to Medium
- **Risk Level:** Low (backwards compatible)
- **Rollback:** Easy (git revert)

---

## What Changed

### 1. New Shared Library (`scripts/lib/`)

A centralized library provides four core modules:

```
scripts/lib/
├── __init__.py           # Package exports
├── config.py             # Centralized configuration
├── logging_config.py     # Structured logging
├── paperless_client.py   # Paperless-ngx API client
└── ollama_client.py      # Ollama LLM client
```

### 2. Environment-Based Configuration

**Before:** Hardcoded credentials
```python
PAPERLESS_TOKEN = "da99fe6aa0b8d021689126cf72b91986abbbd283"
PAPERLESS_URL = "http://192.168.1.139:8040"
```

**After:** Environment variables
```python
from lib import settings

# Automatically loaded from .env file
print(settings.paperless_url)
print(settings.paperless_token)
```

### 3. Typed API Clients

**Before:** Manual urllib requests
```python
def paperless_request(endpoint: str) -> Optional[Dict]:
    url = f"{PAPERLESS_URL}{endpoint}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Token {PAPERLESS_TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))
```

**After:** Robust client with retry logic
```python
from lib import PaperlessClient

with PaperlessClient() as client:
    docs = client.get_all_documents()
    content = client.get_document_content(doc_id)
```

### 4. Structured Logging

**Before:** Print statements
```python
print(f"Processing document {doc_id}...")
print(f"Error: {e}")
```

**After:** Structured logs with context
```python
from lib import get_logger

logger = get_logger(__name__)
logger.info("Processing document", doc_id=doc_id, status="started")
logger.error("Processing failed", doc_id=doc_id, error=str(e))
```

### 5. Better Error Handling

**Before:** Generic exceptions
```python
try:
    response = paperless_request(f"/api/documents/{doc_id}/")
except Exception as e:
    print(f"Error: {e}")
```

**After:** Typed exceptions
```python
try:
    doc = client.get_document(doc_id)
except PaperlessAuthError:
    logger.error("Invalid API token - check .env file")
except PaperlessNotFoundError:
    logger.warning("Document not found", doc_id=doc_id)
except PaperlessConnectionError:
    logger.error("Cannot connect to Paperless server")
```

---

## Migration Overview

### Prerequisites

1. Python 3.8+ installed
2. Git repository initialized
3. Access to Paperless-ngx and Ollama servers
4. Basic understanding of environment variables

### Migration Phases

**Phase 1: Environment Setup** (15 minutes)
- Create `.env` file with credentials
- Install new dependencies
- Test configuration

**Phase 2: Update Scripts** (1-2 hours per script)
- Replace hardcoded config with `settings`
- Replace API calls with shared clients
- Replace print statements with structured logging
- Add type hints and error handling

**Phase 3: Testing** (30 minutes)
- Run updated scripts
- Verify logs are structured correctly
- Test error scenarios

**Phase 4: Cleanup** (15 minutes)
- Remove old code
- Update documentation
- Commit changes

---

## Step-by-Step Migration

### Step 1: Set Up Environment

#### 1.1 Install Dependencies

```bash
cd //192.168.1.139/continuum
pip install -r requirements.txt
```

**New dependencies:**
- `pydantic>=2.0` - Configuration management
- `pydantic-settings` - Environment variable loading
- `structlog` - Structured logging
- `tenacity` - Retry logic

#### 1.2 Create `.env` File

Copy the example and fill in your values:

```bash
cp .env.example .env
nano .env  # or your preferred editor
```

**Required variables:**
```bash
# Paperless-ngx Configuration
PAPERLESS_URL=http://192.168.1.139:8040
PAPERLESS_TOKEN=your_token_here

# Ollama Configuration
OLLAMA_URL=http://192.168.1.139:11434
OLLAMA_MODEL=mistral

# Directories
CONTINUUM_BASE_DIR=/continuum
```

#### 1.3 Test Configuration

```bash
cd scripts
python -m lib.config
```

Expected output:
```
============================================================
The Continuum Report - Configuration Check
============================================================

Configuration: ContinuumSettings(paperless_url='http://192.168.1.139:8040', ...)

Directories:
  Base:       /continuum
  Data:       /continuum/entity_data
  Reports:    /continuum/reports
  Checkpoints:/continuum/checkpoints

Services:
  Paperless:  http://192.168.1.139:8040
  Ollama:     http://192.168.1.139:11434 (model: mistral)

  Token:      [SET]

Validating connections...
  Paperless:  OK
  Ollama:     OK
```

### Step 2: Migrate a Script

Let's migrate `generate_dossiers.py` as an example.

#### 2.1 Update Imports

**Before:**
```python
import json
import os
import urllib.request
```

**After:**
```python
import json
from pathlib import Path

# Import shared library
from lib import settings, get_logger, PaperlessClient, OllamaClient
from lib import PaperlessError, OllamaError
```

#### 2.2 Replace Configuration

**Before:**
```python
PAPERLESS_URL = "http://192.168.1.139:8040"
PAPERLESS_TOKEN = "da99fe6aa0b8d021689126cf72b91986abbbd283"
BASE_DIR = "/continuum"
DATA_DIR = os.path.join(BASE_DIR, "entity_data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
```

**After:**
```python
# Configuration from centralized settings
DATA_DIR = settings.data_dir
REPORTS_DIR = settings.reports_dir
ENTITY_DB_FILE = settings.entity_db_file

# Ensure directories exist
settings.ensure_directories()
```

#### 2.3 Replace API Calls

**Before:**
```python
def paperless_request(endpoint: str) -> Optional[Dict]:
    """Make a request to Paperless API."""
    url = f"{PAPERLESS_URL}{endpoint}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Token {PAPERLESS_TOKEN}")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_document_content(doc_id: int) -> Optional[Dict]:
    """Get full document details."""
    return paperless_request(f"/api/documents/{doc_id}/")
```

**After:**
```python
def get_document_content(doc_id: int) -> Optional[str]:
    """Get full document content."""
    try:
        with PaperlessClient() as client:
            return client.get_document_content(doc_id)
    except PaperlessError as e:
        logger.error("Failed to get document", doc_id=doc_id, error=str(e))
        return None
```

#### 2.4 Add Structured Logging

**Before:**
```python
print(f"Processing entity: {entity_name}")
print(f"Found {len(docs)} documents")
print(f"Error: {e}")
```

**After:**
```python
# Initialize logger at top of file
logger = get_logger(__name__)

# In your functions
logger.info("Processing entity", entity_name=entity_name, entity_type=entity_type)
logger.info("Documents found", count=len(docs))
logger.error("Processing failed", entity=entity_name, error=str(e))
```

#### 2.5 Update Error Handling

**Before:**
```python
try:
    doc = get_document_content(doc_id)
    if not doc:
        print("Document not found")
        continue
except Exception as e:
    print(f"Error: {e}")
    continue
```

**After:**
```python
try:
    content = get_document_content(doc_id)
    if not content:
        logger.warning("Document has no content", doc_id=doc_id)
        continue
except PaperlessAuthError:
    logger.error("Authentication failed - check PAPERLESS_TOKEN")
    sys.exit(1)
except PaperlessNotFoundError:
    logger.warning("Document not found", doc_id=doc_id)
    continue
except PaperlessConnectionError as e:
    logger.error("Cannot connect to Paperless", error=str(e))
    sys.exit(1)
```

### Step 3: Test the Migrated Script

#### 3.1 Run with Debug Logging

```bash
LOG_LEVEL=DEBUG python scripts/your_script.py
```

#### 3.2 Verify Structured Logs

You should see JSON-formatted logs (if `LOG_FORMAT=json`) or colored console output (default):

```
2024-12-24T10:30:00 [info     ] Processing entity              entity_name=Jeffrey Epstein entity_type=Person
2024-12-24T10:30:01 [info     ] Documents found                count=247
2024-12-24T10:30:05 [debug    ] Fetching document              doc_id=1234
```

#### 3.3 Test Error Scenarios

Test with invalid token to verify error handling:
```bash
PAPERLESS_TOKEN=invalid python scripts/your_script.py
```

Expected output:
```
2024-12-24T10:31:00 [error    ] Authentication failed - check PAPERLESS_TOKEN
```

### Step 4: Commit Changes

```bash
git add .
git commit -m "Migrate generate_dossiers.py to shared library

- Replace hardcoded config with lib.settings
- Use PaperlessClient with retry logic
- Add structured logging with structlog
- Improve error handling with typed exceptions"
```

---

## Before & After Examples

### Example 1: Configuration

#### Before: Hardcoded Everything
```python
#!/usr/bin/env python3
"""Old script with hardcoded values."""

import json
import urllib.request

# HARDCODED SECRETS - BAD!
PAPERLESS_URL = "http://192.168.1.139:8040"
PAPERLESS_TOKEN = "da99fe6aa0b8d021689126cf72b91986abbbd283"
OLLAMA_URL = "http://192.168.1.139:11434"
MODEL = "mistral"

# HARDCODED PATHS
BASE_DIR = "/continuum"
DATA_DIR = "/continuum/entity_data"
REPORTS_DIR = "/continuum/reports"
```

#### After: Environment-Based Configuration
```python
#!/usr/bin/env python3
"""
Modern script using shared library.
Version 2.0 - Refactored with Shared Library
"""

from pathlib import Path
from lib import settings, get_logger

# Initialize logger
logger = get_logger(__name__)

# All configuration from environment variables
# No secrets in code!
DATA_DIR = settings.data_dir
REPORTS_DIR = settings.reports_dir
ENTITY_DB_FILE = settings.entity_db_file

# Directories automatically created
settings.ensure_directories()

logger.info("Configuration loaded",
            paperless_url=settings.paperless_url,
            ollama_model=settings.ollama_model)
```

### Example 2: API Calls

#### Before: Manual HTTP Requests
```python
def get_all_documents() -> List[Dict]:
    """Fetch all documents with manual pagination."""
    all_docs = []
    page = 1

    while True:
        url = f"{PAPERLESS_URL}/api/documents/?page={page}&page_size=100"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Token {PAPERLESS_TOKEN}")

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))

            results = data.get("results", [])
            if not results:
                break

            all_docs.extend(results)

            if not data.get("next"):
                break

            page += 1

        except Exception as e:
            print(f"Error fetching documents: {e}")
            break

    return all_docs
```

#### After: Robust Client with Retry Logic
```python
def get_all_documents() -> List[Dict]:
    """Fetch all documents using PaperlessClient."""
    logger.info("Fetching all documents")

    try:
        with PaperlessClient() as client:
            # Automatic pagination, retry logic, connection pooling
            docs = client.get_all_documents(
                exclude_dossiers=True,
                progress_callback=lambda fetched, total:
                    logger.debug("Progress", fetched=fetched, total=total)
            )

            logger.info("Documents fetched", count=len(docs))
            return docs

    except PaperlessAuthError:
        logger.error("Invalid API token - check .env file")
        sys.exit(1)
    except PaperlessConnectionError as e:
        logger.error("Cannot connect to Paperless", error=str(e))
        sys.exit(1)
    except PaperlessError as e:
        logger.error("API error", error=str(e))
        return []
```

**What Improved:**
- Automatic retry on transient failures
- Connection pooling for better performance
- Typed exceptions for specific error handling
- Progress callbacks for long operations
- Context manager ensures cleanup
- Structured logging for observability

### Example 3: Ollama/LLM Integration

#### Before: Manual API Calls
```python
def generate_summary(text: str) -> str:
    """Generate summary using Ollama."""
    url = f"{OLLAMA_URL}/api/generate"

    payload = {
        "model": MODEL,
        "prompt": f"Summarize this: {text}",
        "stream": False
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("response", "")
    except Exception as e:
        print(f"LLM error: {e}")
        return ""
```

#### After: Robust Client with Memory Management
```python
def generate_summary(text: str) -> str:
    """Generate summary using OllamaClient."""
    logger.debug("Generating summary", text_len=len(text))

    try:
        with OllamaClient() as client:
            # Built-in retry logic, timeout handling, memory management
            summary = client.summarize(text, max_length=200)

            logger.info("Summary generated",
                       input_len=len(text),
                       output_len=len(summary))
            return summary

    except OllamaTimeoutError:
        logger.error("LLM request timed out", timeout=settings.ollama_timeout)
        return ""
    except OllamaConnectionError:
        logger.error("Cannot connect to Ollama server")
        return ""
    except OllamaModelError as e:
        logger.error("Model error", model=settings.ollama_model, error=str(e))
        return ""
```

**What Improved:**
- Automatic model unloading for memory management
- Retry logic for transient failures
- Specialized methods (summarize, extract_entities)
- Streaming support for real-time output
- Timeout handling
- GPU memory management

### Example 4: Logging

#### Before: Print Statements
```python
def process_documents(docs):
    print(f"Processing {len(docs)} documents...")

    for i, doc in enumerate(docs):
        print(f"[{i+1}/{len(docs)}] Processing {doc['title']}")

        try:
            content = get_content(doc['id'])
            entities = extract_entities(content)
            print(f"  Found {len(entities)} entities")
        except Exception as e:
            print(f"  ERROR: {e}")
```

**Issues:**
- No timestamps
- No log levels
- Can't filter or search
- No context preservation
- Not machine-readable

#### After: Structured Logging
```python
def process_documents(docs):
    logger.info("Starting document processing", total_docs=len(docs))

    for i, doc in enumerate(docs):
        with_context(doc_id=doc['id'], progress=f"{i+1}/{len(docs)}")

        logger.info("Processing document",
                   title=doc['title'],
                   doc_id=doc['id'])

        try:
            content = get_content(doc['id'])
            entities = extract_entities(content)

            logger.info("Entities extracted",
                       count=len(entities),
                       entity_types=[e['type'] for e in entities])

        except Exception as e:
            logger.error("Processing failed",
                        error=str(e),
                        exc_info=True)
        finally:
            clear_context()

    logger.info("Processing complete", total_docs=len(docs))
```

**Output:**
```json
{
  "event": "Processing document",
  "timestamp": "2024-12-24T10:30:45.123Z",
  "level": "info",
  "logger": "process_documents",
  "title": "Epstein Flight Logs",
  "doc_id": 1234,
  "progress": "5/247"
}
```

**Benefits:**
- Timestamps on every log
- Searchable JSON format
- Context preservation (doc_id, progress)
- Log levels for filtering
- Machine-readable for log aggregation
- Exception tracebacks

---

## Breaking Changes

### 1. Environment Variables Required

**Impact:** Scripts will fail if `.env` file is missing

**Migration:**
```bash
# Copy example and configure
cp .env.example .env
nano .env
```

**Validation:**
```bash
python -m lib.config
```

### 2. Import Paths Changed

**Before:**
```python
from config import PAPERLESS_URL
```

**After:**
```python
from lib import settings
print(settings.paperless_url)
```

### 3. Path Objects Instead of Strings

**Before:**
```python
DATA_DIR = "/continuum/entity_data"
file_path = os.path.join(DATA_DIR, "file.json")
```

**After:**
```python
from pathlib import Path

DATA_DIR = settings.data_dir  # Returns Path object
file_path = DATA_DIR / "file.json"
```

### 4. Logging Instead of Print

**Before:**
```python
print("Processing...")
```

**After:**
```python
logger.info("Processing...")
```

### 5. Typed Exceptions

**Before:**
```python
except Exception as e:
    print(f"Error: {e}")
```

**After:**
```python
except PaperlessAuthError:
    logger.error("Invalid API token")
except PaperlessConnectionError:
    logger.error("Connection failed")
```

---

## Troubleshooting

### Issue 1: "PAPERLESS_TOKEN is not set"

**Error:**
```
UserWarning: PAPERLESS_TOKEN is not set. Set it in your .env file or environment.
```

**Solution:**
```bash
# Create .env file
cp .env.example .env

# Edit and add your token
nano .env
# PAPERLESS_TOKEN=your_actual_token_here
```

### Issue 2: "Cannot connect to Paperless server"

**Error:**
```
PaperlessConnectionError: Cannot connect to http://192.168.1.139:8040
```

**Solution:**
1. Check if Paperless is running: `curl http://192.168.1.139:8040`
2. Verify URL in `.env` file
3. Check firewall/network connectivity
4. Test with: `python -m lib.config`

### Issue 3: "Module 'lib' not found"

**Error:**
```
ModuleNotFoundError: No module named 'lib'
```

**Solution:**
```bash
# Make sure you're in the scripts directory
cd scripts
python your_script.py

# Or use PYTHONPATH
PYTHONPATH=scripts python scripts/your_script.py
```

### Issue 4: Logs Not Appearing

**Problem:** No log output visible

**Solution:**
```bash
# Set log level to DEBUG
LOG_LEVEL=DEBUG python scripts/your_script.py

# Or use console format for colored output
LOG_FORMAT=console python scripts/your_script.py
```

### Issue 5: "Invalid API token"

**Error:**
```
PaperlessAuthError: Invalid API token
```

**Solution:**
1. Get token from Paperless web UI: Settings > API Tokens
2. Update `.env` file with correct token
3. Test: `python -m lib.paperless_client`

### Issue 6: Ollama Model Not Found

**Error:**
```
OllamaModelError: Model 'mistral' not found
```

**Solution:**
```bash
# Pull the model
ollama pull mistral

# Or change model in .env
OLLAMA_MODEL=llama2
```

### Issue 7: Permission Denied on Directories

**Error:**
```
PermissionError: [Errno 13] Permission denied: '/continuum/entity_data'
```

**Solution:**
```bash
# Create directories with proper permissions
sudo mkdir -p /continuum/entity_data
sudo chown $USER:$USER /continuum -R

# Or change base directory in .env
CONTINUUM_BASE_DIR=/home/user/continuum
```

---

## Rollback Plan

If you need to revert changes:

### Quick Rollback (Git)

```bash
# View recent commits
git log --oneline -10

# Revert to before migration
git revert <commit-hash>

# Or reset (destructive)
git reset --hard <commit-hash>
```

### Manual Rollback

1. **Restore old script:**
   ```bash
   cp generate_dossiers.py.backup generate_dossiers.py
   ```

2. **Remove shared library dependency:**
   ```bash
   pip uninstall pydantic pydantic-settings structlog tenacity
   ```

3. **Restore hardcoded config:**
   - Edit script to add back PAPERLESS_URL and PAPERLESS_TOKEN
   - Remove `from lib import ...`
   - Change logging back to print statements

### Keep Both Versions

```bash
# Create a migration branch
git checkout -b migration/shared-library

# Keep old scripts as .legacy
cp generate_dossiers.py generate_dossiers.legacy.py

# Commit new version
git add .
git commit -m "Add shared library (new version)"
```

---

## Migration Checklist

Use this checklist for each script you migrate:

### Pre-Migration
- [ ] Script identified for migration
- [ ] Backup created (`cp script.py script.py.backup`)
- [ ] .env file configured and tested
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Configuration validated (`python -m lib.config`)

### During Migration
- [ ] Imports updated (add `from lib import ...`)
- [ ] Hardcoded config replaced with `settings.*`
- [ ] API calls replaced with client methods
- [ ] Print statements replaced with structured logging
- [ ] Error handling improved with typed exceptions
- [ ] Path handling converted to pathlib
- [ ] Version number bumped in docstring

### Post-Migration
- [ ] Script runs without errors
- [ ] Logs are structured and readable
- [ ] Error scenarios tested
- [ ] Performance verified (no slowdown)
- [ ] Memory usage acceptable
- [ ] Git commit created with clear message
- [ ] Documentation updated (if needed)

### Testing
- [ ] Happy path works (normal operation)
- [ ] Error handling works (invalid token, missing docs, etc.)
- [ ] Logging level adjustable (`LOG_LEVEL=DEBUG`)
- [ ] Configuration overrides work
- [ ] Script can run multiple times safely

---

## Next Steps

### 1. Migrate Remaining Scripts

Priority order:
1. **High Priority** (frequently used):
   - `continuum_pipeline.py` ✅ (already migrated)
   - `entity_discovery.py` ✅ (already migrated)
   - `generate_dossiers.py` (use this guide!)

2. **Medium Priority**:
   - `generate_connection_briefs.py`
   - `parse_brief.py`
   - `redaction_extractor.py`

3. **Low Priority**:
   - `build_graph.py`
   - `export_sources.py`
   - `fix_sources.py`

### 2. Enable Production Logging

For production deployments:

```bash
# .env configuration
LOG_FORMAT=json
LOG_LEVEL=INFO
LOG_FILE=/continuum/logs/continuum.log
```

### 3. Set Up Log Aggregation

Once all scripts use structured logging:

1. Install log aggregator (Loki, ELK, etc.)
2. Configure log shipping
3. Create dashboards for monitoring
4. Set up alerts for errors

### 4. Containerization

With shared library in place, scripts are ready for Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY scripts/lib /app/lib
COPY scripts/continuum_pipeline.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["python", "continuum_pipeline.py"]
```

---

## Additional Resources

### Documentation
- **Configuration Guide:** `docs/CONFIGURATION.md`
- **Library API Reference:** `scripts/lib/README.md`
- **Project README:** `README.md`

### Example Scripts
- **Modernized Pipeline:** `scripts/continuum_pipeline.py`
- **Modernized Discovery:** `scripts/entity_discovery.py`
- **Legacy Example:** `scripts/generate_dossiers.py` (before migration)

### Testing Utilities
```bash
# Test configuration
python -m lib.config

# Test Paperless connection
python -m lib.paperless_client

# Test Ollama connection
python -m lib.ollama_client

# Test logging
python -m lib.logging_config
```

---

## Summary

The modernization brings:

1. **Security:** No hardcoded secrets
2. **Reliability:** Retry logic and error handling
3. **Observability:** Structured logging
4. **Maintainability:** Shared library (DRY)
5. **Scalability:** Ready for containerization

**Migration is low-risk and high-reward.** Each script takes 1-2 hours to migrate and immediately benefits from improved reliability and observability.

**Questions?** Check `scripts/lib/README.md` for API documentation or run test utilities to validate your setup.

---

**Happy Migrating!** 🚀
