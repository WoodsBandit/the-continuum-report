# The Continuum Report - Quick Start Guide
## Essential Templates & Commands for Implementation

---

## GETTING STARTED IN 15 MINUTES

### Step 1: Create Project Repository
```bash
# Create GitHub repository
gh repo create continuum-report --private --description "Professional deployment infrastructure"

# Clone and setup
git clone https://github.com/YOUR_ORG/continuum-report.git
cd continuum-report

# Create branch structure
git branch develop
git push -u origin develop main
```

### Step 2: Create Basic Directory Structure
```bash
mkdir -p src/worker src/api website infrastructure/{monitoring,k8s,terraform} docs tests/{unit,integration,e2e}
touch README.md .gitignore Makefile Dockerfile docker-compose.yml
```

### Step 3: First Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN groupadd -r continuum && useradd -r -g continuum continuum

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

USER continuum:continuum

HEALTHCHECK --interval=10s CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

CMD ["python", "-m", "continuum.worker"]
```

### Step 4: First GitHub Actions Workflow
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/unit/
```

### Step 5: Start Local Environment
```bash
docker-compose up -d
docker exec continuum-worker python -m pytest tests/
```

---

## ESSENTIAL DOCKER TEMPLATES

### Worker Service (Python)
```dockerfile
# syntax=docker/dockerfile:1.4

FROM python:3.11-slim as base

RUN groupadd -r continuum && useradd -r -g continuum continuum

WORKDIR /app

# Production build
FROM base as builder

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM base

COPY --from=builder /root/.local /home/continuum/.local
COPY --chown=continuum:continuum src/worker/ .

ENV PATH=/home/continuum/.local/bin:$PATH PYTHONUNBUFFERED=1

USER continuum:continuum

HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

CMD ["python", "-m", "continuum.worker"]
```

### API Service (Python Flask/FastAPI)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN groupadd -r api && useradd -r -g api api

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/api/ .

USER api:api

HEALTHCHECK --interval=10s CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Website (Node.js)
```dockerfile
# Build
FROM node:18-alpine as builder

WORKDIR /app

COPY website/package*.json .
RUN npm ci

COPY website/ .
RUN npm run build

# Runtime
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY website/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

HEALTHCHECK --interval=10s CMD wget --quiet --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

---

## DOCKER-COMPOSE TEMPLATE

```yaml
version: '3.9'

services:
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    volumes: [redis-data:/data]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  postgres:
    image: postgres:15-alpine
    ports: ["5432:5432"]
    environment:
      POSTGRES_USER: continuum
      POSTGRES_PASSWORD: dev_password
      POSTGRES_DB: continuum_db
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./infrastructure/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U continuum"]
      interval: 5s
      timeout: 3s
      retries: 5

  ollama:
    image: ollama/ollama:latest
    ports: ["11434:11434"]
    volumes: [ollama-models:/root/.ollama]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 10s
      timeout: 5s
      retries: 5

  paperless:
    image: paperlessngx/paperless-ngx:latest
    ports: ["8000:8000"]
    environment:
      PAPERLESS_REDIS: redis://redis:6379
      PAPERLESS_DBHOST: postgres
      PAPERLESS_DBUSER: continuum
      PAPERLESS_DBPASS: dev_password
      PAPERLESS_SECRET_KEY: development-key
      PAPERLESS_ADMIN_USER: admin
      PAPERLESS_ADMIN_PASSWORD: admin
    volumes:
      - paperless-data:/var/lib/paperless
      - paperless-media:/home/user/Maildir
    depends_on:
      redis:
        condition: service_healthy
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/"]
      interval: 10s
      timeout: 5s
      retries: 5

  worker:
    build:
      context: .
      dockerfile: src/worker/Dockerfile
    ports: ["8080:8080"]
    environment:
      REDIS_URL: redis://redis:6379
      DATABASE_URL: postgresql://continuum:dev_password@postgres:5432/continuum_db
      PAPERLESS_URL: http://paperless:8000
      OLLAMA_URL: http://ollama:11434
      LOG_LEVEL: DEBUG
    depends_on:
      redis:
        condition: service_healthy
      postgres:
        condition: service_healthy
      paperless:
        condition: service_healthy
      ollama:
        condition: service_healthy
    volumes:
      - ./src:/app/src

  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes:
      - ./infrastructure/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports: ["3001:3000"]
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  redis-data:
  postgres-data:
  paperless-data:
  paperless-media:
  ollama-models:
  prometheus-data:
  grafana-data:
