# The Continuum Report - Docker Infrastructure

Complete Docker setup for The Continuum Report with Paperless-ngx and Ollama integration. Production-ready with development overrides.

## Overview

The Docker infrastructure consists of:

1. **Continuum App** - Main Python application with AI pipeline
2. **Paperless-ngx** - Document management and OCR
3. **Ollama** - Local LLM inference engine

All services communicate via a shared Docker network with persistent volumes for data.

## Quick Start

### Prerequisites

- Docker and Docker Compose 2.0+
- 8GB+ RAM (16GB+ recommended)
- GPU support optional but recommended for Ollama

### 1. Build the Image

```bash
# Build the continuum image
docker compose build

# Verify the build
docker images | grep continuum
```

### 2. Configuration

Create a `.env` file in the project root:

```bash
# Copy the example
cp .env.example .env

# Edit with your settings
nano .env  # or your favorite editor
```

**Required environment variables:**

```env
# Paperless-ngx - REQUIRED
PAPERLESS_TOKEN=your-api-token-here
PAPERLESS_SECRET_KEY=your-secret-key-here

# Ollama - Optional (defaults to mistral)
OLLAMA_MODEL=mistral
```

**Optional variables:**

```env
# URLs (if using external services)
PAPERLESS_URL=http://localhost:8040
OLLAMA_URL=http://localhost:11434

# Processing limits
MAX_DOCUMENTS_TO_SEARCH=9999
MAX_DOCUMENTS_FOR_ENTITIES=9999

# Timeouts
PAPERLESS_TIMEOUT=30
OLLAMA_TIMEOUT=600
```

### 3. Start Services

**Production mode** (with all services):

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f continuum

# Check service status
docker compose ps
```

**Development mode** (live code reload):

```bash
# Start with development overrides
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Start interactive CLI
docker compose -f docker-compose.yml -f docker-compose.dev.yml run cli bash

# Run tests
docker compose -f docker-compose.yml -f docker-compose.dev.yml run tests
```

### 4. Access Services

| Service | URL | Purpose |
|---------|-----|---------|
| Paperless Web UI | http://localhost:8040 | Document management |
| Paperless API | http://localhost:8040/api | REST API (port 8040) |
| Ollama API | http://localhost:11434 | LLM inference |

## Usage

### Running Specific Scripts

```bash
# Run continuum pipeline
docker compose exec continuum python -m scripts.continuum_pipeline

# Run entity discovery
docker compose exec continuum python -m scripts.entity_discovery

# Run dossier generation
docker compose exec continuum python -m scripts.generate_dossiers

# Interactive Python shell
docker compose exec continuum python -i -c "from lib import settings; print(settings.paperless_url)"
```

### Data Persistence

Data is stored in Docker volumes:

```bash
# View volume information
docker volume ls | grep continuum

# Inspect entity data
docker compose exec continuum ls -la /continuum/entity_data/

# View generated reports
docker compose exec continuum ls -la /continuum/reports/
```

### Accessing Container Shell

```bash
# Development environment with bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml run cli

# Production environment (limited shell)
docker compose exec continuum sh
```

## Configuration

### Environment Variables

**Paperless-ngx Integration:**

```env
PAPERLESS_URL=http://paperless:8000  # Internal service name
PAPERLESS_TOKEN=your-token           # From /admin/api/tokens/
PAPERLESS_TIMEOUT=30                 # Request timeout in seconds
```

**Ollama Integration:**

```env
OLLAMA_URL=http://ollama:11434       # Internal service name
OLLAMA_MODEL=mistral                 # Model name
OLLAMA_CONTEXT_SIZE=1024             # Token window
OLLAMA_TIMEOUT=600                   # Request timeout
```

**Directories:**

```env
CONTINUUM_BASE_DIR=/continuum        # Base data directory (in container)
```

**Processing:**

```env
MAX_DOCUMENTS_TO_SEARCH=9999          # No artificial limit
MAX_DOCUMENTS_FOR_ENTITIES=9999       # No artificial limit
WEBSITE_BASE_URL=https://thecontinuumreport.com
```

### Volume Mapping

Volumes are automatically created and managed by Docker Compose:

| Volume | Purpose | Mount Path |
|--------|---------|-----------|
| `continuum-entity-data` | Entity database | `/continuum/entity_data` |
| `continuum-reports` | Generated reports | `/continuum/reports` |
| `continuum-checkpoints` | Processing checkpoints | `/continuum/checkpoints` |
| `continuum-documents` | Document inbox | `/continuum/documents` |
| `paperless-data` | Paperless database | `/paperless/data` |
| `paperless-media` | Paperless uploads | `/paperless/media` |
| `ollama-models` | LLM models | `/root/.ollama` |

### Resource Limits

**Production settings** (in `docker-compose.yml`):

```yaml
Continuum:
  limits: 4 CPUs, 8GB RAM
  reservations: 2 CPUs, 4GB RAM

