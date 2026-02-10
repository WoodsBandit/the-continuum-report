# The Continuum Report

**An AI-powered document intelligence pipeline for investigative research**

Version: 2.0 (Modernized)
Last Updated: December 24, 2024

---

## Overview

The Continuum Report is an automated intelligence pipeline that:

1. **Ingests** documents from Paperless-ngx document management system
2. **Extracts** named entities (people, organizations, locations, events)
3. **Analyzes** relationships and connections between entities
4. **Generates** comprehensive dossiers and investigative reports
5. **Publishes** findings to a public website

### Key Features

- **Automated Entity Discovery:** LLM-powered extraction of entities from documents
- **Relationship Mapping:** Identify connections between people, organizations, and events
- **Dossier Generation:** Comprehensive profiles with source citations
- **Memory-Safe Processing:** Handles large document sets on modest hardware (16GB RAM)
- **Checkpoint & Resume:** Long-running processes can resume from interruption
- **Source Tracking:** Every claim linked to primary source documents

---

## Quick Start

### Prerequisites

- **Python 3.8+**
- **Paperless-ngx server** (for document storage)
- **Ollama** (for LLM processing)
- **16GB+ RAM** recommended

### Installation

#### 1. Access Repository

```bash
cd "C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum"
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `pydantic>=2.0` - Configuration management
- `pydantic-settings` - Environment variable loading
- `structlog` - Structured logging
- `requests` - HTTP client
- `tenacity` - Retry logic

#### 3. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
nano .env
```

**Minimum required:**
```bash
# Get token from Paperless UI: Settings → API Tokens
PAPERLESS_TOKEN=your_paperless_api_token_here
```

**Optional (has sensible defaults):**
```bash
PAPERLESS_URL=http://localhost:8040
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
CONTINUUM_BASE_DIR=C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum
```

#### 4. Validate Setup

```bash
cd scripts
python -m lib.config
```

Expected output:
```
============================================================
The Continuum Report - Configuration Check
============================================================

Services:
  Paperless:  http://localhost:8040
  Ollama:     http://localhost:11434 (model: mistral)

Validating connections...
  Paperless:  OK
  Ollama:     OK
```

✅ If both services show "OK", you're ready to go!

---

## Usage

### Entity Discovery

Extract entities from all documents in Paperless:

```bash
cd scripts
python entity_discovery.py
```

**What it does:**
1. Fetches all documents from Paperless-ngx
2. Extracts named entities (people, organizations, locations, events)
3. Saves to `entity_database.json`
4. Creates dossier generation queue

**Output:**
- `entity_data/entity_database.json` - All discovered entities
- `entity_data/dossier_queue.json` - Queue for dossier generation

### Generate Dossiers

Create comprehensive profiles for discovered entities:

```bash
cd scripts
python continuum_pipeline.py "Jeffrey Epstein"
```

**What it does:**
1. Searches Paperless for all documents mentioning the subject
2. Extracts relevant information using LLM
3. Generates a comprehensive dossier with source citations
4. Saves to `reports/` directory

**Output:**
- `reports/Dossier_Jeffrey_Epstein.md` - Comprehensive profile
- Includes source links to original documents

### Full Pipeline

Run the complete pipeline for a subject:

```bash
cd scripts

# 1. Discover entities (one-time or periodic)
python entity_discovery.py

# 2. Generate dossier for specific entity
python continuum_pipeline.py "Entity Name"

# 3. Generate connection briefs
python generate_connection_briefs.py
```

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                  The Continuum Report                   │
└─────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Paperless   │─────▶│  Processing  │─────▶│   Website    │
│   (Docs)     │      │   Pipeline   │      │  (Public)    │
└──────────────┘      └──────────────┘      └──────────────┘
                            │
                            ▼
                      ┌──────────────┐
                      │    Ollama    │
                      │    (LLM)     │
                      └──────────────┘

