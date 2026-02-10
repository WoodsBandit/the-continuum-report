# The Continuum Report - Configuration Guide

**Version:** 1.0
**Last Updated:** December 24, 2024

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Environment Variables Reference](#environment-variables-reference)
4. [Configuration Profiles](#configuration-profiles)
5. [Path Configuration](#path-configuration)
6. [Service Configuration](#service-configuration)
7. [Performance Tuning](#performance-tuning)
8. [Security Best Practices](#security-best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The Continuum Report uses **environment-based configuration** with sensible defaults. All configuration is managed through:

1. **Environment variables** (`.env` file or system environment)
2. **Pydantic Settings** (type-safe configuration management)
3. **Automatic validation** (on startup)

### Key Principles

- **No hardcoded secrets:** All credentials loaded from environment
- **Type safety:** Pydantic validates types and formats
- **Sensible defaults:** Works out-of-box for development
- **Override flexibility:** Change any setting via environment
- **Validation:** Automatic connection testing

---

## Quick Start

### Step 1: Create Configuration File

```bash
# From project root
cp .env.example .env
```

### Step 2: Edit Essential Settings

Open `.env` in your editor:

```bash
nano .env  # or vim, code, etc.
```

**Minimum required:**
```bash
# REQUIRED: Your Paperless API token
PAPERLESS_TOKEN=your_token_here

# Optional: Override defaults (local Docker services)
PAPERLESS_URL=http://localhost:8040
OLLAMA_URL=http://localhost:11434
```

### Step 3: Get Your Paperless Token

1. Open Paperless web UI: http://localhost:8040
2. Navigate to **Settings → API Tokens**
3. Click **Create Token**
4. Copy the token value
5. Paste into `.env` file: `PAPERLESS_TOKEN=abc123...`

### Step 4: Validate Configuration

```bash
cd scripts
python -m lib.config
```

Expected output:
```
============================================================
The Continuum Report - Configuration Check
============================================================

Configuration: ContinuumSettings(...)

Directories:
  Base:       /continuum
  Data:       /continuum/entity_data
  Reports:    /continuum/reports

Services:
  Paperless:  http://localhost:8040
  Ollama:     http://localhost:11434 (model: mistral)

  Token:      [SET]

Validating connections...
  Paperless:  OK
  Ollama:     OK
```

If you see "OK" for both services, you're ready to go!

---

## Environment Variables Reference

### Paperless-ngx Configuration

#### `PAPERLESS_URL`

**Description:** Paperless-ngx server URL

**Type:** String (URL)

**Default:** `http://localhost:8040`

**Examples:**
```bash
# Local development
PAPERLESS_URL=http://localhost:8040

# Remote server
PAPERLESS_URL=https://paperless.example.com

# Custom port
PAPERLESS_URL=http://localhost:9000
```

**Validation:** Must be a valid HTTP/HTTPS URL

---

#### `PAPERLESS_TOKEN`

**Description:** API authentication token (REQUIRED)

**Type:** String

**Default:** `""` (empty - will warn if not set)

**How to get:**
1. Paperless UI → Settings → API Tokens
2. Create new token
3. Copy value to `.env`

**Security:**
- Never commit to git
- Keep in `.env` file (gitignored)
- Rotate periodically
- One token per environment

**Examples:**
```bash
PAPERLESS_TOKEN=da99fe6aa0b8d021689126cf72b91986abbbd283
```

---

#### `PAPERLESS_TIMEOUT`

**Description:** API request timeout in seconds

**Type:** Integer

**Default:** `30`

**Use Cases:**
```bash
# Fast network - short timeout
PAPERLESS_TIMEOUT=10

# Slow network - longer timeout
PAPERLESS_TIMEOUT=60

# Large document downloads
PAPERLESS_TIMEOUT=120
```

**Recommendation:** 30 seconds is good for most cases

---

### Ollama Configuration

#### `OLLAMA_URL`

**Description:** Ollama LLM server URL

**Type:** String (URL)

**Default:** `http://localhost:11434`

**Examples:**
```bash
# Local Ollama
OLLAMA_URL=http://localhost:11434

# Remote GPU server
OLLAMA_URL=http://gpu-server.local:11434

# Cloud deployment
OLLAMA_URL=https://ollama.example.com
```

---

#### `OLLAMA_MODEL`

**Description:** LLM model to use for processing

**Type:** String

**Default:** `mistral`

**Available Models:**
- `mistral` - Fast, efficient (recommended)
- `llama2` - General purpose
- `llama2:13b` - Larger, more capable
- `codellama` - Code-focused
- `vicuna` - Instruction-following

**Examples:**
```bash
# Default - good balance
OLLAMA_MODEL=mistral

# More capable (needs more RAM)
OLLAMA_MODEL=llama2:13b

# Faster (smaller model)
OLLAMA_MODEL=llama2:7b
```

**Installation:**
```bash
# Pull model before use
ollama pull mistral
```

**Recommendation:** Start with `mistral` for best performance/quality ratio

---

#### `OLLAMA_CONTEXT_SIZE`

**Description:** Context window size (tokens)

**Type:** Integer

**Default:** `1024`

**Impact:**
- **Lower value:** Less RAM, faster, shorter context
- **Higher value:** More RAM, slower, longer context

**Examples:**
```bash
# Minimal RAM (16GB system)
OLLAMA_CONTEXT_SIZE=512

# Balanced (default)
OLLAMA_CONTEXT_SIZE=1024

# More context (32GB+ RAM)
OLLAMA_CONTEXT_SIZE=2048

# Maximum context (64GB+ RAM)
OLLAMA_CONTEXT_SIZE=4096
```

**Recommendation:** 1024 for 16GB RAM systems

---

#### `OLLAMA_TIMEOUT`

**Description:** LLM request timeout in seconds

**Type:** Integer

**Default:** `600` (10 minutes)

**Use Cases:**
```bash
# Quick generations only
OLLAMA_TIMEOUT=300

# Long dossier generation
OLLAMA_TIMEOUT=900

# Very large documents
OLLAMA_TIMEOUT=1800
```

**Recommendation:** 600 seconds (10 minutes) handles most cases

---

### Directory Configuration

#### `CONTINUUM_BASE_DIR`

**Description:** Base directory for all Continuum data

**Type:** String (path)

**Default:** `/continuum`

**Examples:**
```bash
# Default (Linux/WSL)
CONTINUUM_BASE_DIR=/continuum

# User home directory
CONTINUUM_BASE_DIR=/home/user/continuum

# Windows path
CONTINUUM_BASE_DIR=C:\Users\User\continuum

# Project data directory
CONTINUUM_BASE_DIR=data/paperless
```

**Auto-created subdirectories:**
- `entity_data/` - Entity database and checkpoints
- `reports/` - Generated dossiers and reports
- `checkpoints/` - Processing state for resumption
- `documents/inbox/` - Document processing inbox

**Permissions:**
- Must be writable
- Ensure adequate disk space
- Consider backup requirements

---

### Derived Paths

These are automatically derived from `CONTINUUM_BASE_DIR` and cannot be overridden directly:

#### Data Directory
```python
settings.data_dir  # /continuum/entity_data
```

Stores:
- `entity_database.json` - Entity extraction results
- `dossier_queue.json` - Queue for dossier generation
- `discovery_checkpoint.json` - Entity discovery progress

#### Reports Directory
```python
settings.reports_dir  # /continuum/reports
```

Stores:
- Generated dossiers (markdown)
- Connection briefs
- Analysis reports

#### Checkpoint Directory
```python
settings.checkpoint_dir  # /continuum/checkpoints
```

Stores:
- Pipeline processing state
- Resume points for long operations

#### Documents Inbox
```python
settings.documents_inbox  # /continuum/documents/inbox
```

Stores:
- Processed document exports
- Temporary files during pipeline

---

### Website Configuration

#### `WEBSITE_BASE_URL`

**Description:** Public website base URL

**Type:** String (URL)

**Default:** `https://thecontinuumreport.com`

**Purpose:** Used for generating document source links

**Examples:**
```bash
# Production
WEBSITE_BASE_URL=https://thecontinuumreport.com

# Staging
WEBSITE_BASE_URL=https://staging.thecontinuumreport.com

# Local development
WEBSITE_BASE_URL=http://localhost:3000
```

---

### Processing Configuration

#### `MAX_DOCUMENTS_TO_SEARCH`

**Description:** Maximum documents to search per query

**Type:** Integer

**Default:** `9999`

**Use Cases:**
```bash
# No limit (process everything)
MAX_DOCUMENTS_TO_SEARCH=9999

# Limit for testing
MAX_DOCUMENTS_TO_SEARCH=100

# Quick prototype
MAX_DOCUMENTS_TO_SEARCH=10
```

---

#### `MAX_DOCUMENTS_FOR_ENTITIES`

**Description:** Maximum documents for entity extraction

**Type:** Integer

**Default:** `9999`

**Examples:**
```bash
# Process all matching documents
MAX_DOCUMENTS_FOR_ENTITIES=9999

# Limit to first 500
MAX_DOCUMENTS_FOR_ENTITIES=500
```

---

#### `MAX_DOCUMENTS_FOR_DOSSIER`

**Description:** Maximum documents to include in dossier generation

**Type:** Integer

**Default:** `9999`

**Examples:**
```bash
# Include all references
MAX_DOCUMENTS_FOR_DOSSIER=9999

# Limit for performance
MAX_DOCUMENTS_FOR_DOSSIER=250
```

---

#### `MAX_CHUNK_SIZE`

**Description:** Text chunk size in characters for LLM processing

**Type:** Integer

**Default:** `1500`

**Impact:**
- **Smaller:** Less RAM, more API calls, faster per call
- **Larger:** More RAM, fewer API calls, slower per call

**Examples:**
```bash
# Minimal memory
MAX_CHUNK_SIZE=1000

# Balanced (default)
MAX_CHUNK_SIZE=1500

# More context
MAX_CHUNK_SIZE=2000
```

---

### Memory Safety Settings

Designed for systems with 16GB RAM.

#### `DELAY_BETWEEN_DOCS`

**Description:** Seconds to wait between processing documents

**Type:** Integer

**Default:** `10`

**Purpose:** Prevent memory exhaustion, allow garbage collection

**Examples:**
```bash
# Fast processing (32GB+ RAM)
DELAY_BETWEEN_DOCS=0

# Balanced (16GB RAM)
DELAY_BETWEEN_DOCS=10

# Very cautious (8GB RAM)
DELAY_BETWEEN_DOCS=30
```

---

#### `DELAY_BETWEEN_BATCHES`

**Description:** Seconds to wait every 5 documents

**Type:** Integer

**Default:** `30`

**Purpose:** Allow model to cool down, clear GPU memory

**Examples:**
```bash
# No batch delays (powerful GPU)
DELAY_BETWEEN_BATCHES=0

# Standard (default)
DELAY_BETWEEN_BATCHES=30

# Conservative
DELAY_BETWEEN_BATCHES=60
```

---

#### `UNLOAD_MODEL_EVERY`

**Description:** Unload Ollama model every N documents

**Type:** Integer

**Default:** `10`

**Purpose:** Free GPU/RAM periodically

**Examples:**
```bash
# Never unload (lots of VRAM)
UNLOAD_MODEL_EVERY=0

# Aggressive memory management
UNLOAD_MODEL_EVERY=5

# Balanced (default)
UNLOAD_MODEL_EVERY=10

# Less frequent
UNLOAD_MODEL_EVERY=20
```

**Note:** Set to 0 to disable automatic unloading

---

### Logging Configuration

#### `LOG_LEVEL`

**Description:** Minimum log level to display

**Type:** String

**Default:** `INFO`

**Options:**
- `DEBUG` - Everything (verbose)
- `INFO` - Important events
- `WARNING` - Warnings and errors
- `ERROR` - Errors only
- `CRITICAL` - Critical errors only

**Examples:**
```bash
# Development - see everything
LOG_LEVEL=DEBUG

# Production - important events only
LOG_LEVEL=INFO

# Troubleshooting - detailed
LOG_LEVEL=DEBUG

# Quiet - errors only
LOG_LEVEL=ERROR
```

---

#### `LOG_FORMAT`

**Description:** Log output format

**Type:** String

**Default:** `console`

**Options:**
- `console` - Colored, human-readable
- `json` - JSON format (for log aggregation)

**Examples:**
```bash
# Development - colored console
LOG_FORMAT=console

# Production - JSON for ELK/Loki
LOG_FORMAT=json

# Both (if log file also used)
LOG_FORMAT=json LOG_FILE=/var/log/continuum.log
```

**Console Output:**
```
2024-12-24T10:30:45 [info     ] Processing document            doc_id=123
```

**JSON Output:**
```json
{"event": "Processing document", "timestamp": "2024-12-24T10:30:45Z", "level": "info", "doc_id": 123}
```

---

#### `LOG_FILE`

**Description:** Optional log file path

**Type:** String (path)

**Default:** None (log to stdout only)

**Examples:**
```bash
# Log to file
LOG_FILE=/var/log/continuum.log

# Separate log per script
LOG_FILE=/var/log/continuum_$(date +%Y%m%d).log

# Log to project directory
LOG_FILE=/continuum/logs/continuum.log
```

**Setup:**
```bash
# Create log directory
sudo mkdir -p /var/log/continuum
sudo chown $USER:$USER /var/log/continuum

# Enable logging
export LOG_FILE=/var/log/continuum/app.log
```

---

## Configuration Profiles

### Development Profile

**File:** `.env.development`

```bash
# Development settings - local services, debug logging

# Paperless
PAPERLESS_URL=http://localhost:8040
PAPERLESS_TOKEN=dev_token_here
PAPERLESS_TIMEOUT=30

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OLLAMA_CONTEXT_SIZE=1024
OLLAMA_TIMEOUT=300

# Directories
CONTINUUM_BASE_DIR=/home/user/continuum-dev

# Processing - smaller limits for testing
MAX_DOCUMENTS_TO_SEARCH=100
MAX_DOCUMENTS_FOR_ENTITIES=50
MAX_DOCUMENTS_FOR_DOSSIER=50

# Memory - relaxed for dev
DELAY_BETWEEN_DOCS=5
DELAY_BETWEEN_BATCHES=15
UNLOAD_MODEL_EVERY=20

# Logging - verbose
LOG_LEVEL=DEBUG
LOG_FORMAT=console
```

**Usage:**
```bash
cp .env.development .env
```

---

### Production Profile

**File:** `.env.production`

```bash
# Production settings - optimized for throughput and reliability

# Paperless (local Docker)
PAPERLESS_URL=http://localhost:8040
PAPERLESS_TOKEN=secure_production_token_here
PAPERLESS_TIMEOUT=60

# Ollama (local Docker)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OLLAMA_CONTEXT_SIZE=1024
OLLAMA_TIMEOUT=600

# Directories
CONTINUUM_BASE_DIR=/continuum

# Processing - no limits
MAX_DOCUMENTS_TO_SEARCH=9999
MAX_DOCUMENTS_FOR_ENTITIES=9999
MAX_DOCUMENTS_FOR_DOSSIER=9999

# Memory - balanced for 16GB RAM
DELAY_BETWEEN_DOCS=10
DELAY_BETWEEN_BATCHES=30
UNLOAD_MODEL_EVERY=10

# Logging - JSON for aggregation
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=/var/log/continuum/production.log
```

---

### Testing Profile

**File:** `.env.test`

```bash
# Testing settings - fast, limited scope

# Paperless
PAPERLESS_URL=http://localhost:8040
PAPERLESS_TOKEN=test_token_here
PAPERLESS_TIMEOUT=15

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
OLLAMA_CONTEXT_SIZE=512
OLLAMA_TIMEOUT=120

# Directories
CONTINUUM_BASE_DIR=/tmp/continuum-test

# Processing - very limited
MAX_DOCUMENTS_TO_SEARCH=10
MAX_DOCUMENTS_FOR_ENTITIES=5
MAX_DOCUMENTS_FOR_DOSSIER=5
MAX_CHUNK_SIZE=1000

# Memory - minimal delays
DELAY_BETWEEN_DOCS=1
DELAY_BETWEEN_BATCHES=5
UNLOAD_MODEL_EVERY=5

# Logging - debug
LOG_LEVEL=DEBUG
LOG_FORMAT=console
```

---

### High-Performance Profile

**File:** `.env.highperf`

For systems with 32GB+ RAM and dedicated GPU.

```bash
# High-performance settings - maximum throughput

# Paperless (local Docker)
PAPERLESS_URL=http://localhost:8040
PAPERLESS_TOKEN=your_token_here
PAPERLESS_TIMEOUT=60

# Ollama - larger model, more context (local Docker)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2:13b
OLLAMA_CONTEXT_SIZE=4096
OLLAMA_TIMEOUT=900

# Directories
CONTINUUM_BASE_DIR=/data/continuum

# Processing - no limits
MAX_DOCUMENTS_TO_SEARCH=9999
MAX_DOCUMENTS_FOR_ENTITIES=9999
MAX_DOCUMENTS_FOR_DOSSIER=9999
MAX_CHUNK_SIZE=3000

# Memory - minimal constraints
DELAY_BETWEEN_DOCS=0
DELAY_BETWEEN_BATCHES=0
UNLOAD_MODEL_EVERY=50

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=/data/logs/continuum.log
```

---

## Path Configuration

### Linux/WSL

```bash
# Standard Linux path
CONTINUUM_BASE_DIR=/continuum

# User home directory
CONTINUUM_BASE_DIR=/home/username/continuum

# Mounted volume
CONTINUUM_BASE_DIR=/mnt/data/continuum
```

### Windows (Native Python)

```bash
# Windows path (backslashes escaped)
CONTINUUM_BASE_DIR=C:\\Users\\Username\\continuum

# Or forward slashes
CONTINUUM_BASE_DIR=C:/Users/Username/continuum
```

### Local Project Directory

```bash
# All services run locally via Docker on WoodsDen
# Data is stored within the project folder
CONTINUUM_BASE_DIR=data/paperless
```

### Docker Volumes

```bash
# Named volume
CONTINUUM_BASE_DIR=/continuum

# Then mount in docker-compose.yml:
volumes:
  - continuum-data:/continuum
```

---

## Service Configuration

### Paperless-ngx

#### Connection Test

```bash
# Test API access
curl -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8040/api/

# Expected: {"version": "1.x.x", ...}
```

#### Common Issues

**Invalid Token:**
```bash
# Get new token
# 1. Login to Paperless UI
# 2. Settings → API Tokens
# 3. Create Token
# 4. Update .env file
```

**Connection Refused:**
```bash
# Check if Paperless is running
systemctl status paperless

# Check port
netstat -tuln | grep 8040
```

---

### Ollama

#### Model Management

```bash
# List available models
ollama list

# Pull required model
ollama pull mistral

# Remove unused model
ollama rm old-model
```

#### Connection Test

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Test generation
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Test",
  "stream": false
}'
```

#### GPU Configuration

```bash
# Check GPU usage
nvidia-smi

# Set GPU devices
export CUDA_VISIBLE_DEVICES=0

# Limit GPU memory
export OLLAMA_GPU_MEMORY=8GB
```

---

## Performance Tuning

### Memory-Constrained Systems (8-16GB RAM)

```bash
# Conservative settings
OLLAMA_CONTEXT_SIZE=512
MAX_CHUNK_SIZE=1000
DELAY_BETWEEN_DOCS=15
DELAY_BETWEEN_BATCHES=60
UNLOAD_MODEL_EVERY=5
```

### Balanced Systems (16-32GB RAM)

```bash
# Default settings (optimal for most)
OLLAMA_CONTEXT_SIZE=1024
MAX_CHUNK_SIZE=1500
DELAY_BETWEEN_DOCS=10
DELAY_BETWEEN_BATCHES=30
UNLOAD_MODEL_EVERY=10
```

### High-Performance Systems (32GB+ RAM)

```bash
# Aggressive settings
OLLAMA_CONTEXT_SIZE=2048
MAX_CHUNK_SIZE=3000
DELAY_BETWEEN_DOCS=0
DELAY_BETWEEN_BATCHES=0
UNLOAD_MODEL_EVERY=50
```

### Throughput Optimization

```bash
# Maximize document processing speed
DELAY_BETWEEN_DOCS=0
DELAY_BETWEEN_BATCHES=0
UNLOAD_MODEL_EVERY=0  # Never unload
PAPERLESS_TIMEOUT=10  # Fast fail
OLLAMA_CONTEXT_SIZE=512  # Smaller context
```

### Quality Optimization

```bash
# Maximize analysis quality
OLLAMA_MODEL=llama2:13b  # Larger model
OLLAMA_CONTEXT_SIZE=4096  # More context
MAX_CHUNK_SIZE=3000  # Larger chunks
OLLAMA_TIMEOUT=1800  # Allow long processing
```

---

## Security Best Practices

### 1. Protect API Tokens

**Do:**
```bash
# Store in .env file (gitignored)
echo "PAPERLESS_TOKEN=secret" >> .env

# Use environment variables
export PAPERLESS_TOKEN=secret

# Use secrets management (production)
# - AWS Secrets Manager
# - HashiCorp Vault
# - Kubernetes Secrets
```

**Don't:**
```bash
# Never hardcode in scripts
PAPERLESS_TOKEN = "secret"  # BAD!

# Never commit .env to git
git add .env  # BAD!
```

### 2. File Permissions

```bash
# Restrict .env file
chmod 600 .env

# Verify
ls -la .env
# Should show: -rw------- (read/write owner only)
```

### 3. Token Rotation

```bash
# Rotate tokens periodically
# 1. Generate new token in Paperless UI
# 2. Update .env file
# 3. Test with: python -m lib.config
# 4. Revoke old token
```

### 4. Network Security

```bash
# Use HTTPS in production
PAPERLESS_URL=https://paperless.example.com

# Note: Firewall rules not needed for localhost services
```

### 5. Environment Isolation

```bash
# Separate configs per environment
.env.development
.env.staging
.env.production

# Load appropriate config
ln -sf .env.production .env
```

---

## Troubleshooting

### Issue: Configuration Not Loading

**Symptoms:**
- Warnings about missing PAPERLESS_TOKEN
- Default values used instead of custom

**Diagnosis:**
```bash
# Check .env file exists
ls -la .env

# Check file contents
cat .env

# Test loading
python -m lib.config
```

**Solutions:**
```bash
# Create .env if missing
cp .env.example .env

# Check file format (no spaces around =)
PAPERLESS_TOKEN=value  # CORRECT
PAPERLESS_TOKEN = value  # WRONG

# Verify encoding
file .env
# Should show: ASCII text
```

---

### Issue: Connection Failures

**Symptoms:**
- "Cannot connect to Paperless"
- "Cannot connect to Ollama"

**Diagnosis:**
```bash
# Test Paperless
curl http://localhost:8040/api/

# Test Ollama
curl http://localhost:11434/api/tags

# Check Docker services are running
docker ps
```

**Solutions:**
```bash
# Check services are running
systemctl status paperless
systemctl status ollama

# Check firewall
sudo ufw status

# Test from script
python -m lib.config
```

---

### Issue: Authentication Errors

**Symptoms:**
- "Invalid API token"
- "Access denied"

**Diagnosis:**
```bash
# Verify token in .env
grep PAPERLESS_TOKEN .env

# Test token manually
curl -H "Authorization: Token YOUR_TOKEN" \
     http://localhost:8040/api/documents/
```

**Solutions:**
```bash
# Get new token from Paperless UI
# Settings → API Tokens → Create Token

# Update .env
echo "PAPERLESS_TOKEN=new_token_here" >> .env

# Test
python -m lib.paperless_client
```

---

### Issue: Out of Memory

**Symptoms:**
- Python crashes
- "Killed" messages
- System becomes unresponsive

**Diagnosis:**
```bash
# Check memory usage
free -h
htop

# Monitor during execution
watch -n 1 free -h
```

**Solutions:**
```bash
# Reduce context size
OLLAMA_CONTEXT_SIZE=512

# Increase delays
DELAY_BETWEEN_DOCS=30
DELAY_BETWEEN_BATCHES=60

# Unload more frequently
UNLOAD_MODEL_EVERY=5

# Use smaller model
OLLAMA_MODEL=mistral  # instead of llama2:13b
```

---

### Issue: Slow Processing

**Symptoms:**
- Pipeline takes hours
- Documents process slowly

**Diagnosis:**
```bash
# Check delays
grep DELAY .env

# Check model unloading
grep UNLOAD .env

# Monitor GPU usage
nvidia-smi -l 1
```

**Solutions:**
```bash
# Reduce delays (if RAM permits)
DELAY_BETWEEN_DOCS=0
DELAY_BETWEEN_BATCHES=0

# Less frequent unloading
UNLOAD_MODEL_EVERY=20

# Use faster model
OLLAMA_MODEL=mistral  # Fast and efficient

# Increase chunk size (fewer API calls)
MAX_CHUNK_SIZE=2000
```

---

## Validation Checklist

Use this to verify your configuration:

### Pre-Flight Check

```bash
# 1. Environment file exists
[ -f .env ] && echo "✓ .env exists" || echo "✗ .env missing"

# 2. Token is set
grep -q "PAPERLESS_TOKEN=.\+" .env && echo "✓ Token set" || echo "✗ Token missing"

# 3. Directories writable
[ -w /continuum ] && echo "✓ Base dir writable" || echo "✗ Base dir not writable"

# 4. Paperless reachable
curl -sf http://localhost:8040/api/ > /dev/null && echo "✓ Paperless OK" || echo "✗ Paperless unreachable"

# 5. Ollama reachable
curl -sf http://localhost:11434/api/tags > /dev/null && echo "✓ Ollama OK" || echo "✗ Ollama unreachable"

# 6. Python configuration test
cd scripts && python -m lib.config && echo "✓ Config valid" || echo "✗ Config invalid"
```

### Complete Validation Script

Save as `validate_config.sh`:

```bash
#!/bin/bash
set -e

echo "====================================="
echo "Configuration Validation"
echo "====================================="
echo

# Check .env file
if [ ! -f .env ]; then
    echo "✗ .env file not found"
    echo "  Run: cp .env.example .env"
    exit 1
fi
echo "✓ .env file exists"

# Check token
if ! grep -q "PAPERLESS_TOKEN=.\+" .env; then
    echo "✗ PAPERLESS_TOKEN not set"
    echo "  Add your token to .env file"
    exit 1
fi
echo "✓ PAPERLESS_TOKEN is set"

# Test Paperless
if ! curl -sf http://localhost:8040/api/ > /dev/null 2>&1; then
    echo "✗ Cannot connect to Paperless"
    exit 1
fi
echo "✓ Paperless reachable"

# Test Ollama
if ! curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✗ Cannot connect to Ollama"
    exit 1
fi
echo "✓ Ollama reachable"

# Python validation
cd scripts
if ! python -m lib.config > /dev/null 2>&1; then
    echo "✗ Configuration validation failed"
    exit 1
fi
echo "✓ Python configuration valid"

echo
echo "====================================="
echo "All checks passed!"
echo "====================================="
```

Run:
```bash
chmod +x validate_config.sh
./validate_config.sh
```

---

## Summary

### Essential Configuration

Minimum `.env` file:
```bash
PAPERLESS_TOKEN=your_token_here
```

Everything else has sensible defaults!

### Recommended Production Setup

```bash
# Services (local Docker)
PAPERLESS_URL=http://localhost:8040
PAPERLESS_TOKEN=secure_token
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Directories
CONTINUUM_BASE_DIR=/continuum

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=/var/log/continuum/app.log

# Memory (16GB RAM)
DELAY_BETWEEN_DOCS=10
DELAY_BETWEEN_BATCHES=30
UNLOAD_MODEL_EVERY=10
```

### Quick Reference

```bash
# Validate configuration
python -m lib.config

# Test Paperless client
python -m lib.paperless_client

# Test Ollama client
python -m lib.ollama_client

# Debug logging
LOG_LEVEL=DEBUG python your_script.py

# Production logging
LOG_FORMAT=json LOG_FILE=/var/log/app.log python your_script.py
```

---

## Additional Resources

- **Migration Guide:** `MIGRATION_GUIDE.md` - How to update scripts
- **Library Documentation:** `scripts/lib/README.md` - API reference
- **Quick Start:** `README.md` - Project overview

---

**Questions?** Run `python -m lib.config` to test your configuration!