```

---

## KUBERNETES DEPLOYMENT TEMPLATE

### Minimal Deployment
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: continuum-report

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: continuum-worker
  namespace: continuum-report
spec:
  replicas: 3
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
        image: ghcr.io/your-org/continuum-report/worker:latest
        ports:
        - containerPort: 8080
        env:
        - name: REDIS_URL
          value: "redis://redis:6379"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: continuum-secrets
              key: database-url
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
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: continuum-worker
  namespace: continuum-report
spec:
  selector:
    app: continuum-worker
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: continuum-worker
  namespace: continuum-report
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: continuum-worker
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Complete Service Definition
```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: continuum-config
  namespace: continuum-report
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  OLLAMA_URL: "http://ollama:11434"
  PAPERLESS_URL: "http://paperless:8000"

---
apiVersion: v1
kind: Secret
metadata:
  name: continuum-secrets
  namespace: continuum-report
type: Opaque
stringData:
  database-url: "postgresql://user:password@postgres:5432/continuum_db"
  redis-url: "redis://redis:6379"
  api-token: "your-secret-token"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: continuum-worker
  namespace: continuum-report
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: continuum-worker
  template:
    metadata:
      labels:
        app: continuum-worker
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: continuum-worker
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: worker
        image: ghcr.io/your-org/continuum-report/worker:v1.0
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8080
        env:
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: continuum-secrets
              key: redis-url
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: continuum-secrets
              key: database-url
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: continuum-config
              key: LOG_LEVEL
        - name: ENVIRONMENT
          valueFrom:
            configMapKeyRef:
              name: continuum-config
              key: ENVIRONMENT
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
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 2
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - continuum-worker
              topologyKey: kubernetes.io/hostname

---
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
```

---

## GITHUB ACTIONS WORKFLOW TEMPLATES

### Complete CI/CD Pipeline
```yaml
name: Build & Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/worker

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install ruff black
      - run: ruff check src/
      - run: black --check src/

  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r requirements.txt pytest
      - run: pytest tests/ --cov=src

  build:
    name: Build
    needs: [lint, test]
    runs-on: ubuntu-latest
    permissions:
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: .
          file: ./src/worker/Dockerfile
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

  deploy:
    name: Deploy
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - run: |
          kubectl set image deployment/continuum-worker \
            worker=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -n continuum-report
      - run: kubectl rollout status deployment/continuum-worker -n continuum-report --timeout=5m
```

---

## MAKEFILE TEMPLATE

```makefile
.PHONY: help up down test lint format build push deploy

DOCKER_REGISTRY ?= ghcr.io
IMAGE_NAME ?= continuum-report

help:
	@echo "Continuum Report Commands"
	@echo ""
	@echo "Development:"
	@echo "  make up         - Start local environment"
	@echo "  make down       - Stop local environment"
	@echo "  make logs       - View logs"
	@echo ""
	@echo "Testing:"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Lint code"
	@echo "  make format     - Format code"
	@echo ""
	@echo "Deployment:"
	@echo "  make build      - Build images"
	@echo "  make push       - Push to registry"
	@echo "  make deploy     - Deploy to Kubernetes"

up:
	docker-compose -f infrastructure/docker-compose.yml up -d

down:
	docker-compose -f infrastructure/docker-compose.yml down

logs:
	docker-compose -f infrastructure/docker-compose.yml logs -f

test:
	docker exec continuum-worker pytest tests/ -v

lint:
	docker exec continuum-worker ruff check src/

format:
	docker exec continuum-worker black src/

build:
	docker build -f src/worker/Dockerfile -t $(IMAGE_NAME)/worker:latest .
	docker build -f website/Dockerfile -t $(IMAGE_NAME)/website:latest .

push:
	docker tag $(IMAGE_NAME)/worker:latest $(DOCKER_REGISTRY)/$(IMAGE_NAME)/worker:latest
	docker push $(DOCKER_REGISTRY)/$(IMAGE_NAME)/worker:latest
	docker tag $(IMAGE_NAME)/website:latest $(DOCKER_REGISTRY)/$(IMAGE_NAME)/website:latest
	docker push $(DOCKER_REGISTRY)/$(IMAGE_NAME)/website:latest

deploy:
	kubectl apply -f k8s/base/
	kubectl rollout status deployment/continuum-worker -n continuum-report

clean:
	docker-compose -f infrastructure/docker-compose.yml down -v
	rm -rf .pytest_cache __pycache__
```

---

## ESSENTIAL COMMANDS

### Docker
```bash
# Build image
docker build -f Dockerfile -t image-name:tag .

