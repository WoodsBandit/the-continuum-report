#!/usr/bin/env python3
"""
fix_sources.py - Properly export source documents from Paperless

Maps ECF references to Paperless documents and downloads them.
Uses environment variables for credentials (no hardcoded secrets).
"""

import datetime
import json
import os
import re
import sys
from pathlib import Path

import requests

# Load from environment - no hardcoded secrets
PAPERLESS_URL = os.environ.get("PAPERLESS_URL", "http://192.168.1.139:8040")
API_TOKEN = os.environ.get("PAPERLESS_TOKEN", "")

if not API_TOKEN:
    print("ERROR: PAPERLESS_TOKEN environment variable required")
    print("Set it via: export PAPERLESS_TOKEN=your_token_here")
    sys.exit(1)

# Paths - can be overridden via environment
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "/continuum/website/sources/giuffre-v-maxwell"))
BRIEFS_DIR = Path(os.environ.get("BRIEFS_DIR", "/continuum/briefs"))

HEADERS = {
    "Authorization": f"Token {API_TOKEN}",
    "Accept": "application/json",
}


def get_all_documents():
    """Fetch all documents from Paperless"""
    documents = []
    page = 1
    while True:
        response = requests.get(
            f"{PAPERLESS_URL}/api/documents/",
            headers=HEADERS,
            params={"page": page, "page_size": 100}
        )
        if response.status_code != 200:
            break
        data = response.json()
        documents.extend(data.get("results", []))
        if not data.get("next"):
            break
        page += 1
    return documents


def extract_ecf_from_title(title):
    """Extract ECF number from document title"""
    # Simple format: "1320-9" or "1328-44"
    simple_match = re.match(r'^(\d{4})-(\d{1,2})$', title.strip())
    if simple_match:
        return f"{simple_match.group(1)}-{simple_match.group(2)}"

    # PACER format: gov.uscourts.nysd.447706.1328.44_2
    pacer_match = re.search(r'gov\.uscourts\.\w+\.\d+\.(\d{4})\.(\d{1,2})(?:_\d+)?', title)
    if pacer_match:
        return f"{pacer_match.group(1)}-{pacer_match.group(2)}"

    return None


def get_ecf_references_from_briefs():
    """Extract all ECF references from analytical briefs"""
    ecf_refs = set()
    for brief_file in BRIEFS_DIR.glob("*.md"):
        content = brief_file.read_text()
        # Match patterns like 1320-9, 1328-44
        matches = re.findall(r'\b(1[0-9]{3})-(\d{1,2})\b', content)
        for m in matches:
            ecf_refs.add(f"{m[0]}-{m[1]}")
    return sorted(ecf_refs)


def build_ecf_to_doc_mapping(documents):
    """Build mapping from ECF number to Paperless document"""
    mapping = {}
    for doc in documents:
        title = doc.get("title", "")
        orig_name = doc.get("original_file_name", "")
        doc_id = doc.get("id")

        # Try to extract ECF from title
        ecf = extract_ecf_from_title(title)
        if not ecf:
            # Try original filename
            ecf = extract_ecf_from_title(orig_name.replace(".pdf", ""))

        if ecf:
            # If we have multiple docs for same ECF, prefer the one with simpler title
            if ecf not in mapping or len(title) < len(mapping[ecf]["title"]):
                mapping[ecf] = {
                    "id": doc_id,
                    "title": title,
                    "original_file_name": orig_name
                }

    return mapping


def download_document(doc_id, output_path):
    """Download document from Paperless"""
    try:
        response = requests.get(
            f"{PAPERLESS_URL}/api/documents/{doc_id}/download/",
            headers=HEADERS,
            stream=True
        )
        if response.status_code != 200:
            return False

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    print("=" * 60)
    print("PAPERLESS SOURCE DOCUMENT FIXER")
    print("=" * 60)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Get all documents from Paperless
    print("\nFetching documents from Paperless...")
    documents = get_all_documents()
    print(f"Found {len(documents)} total documents in Paperless")

    # Build ECF mapping
    print("\nBuilding ECF to document mapping...")
    ecf_mapping = build_ecf_to_doc_mapping(documents)
    print(f"Mapped {len(ecf_mapping)} documents to ECF numbers")

    # Get ECF references from briefs
    print("\nExtracting ECF references from briefs...")
    brief_ecfs = get_ecf_references_from_briefs()
    print(f"Found {len(brief_ecfs)} unique ECF references in briefs")

    # Show mapping
    print("\n" + "=" * 60)
    print("ECF MAPPING")
    print("=" * 60)

    found = []
    missing = []

    for ecf in brief_ecfs:
        if ecf in ecf_mapping:
            doc = ecf_mapping[ecf]
            found.append((ecf, doc))
            print(f"  [FOUND] ECF {ecf} -> Doc #{doc['id']}: {doc['title'][:40]}")
        else:
            missing.append(ecf)
            print(f"  [MISSING] ECF {ecf} - NOT IN PAPERLESS")

    print(f"\nFound: {len(found)}, Missing: {len(missing)}")

    # Download found documents
    print("\n" + "=" * 60)
    print("DOWNLOADING DOCUMENTS")
    print("=" * 60)

    downloaded = 0
    skipped = 0
    errors = 0

    for ecf, doc in found:
        filename = f"ecf-{ecf}.pdf"
        output_path = OUTPUT_DIR / filename

        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"  [EXISTS] {filename} ({size_kb:.1f} KB)")
            skipped += 1
            continue

        print(f"  [DOWNLOAD] {filename}...", end=" ", flush=True)
        if download_document(doc["id"], output_path):
            size_kb = output_path.stat().st_size / 1024
            print(f"OK ({size_kb:.1f} KB)")
            downloaded += 1
        else:
            print("FAILED")
            errors += 1

    # Generate index.json
    print("\n" + "=" * 60)
    print("GENERATING INDEX")
    print("=" * 60)

    index = {
        "generated": datetime.datetime.utcnow().isoformat() + "Z",
        "cases": {
            "giuffre-v-maxwell": {
                "case_citation": "Giuffre v. Maxwell, No. 15-cv-07433-LAP (S.D.N.Y.)",
                "documents": []
            }
        }
    }

    for ecf, doc in found:
        filename = f"ecf-{ecf}.pdf"
        file_path = OUTPUT_DIR / filename
        index["cases"]["giuffre-v-maxwell"]["documents"].append({
            "ecf": ecf,
            "filename": filename,
            "available": file_path.exists(),
            "paperless_id": doc["id"]
        })

    # Add missing ECFs to index (marked as unavailable)
    for ecf in missing:
        index["cases"]["giuffre-v-maxwell"]["documents"].append({
            "ecf": ecf,
            "filename": f"ecf-{ecf}.pdf",
            "available": False,
            "paperless_id": None
        })

    index_path = Path("/continuum/website/sources/index.json")
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
    print(f"Index saved to: {index_path}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"ECF references in briefs: {len(brief_ecfs)}")
    print(f"Matched to Paperless: {len(found)}")
    print(f"Not in Paperless: {len(missing)}")
    print(f"Downloaded: {downloaded}")
    print(f"Already existed: {skipped}")
    print(f"Errors: {errors}")

    if missing:
        print(f"\nMissing ECFs that need to be added to Paperless:")
        for ecf in missing:
            print(f"  - {ecf}")

    # List what's actually in the output folder
    print(f"\nFiles in {OUTPUT_DIR}:")
    files = list(OUTPUT_DIR.glob("*.pdf"))
    print(f"  {len(files)} PDF files")


if __name__ == "__main__":
    main()