Data Flow:
1. Documents → Paperless-ngx (storage & OCR)
2. Pipeline → Fetch documents via API
3. Pipeline → Extract entities using Ollama
4. Pipeline → Generate dossiers
5. Dossiers → Published to website
```

### Directory Structure

```
continuum/
├── scripts/
│   ├── lib/                          # Shared library (NEW!)
│   │   ├── config.py                 # Configuration management
│   │   ├── paperless_client.py      # Paperless API client
│   │   ├── ollama_client.py         # Ollama LLM client
│   │   ├── logging_config.py        # Structured logging
│   │   └── __init__.py               # Package exports
│   │
│   ├── entity_discovery.py          # Extract entities from docs
│   ├── continuum_pipeline.py        # Generate dossiers
│   ├── generate_connection_briefs.py # Entity relationships
│   └── ...                           # Other utilities
│
├── entity_data/                      # Entity database
│   ├── entity_database.json         # Discovered entities
│   ├── dossier_queue.json           # Queue for generation
│   └── checkpoints/                 # Processing state
│
├── reports/                          # Generated dossiers
│   └── Dossier_*.md                 # Entity profiles
│
├── documents/                        # Document processing
│   └── inbox/                       # Temporary storage
│
├── docs/                            # Documentation
│   └── CONFIGURATION.md             # Config guide
│
├── .env                             # Configuration (NOT in git)
├── .env.example                     # Example config
├── requirements.txt                 # Python dependencies
├── MIGRATION_GUIDE.md              # Modernization guide
└── README.md                       # This file
```

---

## Core Scripts

### Entity Discovery (`entity_discovery.py`)

**Purpose:** Discover and extract entities from all documents

**Usage:**
```bash
python entity_discovery.py
```

**Features:**
- Fetches all documents from Paperless
- Extracts entities using LLM
- Maintains entity database
- Checkpoint/resume support
- Progress tracking

**Output:**
- `entity_database.json` - All entities with metadata
- `dossier_queue.json` - Prioritized list for dossier generation

---

### Continuum Pipeline (`continuum_pipeline.py`)

**Purpose:** Generate comprehensive dossier for a specific entity

**Usage:**
```bash
python continuum_pipeline.py "Entity Name"

# Examples:
python continuum_pipeline.py "Jeffrey Epstein"
python continuum_pipeline.py "Bill Clinton"
```

**Features:**
- Search Paperless for all mentions
- Extract relevant information using LLM
- Generate structured dossier
- Include source citations
- Memory-safe processing

**Output:**
- `reports/Dossier_Entity_Name.md` - Comprehensive profile

---

### Connection Briefs (`generate_connection_briefs.py`)

**Purpose:** Analyze relationships between entities

**Usage:**
```bash
python generate_connection_briefs.py
```

**Features:**
- Identify entity co-occurrences
- Analyze relationship strength
- Generate connection summaries
- Track evidence

---

## Configuration

### Environment Variables

All configuration via environment variables (`.env` file):

| Variable | Description | Default |
|----------|-------------|---------|
| `PAPERLESS_URL` | Paperless-ngx server URL | `http://localhost:8040` |
| `PAPERLESS_TOKEN` | API authentication token | *Required* |
| `OLLAMA_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | LLM model name | `mistral` |
| `CONTINUUM_BASE_DIR` | Base data directory | Project folder |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `LOG_FORMAT` | Log format (console/json) | `console` |

**See `docs/CONFIGURATION.md` for complete reference.**

### Getting Your Paperless Token

1. Open Paperless web UI: http://localhost:8040
2. Navigate to: **Settings → API Tokens**
3. Click: **Create Token**
4. Copy the token value
5. Add to `.env`: `PAPERLESS_TOKEN=your_token_here`

### Validation

Test your configuration:

```bash
cd scripts

# Test configuration loading
python -m lib.config

# Test Paperless connection
python -m lib.paperless_client

