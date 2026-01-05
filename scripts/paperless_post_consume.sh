#!/bin/bash
#
# The Continuum Report - Paperless Post-Consume Script
#
# This script is called by Paperless-ngx after a document is consumed.
# It triggers the Continuum pipeline by calling the webhook endpoint.
#
# Paperless provides these environment variables:
#   DOCUMENT_ID - The document's primary key
#   DOCUMENT_FILE_NAME - Generated file name
#   DOCUMENT_CREATED - Creation date
#   DOCUMENT_ADDED - When document was added
#   DOCUMENT_ORIGINAL_FILENAME - Original file name
#   DOCUMENT_ARCHIVE_PATH - Path to archived file
#   DOCUMENT_SOURCE_PATH - Path to original file
#   DOCUMENT_DOWNLOAD_URL - API URL to download document
#   DOCUMENT_CORRESPONDENT - Correspondent name
#   DOCUMENT_TAGS - Comma-separated tags
#
# Installation:
#   1. Copy this script to a location accessible by Paperless container
#   2. Make executable: chmod +x paperless_post_consume.sh
#   3. Set PAPERLESS_POST_CONSUME_SCRIPT=/path/to/paperless_post_consume.sh
#   4. Restart Paperless container

set -e

# Configuration
WEBHOOK_URL="${CONTINUUM_WEBHOOK_URL:-http://192.168.1.139:5000/api/continuum/ingest}"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] CONTINUUM: $1"
}

# Check if we have a document ID
if [ -z "$DOCUMENT_ID" ]; then
    log "ERROR: DOCUMENT_ID not set. Exiting."
    exit 1
fi

log "Processing document $DOCUMENT_ID: $DOCUMENT_ORIGINAL_FILENAME"

# Build JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
    "document_id": $DOCUMENT_ID,
    "title": "$DOCUMENT_ORIGINAL_FILENAME",
    "file_name": "$DOCUMENT_FILE_NAME",
    "created": "$DOCUMENT_CREATED",
    "added": "$DOCUMENT_ADDED",
    "archive_path": "$DOCUMENT_ARCHIVE_PATH",
    "source_path": "$DOCUMENT_SOURCE_PATH",
    "correspondent": "$DOCUMENT_CORRESPONDENT",
    "tags": "$DOCUMENT_TAGS",
    "trigger": "paperless_post_consume"
}
EOF
)

# Send to webhook
log "Calling webhook: $WEBHOOK_URL"

RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "$JSON_PAYLOAD" \
    --connect-timeout 10 \
    --max-time 30 \
    2>&1) || {
    log "ERROR: Failed to call webhook"
    # Don't fail the consume - just log the error
    exit 0
}

# Parse response
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "202" ]; then
    log "SUCCESS: Document $DOCUMENT_ID queued for processing"
    log "Response: $BODY"
else
    log "WARNING: Webhook returned $HTTP_CODE"
    log "Response: $BODY"
    # Don't fail - let Paperless continue
fi

exit 0
