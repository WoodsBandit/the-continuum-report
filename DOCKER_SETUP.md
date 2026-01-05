# The Continuum Report - Docker Infrastructure Setup

Complete Docker infrastructure for The Continuum Report with production-ready configuration and developer-friendly tooling.

## Overview

This Docker setup provides:

- **Multi-stage optimized Dockerfile** - ~500MB production image with security best practices
- **Production docker-compose.yml** - Complete service orchestration with networking and volumes
- **Development docker-compose.dev.yml** - Live code reload and debug capabilities
- **Comprehensive documentation** - Guides for setup, deployment, and troubleshooting
- **Helper scripts** - Make, bash scripts, and health checks for easy operations

## Quick Start (5 minutes)

```bash
# 1. Navigate to project root
cd /continuum

# 2. Build the image
docker-compose build

# 3. Copy and configure environment
cp .env.example .env
nano .env
# Fill in: PAPERLESS_TOKEN, PAPERLESS_SECRET_KEY

# 4. Start services
docker-compose up -d

# 5. Verify
docker-compose ps
bash docker/health-check.sh
```

## Files Created

### Core Docker Files

```
Dockerfile                 (70 lines)
  └─ Multi-stage build for production
  └─ Python 3.11 slim base
  └─ Non-root security user
  └─ Health checks configured
  └─ Virtual environment optimization

docker-compose.yml         (196 lines)
  └─ Production service configuration
  └─ Continuum app service
  └─ Paperless-ngx integration
  └─ Ollama LLM service
  └─ Persistent volumes
  └─ Network configuration
  └─ Resource limits
  └─ Health checks

docker-compose.dev.yml     (230 lines)
  └─ Development overrides
  └─ Live code reload (bind mounts)
  └─ Interactive shell access
  └─ Debug logging enabled
  └─ Additional CLI service
  └─ Test runner service
  └─ Reduced resource limits

.dockerignore              (140 lines)
  └─ Build optimization
  └─ Excludes: git, tests, logs, data, docs
  └─ Keeps image small and clean
```

### Documentation

```
docker/README.md           (15KB)
  └─ Comprehensive Docker guide
  └─ Build and run instructions
  └─ Configuration reference
  └─ Troubleshooting guide
  └─ Architecture diagram
  └─ Backup procedures

docker/DEPLOYMENT.md       (12KB)
  └─ Production deployment guide
  └─ Pre-deployment checklist
  └─ Configuration setup
  └─ Health verification
  └─ Monitoring setup
  └─ Backup and recovery
  └─ Scaling strategies
  └─ Maintenance procedures

docker/QUICK_REFERENCE.md  (7KB)
  └─ Fast lookup reference
  └─ Common commands
  └─ Quick start guide
  └─ Troubleshooting quick tips

docker/.env.example        (5.5KB)
  └─ Environment template
  └─ All configuration options
  └─ Required and optional variables
  └─ Security guidelines
  └─ Example values
```

### Helper Tools

```
docker/scripts.sh          (11KB)
  └─ Bash helper functions
  └─ Build, start, stop commands
  └─ Logging functions
  └─ Service testing
  └─ Data management
  └─ Pipeline execution
  └─ Interactive CLI

docker/Makefile            (4.4KB)
  └─ Make targets for convenience
  └─ Build, start, stop, restart
  └─ Logging targets
  └─ Testing targets
  └─ Data management
  └─ Cleanup targets

docker/health-check.sh     (9.3KB)
  └─ Comprehensive health verification
  └─ Docker environment check
  └─ Container status verification
  └─ Network connectivity check
  └─ Service health validation
  └─ Configuration verification
  └─ Resource check
  └─ Summary reporting
```

## Architecture