# Test Ollama connection
python -m lib.ollama_client
```

---

## Modernization (v2.0)

The Continuum Report has been modernized with a **shared library architecture** that provides:

### What's New

✅ **Centralized Configuration**
- Environment-based (no hardcoded secrets)
- Type-safe with Pydantic
- Automatic validation

✅ **Robust API Clients**
- Automatic retry logic
- Connection pooling
- Typed exceptions
- Memory management

✅ **Structured Logging**
- JSON-capable output
- Context propagation
- Log levels
- Machine-readable

✅ **Better Error Handling**
- Typed exceptions
- Meaningful error messages
- Graceful degradation

### Migration Status

| Script | Status | Notes |
|--------|--------|-------|
| `continuum_pipeline.py` | ✅ Migrated | Uses shared library |
| `entity_discovery.py` | ✅ Migrated | Uses shared library |
| `generate_dossiers.py` | ⏳ Pending | See migration guide |
| `generate_connection_briefs.py` | ⏳ Pending | See migration guide |
| Other scripts | ⏳ Pending | Low priority |

**See `MIGRATION_GUIDE.md` for step-by-step migration instructions.**

---

## Performance & Tuning

### Memory Management

Designed for **16GB RAM systems** with conservative defaults:

```bash
# Memory safety settings (in .env)
OLLAMA_CONTEXT_SIZE=1024      # Context window size
DELAY_BETWEEN_DOCS=10         # Seconds between docs
DELAY_BETWEEN_BATCHES=30      # Seconds every 5 docs
UNLOAD_MODEL_EVERY=10         # Unload model every N docs
```

### For High-Performance Systems (32GB+ RAM)

```bash
# Aggressive settings for speed
OLLAMA_CONTEXT_SIZE=2048
DELAY_BETWEEN_DOCS=0
DELAY_BETWEEN_BATCHES=0
UNLOAD_MODEL_EVERY=50
```

### For Memory-Constrained Systems (8GB RAM)

```bash
# Conservative settings
OLLAMA_CONTEXT_SIZE=512
DELAY_BETWEEN_DOCS=30
DELAY_BETWEEN_BATCHES=60
UNLOAD_MODEL_EVERY=5
```

**See `docs/CONFIGURATION.md` for complete tuning guide.**

---

## Logging

### Development (Colored Console)

```bash
LOG_LEVEL=DEBUG LOG_FORMAT=console python script.py
```

Output:
```
2024-12-24T10:30:45 [info     ] Processing document            doc_id=123
2024-12-24T10:30:46 [debug    ] Extracting entities            count=5
```

### Production (JSON)

```bash
LOG_LEVEL=INFO LOG_FORMAT=json LOG_FILE=/var/log/continuum.log python script.py
```

Output:
```json
{"event": "Processing document", "timestamp": "2024-12-24T10:30:45Z", "level": "info", "doc_id": 123}
```

### Log Levels

- `DEBUG` - Detailed information (development)
- `INFO` - Important events (default)
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical failures

---

## Troubleshooting

### Common Issues

#### "PAPERLESS_TOKEN is not set"

**Solution:**
```bash
# Create .env file
cp .env.example .env

# Add your token
echo "PAPERLESS_TOKEN=your_token_here" >> .env

# Validate
python -m lib.config
```

#### "Cannot connect to Paperless"

**Solution:**
```bash
# Check if Paperless is running
curl http://localhost:8040/api/

# Test connection
python -m lib.paperless_client
```

#### "Model 'mistral' not found"

**Solution:**
```bash
# Pull the model
ollama pull mistral