# Run container
docker run -d -p 8080:8080 image-name:tag

# Execute in container
docker exec -it container-name bash

# View logs
docker logs -f container-name

# Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
docker-compose ps
```

### Kubernetes
```bash
# View resources
kubectl get pods -n continuum-report
kubectl get services -n continuum-report
kubectl get deployments -n continuum-report

# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f -k overlays/production

# Logs
kubectl logs -f deployment/continuum-worker -n continuum-report

# Scale
kubectl scale deployment continuum-worker --replicas=5 -n continuum-report

# Rollout
kubectl rollout status deployment/continuum-worker -n continuum-report
kubectl rollout undo deployment/continuum-worker -n continuum-report

# Port forward
kubectl port-forward service/continuum-worker 8080:80 -n continuum-report
```

### Helm
```bash
# Create chart
helm create continuum

# Template rendering
helm template continuum ./continuum -f values.yaml

# Install
helm install continuum ./continuum -n continuum-report

# Upgrade
helm upgrade continuum ./continuum -n continuum-report

# Uninstall
helm uninstall continuum -n continuum-report
```

### Git
```bash
# Create feature branch
git checkout -b feature/new-feature

# Commit
git add .
git commit -m "feat: add new feature"

# Push
git push origin feature/new-feature

# Create pull request
gh pr create --title "Add new feature" --body "Feature description"

# Merge
git checkout main
git merge feature/new-feature
```

---

## PROMETHEUS QUERIES (PromQL)

```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_errors_total[5m]) / rate(http_requests_total[5m])

# Response time (P95)
histogram_quantile(0.95, http_request_duration_seconds)

# Pod restart count
rate(pod_restarts_total[1h])

# Memory usage
container_memory_usage_bytes / container_spec_memory_limit_bytes

# CPU usage
rate(container_cpu_usage_seconds_total[5m])

# Document processing throughput
rate(documents_processed_total[5m])

# Queue length
queue_length

# Error queue
dead_letter_queue_length
```

---

## TROUBLESHOOTING COMMANDS

### Kubernetes Issues
```bash
# Pod logs
kubectl logs pod-name -n namespace --previous  # Previous crashed pod
kubectl logs -f pod-name -n namespace -c container-name

# Pod events
kubectl describe pod pod-name -n namespace

# Node status
kubectl get nodes
kubectl top nodes
kubectl describe node node-name

# Events
kubectl get events -n namespace --sort-by='.lastTimestamp'

# Debug pod
kubectl debug pod-name -n namespace -it --image=busybox
```

### Container Issues
```bash
# Check image
docker inspect image-name:tag

# Rebuild with cache disabled
docker build --no-cache -f Dockerfile -t image-name:tag .

# Check running processes
docker exec container-name ps aux

# Network connectivity
docker exec container-name curl http://other-service:port
```

### Performance Issues
```bash
# Check metrics
kubectl top pods -n continuum-report
kubectl top nodes

# View events
kubectl get events -n continuum-report --sort-by='.lastTimestamp'

# Check resource requests/limits
kubectl describe nodes

# Monitor metrics
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Visit http://localhost:9090
```

---

## FILES TO GITIGNORE

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment variables
.env
.env.local
.env.*.local

# Docker
docker-compose.override.yml

# Kubernetes
kubeconfig
*.kubeconfig

# Terraform
terraform/.terraform/
terraform/terraform.tfstate*
terraform/.tfvars

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build artifacts
dist/
build/
*.egg-info/

# OS
.DS_Store
Thumbs.db
```

---

## ENVIRONMENT VARIABLES TEMPLATE

```bash
# .env.example

# Application
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DEBUG=true

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/continuum_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40

# Redis
REDIS_URL=redis://localhost:6379
REDIS_NAMESPACE=continuum

# External Services
PAPERLESS_URL=http://localhost:8000
PAPERLESS_API_TOKEN=your-token-here
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# API
API_PORT=8080
API_HOST=0.0.0.0
API_WORKERS=4

# Monitoring
PROMETHEUS_PORT=9090
METRICS_ENABLED=true

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000"]

# Email (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password

# Cloud (if applicable)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

---

## NEXT STEPS

1. **Clone this quick start guide** - Copy templates to your project
2. **Create GitHub repository** - Start version control immediately
3. **Set up local Docker** - Get development environment running
4. **Write first CI test** - Automate early
5. **Deploy locally** - Verify everything works before scaling

Start with Phase 1 - spend one week getting the fundamentals right. This foundation enables all future phases.

---

**Document Version:** 1.0
**Last Updated:** December 24, 2025