```
┌──────────────────────────────────────────────────────┐
│          Docker Compose Network (172.25.0.0/16)      │
│                                                      │
│  ┌─────────────────┐  ┌──────────────────────┐    │
│  │ Continuum App   │  │   Paperless-ngx      │    │
│  │ (Python 3.11)   │──┤   (DMS + OCR)        │    │
│  │ Port: internal  │  │   Port: 8040         │    │
│  │ User: continuum │  │   DB: PostgreSQL     │    │
│  └────────┬────────┘  └──────────────────────┘    │
│           │                                        │
│           │                                        │
│  ┌────────┴────────────────────────┐              │
│  │        Shared Docker Network     │              │
│  │  (service-to-service via DNS)   │              │
│  └────────┬─────────────────────────┘              │
│           │                                        │
│  ┌────────┴──────────┐                            │
│  │  Ollama Service   │                            │
│  │  (LLM Inference)  │                            │
│  │  Port: 11434      │                            │
│  │  Models: /root/..  │                            │
│  └───────────────────┘                            │
│                                                   │
│  Persistent Volumes:                             │
│  • continuum-entity-data                         │
│  • continuum-reports                             │
│  • continuum-checkpoints                         │
│  • continuum-documents                           │
│  • paperless-data, paperless-media               │
│  • ollama-models                                 │
│                                                  │
└──────────────────────────────────────────────────┘
```

## Key Features

### Production Ready
- Multi-stage Docker build optimization
- Non-root security user
- Health checks and auto-restart
- Proper logging configuration
- Resource limits and reservations
- Network isolation

### Developer Friendly
- Live code reload with bind mounts
- Interactive shell access
- Debug logging support
- Helper scripts and Makefile
- Quick start guide
- Health check script

### Security Best Practices
- Non-root container user
- Minimal base image (Python 3.11-slim)
- Read-only code volumes (production)
- Environment variable secrets (not hardcoded)
- Network isolation
- Health monitoring

### Easy Operations
- One-command start: `docker-compose up -d`
- Comprehensive helper script: `./docker/scripts.sh`
- Make targets: `make start`, `make logs`, etc.
- Health checks: `bash docker/health-check.sh`
- Backup/restore automation

## Usage

### Build and Start

```bash
# Build production image
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f continuum
```

### Development

```bash
# Start with development overrides
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Interactive shell with code reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml run cli bash

# Changes to scripts/ are immediately visible
```

### Operations

```bash
# Use helper script
./docker/scripts.sh help              # Show all commands
./docker/scripts.sh build             # Build image
./docker/scripts.sh start             # Start services
./docker/scripts.sh logs-continuum    # View logs
./docker/scripts.sh shell             # Open shell
./docker/scripts.sh test-all          # Test all services
./docker/scripts.sh pipeline          # Run pipeline

# Or use Make
make build
make start
make logs
make shell
make test-all
```

### Verify Setup

```bash
# Run comprehensive health check
bash docker/health-check.sh

# Expected: All checks passed
```

## Configuration

### Required Environment Variables

```env
# Paperless API token (from admin panel)
PAPERLESS_TOKEN=your-token-here

# Random secret for Paperless
PAPERLESS_SECRET_KEY=$(openssl rand -base64 32)
```

### Optional Configuration

```env
# LLM Model
OLLAMA_MODEL=mistral

# Context window
OLLAMA_CONTEXT_SIZE=1024

# Processing limits
MAX_DOCUMENTS_TO_SEARCH=9999
MAX_DOCUMENTS_FOR_ENTITIES=9999
```

See `docker/.env.example` for all options.

## Services

### Continuum App
- **Image**: Custom built from Dockerfile
- **Language**: Python 3.11
- **Role**: Main AI pipeline and processing
- **User**: continuum (non-root)
- **Volumes**: Entity data, reports, checkpoints

### Paperless-ngx
- **Image**: ghcr.io/paperless-ngx/paperless-ngx:2.0.0
- **Language**: Python
- **Role**: Document management and OCR
- **Port**: 8040 (external)
- **Database**: PostgreSQL (included)

### Ollama
- **Image**: ollama/ollama:latest
- **Language**: Go/C++
- **Role**: Local LLM inference
- **Port**: 11434 (external)
- **Models**: Configurable (mistral default)

## Documentation

### For Quick Start
- Read: `docker/QUICK_REFERENCE.md` (7KB)
- Time: 5 minutes

### For Full Setup
- Read: `docker/README.md` (15KB)
- Time: 30 minutes

### For Deployment
- Read: `docker/DEPLOYMENT.md` (12KB)
- Time: 1 hour

### For Operations
- Use: `./docker/scripts.sh` or `make` commands
- Use: `bash docker/health-check.sh`

