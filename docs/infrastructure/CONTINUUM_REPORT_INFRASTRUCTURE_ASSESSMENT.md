# The Continuum Report - Infrastructure & Deployment Architecture Assessment

**Assessment Date:** December 24, 2025
**Status:** Current Architecture - Homebrew to Production Roadmap
**Target:** Enterprise-Grade Infrastructure

---

## Executive Summary

The Continuum Report currently operates on a **local, file-based architecture** with manual automation patterns. This assessment identifies critical infrastructure gaps, scalability bottlenecks, and provides a comprehensive modernization roadmap to transition from local deployment to production-grade infrastructure.

### Key Findings:

| Category | Current State | Risk Level | Priority |
|----------|---------------|-----------|----------|
| **Scalability** | Single server, filesystem-based | HIGH | CRITICAL |
| **Automation** | Daemon-based, no orchestration | HIGH | CRITICAL |
| **CI/CD** | Manual/minimal automation | HIGH | CRITICAL |
| **Disaster Recovery** | No backup/failover strategy | CRITICAL | CRITICAL |
| **Infrastructure as Code** | None | HIGH | HIGH |
| **Containerization** | None | MEDIUM | HIGH |
| **Monitoring** | Minimal | HIGH | HIGH |
| **Data Pipeline** | Sequential, file-based | MEDIUM | HIGH |

---

## 1. CURRENT INFRASTRUCTURE ANALYSIS

### 1.1 Existing Architecture Map

```
┌─────────────────────────────────────────────────────────────────┐
│                     THE CONTINUUM REPORT                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Windows Workstation (WoodsDen) - LOCAL DEPLOYMENT            │
│  ├─ Development environment                                   │
│  ├─ Brief creation/editing                                    │
│  ├─ Static site generation                                    │
│  │                                                             │
│  ├─ Docker Services (Local)                                   │
│  │  ├─ Paperless-ngx (http://localhost:8040)                  │
│  │  │  └─ Document ingestion & OCR                           │
│  │  ├─ Ollama (http://localhost:11434)                        │
│  │  │  └─ LLM inference                                       │
│  │  └─ Website (http://localhost:8081)                        │
│  │                                                             │
│  ├─ brief_watcher.py daemon                                    │
│  │  └─ File monitoring & processing                           │
│  ├─ Storage: data/paperless/ (local filesystem)               │
│  └─ Static website files                                      │
│                                                                 │
│          ↓ HTTP/Static File Server                            │
│                                                                 │
│  Website (Static hosting)                                     │
│  └─ Published content                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Current Component Analysis

#### **Paperless-ngx (Document Management)**
- **Purpose**: Document ingestion, OCR, metadata extraction
- **Current Deployment**: Docker container on WoodsDen (http://localhost:8040)
- **Architecture Issues**:
  - Single instance (no HA)
  - Blocking I/O for document processing
  - Filesystem-based storage coupling
  - Manual scaling unavailable

#### **Ollama (LLM Inference)**
- **Purpose**: Local language model processing
- **Current Deployment**: Docker container on WoodsDen (http://localhost:11434)
- **Architecture Issues**:
  - GPU resource contention with Paperless
  - No request queuing
  - Hard to scale to multiple instances
  - No load balancing

#### **brief_watcher.py Daemon**
- **Purpose**: Monitor filesystem for documents, trigger processing
- **Current Approach**:
  ```
  File System Watcher → Processing Logic → JSON Output
  (Synchronous, blocking)
  ```
- **Architecture Issues**:
  - Single-threaded processing
  - No error recovery/retries
  - No distributed processing
  - Tight coupling to filesystem
  - No external observability

#### **Storage Architecture**
- **Current**: Filesystem-based JSON files
- **Location**: Local storage (data/paperless/ within project folder)
- **Issues**:
  - No ACID transactions
  - Difficult concurrent access management
  - Versioning challenges
  - Backup/recovery complexity
  - No query optimization

#### **Website Deployment**
- **Current**: Static file deployment
- **Process**: Manual or script-based generation
- **Issues**:
  - Manual build process
  - No CI/CD pipeline
  - No version control integration
  - Manual content promotion

---

## 2. SCALABILITY ASSESSMENT

### 2.1 Current Limitations

#### **Document Processing Throughput**

```
Current Flow:
1. Document arrives (Paperless-ngx)
2. brief_watcher.py detects change
3. Sequential processing (blocking)
4. JSON written to filesystem
5. Website regenerated

Bottleneck: brief_watcher.py synchronous processing
Current Throughput: ~10-20 documents/hour (estimated)
Latency: 30-120 seconds per document
```

**Scaling Limitations:**
- Single daemon cannot process documents in parallel
- Paperless-ngx and Ollama compete for system resources
- No request queuing means documents are lost if processor is busy
- No dead-letter handling for failures

#### **Storage Architecture Limitations**

| Aspect | Current | Limitation |
|--------|---------|-----------|
| **Concurrency** | File locking | Race conditions possible |
| **Query Performance** | Full file reads | Linear scan for any query |
| **Transactions** | None | Data corruption on crash |
| **Versioning** | Manual snapshots | No rollback capability |
| **Backup** | Manual copies | No point-in-time recovery |
| **Search** | String matching | No full-text search |
| **Relationships** | Denormalized | Data duplication |

#### **Infrastructure Scaling Issues**

**Vertical Scaling (more CPU/RAM):**
- Limited by single server hardware
- Resource contention between services
- No independent scaling of components

**Horizontal Scaling:**
- No load balancing
- No service discovery
- Shared filesystem becomes bottleneck
- Database (filesystem JSON) cannot scale horizontally

### 2.2 Throughput Analysis

**Current State:**
```
Paperless-ngx OCR: 2-5 docs/min (limited by CPU)
Ollama Inference: 1-10 requests/min (limited by GPU)
brief_watcher.py: Sequential (effectively 1 doc/min due to blocking)
Local storage throughput: Limited by disk I/O (SSD recommended)
```

**Realistic current capacity:**
- 600-1,200 documents/day
- Peaks cause queuing/drops
- No graceful degradation

### 2.3 Storage Scalability Roadmap

**Current (Filesystem JSON):**
```
├─ documents/
│  └─ doc_001.json (grows unbounded)
├─ briefs/
│  └─ brief_001.json (linear scaling)
└─ metadata/
   └─ index.json (full read required for queries)
```

**Issues:**
- Linear growth = linear performance degradation
- Search requires loading entire dataset
- No indexing or optimization
- Concurrent writes conflict

---

## 3. AUTOMATION & CI/CD ASSESSMENT

### 3.1 Current Automation Analysis

#### **brief_watcher.py Daemon Assessment**

```python
# Current Pattern (Simplified)
while True:
    files = watch_directory()  # Blocks waiting for changes
    for file in files:
        process_document(file)  # Sequential, blocking
        generate_brief(file)
        update_json_storage()
    time.sleep(5)  # Polling-based (inefficient)
```

**Problems:**
1. **No Orchestration**: Pure file monitoring, no external coordination
2. **No Error Handling**: Single failure cascades
3. **No Observability**: No logging, metrics, or tracing
4. **No Recovery**: Daemon death = stopped processing
5. **No Scaling**: Can't run multiple instances
6. **No Queuing**: No backpressure handling
7. **Tight Coupling**: Direct filesystem dependency

**Maturity Assessment:**
- **Current Maturity Level**: 1/5 (Basic Automation)
- **What's Missing**:
  - CI/CD pipeline
  - Infrastructure as Code
  - Automated testing
  - Deployment automation
  - Monitoring & alerting
  - Version control integration

#### **Document Processing Pipeline**

```
Current Pipeline:
┌─────────────────┐
│ Document Input  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Paperless (OCR) │ ← Blocking, no parallelism
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ brief_watcher   │ ← No queue, synchronous
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ JSON Storage    │ ← Single point of failure
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Website Gen     │ ← Manual trigger
└─────────────────┘
```

**Issues:**
- No intermediate queues
- No branching/conditional logic
- No failure handling
- No monitoring checkpoints

### 3.2 CI/CD Maturity Level

| Aspect | Current | Industry Standard |
|--------|---------|------------------|
| **Automation** | 20% | 95%+ |
| **Version Control** | Unknown | 100% |
| **Testing** | Manual | 90%+ automated |
| **Deployment** | Manual | Fully automated |
| **Monitoring** | None | Comprehensive |
| **Security Scanning** | None | 100% |
| **Documentation** | Unknown | Complete |

---

## 4. CONTAINERIZATION OPPORTUNITIES

### 4.1 Services for Containerization

#### **Tier 1: MUST Containerize (High Impact)**

##### **1. Ollama (LLM Inference)**

**Benefits of Containerization:**
- Resource isolation from Paperless
- GPU passthrough for inference
- Horizontal scaling to multiple instances
- Version pinning for model consistency
- Easy A/B testing of model versions

**Dockerfile Strategy:**
```dockerfile
FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh

# Expose API
EXPOSE 11434

# Volume for models
VOLUME ["/root/.ollama"]

# Health check
HEALTHCHECK --interval=10s --timeout=5s \
  CMD curl -f http://localhost:11434/api/tags || exit 1

