#!/usr/bin/env python3
"""Create missing tags in Paperless-ngx.

This script creates required tags if they don't already exist.
Uses environment variables for credentials (no hardcoded secrets).
"""
import os
import sys

import requests

# Load from environment or .env file
PAPERLESS_URL = os.environ.get("PAPERLESS_URL", "http://localhost:8040")
TOKEN = os.environ.get("PAPERLESS_TOKEN", "")

if not TOKEN:
    print("ERROR: PAPERLESS_TOKEN environment variable required")
    print("Set it via: export PAPERLESS_TOKEN=your_token_here")
    print("Or create a .env file with PAPERLESS_TOKEN=your_token")
    sys.exit(1)

headers = {"Authorization": f"Token {TOKEN}", "Content-Type": "application/json"}

# Required tags that may be missing
required_tags = [
    "TYPE:DEPOSITION", "TYPE:FBI-FILE", "TYPE:CIA-DOCUMENT", "TYPE:FOIA-RELEASE",
    "TYPE:SEC-FILING", "TYPE:FINANCIAL-RECORD", "TYPE:MEDIA-REPORT",
    "TYPE:CONGRESSIONAL-HEARING", "CASE:MAXWELL-CRIMINAL", "CASE:JANE-DOE-V-JPMORGAN",
    "PERSON:LESLIE-WEXNER", "PERSON:ALAN-DERSHOWITZ", "PERSON:PRINCE-ANDREW",
    "PERSON:BILL-CLINTON", "PERSON:DONALD-TRUMP", "PERSON:ROY-COHN",
    "PERSON:SARAH-KELLEN", "PERSON:NADIA-MARCINKOVA", "ORG:L-BRANDS",
    "NETWORK:POLITICAL", "LAYER:4-POLITICAL", "LAYER:6-DECLASSIFIED",
    "PRIORITY:LOW", "UNVERIFIED:LEAKED", "VERIFIED:PRIMARY-SOURCE"
]

# Get existing tags
resp = requests.get(f"{PAPERLESS_URL}/api/tags/?page_size=200", headers=headers)
existing = {t['name']: t['id'] for t in resp.json()['results']}

created = []
for tag in required_tags:
    if tag not in existing:
        try:
            resp = requests.post(f"{PAPERLESS_URL}/api/tags/",
                headers=headers, json={"name": tag})
            if resp.status_code == 201:
                created.append(tag)
                print(f"Created: {tag}")
            else:
                print(f"Failed to create {tag}: {resp.status_code}")
        except Exception as e:
            print(f"Error creating {tag}: {e}")

print(f"\nCreated {len(created)} new tags")
