# Pipeline Deployment Guide

## Architecture Overview

The pipeline runs across two machines:

```
┌─────────────────────────────────────────────────────────────┐
│  TOWER (192.168.1.139) - Unraid Server                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Docker Container: continuum-webhook                │    │
│  │  - Receives Paperless webhooks                      │    │
│  │  - Writes to /continuum/indexes/ingestion_queue.json│    │
│  │  - Port 5000                                        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Paperless-ngx (Port 8040)                          │    │
│  │  - Sends webhook on document upload                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  SMB Share: \\192.168.1.139\continuum                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ SMB Mount
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  WOODSDEN (192.168.1.94) - Workstation                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Pipeline Watcher (pipeline_watcher.py)             │    │
│  │  - Monitors ingestion_queue.json                    │    │
│  │  - Monitors entity_registry.json                    │    │
│  │  - Monitors connection_contexts.json                │    │
│  │  - Monitors approved/ directory                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Claude CLI (installed locally)                     │    │
│  │  - Runs SOP-based processing                        │    │
│  │  - Entity extraction, context analysis, briefs      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Step 1: Deploy Webhook Listener on Tower

### Option A: Using Docker (Recommended)

```bash
# SSH to Tower
ssh root@192.168.1.139

# Navigate to scripts
cd /mnt/user/continuum/scripts

# Build the webhook container
docker build -f Dockerfile.webhook -t continuum-webhook .

# Run it
docker run -d \
    --name continuum-webhook \
    --restart unless-stopped \
    -p 5000:5000 \
    -v /mnt/user/continuum:/continuum \
    continuum-webhook

# Verify it's running
curl http://localhost:5000/health
```

### Option B: Using Nerd Tools

1. Install Nerd Tools plugin in Unraid
2. Enable python3, python-pip, python-setuptools
3. Run:
```bash
pip3 install flask requests
cd /mnt/user/continuum/scripts
python3 webhook_listener.py &
```

## Step 2: Configure Paperless Webhook

In Paperless-ngx (http://192.168.1.139:8040):

1. Go to **Admin** → **Webhooks**
2. Add new webhook:
   - **URL:** `http://192.168.1.139:5000/api/continuum/ingest`
   - **Trigger:** Document consumed
   - **Secret:** (optional - set WEBHOOK_SECRET env var if used)

## Step 3: Run Pipeline on WoodsDen

### Windows

```cmd
REM Mount the share if not already mounted
net use T: \\192.168.1.139\continuum

REM Install dependencies
pip install watchdog pydantic-settings requests

REM Start the pipeline
T:\continuum\scripts\run_pipeline_local.bat
```

### Linux/WSL

```bash
# Mount the share
sudo mount -t cifs //192.168.1.139/continuum /mnt/continuum -o user=your_user

# Install dependencies
pip3 install watchdog pydantic-settings requests

# Start the pipeline
chmod +x /mnt/continuum/scripts/run_pipeline_local.sh
/mnt/continuum/scripts/run_pipeline_local.sh
```

## Step 4: Verify End-to-End Flow

1. **Test webhook endpoint:**
   ```bash
   curl -X POST http://192.168.1.139:5000/api/continuum/ingest \
       -H "Content-Type: application/json" \
       -d '{"document_id": 1, "title": "Test Document"}'
   ```

2. **Check queue:**
   ```bash
   cat //192.168.1.139/continuum/indexes/ingestion_queue.json
   ```

3. **Watch logs on WoodsDen:**
   The pipeline watcher will show activity when it detects queue changes.

## Trigger Flow Summary

| Event | Location | Triggers |
|-------|----------|----------|
| Document uploaded to Paperless | Tower | Webhook → ingestion_queue.json |
| ingestion_queue.json changes | WoodsDen | Stage 1 (Claude entity extraction) |
| entity_registry.json changes | WoodsDen | Stage 2 (context extraction) |
| connection_contexts.json changes | WoodsDen | Stage 3 (brief generation) |
| Files in approved/ | WoodsDen | Stage 4 (publication) |

## Monitoring

### Check webhook health (Tower):
```bash
curl http://192.168.1.139:5000/api/continuum/status
```

### Check queue status (anywhere):
```bash
cat \\192.168.1.139\continuum\indexes\ingestion_queue.json
```

### Check pipeline status (WoodsDen):
```bash
python pipeline_watcher.py --status
```

## Troubleshooting

### Webhook not receiving requests
1. Check Docker container is running: `docker ps | grep continuum-webhook`
2. Check port is open: `curl http://192.168.1.139:5000/health`
3. Check Paperless webhook config

### Pipeline not triggering stages
1. Verify Claude CLI is working: `claude --version`
2. Check file permissions on SMB share
3. Check watchdog is detecting changes: Run with `--dry-run` first

### Claude CLI errors
1. Ensure you're authenticated: `claude login`
2. Check API quota/limits
3. Try running a manual stage: `python run_stage1.py --document-id 1 --dry-run`

## Files Reference

| File | Purpose |
|------|---------|
| `webhook_listener.py` | Receives Paperless webhooks (Tower) |
| `pipeline_watcher.py` | File system watcher (WoodsDen) |
| `invoke_claude.py` | Claude CLI wrapper |
| `run_stage1.py` | Entity extraction |
| `run_stage2.py` | Context extraction |
| `run_stage3.py` | Brief generation |
| `run_stage4.py` | Publication |
| `Dockerfile.webhook` | Docker build for webhook |
| `run_pipeline_local.bat` | Windows startup script |
| `run_pipeline_local.sh` | Linux startup script |
