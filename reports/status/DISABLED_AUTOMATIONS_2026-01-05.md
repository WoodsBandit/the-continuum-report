# Disabled Automations - 2026-01-05

## Summary
Per user request, all automatic scripts and AI services on Tower server have been reviewed and disabled where applicable.

---

## DISABLED

### 1. Nomifactory-CEu (Docker Container)
- **What:** Minecraft modpack server
- **RAM Usage:** ~2.55 GiB when running
- **Action:** Autostart DISABLED via Unraid Docker UI
- **Container still exists:** Yes, can be started manually if needed

### 2. ollama (Docker Container)
- **What:** Local LLM server (Mistral, Llama, etc.)
- **RAM Usage:** ~150 MiB idle, 4-8 GiB when loading models
- **Action:** Autostart DISABLED via Unraid Docker UI
- **Container still exists:** Yes, can be started manually if needed

---

## CHECKED - NO ACTION NEEDED

### 1. User Scripts Plugin
- **Status:** NOT INSTALLED
- **Action:** None required

### 2. Unraid Scheduler
- **Status:** Only standard Unraid tasks configured
  - Parity Check: Monthly, first day, 00:00
  - Mover: Daily at 23:45
- **Action:** None - these are core Unraid maintenance tasks

### 3. continuum-pipeline Container
- **Status:** NOT RUNNING
- **Note:** docker-compose.pipeline.yml exists in T:\scripts\ but container was never deployed
- **Action:** None required

### 4. Scripts in T:\scripts\
- **Status:** Scripts exist but none are set up to run automatically
- **Notable scripts (NOT auto-running):**
  - pipeline_daemon.py
  - pipeline_watcher.py
  - brief_watcher.py
  - webhook_listener.py
- **Action:** None required - these only run when manually invoked

---

## SERVICES THAT REMAIN AUTO-START (Required)

The following containers still have autostart enabled because they are essential:
- paperless-ngx (document management)
- continuum-web (website)
- cloudflared (Cloudflare tunnel)
- claude-code-persistent (Claude Code CLI)
- Redis (cache for Paperless)
- Plex-Media-Server
- radarr, sonarr, sabnzbd (media management)
- Overseerr (media requests)
- PortainerCE (container management)
- audiobookshelf, binhex-readarr-audiobooks (audiobook management)

---

## How to Re-enable

### Nomifactory:
1. Go to Unraid Docker page: http://192.168.1.139/Docker
2. Find Nomifactory-CEu row
3. Click the Autostart toggle to ON

### ollama:
1. Go to Unraid Docker page: http://192.168.1.139/Docker
2. Find ollama row
3. Click the Autostart toggle to ON

---

*Document created: 2026-01-05 by Claude Code*