ENTRYPOINT ["ollama", "serve"]
```

**Deployment Architecture:**
```
┌─────────────────────────────────────┐
│     Ollama Inference Service        │
├─────────────────────────────────────┤
│  ┌─────────────────────────────────┐│
│  │ ollama-1 (GPU-0)                ││
│  │ Container + GPU binding         ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │ ollama-2 (GPU-1)                ││
│  │ Container + GPU binding         ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │ ollama-svc (Load Balancer)      ││
│  │ Round-robin across instances    ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

##### **2. Paperless-ngx (Document Management)**

**Benefits:**
- Independent versioning
- Easy updates without affecting other services
- Persistent volume for documents
- Environment configuration externalization
- Simplified scaling

**Deployment:**
```yaml
# Container with:
- Volume mount for documents
- Environment for configuration
- Health checks
- Restart policies
```

##### **3. brief_watcher.py (Processing Worker)**

**Containerization Strategy:**

Current:
```
Daemon running on host
├─ Watches filesystem directly
├─ Monolithic binary
└─ Single instance
```

Recommended:
```
┌──────────────────────────────────────┐
│        Processing Workers            │
├──────────────────────────────────────┤
│  ┌────────────────────────────────┐  │
│  │ worker-1 (Python container)    │  │
│  │ Connects to message queue      │  │
│  │ Pulls jobs, processes, reports │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │ worker-2 (Python container)    │  │
│  │ Connects to message queue      │  │
│  │ Pulls jobs, processes, reports │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │ worker-N (horizontal scaling)  │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

**Dockerfile for Worker:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY src/ .

# Configuration via environment
ENV QUEUE_URL=redis://queue:6379
ENV PAPERLESS_URL=http://paperless:8000
ENV OLLAMA_URL=http://ollama:11434

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
  CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Start worker
CMD ["python", "-m", "worker.main"]
```

#### **Tier 2: SHOULD Containerize (Medium-High Impact)**

##### **4. Redis (Message Queue)**

**Benefits:**
- Reliable job queuing
- Horizontal scaling readiness
- Atomic operations
- Persistence options
- Pub/Sub for events

##### **5. Website Build Pipeline**

**Current:** Manual on workstation
**Containerized:** Reproducible build environment

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY . .

# Install dependencies and build
RUN npm ci && npm run build

# Output static files to volume
VOLUME ["/output"]

ENTRYPOINT ["sh", "-c", "npm run build && cp -r dist/* /output/"]
```

#### **Tier 3: CONSIDER Containerizing (Medium Impact)**

##### **6. PostgreSQL (Future database)**

```dockerfile
# Use official PostgreSQL image
FROM postgres:15-alpine

# Custom initialization scripts
COPY init-scripts/ /docker-entrypoint-initdb.d/

VOLUME ["/var/lib/postgresql/data"]

EXPOSE 5432
```

##### **7. Monitoring Stack**

- Prometheus (metrics collection)
- Grafana (visualization)
- Loki (log aggregation)
- Promtail (log shipping)

### 4.2 Container Registry Strategy

**Recommended Setup:**

```
┌─────────────────────────────────────┐
│     Container Registry Options      │
├─────────────────────────────────────┤
│ Docker Hub (public images)          │
│ GitHub Container Registry (private) │
│ Self-hosted (Harbor, Nexus)         │
└─────────────────────────────────────┘

Recommended: GitHub Container Registry
├─ Free private registries
├─ Integrated with GitHub Actions
├─ Automatic vulnerability scanning
└─ No external dependencies
```

### 4.3 Container Orchestration Path

**Phase 1: Docker Compose (Development/Testing)**
```yaml
version: '3.8'
services:
  paperless:
    image: paperlessngx/paperless-ngx:latest
    volumes:
      - documents:/var/documents
    ports:
      - "8000:8000"

  ollama:
    image: ollama:latest
    volumes:
      - ollama-models:/root/.ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  worker:
    image: continuum-report/worker:latest
    depends_on:
      - redis
      - paperless
      - ollama
    environment:
      QUEUE_URL: redis://redis:6379
      PAPERLESS_URL: http://paperless:8000
      OLLAMA_URL: http://ollama:11434
    deploy:
      replicas: 3
```

**Phase 2: Kubernetes (Production)**
```yaml
---
# Ollama Deployment with GPU support
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: continuum-report
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      containers:
      - name: ollama
        image: ghcr.io/continuum-report/ollama:v1.0
        ports:
        - containerPort: 11434
        resources:
          requests:
            nvidia.com/gpu: "1"
          limits:
            nvidia.com/gpu: "1"
        volumeMounts:
        - name: ollama-models
          mountPath: /root/.ollama
        livenessProbe:
          httpGet:
            path: /api/tags
            port: 11434
          initialDelaySeconds: 30
          periodSeconds: 10
      volumes:
      - name: ollama-models
        persistentVolumeClaim:
          claimName: ollama-pvc
---
# Redis Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: continuum-report
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-data
          mountPath: /data
      volumes:
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-pvc
---
# Worker Deployment (horizontal scaling)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: continuum-worker
  namespace: continuum-report
spec:
  replicas: 5
  selector:
    matchLabels:
      app: continuum-worker
  template:
    metadata:
      labels:
        app: continuum-worker
    spec:
      containers:
      - name: worker
        image: ghcr.io/continuum-report/worker:v1.0
        env:
        - name: QUEUE_URL
          value: "redis://redis:6379"
        - name: PAPERLESS_URL
          value: "http://paperless:8000"
        - name: OLLAMA_URL
          value: "http://ollama:11434"
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
```

---

## 5. WEBSITE DEPLOYMENT STRATEGY

### 5.1 Current State Assessment

**Current Deployment:**
```
Manual Build → Static Files → HTTP Server
- No version history
- No rollback capability
- No staging environment
- No automated testing
```

### 5.2 Modern Static Site Architecture

#### **Recommended Tech Stack:**

| Component | Tool | Rationale |
|-----------|------|-----------|
| **Site Generator** | Hugo / Next.js / 11ty | Fast builds, great for blogs/docs |
| **Content Repo** | GitHub | Version control, PR reviews |
| **CI/CD** | GitHub Actions | Free, integrated, powerful |
| **Hosting** | Vercel / Netlify / GitHub Pages | CDN included, auto deployments |
| **CDN** | CloudFlare / Bunny CDN | Edge caching, DDoS protection |
| **DNS** | Cloudflare DNS | Fast, free security features |

#### **Deployment Architecture:**

```
┌─────────────────────────────────────────────────┐
│         Content Repository (GitHub)             │
│  ├─ Markdown content                            │
│  ├─ Page templates                              │
│  ├─ Configuration                               │
│  └─ GitHub Actions workflows                    │
└─────────────┬───────────────────────────────────┘
              │
              │ Push to main branch
              ↓
┌─────────────────────────────────────────────────┐
│        GitHub Actions CI/CD Pipeline            │
├─────────────────────────────────────────────────┤
│  1. Checkout code                               │
│  2. Install dependencies                        │
│  3. Run tests                                   │
│  4. Build static site                           │
│  5. Run lighthouse (performance)                │
│  6. Run security scans                          │
│  7. Deploy to Vercel                            │
│  8. Run smoke tests                             │
│  9. Update monitoring/analytics                 │
└─────────────┬───────────────────────────────────┘
              │
              │ Deployment artifacts
              ↓
┌─────────────────────────────────────────────────┐
│         Global CDN (Vercel/Netlify)             │
│  ├─ Edge caching                                │
│  ├─ Image optimization                          │
│  ├─ Automatic compression                       │
│  ├─ Branch previews                             │
│  └─ A/B testing support                         │
└─────────────┬───────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────┐
│          Global Edge CDN (Cloudflare)           │
│  ├─ DDoS protection                             │
│  ├─ WAF rules                                   │
│  ├─ Additional caching layer                    │
│  └─ Analytics                                   │
└─────────────┬───────────────────────────────────┘
              │
              ↓
         End Users
```

### 5.3 GitHub Actions Workflow

**File: `.github/workflows/build-deploy.yml`**

```yaml
name: Build & Deploy Website

on:
  push:
    branches:
      - main
    paths:
      - 'website/**'
      - '.github/workflows/build-deploy.yml'
  pull_request:
    branches:
      - main
    paths:
      - 'website/**'

