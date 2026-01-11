# Technical Infrastructure — Complete Reference

**The Continuum Report**
**Last Updated:** 2025-12-29

---

## Server: Tower (Unraid)

| Spec | Value |
|------|-------|
| Hardware | Intel i7-10700K, 16GB RAM, 12TB storage |
| IP | 192.168.1.139 |
| MAC Address | 74:56:3c:eb:49:93 |
| OS | Unraid |
| SMB Share | `\\192.168.1.139\continuum\` |
| Constraint | Memory limited — Claude Code preferred over local Ollama |

---

## Key Containers

| Container | Port | Purpose |
|-----------|------|---------|
| paperless-ngx | 8040 | Document management, OCR, search |
| ollama-cpu | 11434 | Local LLM (Mistral 7B) — backup option |
| continuum-python | — | Python runtime for scripts |
| continuum-web | 8081 | Nginx serving the website |
| cloudflared-tunnel | — | Secure tunnel to Cloudflare |
| Redis | 6379 | Cache for Paperless |

---

## Paperless-ngx Configuration

| Setting | Value |
|---------|-------|
| URL | http://192.168.1.139:8040 |
| API Token | da99fe6aa0b8d021689126cf72b91986abbbd283 |
| Documents | ~200+ processed |
| Content | Epstein case files, Whitney Webb books, court filings |
| Inbox | `/continuum/documents/inbox/` |

### Paperless API Quick Reference

```bash
# Base configuration
PAPERLESS_URL="http://192.168.1.139:8040"
TOKEN="da99fe6aa0b8d021689126cf72b91986abbbd283"
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

PAPERLESS_URL = "http://192.168.1.139:8040"
headers = {"Authorization": "Token da99fe6aa0b8d021689126cf72b91986abbbd283"}

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

## WoodsDen Mount (Reverse SMB)

| Setting | Value |
|---------|-------|
| WoodsDen IP | 192.168.1.94 |
| Windows Path | `C:\Users\Xx LilMan xX\Documents\Claude Docs` |
| Share Name | `claude-docs` |
| Host Mount | `/mnt/woodsden/claude-docs` ✅ |
| Container Path | `/mnt/woodsden` (requires Docker mapping) |
| Credentials | `/root/.woodsden-creds` |

### Mount Scripts

**Location:** `/mnt/user/continuum/scripts/`

- `mount-woodsden.sh` — Mount WoodsDen share
- `check-woodsden-mount.sh` — Verify mount status

### After Reboot

```bash
# Remount WoodsDen share
/mnt/user/continuum/scripts/mount-woodsden.sh

# Verify mount
/mnt/user/continuum/scripts/check-woodsden-mount.sh
```

### For Container Access

Add Docker path mapping:
- Container: `/mnt/woodsden`
- Host: `/mnt/woodsden`

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

## Network Configuration

| Resource | Location |
|----------|----------|
| Server IP | 192.168.1.139 |
| WoodsDen IP | 192.168.1.94 |
| SMB Share | `\\192.168.1.139\continuum\` |
| Website | https://thecontinuumreport.com |
| Paperless | http://192.168.1.139:8040 |
| Ollama | http://192.168.1.139:11434 |

---

*For CLAUDE.md summary, see: Section 6 (Technical Infrastructure)*