# Or change model in .env
echo "OLLAMA_MODEL=llama2" >> .env
```

#### Out of Memory

**Solution:**
```bash
# Reduce memory usage in .env
OLLAMA_CONTEXT_SIZE=512
DELAY_BETWEEN_DOCS=30
UNLOAD_MODEL_EVERY=5
```

**See `MIGRATION_GUIDE.md` for complete troubleshooting guide.**

---

## Documentation

### For Users

- **README.md** (this file) - Overview and quick start
- **docs/CONFIGURATION.md** - Complete configuration reference
- **MIGRATION_GUIDE.md** - Modernization guide

### For Developers

- **scripts/lib/README.md** - Shared library API reference
- **MIGRATION_GUIDE.md** - How to migrate scripts
- Code documentation in each module

### Infrastructure Documentation

- **EXECUTIVE_SUMMARY.md** - Business case for cloud migration
- **CONTINUUM_REPORT_INFRASTRUCTURE_ASSESSMENT.md** - Technical analysis
- **IMPLEMENTATION_ROADMAP.md** - Phase-by-phase plan
- **QUICK_START_GUIDE.md** - Docker/K8s templates

---

## Development

### Running Scripts

```bash
# From project root
cd scripts

# Run with default logging
python continuum_pipeline.py "Jeffrey Epstein"

# Run with debug logging
LOG_LEVEL=DEBUG python continuum_pipeline.py "Jeffrey Epstein"

# Run with JSON logging
LOG_FORMAT=json python entity_discovery.py
```

### Testing

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

### Code Style

- Use shared library for all new scripts
- Structured logging (no print statements)
- Type hints where possible
- Docstrings for functions
- Configuration via environment variables

---

## Project Status

### Current Capabilities

✅ Document ingestion from Paperless-ngx
✅ Entity extraction with LLM
✅ Dossier generation
✅ Source tracking and citation
✅ Memory-safe processing
✅ Checkpoint/resume support
✅ Structured logging

### In Progress

🚧 Migration to shared library (50% complete)
🚧 Connection brief generation improvements
🚧 Website integration

### Planned

📋 Containerization (Docker)
📋 Kubernetes deployment
📋 CI/CD pipeline
📋 Cloud migration
📋 Advanced entity relationships
📋 Graph visualization

**See `IMPLEMENTATION_ROADMAP.md` for detailed timeline.**

---

## Contributing

### Getting Started

1. **Set up environment** (see Quick Start above)
2. **Read documentation** (`MIGRATION_GUIDE.md`, `scripts/lib/README.md`)
3. **Use shared library** for all new code
4. **Follow conventions** (structured logging, type hints, docstrings)

### Migration Help Needed

Scripts that need migration to shared library:

- `generate_connection_briefs.py`
- `parse_brief.py`
- `redaction_extractor.py`
- `build_graph.py`
- `export_sources.py`

**See `MIGRATION_GUIDE.md` for step-by-step instructions.**

---

## License

Copyright 2024 The Continuum Report

---

## Support

### Documentation

- **Quick Start:** This README
- **Configuration:** `docs/CONFIGURATION.md`
- **Migration:** `MIGRATION_GUIDE.md`
- **API Reference:** `scripts/lib/README.md`

### Validation

```bash
# Test everything is working
cd scripts
python -m lib.config           # Test config
python -m lib.paperless_client # Test Paperless
python -m lib.ollama_client    # Test Ollama
```

### Common Commands

```bash
# Validate setup
python -m lib.config

# Process documents
python entity_discovery.py
python continuum_pipeline.py "Entity Name"

# Debug mode
LOG_LEVEL=DEBUG python script.py

# Production mode
LOG_FORMAT=json LOG_FILE=/var/log/app.log python script.py
```

---

## Acknowledgments

Built with:
- **Paperless-ngx** - Document management
- **Ollama** - Local LLM inference
- **Pydantic** - Configuration management
- **Structlog** - Structured logging
- **Requests** - HTTP client
- **Tenacity** - Retry logic

---

**The Continuum Report** - Automated Intelligence Through Open Source Investigation

For questions or issues, see the troubleshooting sections in `MIGRATION_GUIDE.md` and `docs/CONFIGURATION.md`.
