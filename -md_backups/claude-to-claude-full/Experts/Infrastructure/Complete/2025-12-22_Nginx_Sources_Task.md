# Claude Code Task: Fix Nginx /sources/ 403 Forbidden

**From:** Infrastructure Lead (Claude Main)
**To:** Claude Code (Tower) — ROOT ACCESS
**Date:** 2025-12-22
**Priority:** CRITICAL — Blocks entire Source Verification System

---

## Problem Statement

PDFs exist at `/continuum/website/sources/giuffre-v-maxwell/` but nginx returns 403 Forbidden when accessing `http://192.168.1.139:8081/sources/`.

The documents are ready. The only blocker is nginx configuration.

---

## Objective

Make source documents publicly accessible at:
```
https://thecontinuumreport.com/sources/giuffre-v-maxwell/ecf-1331-14.pdf
```

---

## Phase 1: Diagnosis

### 1.1 Inspect container mounts
```bash
docker inspect continuum-web --format '{{json .Mounts}}' | jq
```
Document: What host paths are mounted? Where is the document root?

### 1.2 Get current nginx config
```bash
docker exec continuum-web cat /etc/nginx/nginx.conf
docker exec continuum-web cat /etc/nginx/conf.d/default.conf
```
Document: Current configuration. Look for existing location blocks.

### 1.3 Verify document root contents
```bash
docker exec continuum-web ls -la /usr/share/nginx/html/
docker exec continuum-web ls -la /usr/share/nginx/html/sources/
```
Document: Confirm sources directory exists inside container.

### 1.4 Check file permissions
```bash
docker exec continuum-web ls -la /usr/share/nginx/html/sources/giuffre-v-maxwell/
```
Document: Are PDFs readable by nginx user?

---

## Phase 2: Fix

Based on diagnosis, implement ONE of these solutions:

### Option A: Config is host-mounted (preferred)

If nginx config lives on host (e.g., `/mnt/user/appdata/continuum-web/`):

1. Edit the config file directly on host
2. Add location block for /sources/:
```nginx
location /sources/ {
    alias /usr/share/nginx/html/sources/;
    autoindex off;
    try_files $uri =404;
    
    # Proper MIME type for PDFs
    types {
        application/pdf pdf;
    }
    
    # Allow direct linking
    add_header Content-Disposition "inline";
    
    # CORS for external verification tools
    add_header Access-Control-Allow-Origin "*";
}
```
3. Reload nginx:
```bash
docker exec continuum-web nginx -s reload
```

### Option B: Config is inside container only

If config is not host-mounted:

1. Copy config out:
```bash
docker cp continuum-web:/etc/nginx/conf.d/default.conf /tmp/default.conf
```

2. Edit `/tmp/default.conf` to add the location block above

3. Copy back in:
```bash
docker cp /tmp/default.conf continuum-web:/etc/nginx/conf.d/default.conf
```

4. Reload:
```bash
docker exec continuum-web nginx -s reload
```

**Note:** Option B doesn't survive container recreation. If using Option B, also document how to make this persistent (modify Dockerfile or use bind mount).

### Option C: Permissions issue

If diagnosis shows permission problems:
```bash
docker exec continuum-web chmod -R 755 /usr/share/nginx/html/sources/
docker exec continuum-web chown -R nginx:nginx /usr/share/nginx/html/sources/
```

---

## Phase 3: Verification

### 3.1 Test internal access
```bash
curl -I http://192.168.1.139:8081/sources/
curl -I http://192.168.1.139:8081/sources/giuffre-v-maxwell/
curl -I http://192.168.1.139:8081/sources/giuffre-v-maxwell/ecf-1331-14.pdf
```

Expected results:
- `/sources/` → 403 (directory listing disabled) OR 200 with index
- `/sources/giuffre-v-maxwell/` → 403 OR 200
- `/sources/giuffre-v-maxwell/ecf-1331-14.pdf` → **200 OK, Content-Type: application/pdf**

### 3.2 Test PDF download
```bash
curl -o /tmp/test.pdf http://192.168.1.139:8081/sources/giuffre-v-maxwell/ecf-1331-14.pdf
file /tmp/test.pdf
```
Expected: `PDF document`

### 3.3 Test public access (via Cloudflare tunnel)
```bash
curl -I https://thecontinuumreport.com/sources/giuffre-v-maxwell/ecf-1331-14.pdf
```
Expected: 200 OK

---

## Phase 4: Documentation

If directory listing is desired for transparency (so researchers can browse):
```nginx
location /sources/ {
    alias /usr/share/nginx/html/sources/;
    autoindex on;
    autoindex_exact_size off;
    autoindex_localtime on;
    # ... rest of config
}
```

---

## Deliverable

Update `Infrastructure_Nginx_Fix_Response.md` with:

1. **Diagnosis results** — What was the actual problem?
2. **Solution applied** — Which option, exact commands run
3. **Verification results** — All curl outputs
4. **Persistence status** — Will this survive container restart?
5. **Public URLs confirmed working** — List 3 example PDF URLs

---

## Success Criteria

An independent journalist can:
```
https://thecontinuumreport.com/sources/giuffre-v-maxwell/ecf-1331-14.pdf
```
...and immediately see the PDF in their browser. No 403, no 404, no download prompt — just the document.

---

## Rollback Plan

If something breaks the website:
```bash
# Restore original config (if backed up)
docker cp /tmp/default.conf.backup continuum-web:/etc/nginx/conf.d/default.conf
docker exec continuum-web nginx -s reload

# Or restart container to reset (if config wasn't persisted)
docker restart continuum-web
```

**Before making changes, back up current config:**
```bash
docker cp continuum-web:/etc/nginx/conf.d/default.conf /tmp/default.conf.backup
```

---

*Task issued by Infrastructure Lead — 2025-12-22*
