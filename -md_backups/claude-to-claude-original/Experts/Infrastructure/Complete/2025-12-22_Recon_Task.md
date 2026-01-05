# Claude Code Task: Infrastructure Reconnaissance

**From:** Infrastructure Lead (Claude Main)
**To:** Claude Code (Tower)
**Date:** 2025-12-21
**Priority:** High — Blocks all subsequent Source Verification work

---

## Objective

Gather infrastructure state information for the Source Verification System build. Do NOT modify anything — reconnaissance only.

---

## Tasks

### 1. Paperless-ngx Inventory

**List all tags:**
```bash
curl -s -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
  "http://192.168.1.139:8040/api/tags/" | jq '.results[] | {id, name, document_count}'
```

**Get total document count:**
```bash
curl -s -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
  "http://192.168.1.139:8040/api/documents/" | jq '.count'
```

**Sample 10 document titles:**
```bash
curl -s -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
  "http://192.168.1.139:8040/api/documents/?page_size=10" | jq '.results[] | {id, title, original_file_name}'
```

---

### 2. Directory State

```bash
# Sources directory
ls -la /mnt/user/continuum/sources/
find /mnt/user/continuum/sources/ -type f 2>/dev/null | head -20

# Website directory structure
ls -la /mnt/user/continuum/website/
```

---

### 3. Nginx Configuration

```bash
# Find the container and its mounts
docker inspect continuum-web --format '{{json .Mounts}}' | jq

# Find nginx config
docker exec continuum-web cat /etc/nginx/nginx.conf 2>/dev/null
docker exec continuum-web cat /etc/nginx/conf.d/default.conf 2>/dev/null

# Check what's being served
docker exec continuum-web ls -la /usr/share/nginx/html/
```

---

### 4. Document Metadata Sample

Pull 5 full document details to assess ECF number availability:
```bash
curl -s -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" \
  "http://192.168.1.139:8040/api/documents/?page_size=5" | jq '.results[] | {id, title, original_file_name, correspondent, tags, created, added}'
```

---

### 5. Cloudflare Tunnel Status

```bash
# List running containers to find cloudflared
docker ps | grep -i cloud

# Check tunnel config if accessible
docker logs $(docker ps -q --filter "name=cloud") --tail 30 2>&1 | head -30
```

---

## Deliverable

Copy your findings into `Infrastructure_Recon_Response.md` in this same folder. Use the template provided there.

**Do not create directories or modify configurations.** Report only.
