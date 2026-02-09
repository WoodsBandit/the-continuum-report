#!/usr/bin/env python3
"""Upload a document to Paperless-ngx with tags.

Usage: upload_doc.py <filepath> <title> <tags>

Uses environment variables for credentials (no hardcoded secrets).
"""
import json
import os
import sys

import requests

PAPERLESS_URL = os.environ.get("PAPERLESS_URL", "http://localhost:8040")
TOKEN = os.environ.get("PAPERLESS_TOKEN", "")

if not TOKEN:
    print("ERROR: PAPERLESS_TOKEN environment variable required")
    print("Set it via: export PAPERLESS_TOKEN=your_token_here")
    sys.exit(1)

# Load tag map
tag_map_path = os.path.join(os.path.dirname(__file__), 'tag_map.json')
if os.path.exists(tag_map_path):
    with open(tag_map_path) as f:
        TAG_MAP = json.load(f)
else:
    # Fallback to /continuum path for backward compatibility
    try:
        with open('/continuum/downloads/tag_map.json') as f:
            TAG_MAP = json.load(f)
    except FileNotFoundError:
        TAG_MAP = {}
        print("Warning: tag_map.json not found, tag resolution disabled")


def get_tag_id(tag_name):
    """Resolve tag name to ID."""
    tag_name = tag_name.strip()
    if tag_name in TAG_MAP:
        return TAG_MAP[tag_name]
    # Try variations
    for key, val in TAG_MAP.items():
        if key.lower() == tag_name.lower():
            return val
        if key.replace(': ', ':').lower() == tag_name.replace(': ', ':').lower():
            return val
    return None


def upload(filepath, title, tags_str):
    """Upload document with specified tags."""
    headers = {"Authorization": f"Token {TOKEN}"}
    tag_names = [t.strip() for t in tags_str.split(',')]
    tag_ids = []
    for t in tag_names:
        tid = get_tag_id(t)
        if tid:
            tag_ids.append(tid)
        else:
            print(f"Warning: Tag '{t}' not found")

    with open(filepath, 'rb') as f:
        files = {'document': (os.path.basename(filepath), f, 'application/pdf')}
        data = [('title', title)]
        for tid in tag_ids:
            data.append(('tags', str(tid)))

        resp = requests.post(
            f"{PAPERLESS_URL}/api/documents/post_document/",
            headers=headers,
            files=files,
            data=data
        )

    if resp.status_code == 200:
        print(f"✓ Uploaded: {os.path.basename(filepath)}")
        return True
    else:
        print(f"✗ Failed ({resp.status_code}): {os.path.basename(filepath)}")
        print(f"  {resp.text[:200]}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: upload_doc.py <filepath> <title> <tags>")
        sys.exit(1)
    success = upload(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(0 if success else 1)