Ollama:
  limits: 8 CPUs, 16GB RAM
  reservations: 4 CPUs, 8GB RAM
```

**Development settings** (in `docker-compose.dev.yml`):

```yaml
Continuum:
  limits: 2 CPUs, 4GB RAM

Ollama:
  limits: 2 CPUs, 4GB RAM
```

Adjust based on your host hardware.

## Advanced Usage

### Using External Paperless/Ollama

If you have Paperless or Ollama running outside Docker:

```bash
# Modify .env
PAPERLESS_URL=http://localhost:8040
OLLAMA_URL=http://localhost:11434

# Start only the continuum service
docker compose up continuum
```

### Debugging

**View application logs:**

```bash
# Real-time logs
docker compose logs -f continuum

# Last 100 lines
docker compose logs --tail=100 continuum

# Specific timestamp
docker compose logs --since 2025-12-24T10:00:00 continuum
```

**Debug mode:**

```bash
# Set log level to DEBUG
docker compose exec continuum python -c "import logging; logging.getLogger().setLevel(logging.DEBUG)"

# Run script with verbose output
docker compose exec continuum python -m scripts.continuum_pipeline --verbose
```

**Inspect service network:**

```bash
# Check network connectivity
docker compose exec continuum curl http://paperless:8000/api

# Test Ollama
docker compose exec continuum curl http://ollama:11434/api/generate -d '{"model":"mistral","prompt":"test"}'
```

### Database/Checkpoint Recovery

```bash
# View checkpoints
docker compose exec continuum ls -la /continuum/checkpoints/

# List entities
docker compose exec continuum python -c "import json; data=json.load(open('/continuum/entity_data/entity_database.json')); print(f'Entities: {len(data)}')"

