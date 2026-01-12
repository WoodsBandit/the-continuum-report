#!/usr/bin/env python3
"""Helper for uploading documents to Paperless-ngx.

Usage: upload_helper.py <filepath> <title> [tag1,tag2,...]

Uses environment variables for credentials (no hardcoded secrets).
"""
import json
import os
import sys

import requests

PAPERLESS_URL = os.environ.get("PAPERLESS_URL", "http://192.168.1.139:8040")
TOKEN = os.environ.get("PAPERLESS_TOKEN", "")

if not TOKEN:
    print("ERROR: PAPERLESS_TOKEN environment variable required")
    print("Set it via: export PAPERLESS_TOKEN=your_token_here")
    sys.exit(1)


def get_tag_ids(tag_names):
    """Convert tag names to IDs."""
    tag_map_path = os.path.join(os.path.dirname(__file__), 'tag_map.json')
    if os.path.exists(tag_map_path):
        with open(tag_map_path) as f:
            tag_map = json.load(f)
    else:
        try:
            with open('/continuum/downloads/tag_map.json') as f:
                tag_map = json.load(f)
        except FileNotFoundError:
            print("Warning: tag_map.json not found")
            return []

    ids = []
    for name in tag_names:
        name = name.strip()
        if name in tag_map:
            ids.append(tag_map[name])
        else:
            # Try case-insensitive and format variations
            found = False
            for key, val in tag_map.items():
                if key.lower() == name.lower():
                    ids.append(val)
                    found = True
                    break
                # Try with space variation (PERSON:X vs PERSON: X)
                if key.replace(': ', ':').lower() == name.replace(': ', ':').lower():
                    ids.append(val)
                    found = True
                    break
            if not found:
                print(f"Warning: Tag '{name}' not found")
    return ids


def upload_document(filepath, title, tag_names):
    """Upload document to Paperless-ngx."""
    headers = {"Authorization": f"Token {TOKEN}"}
    tag_ids = get_tag_ids(tag_names)

    with open(filepath, 'rb') as f:
        files = {'document': (os.path.basename(filepath), f, 'application/pdf')}

        resp = requests.post(
            f"{PAPERLESS_URL}/api/documents/post_document/",
            headers=headers,
            files=files,
            data={'title': title, 'tags': tag_ids}
        )

    if resp.status_code in [200, 202]:
        print(f"SUCCESS: Uploaded {os.path.basename(filepath)}")
        return True
    else:
        print(f"FAILED: {resp.status_code} - {resp.text[:500]}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: upload_helper.py <filepath> <title> [tag1,tag2,...]")
        sys.exit(1)

    filepath = sys.argv[1]
    title = sys.argv[2]
    tags = sys.argv[3].split(',') if len(sys.argv) > 3 else []

    success = upload_document(filepath, title, tags)
    sys.exit(0 if success else 1)