## Resource Requirements

### Minimum (Development)
- CPU: 2 cores
- RAM: 4GB
- Disk: 50GB free

### Recommended (Production)
- CPU: 4+ cores
- RAM: 16GB+
- Disk: 100GB+ free

Adjust in `docker-compose.yml`:

```yaml
services:
  continuum:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

## Testing and Verification

```bash
# All-in-one verification
bash docker/health-check.sh

# Test individual services
./docker/scripts.sh test-paperless
./docker/scripts.sh test-ollama

# List Ollama models
./docker/scripts.sh list-models

# Check entity count
./docker/scripts.sh entity-count

# View reports
./docker/scripts.sh reports
```

## Data Management

### Backup
```bash
# Automated in helper script
./docker/scripts.sh backup

# Manual
docker run --rm -v continuum-entity-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .
```

### Restore
```bash
# From backup file
./docker/scripts.sh restore backup-file.tar.gz
```

### Inspect Data
```bash
# Entity count
./docker/scripts.sh entity-count

# Generated reports
./docker/scripts.sh reports

# Processing checkpoints
./docker/scripts.sh checkpoints
```

## Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs continuum

# Rebuild without cache
docker-compose build --no-cache
```

**Paperless connection error:**
```bash
# Verify token
docker-compose exec paperless python manage.py list_tokens

# Check in .env
grep PAPERLESS_TOKEN .env
```

**Ollama model not found:**
```bash
# Pull model
docker-compose exec ollama ollama pull mistral

# Verify
docker-compose exec ollama ollama list
```

**Out of memory:**
```bash
# Reduce context size in .env
OLLAMA_CONTEXT_SIZE=512

# Or reduce processing batch
MAX_DOCUMENTS_TO_SEARCH=100
```

See `docker/README.md` troubleshooting section for more.

## Directory Structure

```
/continuum/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── .dockerignore
├── .env.example (root)
├── requirements.txt
│
├── docker/
│   ├── README.md
│   ├── DEPLOYMENT.md
│   ├── QUICK_REFERENCE.md
│   ├── .env.example
│   ├── scripts.sh
│   ├── Makefile
│   └── health-check.sh
│
├── scripts/
│   ├── lib/
│   │   ├── config.py
│   │   ├── paperless_client.py
│   │   ├── ollama_client.py
│   │   └── logging_config.py
│   └── continuum_pipeline.py
│   └── entity_discovery.py
│   └── [other scripts]
│
└── [other project directories]
```

## Next Steps

1. **Quick Start** (5 min):
   - Run: `docker-compose build`
   - Run: `docker-compose up -d`
   - Run: `bash docker/health-check.sh`

2. **Full Configuration** (15 min):
   - Read: `docker/README.md`
   - Set up: `.env` file
   - Run: verification commands

3. **Production Deployment** (1-2 hours):
   - Read: `docker/DEPLOYMENT.md`
   - Follow: pre-deployment checklist
   - Deploy and monitor

4. **Ongoing Operations**:
   - Use: `./docker/scripts.sh` for daily tasks
   - Use: `make` targets for convenience
   - Use: `health-check.sh` for verification

## Security Notes

1. Never commit `.env` file with actual secrets
2. Generate strong secrets: `openssl rand -base64 32`
3. Use environment variables for sensitive data
4. Container runs as non-root user
5. Keep Docker and images updated
6. Use read-only mounts for code (production)

## Support Resources

- **Docker Docs**: https://docs.docker.com/
- **Docker Compose Docs**: https://docs.docker.com/compose/
- **Python Docs**: https://docs.python.org/3.11/
- **Project README**: See main project README.md

## Related Files

- **Main README**: `README.md` - Project overview
- **Requirements**: `requirements.txt` - Python dependencies
- **Configuration**: `scripts/lib/config.py` - Settings loading
- **Paperless Client**: `scripts/lib/paperless_client.py` - API integration
- **Ollama Client**: `scripts/lib/ollama_client.py` - LLM integration

## Version Info

- Docker: 20.10+
- Docker Compose: 2.0+
- Python: 3.11
- Paperless-ngx: 2.0.0
- Ollama: latest

## License

The Continuum Report - Docker Infrastructure
See main project LICENSE file