# Reset checkpoints (restart processing)
docker compose exec continuum rm /continuum/checkpoints/*.json
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose logs continuum

# Verify image exists
docker images | grep continuum

# Rebuild image
docker compose build --no-cache
```

### Paperless Token Issues

```bash
# Get token from running Paperless
docker compose exec paperless python -m paperless list_tokens

# Or access web UI
# http://localhost:8040 -> Settings -> Admin -> API Tokens
```

### Ollama Model Not Found

```bash
# Pull model (uses ~2-4GB)
docker compose exec ollama ollama pull mistral

# List available models
docker compose exec ollama ollama list

# Verify model download
docker compose exec ollama ls -lh /root/.ollama/models/manifests/registry.ollama.ai/library/
```

### Memory Issues

If Ollama crashes with out-of-memory:

```env
# Reduce context window
OLLAMA_CONTEXT_SIZE=512

# Or reduce max docs processed
MAX_DOCUMENTS_TO_SEARCH=100
```

### Network Connectivity

```bash
# Test Paperless connection
docker compose exec continuum python -c "from lib import PaperlessClient; c = PaperlessClient(); print(c.get_documents(limit=1))"

# Test Ollama connection
docker compose exec continuum python -c "from lib import OllamaClient; c = OllamaClient(); print(c.generate('test prompt'))"
```

## Security

### Production Recommendations

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use strong API tokens** - Generate from Paperless admin panel
3. **Change default secrets:**

   ```env
   # In .env
   PAPERLESS_SECRET_KEY=$(openssl rand -base64 32)
   ```

4. **Network isolation** - Use Docker networks (already configured)
5. **Non-root user** - Container runs as `continuum` user
6. **Read-only code volumes** - Scripts mounted read-only in production
7. **Health checks** - Automatic restart on failure

### Secrets Management

For production deployments:

```bash
# Use environment files
docker compose --env-file=/run/secrets/.env up

# Or Docker secrets (Swarm)
docker secret create paperless_token /path/to/token
```

Update `docker-compose.yml` to use secrets:

```yaml
services:
  continuum:
    environment:
      PAPERLESS_TOKEN_FILE: /run/secrets/paperless_token
```

## Performance Tuning

### Ollama Optimization

```env
# For slower hardware
OLLAMA_CONTEXT_SIZE=256
OLLAMA_TIMEOUT=1200  # 20 minutes

# For faster hardware
OLLAMA_CONTEXT_SIZE=2048
```

### Paperless Optimization

```env
PAPERLESS_TIMEOUT=60  # Increase if many documents
```

### Docker Compose Optimization

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker compose build

# Parallel processing
docker compose up -d --scale continuum=3  # Not recommended - use orchestration
```

## Maintenance

### Clean Up

```bash
# Stop all services
docker compose down

# Remove volumes (WARNING: deletes data)
docker compose down -v

# Clean up unused images
docker image prune -a

# Full cleanup (removes all containers/images/volumes)
docker compose down -v && docker system prune -a
```

### Backup

```bash
# Backup volumes
docker run --rm -v continuum-entity-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/entity-data.tar.gz -C /data .

# Restore volumes
docker run --rm -v continuum-entity-data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/entity-data.tar.gz -C /data
```

### Update Services

```bash
# Update Paperless
docker compose pull paperless
docker compose up -d paperless

# Update Ollama
docker compose pull ollama
docker compose up -d ollama

# Rebuild Continuum
docker compose build --no-cache continuum
docker compose up -d continuum
```

## Multi-Stage Build Details

The Dockerfile uses a multi-stage build:

1. **Builder Stage** - Installs dependencies in virtual environment
   - Only Python 3.11 slim base + build tools
   - Creates `/opt/venv` with all dependencies
   - No application code

2. **Runtime Stage** - Minimal production image
   - Copies only virtual environment from builder
   - Adds non-root `continuum` user
   - ~500MB final image size (vs ~1.5GB with single stage)
   - Security: reduced attack surface

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose Network                  │
│                   (172.25.0.0/16 bridge)                   │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │   Continuum App  │  │    Paperless     │              │
│  │ Port: (internal) │  │   Port: 8040     │              │
│  │ Language: Python │  │ Language: Python │              │
│  │ Status: Running  │  │ DB: PostgreSQL   │              │
│  │ User: continuum  │  │ Status: Running  │              │
│  └────────┬─────────┘  └────────┬─────────┘              │
│           │                     │                         │
│           └──────────┬──────────┘                         │
│                      │                                    │
│  ┌──────────────────┴──────────────────┐               │
│  │          Shared Docker Network      │               │
│  │  (service-to-service via hostname) │               │
│  └──────────────┬───────────────────┘               │
│                │                                    │
│  ┌─────────────┴────────────┐                      │
│  │       Ollama Service     │                      │
│  │      Port: 11434         │                      │
│  │    Language: Go/C        │                      │
│  │   Models: ~/root/.ollama │                      │
│  │    Status: Running       │                      │
│  └──────────────────────────┘                      │
│                                                   │
│         Persistent Volumes                       │
│  ├─ continuum-entity-data                        │
│  ├─ continuum-reports                            │
│  ├─ continuum-checkpoints                        │
│  ├─ continuum-documents                          │
│  ├─ paperless-data                               │
│  ├─ paperless-media                              │
│  └─ ollama-models                                │
│                                                  │
└──────────────────────────────────────────────────┘

        ┌─────────────────────────────────┐
        │    Host System (outside Docker) │
        │                                 │
        │ Ports exposed:                  │
        │ - 8040 (Paperless)              │
        │ - 11434 (Ollama)                │
        └─────────────────────────────────┘
```

## Related Files

- **Dockerfile** - Multi-stage build for production image
- **docker-compose.yml** - Production configuration
- **docker-compose.dev.yml** - Development overrides
- **.dockerignore** - Files to exclude from image
- **scripts/lib/config.py** - Configuration loading
- **requirements.txt** - Python dependencies

## Support

For issues or questions:

1. Check logs: `docker compose logs -f`
2. Verify environment: `docker compose config`
3. Test connectivity: See "Troubleshooting" section
4. Review application code: `/continuum/scripts/`

## License

The Continuum Report - Docker Infrastructure
See main project LICENSE file
