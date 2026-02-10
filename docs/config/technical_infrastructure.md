# Technical Infrastructure — Complete Reference

**The Continuum Report**
**Last Updated:** 2026-02-09

---

## Host: WoodsDen (Local Docker)

| Spec | Value |
|------|-------|
| Platform | Windows with Docker Desktop |
| Services | All run locally via Docker Compose |
| Project Root | `C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum\` |
| Data Storage | `data/paperless/` (within project folder) |

---

## Docker Containers

| Container | Port | Purpose |
|-----------|------|---------|
| paperless-ngx | 8040 | Document management, OCR, search |
| continuum-web | 8081 | Nginx serving the website |
| Redis | 6379 | Cache for Paperless |

**Start services:**
```bash
cd docker
docker-compose -f docker-compose.woodsden.yml up -d
```

---

## Paperless-ngx Configuration

| Setting | Value |
|---------|-------|
| URL | http://localhost:8040 |
| Credentials | admin / continuum2026 |
| Documents | ~200+ processed |
| Content | Epstein case files, Whitney Webb books, court filings |
| Inbox | `data/paperless/consume/` |
| Media | `data/paperless/media/` |

### Paperless API Quick Reference

```bash
# Base configuration
PAPERLESS_URL="http://localhost:8040"
TOKEN="your_api_token_here"
HEADERS="Authorization: Token $TOKEN"

# Search documents
curl -H "$HEADERS" "$PAPERLESS_URL/api/documents/?query=Bill+Clinton"

# Get document by ID
curl -H "$HEADERS" "$PAPERLESS_URL/api/documents/42/"

# Update document (tags, etc.)
curl -X PATCH -H "$HEADERS" \
  -H "Content-Type: application/json" \
  -d '{"tags": [1, 2, 3]}' \
  "$PAPERLESS_URL/api/documents/42/"

# Create tag
curl -X POST -H "$HEADERS" \
  -H "Content-Type: application/json" \
  -d '{"name": "epstein", "color": "#ff0000"}' \
  "$PAPERLESS_URL/api/tags/"

# Download original document
curl -H "$HEADERS" \
  "$PAPERLESS_URL/api/documents/42/download/" \
  -o document.pdf
```

### Paperless Python Integration

```python
import requests

PAPERLESS_URL = "http://localhost:8040"
headers = {"Authorization": "Token your_api_token_here"}

# Search
response = requests.get(
    f"{PAPERLESS_URL}/api/documents/",
    headers=headers,
    params={"query": "Epstein"}
)
documents = response.json()

# Get document
doc = requests.get(
    f"{PAPERLESS_URL}/api/documents/42/",
    headers=headers
).json()

# Update
requests.patch(
    f"{PAPERLESS_URL}/api/documents/42/",
    headers=headers,
    json={"tags": [1, 2, 3]}
)
```

---

## Website Infrastructure

| Component | Status |
|-----------|--------|
| Domain | thecontinuumreport.com (LIVE) |
| Pages | index.html, about.html, legal.html, continuum.html, sources/index.html |
| Routing | Cloudflare tunnel → continuum-web (8081) |
| Email | contact@thecontinuumreport.com |
| Design | Purple/black/gold theme |
| Fonts | Cinzel, Cormorant Garamond, Source Sans 3 |

### Website File Structure

```
/continuum/website/
├── index.html              # Homepage
├── about.html              # About page
├── legal.html              # Legal methodology
├── continuum.html          # Interactive visualization (main interface)
├── sources/
│   └── index.html          # Source documents archive
├── data/
│   ├── entities.json       # Entity data for visualization
│   ├── connections.json    # Connection graph data
│   └── hierarchy.json      # Entity categorization
├── briefs/
│   ├── entity/             # 37 entity briefs (HTML)
│   └── connections/        # 86 connection briefs (HTML)
└── sources/                # 33,745+ PDF files
    ├── house-oversight-2025/
    ├── giuffre-v-maxwell/
    └── [12 other categories]
```

**Note:** Briefs are ONLY accessible through continuum.html interactive interface — no direct URL access to individual brief files.

---

## Local Development

| Setting | Value |
|---------|-------|
| Platform | WoodsDen (Windows + Docker Desktop) |
| Project Path | `C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum` |
| Docker Compose | `docker/docker-compose.woodsden.yml` |
| Data Storage | `data/paperless/` |

### Starting Services

```bash
cd "C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum\docker"
docker-compose -f docker-compose.woodsden.yml up -d
```

### Stopping Services

```bash
cd "C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum\docker"
docker-compose -f docker-compose.woodsden.yml down
```

---

## Docker Commands Reference

```bash
# List running containers
docker ps --format "table {{.Names}}\t{{.Status}}"

# Execute commands in container
docker exec -it paperless-ngx bash
docker exec -it continuum-python python /continuum/scripts/script.py

# View logs
docker logs continuum-web --tail 50
docker logs paperless-ngx --tail 100

# Restart containers
docker restart continuum-web
docker restart paperless-ngx

# Stop/start containers
docker stop continuum-web
docker start continuum-web
```

---

## Python Pipeline Scripts

**Location:** `/continuum/scripts/`

### Available Scripts

```bash
# Continuum pipeline (WIP - not complete)
python /continuum/scripts/continuum_pipeline.py dossier "Subject Name"
python /continuum/scripts/continuum_pipeline.py test
python /continuum/scripts/continuum_pipeline.py batch [limit]

# Brief parsing (WIP)
python /continuum/scripts/parse_brief.py analytical_brief_name.md

# Graph building (WIP)
python /continuum/scripts/build_graph.py
```

**Note:** Python automation scripts are work in progress. Goal: automate brief → JSON pipeline (drop markdown → auto-update entities.json/connections.json).

---

## Service URLs

| Resource | Location |
|----------|----------|
| Website (Production) | https://thecontinuumreport.com |
| Website (Local Dev) | http://localhost:8081 |
| Paperless | http://localhost:8040 |
| GitHub | WoodsBandit/the-continuum-report |

---

*All services run locally on WoodsDen via Docker. There is no remote server.*
