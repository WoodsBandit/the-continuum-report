# Docker Quick Reference

Fast lookup for common Docker commands for The Continuum Report.

## Quick Start

```bash
# 1. Build image
docker-compose build

# 2. Configure environment
cp .env.example .env
nano .env  # Edit with your values

# 3. Start services
docker-compose up -d

# 4. Verify
docker-compose ps
bash docker/health-check.sh
```

## Using Make (Recommended)

```bash
make build           # Build image
make start           # Start services
make stop            # Stop services
make logs            # View logs
make shell           # Open shell
make test-all        # Test all services
make pipeline        # Run pipeline
make backup          # Backup data
```

## Using Helper Script

```bash
./docker/scripts.sh build          # Build image
./docker/scripts.sh start          # Start services
./docker/scripts.sh logs           # View logs
./docker/scripts.sh shell          # Open shell
./docker/scripts.sh test-all       # Test connections
./docker/scripts.sh pipeline       # Run pipeline
```

## Common Tasks

### Viewing Logs

```bash
docker-compose logs -f continuum       # Follow Continuum logs
docker-compose logs --tail=50 continuum # Last 50 lines
docker-compose logs --since=1h continuum # Since 1 hour ago
```

### Accessing Container

```bash
docker-compose exec continuum sh         # Shell access
docker-compose exec continuum python     # Python shell
docker-compose run cli bash              # Dev interactive shell
```

### Running Scripts

```bash
# Pipeline
docker-compose exec continuum python -m scripts.continuum_pipeline

# Entity discovery
docker-compose exec continuum python -m scripts.entity_discovery

# Dossier generation
docker-compose exec continuum python -m scripts.generate_dossiers
```

### Testing Connections

```bash
# Test Paperless
docker-compose exec continuum python -c "
from lib import PaperlessClient
c = PaperlessClient()
print(f'Connected: {len(c.get_documents(limit=1))} docs')
"

# Test Ollama
docker-compose exec continuum python -c "
from lib import OllamaClient
c = OllamaClient()
result = c.generate('test')
print('Connected: Model working')
"
```

### Data Management

```bash
# Entity count
docker-compose exec continuum python -c "
import json
data = json.load(open('/continuum/entity_data/entity_database.json'))
print(f'Total entities: {len(data)}')
"

# View reports
docker-compose exec continuum ls -lh /continuum/reports/

# Backup data
docker run --rm -v continuum-entity-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .
```

### Maintenance

```bash
# Stop services
docker-compose down

# Stop and remove volumes (deletes data!)
docker-compose down -v

# Prune unused images
docker image prune -a

# View volumes
docker volume ls | grep continuum

# Restart services
docker-compose restart
```

## Environment Variables

```bash
# Paperless (required)
PAPERLESS_TOKEN=your-token
PAPERLESS_SECRET_KEY=$(openssl rand -base64 32)

# Ollama
OLLAMA_MODEL=mistral
OLLAMA_CONTEXT_SIZE=1024

# Processing
MAX_DOCUMENTS_TO_SEARCH=9999
```

## File Structure

```
continuum/
├── Dockerfile              # Multi-stage build
├── docker-compose.yml      # Production config
├── docker-compose.dev.yml  # Development overrides
├── .dockerignore          # Build exclusions
├── requirements.txt       # Python dependencies
└── docker/
    ├── README.md          # Full documentation
    ├── DEPLOYMENT.md      # Deployment guide
    ├── .env.example       # Environment template
    ├── scripts.sh         # Helper commands
    ├── Makefile           # Make targets
    └── health-check.sh    # Health verification
```

## Health Check

```bash
# Run comprehensive health check
bash docker/health-check.sh

# Expected output: All checks passed
```

## Docker Compose Commands

```bash
# Build
docker-compose build
docker-compose build --no-cache

# Manage services
docker-compose up -d              # Start background
docker-compose down               # Stop all
docker-compose restart            # Restart all
docker-compose ps                 # Status

# Inspect
docker-compose logs -f            # Follow logs
docker-compose config             # Show config
docker-compose top continuum      # View processes

# Access
docker-compose exec continuum sh  # Shell
docker-compose run cli bash       # Interactive shell

# Data
docker-compose exec continuum python -m scripts.continuum_pipeline
```

## Troubleshooting

### Check container status
```bash
docker-compose ps
```

### View error logs
```bash
docker-compose logs continuum | grep ERROR
```

### Test service connection
```bash
docker-compose exec continuum curl http://paperless:8000
```

### Verify Ollama model
```bash
docker-compose exec ollama ollama list
```

### Check disk usage
```bash
du -sh /var/lib/docker/volumes/continuum*
```

## Development

### Live code reload

```bash
# Start development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Run interactive shell
docker-compose -f docker-compose.yml -f docker-compose.dev.yml run cli bash

# Changes to scripts/ are reflected immediately
```

### Run tests

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml run tests
```

## Performance Tips

1. **Reduce context size** if running out of memory:
   ```env
   OLLAMA_CONTEXT_SIZE=512
   ```

2. **Limit document processing** for testing:
   ```env
   MAX_DOCUMENTS_TO_SEARCH=100
   ```

3. **Use BuildKit** for faster builds:
   ```bash
   DOCKER_BUILDKIT=1 docker-compose build
   ```

## Security Quick Tips

1. Never commit `.env` file
2. Generate strong secrets: `openssl rand -base64 32`
3. Use read-only volume mounts for production
4. Run container as non-root user (default)
5. Keep Docker updated

## Resource Limits

```yaml
# Production (default)
Continuum: 4 CPUs, 8GB RAM
Ollama: 8 CPUs, 16GB RAM

# Development (in dev config)
Continuum: 2 CPUs, 4GB RAM
Ollama: 2 CPUs, 4GB RAM
```

Adjust in `docker-compose.yml` based on hardware.

## Port Mappings

| Service | Port | Purpose |
|---------|------|---------|
| Paperless | 8040 | Web UI |
| Ollama | 11434 | API |
| Continuum | None | Internal only |

## Network

All services communicate via `continuum-network` Docker bridge network.

Access between services:
- `http://paperless:8000` (from continuum)
- `http://ollama:11434` (from continuum)

## Backup Strategy

```bash
# Quick backup
docker run --rm -v continuum-entity-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup-$(date +%Y%m%d).tar.gz -C /data .

# Quick restore
docker run --rm -v continuum-entity-data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/backup-YYYYMMDD.tar.gz -C /data
```

## Getting Help

1. Check logs: `docker-compose logs -f`
2. Run health check: `bash docker/health-check.sh`
3. Read README: `cat docker/README.md`
4. Read deployment guide: `cat docker/DEPLOYMENT.md`

## Key Files Reference

| File | Purpose |
|------|---------|
| Dockerfile | Container image definition |
| docker-compose.yml | Production services config |
| docker-compose.dev.yml | Development overrides |
| .dockerignore | Build optimization |
| .env | Environment variables (never commit) |
| .env.example | Environment template |
