# The Continuum Report - Docker Deployment Guide

Complete guide for deploying The Continuum Report in production using Docker.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Initial Setup](#initial-setup)
3. [Configuration](#configuration)
4. [Deployment](#deployment)
5. [Verification](#verification)
6. [Monitoring](#monitoring)
7. [Scaling](#scaling)
8. [Disaster Recovery](#disaster-recovery)
9. [Updates & Maintenance](#updates--maintenance)

## Pre-Deployment Checklist

Before deploying to production:

- [ ] Server has 16GB+ RAM (8GB minimum)
- [ ] 100GB+ free disk space for data
- [ ] Docker Engine 20.10+ installed
- [ ] Docker Compose 2.0+ installed
- [ ] Network connectivity verified
- [ ] Firewall rules configured
- [ ] Backup strategy planned
- [ ] Monitoring setup planned

## Initial Setup

### 1. System Preparation

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 2. Clone Repository

```bash
# Clone the project
git clone <repository-url> /opt/continuum
cd /opt/continuum

# Set proper permissions
sudo chown -R $USER:$USER /opt/continuum
chmod 755 /opt/continuum
```

### 3. Directory Structure

```
/opt/continuum/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── .dockerignore
├── docker/
│   ├── README.md
│   ├── DEPLOYMENT.md
│   ├── .env.example
│   ├── scripts.sh
│   ├── Makefile
│   └── health-check.sh
├── scripts/
│   ├── lib/
│   │   ├── config.py
│   │   ├── paperless_client.py
│   │   ├── ollama_client.py
│   │   └── logging_config.py
│   └── continuum_pipeline.py
├── .env.example
└── requirements.txt
```

## Configuration

### 1. Environment Setup

```bash
# Copy example configuration
cp .env.example .env

# Edit with production values
nano .env
```

### 2. Required Environment Variables

**Paperless-ngx (REQUIRED):**

```env
PAPERLESS_TOKEN=<get-from-paperless-admin-panel>
PAPERLESS_SECRET_KEY=<generate-with-openssl>
PAPERLESS_URL=http://paperless:8000
```

Get Paperless token:

1. Access Paperless web interface: http://your-host:8040
2. Go to Settings -> Admin -> Authentification -> API Tokens
3. Create new token or copy existing
4. Add to .env as `PAPERLESS_TOKEN`

Generate secret key:

```bash
# Generate 32-byte random string
openssl rand -base64 32
```

**Ollama (OPTIONAL):**

```env
OLLAMA_MODEL=mistral
OLLAMA_URL=http://ollama:11434
OLLAMA_CONTEXT_SIZE=1024
```

### 3. Verify Configuration

```bash
# Check configuration syntax
docker-compose config > /dev/null && echo "Configuration valid" || echo "Configuration invalid"

# View final configuration
docker-compose config
```

## Deployment

### 1. Build Docker Image

```bash
# Build production image
cd /opt/continuum
docker-compose build

# Verify build
docker images | grep continuum
```

### 2. Start Services

```bash
# Start all services in background
docker-compose up -d

# Watch startup progress
docker-compose logs -f

# Verify containers are running
docker-compose ps
```

Expected output:

```
NAME           COMMAND    SERVICE    STATUS
continuum      python     continuum  Up (healthy)
paperless      python     paperless  Up
ollama         ./ollama   ollama     Up
```

### 3. Initial Paperless Setup (if using containerized)

```bash
# Create superuser
docker-compose exec paperless python manage.py createsuperuser

# Access web interface
# http://localhost:8040 (or your domain)
```

### 4. Load Ollama Model

```bash
# Pull the model (~2-4GB)
docker-compose exec ollama ollama pull mistral

# Verify model loaded
docker-compose exec ollama ollama list
```

## Verification

### 1. Health Checks

```bash
# Run comprehensive health check
bash docker/health-check.sh

# Or use make
make -f docker/Makefile test-all
```

### 2. Service Connectivity

```bash
# Test Paperless
docker-compose exec continuum python -c "
from lib import PaperlessClient
c = PaperlessClient()
docs = c.get_documents(limit=1)
print(f'✓ Paperless: {len(docs)} documents')
"

# Test Ollama
docker-compose exec continuum python -c "
from lib import OllamaClient
c = OllamaClient()
result = c.generate('Hello')
print(f'✓ Ollama: Model responding')
"
```

### 3. Data Verification

```bash
# Check entity database
docker-compose exec continuum ls -lh /continuum/entity_data/

# Verify volume persistence
docker volume ls | grep continuum

# Check disk usage
docker compose exec continuum du -sh /continuum/*
```

## Monitoring

### 1. Logging

**View application logs:**

```bash
# Real-time logs
docker-compose logs -f continuum

# Last N lines
docker-compose logs --tail=100 continuum

# Specific time range
docker-compose logs --since 2h continuum

# Export logs
docker-compose logs continuum > logs.txt
```

**Centralized logging setup:**

```bash
# Configure log rotation
cat > /etc/docker/daemon.json << EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3",
    "labels": "service=continuum"
  }
}
EOF

# Restart Docker
sudo systemctl restart docker
```

### 2. Resource Monitoring

```bash
# Monitor Docker resources
watch docker stats

# Monitor disk usage
du -sh /var/lib/docker/volumes/continuum*

# Monitor processes
docker-compose top continuum
```

### 3. Automated Monitoring

Set up with Prometheus and Grafana:

```bash
# Add monitoring service to docker-compose.yml
# (See prometheus-docker-compose.yml example)
```

## Scaling

### 1. Horizontal Scaling (Multiple Instances)

For production with high load:

```bash
# Scale continuum service (not recommended due to shared state)
docker-compose up -d --scale continuum=3

# Use load balancer in front
# nginx/traefik/HAProxy configuration needed
```

**Note:** Continuum shares entity state. Use separate instances only with proper queue system (Phase 2+).

### 2. Resource Scaling

Increase container resource limits:

```bash
# Modify docker-compose.yml
services:
  continuum:
    deploy:
      resources:
        limits:
          cpus: '8'
          memory: 16G
        reservations:
          cpus: '4'
          memory: 8G

  ollama:
    deploy:
      resources:
        limits:
          cpus: '16'
          memory: 32G
```

### 3. Ollama Model Scaling

Use multiple models or optimize:

```bash
# Keep multiple models loaded
docker-compose exec ollama ollama pull llama2
docker-compose exec ollama ollama pull neural-chat

# Or use quantized smaller models
docker-compose exec ollama ollama pull mistral:7b-q4
```

## Disaster Recovery

### 1. Backup Strategy

**Automated daily backups:**

```bash
#!/bin/bash
# /usr/local/bin/backup-continuum.sh

BACKUP_DIR="/backups/continuum"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p $BACKUP_DIR

# Backup volumes
docker run --rm \
  -v continuum-entity-data:/data \
  -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/entity-data-$TIMESTAMP.tar.gz -C /data .

# Backup database
docker-compose exec -T paperless python manage.py dumpdata > \
  $BACKUP_DIR/paperless-db-$TIMESTAMP.json

# Cleanup old backups (keep 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/entity-data-$TIMESTAMP.tar.gz"
```

Schedule with cron:

```bash
# Add to crontab
0 2 * * * /usr/local/bin/backup-continuum.sh
```

### 2. Restore from Backup

```bash
# Restore entity data
docker run --rm \
  -v continuum-entity-data:/data \
  -v /backups/continuum:/backup \
  alpine tar xzf /backup/entity-data-2025-12-24-020000.tar.gz -C /data

# Restore Paperless database
docker-compose exec -T paperless python manage.py loaddata \
  /backup/paperless-db-2025-12-24-020000.json

# Restart services
docker-compose restart
```

### 3. Disaster Recovery Plan

```
RTO (Recovery Time Objective): 1 hour
RPO (Recovery Point Objective): 1 day

Procedure:
1. Backup latest volumes to external storage
2. Restore from backup on new server
3. Verify service connectivity
4. Run health checks
5. Resume operations
```

## Updates & Maintenance

### 1. System Updates

```bash
# Update base images
docker-compose pull

# Rebuild application image
docker-compose build --no-cache

# Restart services (zero-downtime)
docker-compose up -d
```

### 2. Security Updates

```bash
# Check for vulnerabilities
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  anchore/grype continuum-report:latest

# Update Python dependencies
# Modify requirements.txt and rebuild
docker-compose build --no-cache continuum
```

### 3. Database Migrations (Paperless)

```bash
# Run migrations automatically on startup
docker-compose exec paperless python manage.py migrate

# Verify migration status
docker-compose exec paperless python manage.py showmigrations
```

### 4. Routine Maintenance

**Weekly:**

```bash
# Check logs for errors
docker-compose logs --tail=500 | grep ERROR

# Verify service health
bash docker/health-check.sh

# Check disk space
df -h /var/lib/docker
```

**Monthly:**

```bash
# Clean up unused Docker resources
docker system prune -a

# Update security patches
sudo apt-get update && sudo apt-get upgrade -y

# Backup complete system
/usr/local/bin/backup-continuum.sh
```

**Quarterly:**

```bash
# Test disaster recovery procedure
# 1. Backup current system
# 2. Simulate failure
# 3. Restore from backup
# 4. Verify functionality
```

## Production Checklist

Before going live:

- [ ] All environment variables configured
- [ ] Database initialized and verified
- [ ] Ollama model loaded and tested
- [ ] Health checks passing
- [ ] Backup strategy implemented
- [ ] Monitoring configured
- [ ] Log collection active
- [ ] Firewall rules applied
- [ ] SSL/TLS configured (if needed)
- [ ] Load balancer configured (if needed)
- [ ] Disaster recovery tested
- [ ] Team trained on operations
- [ ] Documentation updated

## Support & Troubleshooting

### Common Issues

**Containers not starting:**

```bash
# Check logs
docker-compose logs continuum

# Verify configuration
docker-compose config

# Rebuild image
docker-compose build --no-cache
```

**Out of memory:**

```bash
# Check memory usage
docker stats

# Reduce Ollama context size in .env
OLLAMA_CONTEXT_SIZE=512

# Increase server RAM or swap
sudo dd if=/dev/zero of=/swapfile bs=1G count=8
sudo mkswap /swapfile
sudo swapon /swapfile
```

**Paperless API errors:**

```bash
# Verify token
docker-compose exec paperless python manage.py list_tokens

# Test API
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8040/api/documents/?limit=1
```

## Related Files

- **README.md** - General Docker setup
- **docker-compose.yml** - Production configuration
- **docker-compose.dev.yml** - Development configuration
- **.dockerignore** - Build optimization
- **scripts.sh** - Convenience commands
- **Makefile** - Make targets
- **health-check.sh** - Health verification

## Next Steps

1. Deploy to staging environment first
2. Run health checks and verify functionality
3. Test backup and restore procedures
4. Monitor for 24-48 hours
5. Deploy to production
6. Set up ongoing monitoring and maintenance
