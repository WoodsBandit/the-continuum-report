# The Continuum Report - Shared Library

**Version:** 1.0.0
**Location:** `scripts/lib/`
**Language:** Python 3.8+

## Overview

The shared library provides centralized, production-ready components for The Continuum Report pipeline. It eliminates code duplication, improves reliability, and provides a consistent interface for all scripts.

### Core Modules

| Module | Purpose | Key Features |
|--------|---------|--------------|
| `config.py` | Configuration management | Environment variables, path management, validation |
| `paperless_client.py` | Paperless-ngx API | Retry logic, pagination, caching, typed errors |
| `ollama_client.py` | Ollama LLM API | Memory management, streaming, specialized prompts |
| `logging_config.py` | Structured logging | JSON output, context propagation, log levels |

### Quick Start

```python
# Import everything you need
from lib import settings, get_logger, PaperlessClient, OllamaClient

# Initialize logger
logger = get_logger(__name__)

# Access configuration
logger.info("Starting pipeline",
            paperless_url=settings.paperless_url,
            ollama_model=settings.ollama_model)

# Use clients with context managers
with PaperlessClient() as paperless:
    docs = paperless.get_all_documents()

with OllamaClient() as ollama:
    summary = ollama.summarize(text)
```

---

## Table of Contents

1. [Installation](#installation)
2. [Configuration Module](#configuration-module)
3. [Paperless Client](#paperless-client)
4. [Ollama Client](#ollama-client)
5. [Logging Configuration](#logging-configuration)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Testing & Validation](#testing--validation)

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Access to Paperless-ngx server
- Access to Ollama server

### Install Dependencies

```bash
cd //192.168.1.139/continuum
pip install -r requirements.txt
```

**Required packages:**
```txt
pydantic>=2.0
pydantic-settings
structlog
requests
tenacity
```

### Set Up Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit with your values
nano .env
```

### Validate Installation

```bash
cd scripts
python -m lib.config
```

---

## Configuration Module

**File:** `lib/config.py`

Provides centralized, type-safe configuration management using Pydantic Settings.

### Quick Reference

```python
from lib.config import settings

# Paperless configuration
settings.paperless_url       # http://192.168.1.139:8040
settings.paperless_token     # Your API token (from .env)
settings.paperless_timeout   # 30 seconds

# Ollama configuration
settings.ollama_url          # http://192.168.1.139:11434
settings.ollama_model        # mistral
settings.ollama_context_size # 1024
settings.ollama_timeout      # 600 seconds

# Directory paths (pathlib.Path objects)
settings.continuum_base_dir  # /continuum
settings.data_dir           # /continuum/entity_data
settings.reports_dir        # /continuum/reports
settings.checkpoint_dir     # /continuum/checkpoints
settings.documents_inbox    # /continuum/documents/inbox

# File paths
settings.entity_db_file     # /continuum/entity_data/entity_database.json
settings.dossier_queue_file # /continuum/entity_data/dossier_queue.json

# Processing configuration
settings.max_documents_to_search     # 9999
settings.max_documents_for_entities  # 9999
settings.max_documents_for_dossier   # 9999
settings.max_chunk_size             # 1500

# Memory management
settings.delay_between_docs     # 10 seconds
settings.delay_between_batches  # 30 seconds
settings.unload_model_every     # 10 documents
```

### API Reference

#### `ContinuumSettings`

Main configuration class. Automatically loads from `.env` file.

**Attributes:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `paperless_url` | `str` | `http://192.168.1.139:8040` | Paperless-ngx server URL |
| `paperless_token` | `str` | `""` | API authentication token (REQUIRED) |
| `paperless_timeout` | `int` | `30` | Request timeout in seconds |
| `ollama_url` | `str` | `http://192.168.1.139:11434` | Ollama server URL |
| `ollama_model` | `str` | `mistral` | LLM model name |
| `ollama_context_size` | `int` | `1024` | Context window size |
| `ollama_timeout` | `int` | `600` | LLM request timeout (10 min) |
| `continuum_base_dir` | `Path` | `/continuum` | Base directory |
| `website_base_url` | `str` | `https://thecontinuumreport.com` | Public website URL |

**Methods:**

##### `ensure_directories()`
Create all required directories if they don't exist.

```python
settings.ensure_directories()
# Creates: data_dir, reports_dir, checkpoint_dir, documents_inbox
```

##### `validate_connection() -> dict`
Test connections to Paperless and Ollama.

```python
status = settings.validate_connection()

if status["paperless"] and status["ollama"]:
    print("All services healthy")
else:
    print("Errors:", status["errors"])
```

**Returns:**
```python
{
    "paperless": True/False,
    "ollama": True/False,
    "errors": ["error message", ...]
}
```

### Usage Examples

#### Basic Configuration

```python
from lib.config import settings

print(f"Paperless URL: {settings.paperless_url}")
print(f"Model: {settings.ollama_model}")
print(f"Reports directory: {settings.reports_dir}")
```

#### Environment Overrides

```bash
# Override via environment variables
export OLLAMA_MODEL=llama2
export CONTINUUM_BASE_DIR=/home/user/data

python your_script.py
```

#### Path Handling

```python
from lib.config import settings

# Use pathlib for file operations
report_file = settings.reports_dir / "dossier.md"
report_file.write_text(content)

# Iterate directory
for file in settings.data_dir.glob("*.json"):
    print(file.name)
```

#### Validation

```python
from lib.config import settings

# Check if token is set
if not settings.paperless_token:
    print("ERROR: PAPERLESS_TOKEN not configured!")
    sys.exit(1)

# Validate connections
status = settings.validate_connection()
if not all([status["paperless"], status["ollama"]]):
    print("Service health check failed:")
    for error in status["errors"]:
        print(f"  - {error}")
    sys.exit(1)
```

---

## Paperless Client

**File:** `lib/paperless_client.py`

Robust API client for Paperless-ngx with automatic retry, pagination, and connection pooling.

### Quick Reference

```python
from lib import PaperlessClient, PaperlessError

# Create client (uses settings by default)
with PaperlessClient() as client:
    # Fetch documents
    all_docs = client.get_all_documents()
    doc = client.get_document(123)
    content = client.get_document_content(123)

    # Search
    results = client.search_all("Epstein")

    # Metadata
    tags = client.get_all_tags()
    doc_types = client.get_all_document_types()

    # Health check
    if client.health_check():
        print("Paperless is healthy")
```

### API Reference

#### `PaperlessClient(base_url=None, token=None, timeout=None)`

**Parameters:**
- `base_url` (str, optional): Server URL (defaults to `settings.paperless_url`)
- `token` (str, optional): API token (defaults to `settings.paperless_token`)
- `timeout` (int, optional): Request timeout (defaults to `settings.paperless_timeout`)

**Features:**
- Automatic retry with exponential backoff (3 attempts)
- Connection pooling (10 connections)
- Response caching for tags and document types
- Context manager support (auto-cleanup)

#### Document Methods

##### `get_document(doc_id: int) -> Dict[str, Any]`
Fetch a single document's metadata.

```python
doc = client.get_document(123)
print(doc['title'])
print(doc['created'])
print(doc['tags'])  # List of tag IDs
```

##### `get_document_content(doc_id: int) -> str`
Fetch document text content.

```python
content = client.get_document_content(123)
print(f"Length: {len(content)} characters")
```

##### `get_documents_page(page=1, page_size=25, ordering="-created", **filters) -> Dict`
Fetch a paginated page of documents.

```python
# Get first page
page = client.get_documents_page(page=1, page_size=100)
print(f"Total: {page['count']}")
print(f"Results: {len(page['results'])}")

# With filters
page = client.get_documents_page(
    page=1,
    tags__id=42,  # Filter by tag
    document_type=3,  # Filter by type
    ordering="title"  # Sort by title
)
```

##### `get_all_documents(page_size=100, exclude_dossiers=True, progress_callback=None, **filters) -> List[Dict]`
Fetch ALL documents with automatic pagination.

```python
# Fetch everything
all_docs = client.get_all_documents()

# With progress callback
def show_progress(fetched, total):
    print(f"Progress: {fetched}/{total}")

docs = client.get_all_documents(
    exclude_dossiers=True,
    progress_callback=show_progress
)

# With filters
court_docs = client.get_all_documents(
    document_type=5,  # Court documents only
    exclude_dossiers=True
)
```

**Parameters:**
- `page_size` (int): Documents per page (default: 100)
- `exclude_dossiers` (bool): Skip AI-generated documents (default: True)
- `progress_callback` (callable): Called with `(fetched, total)` after each page
- `**filters`: Additional query parameters

##### `iter_all_documents(page_size=100, **filters) -> Generator`
Iterate over all documents without loading all into memory.

```python
# Memory-efficient iteration
for doc in client.iter_all_documents():
    print(f"Processing: {doc['title']}")
    # Process one at a time
```

#### Search Methods

##### `search(query: str, page=1, page_size=25) -> Dict`
Search documents (single page).

```python
results = client.search("Epstein", page=1, page_size=100)
print(f"Found: {results['count']} documents")

for doc in results['results']:
    print(f"  - {doc['title']}")
```

##### `search_all(query: str) -> List[Dict]`
Search and return ALL matching documents.

```python
# Get all matching documents
docs = client.search_all("Jeffrey Epstein")
print(f"Total matches: {len(docs)}")
```

#### Metadata Methods

##### `get_all_tags(use_cache=True) -> Dict[int, Dict]`
Fetch all tags as a dictionary keyed by ID.

```python
tags = client.get_all_tags()

# Access by ID
print(tags[42]['name'])  # "Legal"

# Iterate
for tag_id, tag in tags.items():
    print(f"{tag_id}: {tag['name']}")
```

##### `get_tag_name(tag_id: int) -> Optional[str]`
Get tag name by ID (uses cache).

```python
name = client.get_tag_name(42)
print(name)  # "Legal"
```

##### `get_all_document_types(use_cache=True) -> Dict[int, Dict]`
Fetch all document types.

```python
doc_types = client.get_all_document_types()

for type_id, dt in doc_types.items():
    print(f"{type_id}: {dt['name']}")
```

##### `get_document_type_name(type_id: int) -> Optional[str]`
Get document type name by ID.

```python
name = client.get_document_type_name(3)
print(name)  # "Court Filing"
```

##### `get_all_correspondents() -> Dict[int, Dict]`
Fetch all correspondents.

```python
correspondents = client.get_all_correspondents()
for corr_id, corr in correspondents.items():
    print(f"{corr['name']}")
```

#### Health Check

##### `health_check() -> bool`
Test if server is reachable and authenticated.

```python
if client.health_check():
    print("Paperless is healthy")
else:
    print("Cannot connect to Paperless")
```

### Exceptions

All exceptions inherit from `PaperlessError`:

| Exception | Meaning | HTTP Code |
|-----------|---------|-----------|
| `PaperlessError` | Base exception | Any error |
| `PaperlessAuthError` | Authentication failed | 401, 403 |
| `PaperlessNotFoundError` | Resource not found | 404 |
| `PaperlessConnectionError` | Cannot connect | Connection error |

### Usage Examples

#### Basic Document Fetching

```python
from lib import PaperlessClient, PaperlessError, get_logger

logger = get_logger(__name__)

try:
    with PaperlessClient() as client:
        # Health check first
        if not client.health_check():
            logger.error("Paperless not available")
            sys.exit(1)

        # Fetch all documents
        docs = client.get_all_documents(exclude_dossiers=True)
        logger.info("Documents fetched", count=len(docs))

        # Process each document
        for doc in docs:
            content = client.get_document_content(doc['id'])
            logger.info("Processing", doc_id=doc['id'], length=len(content))

except PaperlessAuthError:
    logger.error("Invalid API token - check .env file")
    sys.exit(1)
except PaperlessConnectionError as e:
    logger.error("Cannot connect to Paperless", error=str(e))
    sys.exit(1)
```

#### Search and Filter

```python
with PaperlessClient() as client:
    # Search for entity
    docs = client.search_all("Jeffrey Epstein")
    logger.info("Search results", query="Jeffrey Epstein", count=len(docs))

    # Filter by tag
    tags = client.get_all_tags()
    legal_tag_id = next(
        (tid for tid, tag in tags.items() if tag['name'] == 'Legal'),
        None
    )

    if legal_tag_id:
        legal_docs = client.get_all_documents(tags__id=legal_tag_id)
        logger.info("Legal documents", count=len(legal_docs))
```

#### Memory-Efficient Processing

```python
with PaperlessClient() as client:
    # Stream documents one at a time
    for doc in client.iter_all_documents(page_size=50):
        # Process immediately without loading all into memory
        content = client.get_document_content(doc['id'])
        process_document(content)

        # Explicit memory management
        del content
        gc.collect()
```

---

## Ollama Client

**File:** `lib/ollama_client.py`

Robust LLM client for Ollama with memory management, retry logic, and specialized prompts.

### Quick Reference

```python
from lib import OllamaClient, OllamaError

with OllamaClient() as client:
    # Simple generation
    response = client.generate("What is OSINT?")

    # Streaming
    for chunk in client.generate_stream("Analyze this..."):
        print(chunk, end="", flush=True)

    # Specialized methods
    entities = client.extract_entities(document_text)
    summary = client.summarize(text, max_length=200)
    analysis = client.analyze_connections(entity1, entity2, context)

    # Memory management
    client.unload_model()  # Free GPU memory
```

### API Reference

#### `OllamaClient(base_url=None, model=None, context_size=None, timeout=None)`

**Parameters:**
- `base_url` (str, optional): Ollama server URL (defaults to `settings.ollama_url`)
- `model` (str, optional): Model name (defaults to `settings.ollama_model`)
- `context_size` (int, optional): Context window (defaults to `settings.ollama_context_size`)
- `timeout` (int, optional): Request timeout (defaults to `settings.ollama_timeout`)

**Features:**
- Automatic retry with exponential backoff (3 attempts)
- Automatic model unloading for memory management
- Streaming support
- Specialized prompts for common tasks
- Connection pooling

#### Generation Methods

##### `generate(prompt: str, system=None, temperature=0.7, max_tokens=None) -> str`
Generate a response from the LLM.

```python
response = client.generate(
    prompt="Summarize this document: ...",
    system="You are a legal document analyst.",
    temperature=0.3,  # Lower = more deterministic
    max_tokens=500
)
```

**Parameters:**
- `prompt` (str): User prompt
- `system` (str, optional): System prompt
- `temperature` (float): Sampling temperature (0.0-1.0)
- `max_tokens` (int, optional): Max tokens to generate

**Automatic Features:**
- Retry on connection errors (3 attempts)
- Memory management (auto-unload every N generations)
- Timeout handling

##### `generate_stream(prompt: str, system=None, temperature=0.7) -> Generator[str]`
Generate a streaming response.

```python
print("Response: ", end="")
for chunk in client.generate_stream("Analyze this document..."):
    print(chunk, end="", flush=True)
print()
```

**Use Cases:**
- Real-time output for long generations
- Progress indication for users
- Reduced latency (first token faster)

#### Specialized Methods

##### `extract_entities(text: str, entity_types=None) -> List[Dict]`
Extract named entities from text.

```python
entities = client.extract_entities(
    text=document_content,
    entity_types=["Person", "Organization", "Location"]
)

for entity in entities:
    print(f"{entity['type']}: {entity['name']}")
    print(f"  Context: {entity['context']}")
```

**Default entity types:**
- Person
- Organization
- Location
- Event
- Date
- Document

**Returns:**
```python
[
    {
        "name": "Jeffrey Epstein",
        "type": "Person",
        "context": "...meetings with Jeffrey Epstein in 2010..."
    },
    ...
]
```

##### `summarize(text: str, max_length=200) -> str`
Generate a concise summary.

```python
summary = client.summarize(
    text=long_document,
    max_length=200  # Approximate word count
)

print(summary)
```

**Features:**
- Factual, concise summaries
- Key points extraction
- Configurable length

##### `analyze_connections(entity1: str, entity2: str, context: str) -> Dict`
Analyze relationship between two entities.

```python
analysis = client.analyze_connections(
    entity1="Jeffrey Epstein",
    entity2="Bill Clinton",
    context=document_text
)

print(f"Relationship: {analysis['relationship']}")
print(f"Confidence: {analysis['confidence']}")
print(f"Evidence: {analysis['evidence']}")
```

**Returns:**
```python
{
    "relationship": "Brief description of connection",
    "confidence": "high" | "medium" | "low",
    "evidence": "Key quotes or facts"
}
```

#### Memory Management

##### `unload_model() -> bool`
Manually unload model from GPU/RAM.

```python
# After processing batch
client.unload_model()
gc.collect()  # Python garbage collection

# Wait before next batch
time.sleep(30)
```

**Automatic Unloading:**
Model is automatically unloaded every N generations (configurable via `settings.unload_model_every`).

##### Model Management

##### `list_models() -> List[Dict]`
List all available models.

```python
models = client.list_models()
for model in models:
    print(f"- {model['name']} ({model['size']})")
```

##### `model_exists(model_name=None) -> bool`
Check if a model is available.

```python
if client.model_exists("mistral"):
    print("Model is available")
else:
    print("Model not found - run: ollama pull mistral")
```

##### `health_check() -> bool`
Check if Ollama server is reachable.

```python
if client.health_check():
    print("Ollama is healthy")
else:
    print("Cannot connect to Ollama")
```

### Exceptions

All exceptions inherit from `OllamaError`:

| Exception | Meaning | When Raised |
|-----------|---------|-------------|
| `OllamaError` | Base exception | Any error |
| `OllamaConnectionError` | Cannot connect | Server unreachable |
| `OllamaModelError` | Model issue | Model not found/failed to load |
| `OllamaTimeoutError` | Request timeout | Generation took too long |

### Usage Examples

#### Basic Generation

```python
from lib import OllamaClient, OllamaError, get_logger

logger = get_logger(__name__)

try:
    with OllamaClient() as client:
        # Health check
        if not client.health_check():
            logger.error("Ollama not available")
            sys.exit(1)

        # Verify model exists
        if not client.model_exists():
            logger.error("Model not found", model=client.model)
            logger.info("Run: ollama pull mistral")
            sys.exit(1)

        # Generate response
        response = client.generate(
            prompt="What is open source intelligence?",
            temperature=0.5
        )

        logger.info("Generation complete", length=len(response))
        print(response)

except OllamaTimeoutError:
    logger.error("Request timed out", timeout=client.timeout)
except OllamaConnectionError:
    logger.error("Cannot connect to Ollama server")
except OllamaError as e:
    logger.error("LLM error", error=str(e))
```

#### Entity Extraction Pipeline

```python
with OllamaClient() as client:
    # Extract entities from all documents
    all_entities = []

    for doc in documents:
        logger.info("Extracting entities", doc_id=doc['id'])

        try:
            entities = client.extract_entities(
                text=doc['content'],
                entity_types=["Person", "Organization"]
            )

            logger.info("Entities found",
                       doc_id=doc['id'],
                       count=len(entities))

            all_entities.extend(entities)

        except OllamaError as e:
            logger.error("Extraction failed",
                        doc_id=doc['id'],
                        error=str(e))
            continue

        # Memory management
        if doc['id'] % 10 == 0:
            client.unload_model()
            time.sleep(30)

    logger.info("Extraction complete", total_entities=len(all_entities))
```

#### Streaming Output

```python
with OllamaClient() as client:
    print("Generating dossier... ", end="", flush=True)

    full_response = ""
    for chunk in client.generate_stream(
        prompt=f"Generate a dossier for: {entity_name}",
        system="You are an intelligence analyst.",
        temperature=0.7
    ):
        print(chunk, end="", flush=True)
        full_response += chunk

    print("\n\nGeneration complete!")
    return full_response
```

---

## Logging Configuration

**File:** `lib/logging_config.py`

Structured logging with JSON output, context propagation, and log levels.

### Quick Reference

```python
from lib import get_logger, with_context, clear_context

# Get logger
logger = get_logger(__name__)

# Basic logging
logger.info("Processing started", entity="Epstein", doc_count=247)
logger.warning("Retrying request", attempt=2, max_attempts=3)
logger.error("Processing failed", error=str(e), exc_info=True)

# Context propagation
with_context(request_id="abc123", user="system")
logger.info("Processing")  # Includes request_id and user
clear_context()
```

### API Reference

#### `get_logger(name: str = None) -> BoundLogger`
Get a structured logger instance.

```python
# Typically use __name__
logger = get_logger(__name__)

# Or custom name
logger = get_logger("my_pipeline")
```

#### `configure_logging(level="INFO", json_format=False, log_file=None)`
Configure logging format and output.

**Parameters:**
- `level` (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `json_format` (bool): Output JSON instead of console format
- `log_file` (str): Optional file path for logs

```python
from lib.logging_config import configure_logging

# Reconfigure for production
configure_logging(
    level="INFO",
    json_format=True,
    log_file="/var/log/continuum.log"
)
```

#### Context Management

##### `with_context(**kwargs)`
Bind context variables to all subsequent log messages.

```python
# Add context
with_context(doc_id=123, entity="Epstein")

logger.info("Processing")
# Output includes: doc_id=123, entity="Epstein"

logger.info("Complete")
# Output STILL includes: doc_id=123, entity="Epstein"
```

##### `clear_context()`
Clear all bound context variables.

```python
with_context(doc_id=123)
logger.info("Message 1")  # Has doc_id

clear_context()
logger.info("Message 2")  # No doc_id
```

### Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| `DEBUG` | Development, detailed flow | `logger.debug("Parsing chunk", chunk_num=5)` |
| `INFO` | Important state changes | `logger.info("Processing started", count=100)` |
| `WARNING` | Recoverable issues | `logger.warning("Retry attempt", attempt=2)` |
| `ERROR` | Failures that stop a task | `logger.error("Document failed", error=str(e))` |
| `CRITICAL` | System-wide failures | `logger.critical("Database unreachable")` |

### Output Formats

#### Console Format (Default)

```
2024-12-24T10:30:45 [info     ] Processing document            doc_id=123 title=Flight Logs
2024-12-24T10:30:46 [warning  ] Retry attempt                  attempt=2 max_attempts=3
2024-12-24T10:30:47 [error    ] Processing failed              doc_id=123 error=Connection timeout
```

**Features:**
- Colored output (info=green, warning=yellow, error=red)
- Human-readable timestamps
- Key-value pairs clearly visible

#### JSON Format (Production)

Set `LOG_FORMAT=json` in environment:

```json
{
  "event": "Processing document",
  "timestamp": "2024-12-24T10:30:45.123456Z",
  "level": "info",
  "logger": "continuum_pipeline",
  "doc_id": 123,
  "title": "Flight Logs"
}
```

**Benefits:**
- Machine-readable
- Log aggregation ready (ELK, Loki, etc.)
- Searchable and filterable
- Structured data preserved

### Usage Examples

#### Basic Logging

```python
from lib import get_logger

logger = get_logger(__name__)

def process_documents(docs):
    logger.info("Starting processing", total_docs=len(docs))

    for i, doc in enumerate(docs):
        logger.debug("Processing document",
                    doc_id=doc['id'],
                    progress=f"{i+1}/{len(docs)}")

        try:
            result = process_doc(doc)
            logger.info("Document complete",
                       doc_id=doc['id'],
                       entities_found=len(result))

        except Exception as e:
            logger.error("Processing failed",
                        doc_id=doc['id'],
                        error=str(e),
                        exc_info=True)  # Include stack trace

    logger.info("Processing complete", total_docs=len(docs))
```

#### Context Propagation

```python
from lib import get_logger, with_context, clear_context

logger = get_logger(__name__)

def process_entity(entity_name, entity_type):
    # Add context for all logs in this function
    with_context(entity_name=entity_name, entity_type=entity_type)

    logger.info("Starting entity processing")
    # Output includes: entity_name and entity_type

    docs = search_documents(entity_name)
    logger.info("Documents found", count=len(docs))
    # Output STILL includes: entity_name and entity_type

    for doc in docs:
        with_context(doc_id=doc['id'])  # Add more context
        logger.info("Processing document")
        # Output includes: entity_name, entity_type, doc_id

        clear_context()  # Clear doc_id
        # entity_name and entity_type still present

    clear_context()  # Clear all context
    logger.info("Entity complete")
    # No context included
```

#### Environment-Based Configuration

```bash
# Development - colored console output with debug logs
LOG_LEVEL=DEBUG LOG_FORMAT=console python script.py

# Production - JSON output to file
LOG_LEVEL=INFO LOG_FORMAT=json LOG_FILE=/var/log/continuum.log python script.py

# Debugging specific issue
LOG_LEVEL=DEBUG python script.py 2>&1 | tee debug.log
```

---

## Error Handling

### Exception Hierarchy

```
Exception
├── PaperlessError (base)
│   ├── PaperlessAuthError (401, 403)
│   ├── PaperlessNotFoundError (404)
│   └── PaperlessConnectionError (network)
│
└── OllamaError (base)
    ├── OllamaConnectionError (network)
    ├── OllamaModelError (model issues)
    └── OllamaTimeoutError (timeout)
```

### Best Practices

#### 1. Catch Specific Exceptions

**Bad:**
```python
try:
    docs = client.get_all_documents()
except Exception as e:
    print(f"Error: {e}")
```

**Good:**
```python
try:
    docs = client.get_all_documents()
except PaperlessAuthError:
    logger.error("Invalid API token - check .env")
    sys.exit(1)
except PaperlessConnectionError:
    logger.error("Cannot connect - is Paperless running?")
    sys.exit(1)
except PaperlessError as e:
    logger.error("Unexpected Paperless error", error=str(e))
    sys.exit(1)
```

#### 2. Use exc_info for Stack Traces

```python
try:
    result = process_document(doc)
except Exception as e:
    logger.error("Processing failed",
                doc_id=doc['id'],
                error=str(e),
                exc_info=True)  # Include full traceback
```

#### 3. Fail Fast on Fatal Errors

```python
# Check prerequisites before processing
if not settings.paperless_token:
    logger.error("PAPERLESS_TOKEN not configured")
    sys.exit(1)

with PaperlessClient() as client:
    if not client.health_check():
        logger.error("Paperless not accessible")
        sys.exit(1)

# Now safe to proceed
```

---

## Best Practices

### 1. Always Use Context Managers

**Good:**
```python
with PaperlessClient() as client:
    docs = client.get_all_documents()
# Client automatically closed
```

**Bad:**
```python
client = PaperlessClient()
docs = client.get_all_documents()
# Must remember to call client.close()
```

### 2. Structured Logging with Context

**Good:**
```python
logger.info("Processing document",
           doc_id=123,
           title="Flight Logs",
           entity_count=15)
```

**Bad:**
```python
print(f"Processing document 123: Flight Logs (15 entities)")
```

### 3. Validate Configuration Early

```python
# At start of script
logger.info("Validating configuration")

status = settings.validate_connection()
if not all([status["paperless"], status["ollama"]]):
    logger.error("Service validation failed", errors=status["errors"])
    sys.exit(1)

settings.ensure_directories()
logger.info("Configuration valid")
```

### 4. Memory Management for Large Batches

```python
with OllamaClient() as client:
    for i, doc in enumerate(documents):
        # Process document
        result = client.generate(f"Analyze: {doc['content']}")

        # Periodic memory cleanup
        if i % 10 == 0:
            client.unload_model()
            gc.collect()
            time.sleep(settings.delay_between_batches)
```

### 5. Progress Tracking

```python
with PaperlessClient() as client:
    def log_progress(fetched, total):
        logger.info("Fetch progress",
                   fetched=fetched,
                   total=total,
                   percent=round(100 * fetched / total, 1))

    docs = client.get_all_documents(progress_callback=log_progress)
```

---

## Testing & Validation

### Test Individual Modules

#### Test Configuration
```bash
cd scripts
python -m lib.config
```

Expected: Configuration details and connection validation results.

#### Test Paperless Client
```bash
python -m lib.paperless_client
```

Expected: Connection status, tag/document counts, sample documents.

#### Test Ollama Client
```bash
python -m lib.ollama_client
```

Expected: Model list, health check, sample generation.

#### Test Logging
```bash
python -m lib.logging_config
```

Expected: Sample log messages in various formats.

### Integration Test Script

Create `test_integration.py`:

```python
#!/usr/bin/env python3
"""Integration test for shared library."""

from lib import (
    settings,
    get_logger,
    PaperlessClient,
    OllamaClient,
    with_context,
    clear_context
)

logger = get_logger(__name__)

def main():
    logger.info("Starting integration test")

    # Test configuration
    logger.info("Configuration loaded",
               paperless_url=settings.paperless_url,
               ollama_model=settings.ollama_model)

    # Test Paperless
    with PaperlessClient() as paperless:
        if not paperless.health_check():
            logger.error("Paperless health check failed")
            return False

        docs = paperless.get_documents_page(page_size=5)
        logger.info("Paperless test passed", doc_count=docs['count'])

    # Test Ollama
    with OllamaClient() as ollama:
        if not ollama.health_check():
            logger.error("Ollama health check failed")
            return False

        response = ollama.generate("Say 'test passed' if you can read this.")
        logger.info("Ollama test passed", response=response)

    # Test context
    with_context(test_id="integration-001")
    logger.info("Context test")
    clear_context()

    logger.info("All tests passed!")
    return True

if __name__ == "__main__":
    main()
```

Run:
```bash
python test_integration.py
```

---

## Troubleshooting

### Issue: Import Error

**Error:** `ModuleNotFoundError: No module named 'lib'`

**Solution:**
```bash
# Run from scripts directory
cd scripts
python your_script.py

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:scripts"
```

### Issue: Configuration Not Loaded

**Error:** `PAPERLESS_TOKEN is not set`

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check it has correct values
cat .env | grep PAPERLESS_TOKEN

# Test loading
python -m lib.config
```

### Issue: Connection Failures

**Error:** `PaperlessConnectionError: Cannot connect`

**Solution:**
```bash
# Test Paperless directly
curl http://192.168.1.139:8040/api/

# Test Ollama
curl http://192.168.1.139:11434/api/tags

# Check firewall
sudo ufw status

# Validate configuration
python -m lib.config
```

---

## Summary

The shared library provides:

1. **Configuration:** Type-safe, environment-based settings
2. **API Clients:** Robust, retry-enabled clients for Paperless and Ollama
3. **Logging:** Structured, searchable logs with context propagation
4. **Error Handling:** Typed exceptions for specific error scenarios

**All scripts should use the shared library for consistency, reliability, and maintainability.**

For migration guidance, see `MIGRATION_GUIDE.md`.
For environment variables, see `docs/CONFIGURATION.md`.

---

**Version:** 1.0.0
**Maintainer:** The Continuum Report Team
**Last Updated:** December 24, 2024