env:
  NODE_VERSION: '18'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci
        working-directory: ./website

      - name: Lint
        run: npm run lint
        working-directory: ./website

      - name: Test
        run: npm run test
        working-directory: ./website

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci
        working-directory: ./website

      - name: Build
        run: npm run build
        working-directory: ./website

      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          path: ./website/dist
          format: spdx-json

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: website-build
          path: ./website/dist
          retention-days: 30

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          configPath: './website/lighthouserc.json'
          uploadArtifacts: true

  security-scan:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: './website'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

      - name: NPM audit
        run: npm audit --production
        working-directory: ./website
        continue-on-error: true

  deploy:
    needs: [build, security-scan]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: website-build
          path: ./dist

      - name: Deploy to Vercel
        uses: vercel/action@v4
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          github-deployment: true

      - name: Smoke tests
        run: |
          for url in \
            "https://continuum-report.com/" \
            "https://continuum-report.com/about" \
            "https://continuum-report.com/briefs"
          do
            status=$(curl -s -o /dev/null -w "%{http_code}" $url)
            if [ $status -ne 200 ]; then
              echo "Health check failed for $url: $status"
              exit 1
            fi
          done

      - name: Notify Slack (optional)
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Website deployment ${{ job.status }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### 5.4 Content Generation Integration

**Integrate with Backend Pipeline:**

```yaml
# Enhanced Data Pipeline
┌──────────────────────────────┐
│   Document Processing        │
│   (Containerized workers)    │
└─────────────┬────────────────┘
              │
              ↓
┌──────────────────────────────┐
│   Generate Brief Metadata    │
│   (JSON + Frontmatter)       │
└─────────────┬────────────────┘
              │
              ↓
┌──────────────────────────────┐
│   Commit to GitHub (Website) │
│   via GitHub API             │
└─────────────┬────────────────┘
              │
              ↓
┌──────────────────────────────┐
│   GitHub Actions CI/CD       │
│   Automatically builds site  │
└─────────────┬────────────────┘
              │
              ↓
┌──────────────────────────────┐
│   Deploy to CDN              │
│   (Vercel/Netlify)           │
└──────────────────────────────┘
```

---

## 6. DATA PIPELINE ARCHITECTURE IMPROVEMENTS

### 6.1 Current Pipeline Analysis

```
Current State:
┌────────────┐    ┌──────────────┐    ┌──────────┐    ┌────────┐
│ Paperless  │───→│ brief_watcher│───→│ JSON fs  │───→│Website │
│ (OCR)      │    │ (daemon)     │    │(storage) │    │ output │
└────────────┘    └──────────────┘    └──────────┘    └────────┘

Issues:
├─ Synchronous (blocking)
├─ No error recovery
├─ No parallelism
├─ Single point of failure
├─ No observability
└─ Tight coupling
```

### 6.2 Recommended Message-Driven Architecture

#### **Using Redis for Queuing:**

```python
# Producer (Paperless webhook/listener)
import redis
import json
from datetime import datetime

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

def on_document_added(document_id: str, filename: str):
    """Called when Paperless adds a document"""

    # Create job
    job = {
        'id': document_id,
        'filename': filename,
        'timestamp': datetime.utcnow().isoformat(),
        'status': 'pending',
        'attempts': 0,
        'max_attempts': 3,
    }

    # Push to queue
    redis_client.rpush('document-queue', json.dumps(job))

    # Emit event for monitoring
    redis_client.publish('document-events', json.dumps({
        'event': 'document_queued',
        'document_id': document_id,
        'timestamp': job['timestamp'],
    }))

# Consumer (brief_watcher worker - parallelizable)
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DocumentWorker:
    def __init__(self, redis_url: str, ollama_url: str, paperless_url: str):
        self.redis = redis.Redis.from_url(redis_url, decode_responses=True)
        self.ollama_url = ollama_url
        self.paperless_url = paperless_url

    def process_job(self, job: Dict[str, Any]) -> bool:
        """Process a single document job"""

        job_id = job['id']

        try:
            logger.info(f"Processing document {job_id}")

            # Step 1: Fetch document from Paperless
            document = self._fetch_document(job_id)

            # Step 2: Extract text (OCR already done by Paperless)
            text = document['content']

            # Step 3: Generate brief using Ollama
            brief = self._generate_brief(text)

            # Step 4: Store result
            self._store_brief(job_id, brief, document)

            # Step 5: Update status
            self._update_status(job_id, 'completed')

            logger.info(f"Document {job_id} processed successfully")
            return True

        except Exception as e:
            logger.error(f"Error processing {job_id}: {str(e)}")

            # Retry logic
            if job.get('attempts', 0) < job.get('max_attempts', 3):
                job['attempts'] += 1
                self.redis.rpush('document-queue', json.dumps(job))
                logger.info(f"Requeued document {job_id} (attempt {job['attempts']})")
                return True
            else:
                # Max attempts exceeded
                self._update_status(job_id, 'failed', error=str(e))
                self.redis.rpush('dead-letter-queue', json.dumps(job))
                return False

    def run(self):
        """Main worker loop"""
        logger.info("Starting document worker")

        while True:
            try:
                # Block waiting for next job (5 second timeout)
                result = self.redis.brpop('document-queue', timeout=5)

                if result:
                    queue_name, job_json = result
                    job = json.loads(job_json)
                    self.process_job(job)

            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
                time.sleep(1)

    def _fetch_document(self, doc_id: str) -> Dict:
        """Fetch from Paperless API"""
        response = requests.get(
            f"{self.paperless_url}/api/documents/{doc_id}/",
            headers={'Authorization': f'Token {os.getenv("PAPERLESS_TOKEN")}'}
        )
        response.raise_for_status()
        return response.json()

    def _generate_brief(self, text: str) -> str:
        """Generate brief using Ollama"""
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                'model': 'mistral',  # or configured model
                'prompt': f"Summarize this document concisely:\n\n{text[:2000]}",
                'stream': False,
            }
        )
        response.raise_for_status()
        return response.json()['response']

    def _store_brief(self, doc_id: str, brief: str, metadata: Dict):
        """Store brief in database"""
        brief_record = {
            'id': doc_id,
            'brief': brief,
            'source': metadata['filename'],
            'created_at': datetime.utcnow().isoformat(),
            'document_count': 1,
        }

        # Store in Redis (temporary) and database (permanent)
        self.redis.hset('briefs', doc_id, json.dumps(brief_record))

        # Also store in database for durability
        self._store_in_database(brief_record)

    def _update_status(self, doc_id: str, status: str, error: str = None):
        """Update job status"""
        status_record = {
            'status': status,
            'updated_at': datetime.utcnow().isoformat(),
            'error': error,
        }
        self.redis.hset('job-status', doc_id, json.dumps(status_record))
```

#### **Redis-Based Architecture:**

```
┌────────────────────────────────────────────────────────┐
│              Message-Driven Architecture              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Producer (Paperless Listener)                       │
│  └─ Detects new documents                            │
│     └─ Enqueues to Redis queue                       │
│                                                        │
│  ┌─────────────────────────────────────────────────┐ │
│  │           Redis Message Broker                  │ │
│  ├─────────────────────────────────────────────────┤ │
│  │ Queues:                                         │ │
│  │  - document-queue (main work queue)             │ │
│  │  - dead-letter-queue (failed jobs)              │ │
│  │ Caches:                                         │ │
│  │  - briefs (recent results)                      │ │
│  │  - job-status (processing status)               │ │
│  │ Pub/Sub:                                        │ │
│  │  - document-events (monitoring)                 │ │
│  └─────────────────────────────────────────────────┘ │
│                      ↑                                │
│     ┌────────────────┼────────────────┐             │
│     │                │                │             │
│  Worker-1        Worker-2         Worker-N         │
│  (Parallel      (Parallel        (Horizontal      │
│   processing)    processing)      scaling)        │
│                                                    │
│  Each worker:                                     │
│  ├─ Pulls jobs from queue (FIFO)                 │
│  ├─ Processes independently                      │
│  ├─ Reports status to Redis                      │
│  ├─ Publishes completion events                  │
│  └─ Retries on failure                           │
│                                                    │
└────────────────────────────────────────────────────────┘
```

### 6.3 Database Migration Path

#### **Current State:**
```
JSON files on filesystem
├─ No schema
├─ No indexing
├─ No relationships
├─ No transactions
└─ Manual backups
```

#### **Recommended Migration (Progressive):**

**Phase 1: PostgreSQL with JSON Support (Short-term)**
```sql
-- Hybrid approach: relational + JSON
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    document_id VARCHAR(255) UNIQUE NOT NULL,
    filename VARCHAR(512) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB NOT NULL,  -- Flexible schema
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    indexed_at TIMESTAMP,
    processing_status VARCHAR(50) DEFAULT 'pending'
);

CREATE INDEX idx_document_id ON documents(document_id);
CREATE INDEX idx_created_at ON documents(created_at);
CREATE INDEX idx_status ON documents(processing_status);
CREATE INDEX idx_metadata ON documents USING GIN (metadata);

CREATE TABLE briefs (
    id SERIAL PRIMARY KEY,
    document_id VARCHAR(255) REFERENCES documents(document_id),
    brief_text TEXT NOT NULL,
    summary JSONB,  -- Flexible summary structure
    generated_at TIMESTAMP DEFAULT NOW(),
    model_version VARCHAR(50),
    confidence FLOAT,
    UNIQUE(document_id)
);

CREATE INDEX idx_brief_document ON briefs(document_id);
CREATE INDEX idx_brief_generated ON briefs(generated_at);
```

**Phase 2: Normalized Schema (Medium-term)**
```sql
-- Fully relational model
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    external_id VARCHAR(255) UNIQUE NOT NULL,
    filename VARCHAR(512) NOT NULL,
    file_path VARCHAR(1024),
    file_size_bytes BIGINT,
    content_type VARCHAR(100),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    processing_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    error_message TEXT
);

CREATE TABLE document_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    raw_text TEXT NOT NULL,
    extracted_text TEXT,
    language VARCHAR(10),
    word_count INT,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE briefs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    brief_text TEXT NOT NULL,
    word_count INT,
    generation_model VARCHAR(100),
    generation_prompt_tokens INT,
    generation_completion_tokens INT,
    confidence_score FLOAT,
    generated_at TIMESTAMP NOT NULL,
    UNIQUE(document_id)
);

CREATE TABLE brief_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brief_id UUID NOT NULL REFERENCES briefs(id) ON DELETE CASCADE,
    key VARCHAR(100) NOT NULL,
    value TEXT,
    created_at TIMESTAMP NOT NULL,
    UNIQUE(brief_id, key)
);

-- Indexes for performance
CREATE INDEX idx_documents_external_id ON documents(external_id);
CREATE INDEX idx_documents_status ON documents(processing_status);
CREATE INDEX idx_documents_created ON documents(created_at DESC);
CREATE INDEX idx_briefs_document ON briefs(document_id);
CREATE INDEX idx_briefs_generated ON briefs(generated_at DESC);
```

**Phase 3: Time-Series Data (Long-term)**
```sql
-- TimescaleDB extension for analytics
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE processing_metrics (
    time TIMESTAMP NOT NULL,
    document_id VARCHAR(255),
    processing_duration_ms INT,
    ollama_duration_ms INT,
    storage_duration_ms INT,
    status VARCHAR(50),
    error VARCHAR(500)
);

SELECT create_hypertable('processing_metrics', 'time', if_not_exists => TRUE);
CREATE INDEX idx_metrics_document ON processing_metrics(document_id, time DESC);
CREATE INDEX idx_metrics_status ON processing_metrics(status, time DESC);

-- Materialized view for daily metrics
CREATE MATERIALIZED VIEW daily_processing_stats AS
SELECT
    DATE(time) as date,
    COUNT(*) as total_documents,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as successful,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed,
    AVG(processing_duration_ms) as avg_duration_ms,
    MAX(processing_duration_ms) as max_duration_ms,
    MIN(processing_duration_ms) as min_duration_ms
FROM processing_metrics
GROUP BY DATE(time);
```

**Migration Path (Progressive, Zero-Downtime):**

```
Step 1: Run PostgreSQL alongside JSON files
├─ Write to both systems
├─ Verify consistency
└─ Maintain backward compatibility

Step 2: Read-primarily from PostgreSQL
├─ Keep JSON files for reference
├─ Gradual cutover of queries
└─ Validate results

Step 3: Full migration
├─ Stop writing to JSON
├─ Archive JSON files
├─ PostgreSQL becomes source of truth
└─ Implement backup strategy

Step 4: Decommission JSON
├─ Retain backups for 90 days
├─ Close on JSON file references
└─ Celebrate success
```

---

## 7. RECOMMENDED CI/CD PIPELINE ARCHITECTURE

### 7.1 Complete CI/CD System

```
┌──────────────────────────────────────────────────────────┐
│                  GitHub Repository                       │
│  ├─ Source code (Python, website)                       │
│  ├─ Configuration (env, docker-compose, k8s)           │
│  ├─ Tests (unit, integration, e2e)                     │
│  └─ CI/CD workflows (GitHub Actions)                   │
└──────────────────┬───────────────────────────────────────┘
                   │
     ┌─────────────┼─────────────┐
     │             │             │
     ↓             ↓             ↓
┌─────────┐  ┌─────────┐  ┌─────────────┐
│ Backend │  │ Website │  │ Infrastructure
│ Pipeline│  │ Pipeline│  │ Pipeline
└────┬────┘  └────┬────┘  └─────┬───────┘
     │             │             │
     ↓             ↓             ↓
┌─────────────────────────────────────────┐
│         Build Artifacts                 │
├─────────────────────────────────────────┤
│ ├─ Docker images (GHCR)                │
│ ├─ Static website build                │
│ └─ IaC artifacts                       │
└────────────────┬────────────────────────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
     ↓           ↓           ↓
┌────────┐ ┌────────┐ ┌──────────┐
│  Dev   │ │ Staging│ │Production│
│  Env   │ │  Env   │ │   Env    │
└────────┘ └────────┘ └──────────┘
```

### 7.2 Multi-Stage CI/CD Workflow

**File: `.github/workflows/complete-pipeline.yml`**

```yaml
name: Complete CI/CD Pipeline

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
      - develop

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: continuum-report

jobs:
  # ============================================================
  # Stage 1: Code Quality & Security
  # ============================================================

  code-quality:
    name: Code Quality Checks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for better analysis

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff pylint mypy pytest pytest-cov

      - name: Ruff lint
        run: ruff check src/

      - name: Type checking (mypy)
        run: mypy src/ --ignore-missing-imports

      - name: Code coverage
        run: pytest --cov=src --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  security-scan:
    name: Security Scanning
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy filesystem scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-fs.sarif'

      - name: Run dependency check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          path: '.'
          format: 'SARIF'
          args: >
            --enable-retired

      - name: Upload scan results
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-fs.sarif'

  # ============================================================
  # Stage 2: Build Artifacts
  # ============================================================

  build-backend:
    name: Build Backend Docker Image
    needs: [code-quality, security-scan]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ github.repository }}/worker
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-

      - name: Build and push Docker image
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run Trivy vulnerability scan on image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ steps.meta.outputs.tags }}
          format: 'sarif'
          output: 'trivy-image.sarif'

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        if: always()
        with:
          sarif_file: 'trivy-image.sarif'

      - name: SBOM generation
        uses: anchore/sbom-action@v0
        with:
          image: ${{ steps.meta.outputs.tags }}
          format: cyclonedx-json
          output-file: sbom.json

      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.json

  build-website:
    name: Build Website
    needs: code-quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: 'website/package-lock.json'

      - name: Install dependencies
        run: npm ci
        working-directory: website

      - name: Run tests
        run: npm run test
        working-directory: website

      - name: Build
        run: npm run build
        working-directory: website

      - name: Run Lighthouse
        uses: treosh/lighthouse-ci-action@v10
        with:
          configPath: './website/lighthouserc.json'
          uploadArtifacts: true
          temporaryPublicStorage: true

      - name: Upload build
        uses: actions/upload-artifact@v3
        with:
          name: website-build
          path: website/dist
          retention-days: 30

  # ============================================================
  # Stage 3: Integration Testing
  # ============================================================

  integration-tests:
    name: Integration Tests
    needs: build-backend
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: continuum_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/continuum_test
          REDIS_URL: redis://localhost:6379
          OLLAMA_URL: http://ollama:11434
          PAPERLESS_URL: http://paperless:8000
        run: pytest tests/integration/ -v

  # ============================================================
  # Stage 4: Deploy to Staging
  # ============================================================

  deploy-staging:
    name: Deploy to Staging
    needs: [build-backend, build-website, integration-tests]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.continuum-report.com
    steps:
      - uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v3

      - name: Deploy to staging cluster
        run: |
          # Deploy via kubectl or helm
          kubectl set image deployment/continuum-worker \
            worker=${{ needs.build-backend.outputs.image-tag }} \
            --namespace=continuum-staging \
            --record

      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/continuum-worker \
            --namespace=continuum-staging \
            --timeout=5m

      - name: Run smoke tests
        run: |
          ./scripts/smoke-tests.sh https://staging.continuum-report.com

  # ============================================================
  # Stage 5: Deploy to Production
  # ============================================================

  deploy-production:
    name: Deploy to Production
    needs: [build-backend, build-website, deploy-staging]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://continuum-report.com
    concurrency:
      group: production-deployment
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@v4

      - name: Request approval
        id: approval
        uses: actions/github-script@v7
        with:
          script: |
            console.log('Production deployment requires manual approval');
            console.log('Check environment protection rules');

      - name: Download artifacts
        uses: actions/download-artifact@v3

      - name: Prepare deployment
        run: |
          # Create deployment manifest with specific versions
          cat > deployment-prod.yaml <<EOF
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: continuum-worker-prod
            namespace: continuum-report
          spec:
            replicas: 5
            selector:
              matchLabels:
                app: continuum-worker
                environment: production
            template:
              metadata:
                labels:
                  app: continuum-worker
                  environment: production
                  version: ${{ github.sha }}
              spec:
                containers:
                - name: worker
                  image: ${{ needs.build-backend.outputs.image-tag }}
                  resources:
                    requests:
                      cpu: "500m"
                      memory: "512Mi"
                    limits:
                      cpu: "1000m"
                      memory: "1Gi"
                  livenessProbe:
                    httpGet:
                      path: /health
                      port: 8080
                    initialDelaySeconds: 30
                    periodSeconds: 10
          EOF

      - name: Canary deployment (10% traffic)
        run: |
          kubectl patch service continuum-worker \
            --namespace=continuum-report \
            -p '{"spec":{"trafficPolicy":{"canary":{"weight":10}}}}'

      - name: Monitor canary metrics
        run: |
          # Monitor error rate, latency for 5 minutes
          ./scripts/monitor-canary.sh 5

      - name: Check canary health
        run: |
          error_rate=$(./scripts/get-error-rate.sh)
          if (( $(echo "$error_rate > 0.5" | bc -l) )); then
            echo "Canary error rate too high: $error_rate"
            exit 1
          fi

      - name: Full production deployment
        run: |
          # Gradually shift traffic: 10% → 25% → 50% → 100%
          for weight in 25 50 100; do
            kubectl patch service continuum-worker \
              --namespace=continuum-report \
              -p "{\"spec\":{\"trafficPolicy\":{\"canary\":{\"weight\":$weight}}}}"
            sleep 120  # Monitor for 2 minutes at each step
          done

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/continuum-worker-prod \
            --namespace=continuum-report \
            --timeout=10m

      - name: Run production smoke tests
        run: |
          ./scripts/smoke-tests.sh https://continuum-report.com

      - name: Update deployment documentation
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          cat > DEPLOYMENT_LOG.md <<EOF
          # Deployment Log

          **Date**: $(date -u)
          **Commit**: ${{ github.sha }}
          **Author**: ${{ github.actor }}
          **Message**: ${{ github.event.head_commit.message }}

          **Deployed Services**:
          - continuum-worker: ${{ needs.build-backend.outputs.image-tag }}
          - Website: ${{ github.sha }}

          **Deployment Strategy**: Canary (10% → 100%)
          **Status**: Successful

          EOF
          git add DEPLOYMENT_LOG.md
          git commit -m "Deployment log: $(date -u)" || true
          git push

      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            Production Deployment ${{ job.status }}
            Commit: ${{ github.sha }}
            Author: ${{ github.actor }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK_DEPLOYMENTS }}

  # ============================================================
  # Post-Deployment
  # ============================================================

  post-deploy:
    name: Post-Deployment Tasks
    needs: deploy-production
    runs-on: ubuntu-latest
    if: always()
    steps:
      - uses: actions/checkout@v4

      - name: Update deployment record
        run: |
          # Record deployment in database
          curl -X POST https://api.continuum-report.com/deployments \
            -H "Authorization: Bearer ${{ secrets.API_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{
              "commit": "${{ github.sha }}",
              "timestamp": "'$(date -u -Iseconds)'",
              "status": "${{ job.status }}",
              "deployer": "${{ github.actor }}"
            }'

      - name: Generate deployment report
        run: |
          # Create deployment metrics report
          ./scripts/generate-deployment-report.sh > deployment-report.json

      - name: Archive deployment artifacts
        uses: actions/upload-artifact@v3
        with:
          name: deployment-artifacts
          path: |
            deployment-report.json
            DEPLOYMENT_LOG.md
          retention-days: 90
```

---

## 8. MONITORING, LOGGING & OBSERVABILITY

### 8.1 Observability Stack

```
┌──────────────────────────────────────────────────────────┐
│              Observability Architecture                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Metrics Layer (Prometheus)                             │
│  ├─ Application metrics                                 │
│  ├─ Infrastructure metrics                              │
│  └─ Business metrics                                    │
│        ↓                                                │
│  Aggregation (Prometheus Remote Storage)               │
│        ↓                                                │
│  Visualization (Grafana)                               │
│  └─ Dashboards, alerts                                 │
│                                                          │
│  Logs Layer (Loki)                                      │
│  ├─ Application logs                                    │
│  ├─ Containerized log shipping (Promtail)             │
│  └─ Structured logging                                 │
│        ↓                                                │
│  Aggregation (Loki)                                    │
│        ↓                                                │
│  Query (LogQL in Grafana)                              │
│                                                          │
│  Traces Layer (Jaeger/Tempo)                           │
│  ├─ Distributed tracing                                │
│  ├─ Instrument code with OpenTelemetry                │
│  └─ Correlate logs/metrics/traces                      │
│        ↓                                                │
│  Aggregation (Tempo)                                   │
│        ↓                                                │
│  Visualization (Grafana)                               │
│                                                          │
│  Alerting Layer (Alertmanager)                         │
│  ├─ Threshold-based alerts                             │
│  ├─ Anomaly detection                                  │
│  └─ Escalation policies                                │
│        ↓                                                │
│  Routing (PagerDuty/Slack)                             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 8.2 Key Metrics to Track

```
Application Metrics:
├─ Document Processing
│  ├─ docs_processed_total (counter)
│  ├─ documents_processing_duration_seconds (histogram)
│  ├─ documents_failed_total (counter)
│  ├─ documents_pending (gauge)
│  └─ ollama_inference_duration_seconds (histogram)
│
├─ Queue Health
│  ├─ queue_length (gauge)
│  ├─ queue_processing_rate (gauge)
│  ├─ queue_wait_time_seconds (histogram)
│  └─ dead_letter_queue_length (gauge)
│
├─ API Performance
│  ├─ http_request_duration_seconds (histogram)
│  ├─ http_requests_total (counter)
│  └─ http_errors_total (counter by endpoint)
│
└─ Resource Usage
   ├─ gpu_utilization (gauge)
   ├─ memory_usage_bytes (gauge)
   ├─ cpu_usage_percent (gauge)
   └─ storage_usage_bytes (gauge)

Infrastructure Metrics:
├─ Kubernetes
│  ├─ pod_restarts_total
│  ├─ pod_cpu_usage_cores
│  ├─ pod_memory_usage_bytes
│  └─ pvc_used_bytes
│
├─ Database
│  ├─ db_connections_active (gauge)
│  ├─ db_query_duration_seconds (histogram)
│  ├─ db_errors_total (counter)
│  └─ db_replication_lag_seconds (gauge)
│
└─ Network
   ├─ network_bytes_sent_total
   ├─ network_bytes_received_total
   └─ network_errors_total
```

### 8.3 Prometheus Configuration

**File: `monitoring/prometheus.yml`**

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'continuum-report'
    environment: 'production'

# Alertmanager for handling alerts
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

# Load alert rules
rule_files:
  - '/etc/prometheus/rules/*.yml'

scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Worker service metrics
  - job_name: 'continuum-worker'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - continuum-report
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: continuum-worker
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace

  # Ollama metrics
  - job_name: 'ollama'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - continuum-report
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: ollama
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod

  # PostgreSQL metrics
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  # Redis metrics
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  # Node metrics
  - job_name: 'node'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - source_labels: [__address__]
        regex: '([^:]+)(?::\d+)?'
        replacement: '${1}:9100'
        target_label: __address__
      - source_labels: [__meta_kubernetes_node_name]
        target_label: node
```

### 8.4 Alert Rules

**File: `monitoring/rules/continuum.yml`**

```yaml
groups:
  - name: continuum_application
    interval: 30s
    rules:
      # High error rate in document processing
      - alert: HighDocumentProcessingErrorRate
        expr: |
          (
            rate(documents_failed_total[5m]) /
            rate(documents_processed_total[5m])
          ) > 0.05
        for: 5m
        labels:
          severity: critical
          component: document-processing
        annotations:
          summary: "High error rate in document processing"
          description: "Document processing error rate is {{ $value | humanizePercentage }} (threshold: 5%)"

      # Queue backlog growing
      - alert: QueueBacklogGrowing
        expr: |
          rate(queue_length[5m]) > 0
          AND queue_length > 100
        for: 10m
        labels:
          severity: warning
          component: queue
        annotations:
          summary: "Queue backlog is growing"
          description: "Queue has {{ $value }} pending items and is growing"

      # Dead letter queue has messages
      - alert: DeadLetterQueueNotEmpty
        expr: dead_letter_queue_length > 0
        for: 15m
        labels:
          severity: warning
          component: queue
        annotations:
          summary: "Dead letter queue has messages"
          description: "{{ $value }} failed jobs in dead letter queue"

      # Processing latency too high
      - alert: HighProcessingLatency
        expr: |
          histogram_quantile(0.95, documents_processing_duration_seconds) > 60
        for: 5m
        labels:
          severity: warning
          component: document-processing
        annotations:
          summary: "Document processing latency is high"
          description: "P95 latency is {{ $value }}s (threshold: 60s)"

      # GPU utilization high
      - alert: HighGPUUtilization
        expr: gpu_utilization > 0.9
        for: 10m
        labels:
          severity: warning
          component: infrastructure
        annotations:
          summary: "GPU utilization is high"
          description: "GPU utilization is {{ $value | humanizePercentage }}"

      # Pod restart storm
      - alert: PodRestartStorm
        expr: |
          rate(pod_restarts_total{pod=~"continuum-.*"}[1h]) > 0.1
        labels:
          severity: critical
          component: kubernetes
        annotations:
          summary: "Pod is restarting frequently"
          description: "Pod {{ $labels.pod }} restarting {{ $value }} times/hour"

      # Database connection pool exhaustion
      - alert: DBConnectionPoolExhaustion
        expr: |
          db_connections_active / 20 > 0.9
        labels:
          severity: critical
          component: database
        annotations:
          summary: "Database connection pool nearly exhausted"
          description: "{{ $value | humanizePercentage }} of connections in use"

      # Storage running out
      - alert: StorageAlmostFull
        expr: |
          (1 - pvc_available_bytes / pvc_total_bytes) > 0.85
        labels:
          severity: warning
          component: storage
        annotations:
          summary: "Storage is {{ $value | humanizePercentage }} full"
          description: "PVC {{ $labels.pvc }} is {{ $value | humanizePercentage }} full"

  - name: continuum_slos
    interval: 60s
    rules:
      # SLO: 99.9% uptime
      - alert: SLOViolation_Availability
        expr: |
          (1 - increase(http_errors_total[6h]) / increase(http_requests_total[6h])) < 0.999
        for: 15m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "Availability SLO violated"
          description: "Availability over last 6h is {{ $value | humanizePercentage }} (target: 99.9%)"

      # SLO: P95 latency < 500ms
      - alert: SLOViolation_Latency
        expr: |
          histogram_quantile(0.95, http_request_duration_seconds) > 0.5
        for: 15m
        labels:
          severity: warning
          slo: latency
        annotations:
          summary: "Latency SLO violated"
          description: "P95 latency is {{ $value }}s (target: 0.5s)"
```

---

## 9. DISASTER RECOVERY & HIGH AVAILABILITY

### 9.1 Backup Strategy

```
Backup Architecture:
┌──────────────────────────────────────┐
│   Production Data Sources            │
├──────────────────────────────────────┤
│ ├─ PostgreSQL database               │
│ ├─ Redis (state)                     │
│ ├─ Document storage                  │
│ └─ Ollama models                     │
└────────┬─────────────────────────────┘
         │
    ┌────┴────┬─────────────┬──────────────┐
    │          │             │              │
    ↓          ↓             ↓              ↓
 Hourly    Daily       Weekly        Monthly
  Snap      Full       Archive       Archive
  (Local)   (Local)    (S3)          (Glacier)
    │          │         │              │
    ├──────────┼─────────┼──────────────┤
    │
    ↓
Cross-region replication (3-region strategy)
```

**Backup Implementation:**

```bash
#!/bin/bash
# backup-continuum.sh

set -e

BACKUP_DIR="/var/backups/continuum"
S3_BUCKET="continuum-report-backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# PostgreSQL
pg_dump \
  --host=$DB_HOST \
  --username=$DB_USER \
  --password=$DB_PASSWORD \
  continuum_db | \
  gzip > $BACKUP_DIR/db_${TIMESTAMP}.sql.gz

# Redis
redis-cli --rdb $BACKUP_DIR/redis_${TIMESTAMP}.rdb

# Document storage
tar -czf \
  $BACKUP_DIR/documents_${TIMESTAMP}.tar.gz \
  /var/continuum/documents

# Ollama models (less frequently, they're large)
if [[ $(date +%H) == "02" ]]; then  # 2 AM UTC
  tar -czf \
    $BACKUP_DIR/ollama_models_${TIMESTAMP}.tar.gz \
    /root/.ollama
fi

# Upload to S3 (keeping 7 days locally, 30 days in S3)
aws s3 sync $BACKUP_DIR \
  s3://$S3_BUCKET/$(date +%Y/%m/%d)/ \
  --sse AES256

# Clean up old local backups (keep 7 days)
find $BACKUP_DIR -mtime +7 -delete

# Verify backups
aws s3 ls s3://$S3_BUCKET/$(date +%Y/%m/%d)/
```

### 9.2 RTO/RPO Targets

| Component | RTO | RPO | Strategy |
|-----------|-----|-----|----------|
| **Database** | 15 min | 1 hour | Continuous replication + hourly snapshots |
| **Document Storage** | 1 hour | 6 hours | Daily snapshots + S3 backup |
| **Redis (Queue)** | 5 min | Minimal | Replicated cluster, data reloadable |
| **Ollama Models** | 2 hours | 24 hours | S3 backup, not time-critical |
| **Full System** | 4 hours | 1 hour | Multi-region Kubernetes cluster |

### 9.3 High Availability Architecture

```
Production HA Setup:
┌─────────────────────────────────────────┐
│       Kubernetes Cluster (HA)           │
├─────────────────────────────────────────┤
│                                         │
│  Node Pool 1 (Zone A)                  │
│  ├─ continuum-worker-a-1               │
│  ├─ continuum-worker-a-2               │
│  ├─ continuum-worker-a-3               │
│  └─ postgres-replica-a                 │
│                                         │
│  Node Pool 2 (Zone B)                  │
│  ├─ continuum-worker-b-1               │
│  ├─ continuum-worker-b-2               │
│  ├─ continuum-worker-b-3               │
│  └─ postgres-primary-b                 │
│                                         │
│  Node Pool 3 (Zone C)                  │
│  ├─ continuum-worker-c-1               │
│  ├─ continuum-worker-c-2               │
│  ├─ continuum-worker-c-3               │
│  └─ postgres-replica-c                 │
│                                         │
│  Distributed Components:               │
│  ├─ Redis Cluster (3 nodes)            │
│  ├─ Ollama (3 instances, GPU pool)     │
│  └─ Paperless (2 replicas)             │
│                                         │
└─────────────────────────────────────────┘
         ↑                       ↑
    Zone A                   Zone B
   Region 1               Region 1
         ├──── Primary ────┤
         └──── Replica ────┘
              + Continuous replication
```

---

## 10. SECURITY HARDENING

### 10.1 Container Security

```dockerfile
# Hardened Dockerfile
FROM python:3.11-slim

# Security: Non-root user
RUN groupadd -r continuum && useradd -r -g continuum continuum

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=continuum:continuum src/ .

# Security: Remove setuid/setgid bits
RUN find / -xdev -perm /6000 -delete || true

# Security: Read-only root filesystem (where possible)
RUN chmod 755 /app

# Security: Use non-root user
USER continuum:continuum

# Security: Health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run application
EXPOSE 8080
CMD ["python", "-m", "continuum.worker"]
```

### 10.2 Kubernetes Security Policies

```yaml
---
# Pod Security Policy
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: continuum-restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'MustRunAs'
    seLinuxOptions:
      level: 's0:c123,c456'
  fsGroup:
    rule: 'MustRunAs'
    fsGroupOptions:
      ranges:
        - min: 1
          max: 65535
  readOnlyRootFilesystem: true
  hostNetwork: false
  hostIPC: false
  hostPID: false

---
# Network Policy - Deny all by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: continuum-default-deny
  namespace: continuum-report
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Network Policy - Allow internal traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: continuum-allow-internal
  namespace: continuum-report
spec:
  podSelector:
    matchLabels:
      app: continuum-worker
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: continuum-report
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: continuum-report
      ports:
        - protocol: TCP
          port: 5432
        - protocol: TCP
          port: 6379
        - protocol: TCP
          port: 11434
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: TCP
          port: 53
        - protocol: UDP
          port: 53

---
# RBAC - Least privilege
apiVersion: v1
kind: ServiceAccount
metadata:
  name: continuum-worker
  namespace: continuum-report

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: continuum-worker
  namespace: continuum-report
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get"]
    resourceNames: ["continuum-secrets"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: continuum-worker
  namespace: continuum-report
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: continuum-worker
subjects:
  - kind: ServiceAccount
    name: continuum-worker
    namespace: continuum-report

---
# Secrets Management with External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: continuum-secrets
  namespace: continuum-report
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: continuum-db-secret
  namespace: continuum-report
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: continuum-secrets
    kind: SecretStore
  target:
    name: continuum-db-credentials
    creationPolicy: Owner
  data:
    - secretKey: password
      remoteRef:
        key: continuum/db/password
    - secretKey: username
      remoteRef:
        key: continuum/db/username
```

---

## 11. INFRASTRUCTURE AS CODE ROADMAP

### 11.1 Current State → IaC Strategy

```
Current:
├─ Manual configuration
├─ Undocumented setup
├─ No version control
└─ Difficult to replicate

Target:
├─ Everything in Git
├─ Automated provisioning
├─ Self-documenting
├─ Multi-environment parity
└─ Disaster recovery ready
```

### 11.2 Recommended IaC Stack

```
Infrastructure Layers:

Layer 1: Cloud Provisioning (Terraform)
├─ Kubernetes cluster
├─ Node pools with auto-scaling
├─ Storage (block, object, database)
├─ Networking (VPC, subnets, security groups)
└─ Load balancers and DNS

Layer 2: Kubernetes Manifests (Helm)
├─ Application deployments
├─ Services and ingress
├─ ConfigMaps and Secrets
├─ RBAC and network policies
└─ Persistent volumes

Layer 3: Application Configuration (Kustomize overlays)
├─ Environment-specific configs
├─ Development, staging, production
├─ Secrets management
└─ Resource limits

Layer 4: GitOps Sync (ArgoCD)
├─ Automatic deployment
├─ Git as source of truth
├─ Drift detection
└─ Automated rollbacks
```

### 11.3 Terraform Structure

```
terraform/
├─ environments/
│  ├─ dev/
│  │  └─ terraform.tfvars
│  ├─ staging/
│  │  └─ terraform.tfvars
│  └─ prod/
│     └─ terraform.tfvars
├─ modules/
│  ├─ kubernetes/
│  │  ├─ main.tf
│  │  ├─ variables.tf
│  │  └─ outputs.tf
│  ├─ rds/
│  ├─ elasticache/
│  ├─ networking/
│  └─ security/
├─ main.tf
├─ variables.tf
├─ outputs.tf
└─ backend.tf  (remote state)
```

**File: `terraform/main.tf`**

```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }

  # Remote state with locking
  backend "s3" {
    bucket         = "continuum-report-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "continuum-report"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Kubernetes cluster
module "kubernetes" {
  source = "./modules/kubernetes"

  cluster_name    = "continuum-${var.environment}"
  cluster_version = "1.28"

  node_pools = {
    general = {
      desired_size = 3
      min_size     = 3
      max_size     = 10
      machine_type = "t3.large"
    }
    gpu = {
      desired_size = 1
      min_size     = 1
      max_size     = 5
      machine_type = "g4dn.xlarge"
    }
  }

  tags = {
    Service = "container-orchestration"
  }
}

# Database
module "rds" {
  source = "./modules/rds"

  engine                   = "postgres"
  engine_version           = "15"
  allocated_storage        = var.db_allocated_storage
  instance_class           = var.db_instance_class
  multi_az                 = var.environment == "prod" ? true : false
  backup_retention_days    = var.environment == "prod" ? 30 : 7

  depends_on = [module.kubernetes]
}

# Cache layer
module "redis" {
  source = "./modules/elasticache"

  engine                = "redis"
  engine_version        = "7.0"
  node_type             = "cache.r7g.large"
  num_cache_nodes       = var.environment == "prod" ? 3 : 1
  automatic_failover    = var.environment == "prod" ? true : false
  multi_az_enabled      = var.environment == "prod" ? true : false

  depends_on = [module.kubernetes]
}

# Deploy applications via Helm
resource "helm_release" "continuum" {
  name            = "continuum-report"
  repository      = "https://charts.continuum-report.dev"
  chart           = "continuum-report"
  version         = var.chart_version
  namespace       = "continuum-report"
  create_namespace = true

  values = [
    file("${path.module}/helm-values/${var.environment}.yaml")
  ]

  set {
    name  = "image.tag"
    value = var.app_version
  }

  depends_on = [
    module.kubernetes,
    module.rds,
    module.redis
  ]
}

# Monitoring stack
resource "helm_release" "prometheus" {
  name      = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart     = "kube-prometheus-stack"
  version   = "52.0.0"
  namespace = "monitoring"
  create_namespace = true
}
```

---

## 12. MODERNIZATION ROADMAP (Phase-by-Phase)

### 12.1 Phase 1: Foundation (Weeks 1-4)

**Objective:** Establish modern infrastructure basics

**Deliverables:**
- [x] Git repository with IaC
- [x] Docker images for all services
- [x] Docker Compose for local development
- [x] Basic CI/CD pipeline (linting, testing)
- [x] Monitoring stack (Prometheus, Grafana)

**Resources:** 1-2 engineers
**Success Metrics:**
- All code in Git
- Local dev environment reproducible
- Tests running in CI
- Basic metrics visible

**Key Tasks:**
1. Create project repository structure
2. Containerize all services
3. Write Dockerfile and docker-compose.yml
4. Create GitHub Actions workflow (test, lint, build)
5. Set up Prometheus + Grafana
6. Document local setup

### 12.2 Phase 2: Containerization & Orchestration (Weeks 5-12)

**Objective:** Move from host-based to container-based deployment

**Deliverables:**
- [x] Kubernetes cluster (dev/staging)
- [x] Helm charts for all services
- [x] Persistent storage configuration
- [x] Load balancing
- [x] Container registry (GitHub Container Registry)

**Resources:** 2 engineers
**Success Metrics:**
- Services running in Kubernetes
- Deployments automated via CI/CD
- Storage persisted correctly
- Multi-pod deployments working

**Key Tasks:**
1. Set up local Kubernetes (minikube)
2. Create Helm charts
3. Deploy to staging Kubernetes cluster
4. Configure persistent volumes
5. Set up service discovery
6. Implement health checks

### 12.3 Phase 3: Message Queue & Async Processing (Weeks 13-20)

**Objective:** Replace synchronous daemon with message-driven architecture

**Deliverables:**
- [x] Redis message queue
- [x] Multiple worker instances
- [x] Dead letter queue handling
- [x] Retry logic and error handling
- [x] Queue monitoring

**Resources:** 2 engineers
**Success Metrics:**
- Documents processing in parallel
- 5-10x throughput increase
- Error recovery working
- Queue metrics visible

**Key Tasks:**
1. Design queue-based architecture
2. Implement Redis queue client
3. Refactor brief_watcher as worker
4. Implement retries and DLQ
5. Add queue metrics
6. Load testing

### 12.4 Phase 4: Database Migration (Weeks 21-28)

**Objective:** Migrate from filesystem JSON to PostgreSQL

**Deliverables:**
- [x] PostgreSQL deployment
- [x] Schema design
- [x] Data migration pipeline
- [x] Backup strategy
- [x] Query optimization

**Resources:** 2 engineers
**Success Metrics:**
- Database functioning correctly
- Data migrated and validated
- Backups automated
- Query performance optimized

**Key Tasks:**
1. Design database schema
2. Set up PostgreSQL cluster
3. Create migration scripts
4. Migrate data from JSON
5. Update application to use database
6. Implement backup/restore

### 12.5 Phase 5: GitOps & Continuous Deployment (Weeks 29-36)

**Objective:** Implement GitOps workflow for automated deployments

**Deliverables:**
- [x] ArgoCD deployment
- [x] Git-based deployment process
- [x] Automated rollbacks
- [x] Environment parity
- [x] Progressive delivery (canary)

**Resources:** 1-2 engineers
**Success Metrics:**
- Deployments automated from Git
- Rollbacks working automatically
- Staging/production in sync
- Zero-downtime deployments

**Key Tasks:**
1. Set up ArgoCD
2. Create application manifests
3. Implement GitOps workflow
4. Configure canary deployments
5. Test automated rollbacks
6. Document deployment process

### 12.6 Phase 6: Observability & Hardening (Weeks 37-44)

**Objective:** Complete observability and security hardening

**Deliverables:**
- [x] Distributed tracing
- [x] Log aggregation (Loki)
- [x] Alert rules and dashboards
- [x] Security policies (RBAC, network)
- [x] Compliance checks

**Resources:** 2 engineers
**Success Metrics:**
- All services traced
- Logs centralized
- Alerts triggering correctly
- Security policies enforced
- Compliance verified

**Key Tasks:**
1. Instrument applications with tracing
2. Deploy Loki for log aggregation
3. Create dashboards
4. Write alert rules
5. Implement network policies
6. Security audit

### 12.7 Phase 7: Production Deployment & Optimization (Weeks 45-52)

**Objective:** Production-ready system with HA and DR

**Deliverables:**
- [x] Multi-region setup (if applicable)
- [x] HA configuration
- [x] Disaster recovery plan
- [x] Load testing results
- [x] Documentation

**Resources:** 2-3 engineers
**Success Metrics:**
- Production deployment successful
- HA working (no single point of failure)
- RTO/RPO targets met
- Load testing completed
- Documentation complete

**Key Tasks:**
1. Production cluster setup
2. Data replication across regions
3. Load testing
4. Failover testing
5. Runbooks and playbooks
6. Go-live procedures

### 12.8 Timeline Summary

```
Phase       Duration    Start   End      Team Size
─────────────────────────────────────────────────
Phase 1     4 weeks     Wk 1    Wk 4     1-2 eng
Phase 2     8 weeks     Wk 5    Wk 12    2 eng
Phase 3     8 weeks     Wk 13   Wk 20    2 eng
Phase 4     8 weeks     Wk 21   Wk 28    2 eng
Phase 5     8 weeks     Wk 29   Wk 36    1-2 eng
Phase 6     8 weeks     Wk 37   Wk 44    2 eng
Phase 7     8 weeks     Wk 45   Wk 52    2-3 eng
─────────────────────────────────────────────────
Total       52 weeks    ~1 year          12 eng-months

Parallel Activities:
- Documentation (ongoing)
- Training (ongoing)
- Cost optimization (from week 20)
- Performance optimization (from week 24)
```

---

## 13. COST ANALYSIS & OPTIMIZATION

### 13.1 Current State Costs

```
Hardware (Local on WoodsDen):
├─ WoodsDen workstation  ~$1,200 (capital)
│                        + $50/month (power)
├─ Local storage         Included in workstation
└─ No network infrastructure needed (all local)
                         ───────────
                         ~$50/month running costs

Development:
├─ Docker Desktop        Free (personal use)
└─ Software licenses    ~$100/month

Total: ~$150/month + initial capital
```

### 13.2 Cloud Architecture Costs (Estimate)

```
Kubernetes Cluster (AWS/GCP):
├─ Control plane        ~$100-200/month
├─ Compute nodes (3)    ~$300/month (t3.large)
├─ GPU node (1)         ~$200/month (g4dn.xlarge, shared)
└─ Data transfer        ~$50/month
                        ───────────
                        ~$700-800/month

Database (RDS PostgreSQL):
├─ Multi-AZ             ~$300/month (db.t3.large)
└─ Backup storage       ~$50/month
                        ───────────
                        ~$350/month

Cache (ElastiCache Redis):
├─ Cluster              ~$150/month
                        ───────────
                        ~$150/month

Storage:
├─ EBS volumes          ~$100/month
├─ S3 (documents)       ~$50/month
└─ Backups (Glacier)    ~$10/month
                        ───────────
                        ~$160/month

Data Transfer:
├─ Inter-region         ~$50/month
└─ Internet egress      ~$50/month
                        ───────────
                        ~$100/month

Monitoring & Logging:
├─ CloudWatch           ~$50/month
├─ External monitoring  ~$100/month (optional)
                        ───────────
                        ~$50-150/month

─────────────────────────────────────
Total Cloud: ~$1,400-1,600/month
```

### 13.3 Cost Optimization Strategies

```
Immediate Wins:
├─ Reserved Instances   -20-30% (commit to 1-3 years)
├─ Spot Instances       -70% for non-critical work
├─ Rightsizing          -10-20% (match actual usage)
├─ Storage tiering      -30% (archive cold data)
└─ Auto-scaling         -15% (scale down off-hours)
                        ───────────
                        Potential: -40-50% savings

Long-term Optimizations:
├─ Multi-cloud          -10% (negotiate rates)
├─ Committed use plans  -20-30%
├─ Waste elimination    -10%
└─ Efficiency           -5-10%
                        ───────────
                        Potential: Additional -30% savings

Recommendation:
Start: ~$1,500/month
With optimization: ~$750-1,000/month
```

---

## 14. RISK MITIGATION & TRANSITION STRATEGY

### 14.1 Key Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|-----------|
| **Migration data loss** | CRITICAL | Low | Backup before each phase, parallel run during migration |
| **Downtime during transition** | HIGH | Medium | Staged rollout, feature flags, rollback procedures |
| **Skills gap (Kubernetes)** | HIGH | High | Training, documentation, mentoring |
| **Performance degradation** | MEDIUM | Medium | Load testing, performance baselines, monitoring |
| **Security vulnerabilities** | CRITICAL | Medium | Security scanning, code review, penetration testing |
| **Cost overruns** | MEDIUM | Medium | Budget tracking, cost alerts, optimization |
| **Vendor lock-in** | MEDIUM | Low | Multi-cloud ready, containerization, open standards |

### 14.2 Zero-Downtime Transition Plan

```
Phase 1: Parallel Run (2 weeks)
├─ Old system (current) running normally
├─ New system (Docker) running alongside
├─ Data sync between systems
├─ Monitor both systems
└─ Compare results

Phase 2: Gradual Cutover (1 week)
├─ 10% traffic → new system
├─ Monitor error rates, latency
├─ Gradually increase: 25%, 50%, 75%, 100%
├─ Ready to rollback at any time
└─ Complete cutover by end of week

Phase 3: Stabilization (1 week)
├─ Monitor closely
├─ Fix any issues discovered
├─ Finalize configuration
├─ Document actual deployment
└─ Decommission old system
```

---

## 15. EXECUTIVE SUMMARY & RECOMMENDATIONS

### 15.1 Current State Assessment

**Strengths:**
- Functional local infrastructure
- Working document processing pipeline
- Clear use case and domain

**Critical Weaknesses:**
- No scalability (single server)
- Synchronous processing (bottleneck)
- Manual operations
- No disaster recovery
- Filesystem-based data (unreliable)
- No monitoring or observability
- No automated testing/deployment
- Security gaps (single point of failure)

### 15.2 Strategic Recommendations

**Recommendation 1: Adopt Container-First Approach**
- Timeline: Immediate (Phase 1)
- Effort: Moderate (2-4 weeks)
- ROI: High (enables all other improvements)
- Action: Start containerizing with Docker Compose

**Recommendation 2: Implement Message Queue**
- Timeline: Short-term (Phase 3)
- Effort: Moderate-High (6-8 weeks)
- ROI: Very High (5-10x throughput increase)
- Action: Deploy Redis, refactor brief_watcher

**Recommendation 3: Migrate to Cloud Kubernetes**
- Timeline: Medium-term (Phases 2-5)
- Effort: High (16-20 weeks)
- ROI: High (scalability, reliability, automation)
- Action: Start with dev cluster, move staging, then production

**Recommendation 4: Implement Modern CI/CD**
- Timeline: Ongoing (all phases)
- Effort: Moderate (existing templates available)
- ROI: Very High (automation, safety, speed)
- Action: Start with GitHub Actions, add quality gates

**Recommendation 5: Establish Observability**
- Timeline: Phases 1-6 (ongoing)
- Effort: Moderate (tools provided)
- ROI: Very High (visibility, debugging, SLOs)
- Action: Deploy Prometheus/Grafana, add instrumentation

### 15.3 Investment Summary

**Total Investment:** 12 engineer-months over 52 weeks

**Breakdown:**
- Architecture & Design: 4 weeks (2 eng)
- Development & Implementation: 32 weeks (2-3 eng)
- Testing & Validation: 8 weeks (2 eng)
- Documentation & Training: 8 weeks (1-2 eng)

**Expected Outcomes:**
- 10-100x throughput improvement
- 99.9%+ system availability
- Automated deployments (0 manual steps)
- Complete observability
- Disaster recovery capability
- 5-10 minute RTO, 1-hour RPO
- Cost-optimized infrastructure
- Secure, compliant system

### 15.4 Next Steps (This Week)

1. **Day 1-2**: Create project repository
2. **Day 3-5**: Containerize existing services
3. **Week 2**: Set up local Kubernetes (minikube)
4. **Week 3**: Deploy to staging cluster
5. **Week 4**: Establish CI/CD pipeline

---

## APPENDIX: Reference Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    THE CONTINUUM REPORT                       │
│              Production-Grade Architecture                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              Global CDN + Edge Caching                  │ │
│  │        (Cloudflare / Bunny CDN / Vercel Edge)          │ │
│  └────────────────────────┬─────────────────────────────────┘ │
│                           │                                    │
│  ┌────────────────────────┴──────────────────────────────────┐ │
│  │      Kubernetes Cluster (Multi-Region HA)                │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │                                                            │ │
│  │  ┌─ API Gateway & Load Balancer                          │ │
│  │  │                                                        │ │
│  │  ├─ Service Mesh (Istio/Linkerd)                         │ │
│  │  │  ├─ Traffic management                                │ │
│  │  │  ├─ Canary deployments                                │ │
│  │  │  ├─ Security policies                                 │ │
│  │  │  └─ Observability                                     │ │
│  │  │                                                        │ │
│  │  ├─ Application Deployments                              │ │
│  │  │  ├─ continuum-worker (auto-scaling, 5-50 replicas)   │ │
│  │  │  ├─ paperless-ngx (2 replicas)                        │ │
│  │  │  ├─ ollama-inference (3 replicas, GPU)                │ │
│  │  │  ├─ api-gateway (3 replicas)                          │ │
│  │  │  └─ [future services]                                 │ │
│  │  │                                                        │ │
│  │  ├─ Data Layer                                           │ │
│  │  │  ├─ PostgreSQL (Primary + Replicas)                   │ │
│  │  │  ├─ Redis Cluster (3 nodes)                           │ │
│  │  │  ├─ PersistentVolumes (EBS/Network Storage)           │ │
│  │  │  └─ S3-compatible storage (documents)                 │ │
│  │  │                                                        │ │
│  │  ├─ Observability Stack                                  │ │
│  │  │  ├─ Prometheus (metrics)                              │ │
│  │  │  ├─ Grafana (dashboards)                              │ │
│  │  │  ├─ Loki (logs)                                       │ │
│  │  │  ├─ Jaeger (traces)                                   │ │
│  │  │  ├─ Alertmanager (routing)                            │ │
│  │  │  └─ PagerDuty/Slack integration                       │ │
│  │  │                                                        │ │
│  │  └─ Security & Compliance                                │ │
│  │     ├─ Network policies (deny-all default)               │ │
│  │     ├─ RBAC (least privilege)                            │ │
│  │     ├─ Pod security policies                             │ │
│  │     ├─ Secrets management (External Secrets)             │ │
│  │     ├─ Audit logging                                     │ │
│  │     └─ Compliance scanning                               │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              CI/CD Pipeline (GitHub Actions)              │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │                                                            │ │
│  │  Code Push (GitHub)                                       │ │
│  │        ↓                                                  │ │
│  │  Trigger Actions Workflow                                │ │
│  │        ├─ Lint & Format Check                            │ │
│  │        ├─ Security Scan (SAST)                           │ │
│  │        ├─ Unit Tests                                     │ │
│  │        ├─ Build Docker Images                            │ │
│  │        ├─ Container Scan (Trivy)                         │ │
│  │        ├─ Push to Registry (GHCR)                        │ │
│  │        ├─ Integration Tests                              │ │
│  │        ├─ Deploy to Staging                              │ │
│  │        ├─ Smoke Tests                                    │ │
│  │        ├─ Performance Tests                              │ │
│  │        ├─ Manual Approval (for production)               │ │
│  │        └─ Canary Deploy → Full Deploy to Production     │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │            Infrastructure as Code (Terraform)             │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │                                                            │ │
│  │  Git Repository                                           │ │
│  │  ├─ Terraform configuration                              │ │
│  │  ├─ Helm charts                                          │ │
│  │  ├─ Kubernetes manifests                                 │ │
│  │  ├─ IaC for monitoring/logging                           │ │
│  │  └─ Configuration management                             │ │
│  │        ↓                                                  │ │
│  │  Terraform Plan & Apply                                  │ │
│  │        ↓                                                  │ │
│  │  Infrastructure Created/Updated                          │ │
│  │  ├─ Cloud resources (compute, storage, network)          │ │
│  │  ├─ Kubernetes cluster provisioned                       │ │
│  │  └─ Applications deployed via GitOps                     │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │          Backup & Disaster Recovery                       │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │                                                            │ │
│  │  Continuous Backups                                       │ │
│  │  ├─ Database snapshots (hourly)                          │ │
│  │  ├─ Replication to warm standby                          │ │
│  │  ├─ Document backups (daily)                             │ │
│  │  └─ Cross-region replication                             │ │
│  │        ↓                                                  │ │
│  │  S3 / Cold Storage                                        │ │
│  │  ├─ 30-day retention (S3 Standard)                       │ │
│  │  ├─ Long-term archive (Glacier)                          │ │
│  │  └─ Compliance/audit copies                              │ │
│  │                                                            │ │
│  │  Disaster Recovery Plan                                   │ │
│  │  ├─ RTO: 4 hours (full system recovery)                  │ │
│  │  ├─ RPO: 1 hour (data loss limit)                        │ │
│  │  └─ Tested quarterly                                     │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## Document Control

**Version:** 1.0
**Created:** December 24, 2025
**Last Updated:** December 24, 2025
**Author:** Infrastructure & Deployment Engineering Team
**Classification:** Internal Documentation

**Change History:**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-24 | Initial comprehensive assessment |

---

**End of Infrastructure & Deployment Architecture Assessment**
