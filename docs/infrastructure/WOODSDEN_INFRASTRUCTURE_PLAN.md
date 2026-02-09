# WoodsDen Local Infrastructure Plan

**Created:** 2026-02-09
**Status:** In Progress

---

## System Specs

| Component | Value |
|-----------|-------|
| **OS** | Windows 11 Pro |
| **CPU** | Intel i7-12700K (12th Gen, 12 cores) |
| **RAM** | 48 GB |
| **Primary Storage** | C: 930 GB (157 GB free) |
| **Data Storage** | Z: 1.9 TB (631 GB free) |
| **Virtualization** | Hyper-V Enabled |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        WOODSDEN (Windows 11)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐     ┌──────────────────┐                  │
│  │   Docker Desktop  │     │   Cloudflare     │                  │
│  │                   │     │   Tunnel (cloudflared)              │
│  │  ┌─────────────┐ │     │                  │                  │
│  │  │ Paperless   │ │     │  localhost:8081 ◄────► thecontinuumreport.com
│  │  │ :8040       │ │     │                  │                  │
│  │  └─────────────┘ │     └──────────────────┘                  │
│  │                   │                                           │
│  │  ┌─────────────┐ │     ┌──────────────────┐                  │
│  │  │ nginx       │ │     │   Claude Code    │                  │
│  │  │ :8081       │ │     │   CLI            │                  │
│  │  └─────────────┘ │     │                  │                  │
│  │                   │     │  BNIS Pipeline   │                  │
│  └──────────────────┘     └──────────────────┘                  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Z: Drive (1.9 TB)                      │   │
│  │  /continuum/          - Project files                     │   │
│  │  /paperless/media/    - OCR'd documents                   │   │
│  │  /paperless/data/     - Paperless database                │   │
│  │  /sources/            - Source document archive           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Docker Desktop
- **Purpose:** Container runtime for all services
- **Install:** https://www.docker.com/products/docker-desktop/
- **Config:** Use WSL2 backend (faster than Hyper-V backend)

### 2. Paperless-ngx
- **Purpose:** Document management, OCR, search, tagging
- **Port:** 8040
- **Data Location:** Z:\paperless\
- **Features:**
  - Automatic OCR on upload
  - Full-text search
  - REST API for Claude Code integration
  - Tag-based organization

### 3. Web Server (nginx)
- **Purpose:** Serve thecontinuumreport.com locally
- **Port:** 8081
- **Document Root:** C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum\website\

### 4. Cloudflare Tunnel
- **Purpose:** Route thecontinuumreport.com to localhost
- **Config:** Point to localhost:8081
- **Install:** cloudflared CLI

### 5. BNIS Pipeline
- **Purpose:** Breaking news monitoring and narrative generation
- **Components:**
  - News fetchers (GDELT, RSS, NewsAPI)
  - Entity matcher (2,008+ entities)
  - Claude Code CLI integration
  - Auto-approval workflow
- **Voice:** The Continuum Report editorial style

### 6. Protection Layer
- **Docker Isolation:** Containers run in isolated networks
- **Legal Framework:** Milkovich v. Lorain Journal opinion protection
- **Backup:** Automated backups to Z: drive

---

## Installation Order

1. [ ] Docker Desktop
2. [ ] Paperless-ngx container
3. [ ] nginx container (or local Python server)
4. [ ] Cloudflare tunnel
5. [ ] BNIS pipeline configuration
6. [ ] Claude Code automation scripts

---

## Docker Compose Configuration

See: `docker/docker-compose.woodsden.yml`

---

## Data Locations

| Data | Location | Size Estimate |
|------|----------|---------------|
| Project files | C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum\ | ~5 GB |
| Paperless media | Z:\paperless\media\ | ~50-100 GB |
| Paperless database | Z:\paperless\data\ | ~1 GB |
| Source archives | Z:\continuum-sources\ | ~100+ GB |
| Backups | Z:\backups\ | ~50 GB |

---

## API Endpoints (Local)

| Service | URL |
|---------|-----|
| Paperless API | http://localhost:8040/api/ |
| Website | http://localhost:8081/ |
| Paperless UI | http://localhost:8040/ |

---

## Security Considerations

1. **Network Isolation:** Docker containers on internal bridge network
2. **No External Ports:** Only Cloudflare tunnel exposes site
3. **Local-only APIs:** Paperless API not exposed externally
4. **Legal Protection:** All content follows Milkovich framework
5. **Backup Strategy:** Daily backups to Z: drive

---

## Next Steps

1. Download Docker Desktop installer
2. Run installation
3. Create docker-compose.woodsden.yml
4. Deploy Paperless-ngx
5. Test OCR functionality
6. Configure Cloudflare tunnel
7. Set up BNIS automation
