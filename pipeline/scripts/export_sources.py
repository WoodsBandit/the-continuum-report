#!/usr/bin/env python3
"""
export_sources.py - Export source documents from Paperless to website sources directory
Version 2.0 - Refactored with Shared Library

Connects to Paperless API, finds documents tagged with case tags,
downloads the original PDFs, and saves them with standardized naming.

Changes in v2.0:
- Uses centralized configuration (lib.config)
- Uses PaperlessClient with retry logic (lib.paperless_client)
- Structured logging with structlog (lib.logging_config)
- No hardcoded secrets - uses environment variables
- Path handling with pathlib

Usage:
    python export_sources.py [--dry-run] [--case CASE_NAME]
    python export_sources.py --all-cases
"""

import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Import shared library
from lib import settings, get_logger, PaperlessClient, PaperlessError

# Initialize logger
logger = get_logger(__name__)

# Configuration (from centralized config)
OUTPUT_BASE_DIR = Path(settings.continuum_base_dir) / "website" / "sources"

# Case configurations - maps tag IDs to case info
CASES = {
    14: {
        "tag_name": "CASE: Giuffre-v-Maxwell",
        "folder": "giuffre-v-maxwell",
        "case_citation": "Giuffre v. Maxwell, No. 15-cv-07433-LAP (S.D.N.Y.)",
        "pacer_url": "https://pacer.uscourts.gov",
    },
    15: {
        "tag_name": "CASE: Epstein-SDNY",
        "folder": "epstein-sdny",
        "case_citation": "United States v. Epstein, No. 19-cr-00490 (S.D.N.Y.)",
        "pacer_url": "https://pacer.uscourts.gov",
    },
    16: {
        "tag_name": "CASE:Maxwell-Criminal",
        "folder": "maxwell-criminal",
        "case_citation": "United States v. Maxwell, No. 20-cr-00330 (S.D.N.Y.)",
        "pacer_url": "https://pacer.uscourts.gov",
    },
}

# Ensure directory exists
OUTPUT_BASE_DIR.mkdir(parents=True, exist_ok=True)


def get_paperless_client() -> PaperlessClient:
    """Get a configured Paperless client."""
    return PaperlessClient()


def get_all_tags() -> List[dict]:
    """Fetch all tags from Paperless"""
    try:
        with get_paperless_client() as client:
            tags = client.get_all_tags()
            # Convert dict to list format
            return [{"id": tag_id, "name": name} for name, tag_id in tags.items()]
    except PaperlessError as e:
        logger.error("Failed to fetch tags", error=str(e))
        return []


def get_documents_by_tag(tag_id: int) -> List[dict]:
    """Fetch all documents with a specific tag"""
    logger.info("Fetching documents by tag", tag_id=tag_id)
    try:
        with get_paperless_client() as client:
            documents = client.get_documents_by_tag(tag_id)
            logger.info("Documents fetched", tag_id=tag_id, count=len(documents))
            return documents
    except PaperlessError as e:
        logger.error("Failed to fetch documents", tag_id=tag_id, error=str(e))
        print(f"  Error fetching documents: {e}")
        return []


def get_all_documents() -> List[dict]:
    """Fetch all documents from Paperless"""
    logger.info("Fetching all documents")
    try:
        with get_paperless_client() as client:
            documents = client.get_all_documents()
            logger.info("All documents fetched", count=len(documents))
            return documents
    except PaperlessError as e:
        logger.error("Failed to fetch all documents", error=str(e))
        return []


def extract_ecf_number(doc: dict) -> Optional[str]:
    """Extract ECF document number from document title or filename"""
    title = doc.get("title", "")
    original_name = doc.get("original_file_name", "")

    # Standard patterns
    patterns = [
        r'ECF\s*(?:Doc\.?\s*)?(\d+(?:-\d+)?)',
        r'Doc\.?\s*(\d+(?:-\d+)?)',
        r'Exhibit\s*(\d+(?:-\d+)?)',
        r'^(\d{3,4}-\d{1,3})$',
        r'^(\d{3,4}-\d{1,3})\.',
    ]

    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            return match.group(1)

    # PACER-style filename: gov.uscourts.nysd.447706.1328.44
    pacer_pattern = r'gov\.uscourts\.\w+\.\d+\.(\d+)\.(\d+)'
    pacer_match = re.search(pacer_pattern, title) or re.search(pacer_pattern, original_name)
    if pacer_match:
        return f"{pacer_match.group(1)}-{pacer_match.group(2)}"

    # With suffix: gov.uscourts.nysd.447706.1328.44_2
    pacer_pattern2 = r'gov\.uscourts\.\w+\.\d+\.(\d+)\.(\d+)(?:_\d+)?'
    pacer_match2 = re.search(pacer_pattern2, title) or re.search(pacer_pattern2, original_name)
    if pacer_match2:
        return f"{pacer_match2.group(1)}-{pacer_match2.group(2)}"

    # Single docket number
    pacer_single = r'gov\.uscourts\.\w+\.\d+\.(\d+)(?:[._]|$)'
    single_match = re.search(pacer_single, title) or re.search(pacer_single, original_name)
    if single_match:
        return single_match.group(1)

    # Check original filename
    for pattern in patterns:
        match = re.search(pattern, original_name, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def normalize_ecf_number(ecf: str) -> str:
    """Normalize ECF number to consistent format"""
    ecf = ecf.strip()
    if '-' in ecf:
        parts = ecf.split('-')
        return f"{parts[0]}-{parts[1]}"
    return ecf


def generate_filename(ecf: str) -> str:
    """Generate standardized filename from ECF number"""
    normalized = normalize_ecf_number(ecf)
    return f"ecf-{normalized}.pdf"


def download_document(doc_id: int, output_path: Path) -> bool:
    """Download the original document from Paperless"""
    logger.debug("Downloading document", doc_id=doc_id, output=str(output_path))
    try:
        with get_paperless_client() as client:
            content = client.download_document(doc_id)
            if content:
                with open(output_path, 'wb') as f:
                    f.write(content)
                logger.info("Document downloaded", doc_id=doc_id, size_kb=len(content)/1024)
                return True
            return False
    except PaperlessError as e:
        logger.error("Download failed", doc_id=doc_id, error=str(e))
        print(f"  Error: {e}")
        return False


def process_case(tag_id: int, case_info: dict, dry_run: bool = False) -> dict:
    """Process all documents for a single case"""
    folder = case_info["folder"]
    tag_name = case_info["tag_name"]
    output_dir = OUTPUT_BASE_DIR / folder

    logger.info("Processing case", tag_id=tag_id, case=folder, dry_run=dry_run)

    results = {
        "case": folder,
        "tag_name": tag_name,
        "case_citation": case_info["case_citation"],
        "documents_found": 0,
        "documents_exported": 0,
        "documents_skipped": 0,
        "documents_error": 0,
        "ecf_documents": [],
        "non_ecf_documents": [],
    }

    print(f"\n{'='*60}")
    print(f"CASE: {tag_name}")
    print(f"Folder: {folder}")
    print(f"{'='*60}")

    # Create output directory
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Fetch documents
    documents = get_documents_by_tag(tag_id)
    results["documents_found"] = len(documents)
    print(f"Found {len(documents)} documents")

    # Process each document
    for doc in documents:
        doc_id = doc.get("id")
        title = doc.get("title", "Unknown")[:50]

        ecf = extract_ecf_number(doc)

        if not ecf:
            results["non_ecf_documents"].append({
                "id": doc_id,
                "title": doc.get("title"),
            })
            results["documents_skipped"] += 1
            continue

        filename = generate_filename(ecf)
        file_path = output_dir / filename

        doc_record = {
            "ecf": ecf,
            "filename": filename,
            "title": doc.get("title"),
            "doc_id": doc_id,
            "path": str(file_path),
        }

        if dry_run:
            print(f"  [DRY] ECF {ecf}: {filename}")
            doc_record["status"] = "dry_run"
            results["ecf_documents"].append(doc_record)
            continue

        if file_path.exists():
            print(f"  [EXISTS] ECF {ecf}: {filename}")
            doc_record["status"] = "exists"
            doc_record["size_kb"] = file_path.stat().st_size / 1024
            results["ecf_documents"].append(doc_record)
            results["documents_skipped"] += 1
            continue

        print(f"  [DOWNLOAD] ECF {ecf}: {filename}...", end=" ")
        if download_document(doc_id, file_path):
            size_kb = file_path.stat().st_size / 1024
            print(f"OK ({size_kb:.1f} KB)")
            doc_record["status"] = "downloaded"
            doc_record["size_kb"] = size_kb
            results["documents_exported"] += 1
        else:
            print("FAILED")
            doc_record["status"] = "error"
            results["documents_error"] += 1

        results["ecf_documents"].append(doc_record)

    # Save case manifest
    if not dry_run:
        manifest_path = output_dir / "manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump({
                "case": folder,
                "case_citation": case_info["case_citation"],
                "generated": datetime.utcnow().isoformat() + "Z",
                "documents": results["ecf_documents"],
            }, f, indent=2)

    return results


def generate_report(all_results: List[dict], output_path: Path):
    """Generate a comprehensive export report"""
    report = {
        "generated": datetime.utcnow().isoformat() + "Z",
        "summary": {
            "total_cases": len(all_results),
            "total_documents_found": 0,
            "total_documents_exported": 0,
            "total_documents_skipped": 0,
            "total_documents_error": 0,
            "total_documents_without_ecf": 0,
        },
        "cases": [],
        "missing_documents": [],
    }

    for result in all_results:
        report["summary"]["total_documents_found"] += result["documents_found"]
        report["summary"]["total_documents_exported"] += result["documents_exported"]
        report["summary"]["total_documents_skipped"] += result["documents_skipped"]
        report["summary"]["total_documents_error"] += result["documents_error"]
        report["summary"]["total_documents_without_ecf"] += len(result["non_ecf_documents"])

        report["cases"].append({
            "case": result["case"],
            "tag_name": result["tag_name"],
            "case_citation": result["case_citation"],
            "documents_found": result["documents_found"],
            "documents_exported": result["documents_exported"],
            "ecf_count": len(result["ecf_documents"]),
        })

        # Track non-ECF documents as potentially missing
        for doc in result["non_ecf_documents"]:
            report["missing_documents"].append({
                "case": result["case"],
                "doc_id": doc["id"],
                "title": doc["title"],
                "reason": "No ECF number found",
            })

    # Save report
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

    return report


def print_summary(report: dict):
    """Print a summary of the export"""
    print("\n" + "=" * 60)
    print("EXPORT SUMMARY")
    print("=" * 60)

    s = report["summary"]
    print(f"Total cases processed: {s['total_cases']}")
    print(f"Total documents found: {s['total_documents_found']}")
    print(f"Documents exported: {s['total_documents_exported']}")
    print(f"Documents skipped (exists): {s['total_documents_skipped']}")
    print(f"Documents with errors: {s['total_documents_error']}")
    print(f"Documents without ECF number: {s['total_documents_without_ecf']}")

    print("\nBy Case:")
    print("-" * 40)
    for case in report["cases"]:
        print(f"  {case['case']}: {case['ecf_count']} ECF documents")

    if report["missing_documents"]:
        print(f"\nDocuments Missing ECF Numbers ({len(report['missing_documents'])}):")
        print("-" * 40)
        for doc in report["missing_documents"][:10]:
            print(f"  [{doc['case']}] #{doc['doc_id']}: {doc['title'][:40]}...")
        if len(report["missing_documents"]) > 10:
            print(f"  ... and {len(report['missing_documents']) - 10} more")


def main():
    parser = argparse.ArgumentParser(description="Export Paperless documents to website sources")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be downloaded")
    parser.add_argument("--case", type=str, help="Process only this case folder name")
    parser.add_argument("--all-cases", action="store_true", help="Process all configured cases")
    parser.add_argument("--tag", type=int, help="Process specific tag ID")
    args = parser.parse_args()

    logger.info("Export started", dry_run=args.dry_run, case=args.case, tag=args.tag)

    print("=" * 60)
    print("PAPERLESS SOURCE DOCUMENT EXPORTER v2.0")
    print("=" * 60)
    print(f"Paperless URL: {settings.paperless_url}")
    print(f"Output directory: {OUTPUT_BASE_DIR}")
    print(f"Dry run: {args.dry_run}")

    all_results = []

    # Determine which cases to process
    if args.tag:
        if args.tag in CASES:
            cases_to_process = {args.tag: CASES[args.tag]}
        else:
            print(f"Unknown tag ID: {args.tag}")
            return 1
    elif args.case:
        # Find case by folder name
        cases_to_process = {
            tid: info for tid, info in CASES.items()
            if info["folder"] == args.case
        }
        if not cases_to_process:
            print(f"Unknown case: {args.case}")
            return 1
    elif args.all_cases:
        cases_to_process = CASES
    else:
        # Default to all cases
        cases_to_process = CASES

    # Process each case
    for tag_id, case_info in cases_to_process.items():
        result = process_case(tag_id, case_info, dry_run=args.dry_run)
        all_results.append(result)

    # Generate and save report
    if not args.dry_run:
        report_path = OUTPUT_BASE_DIR / "export_report.json"
        report = generate_report(all_results, report_path)
        logger.info("Report generated", path=str(report_path))
        print(f"\nReport saved to: {report_path}")
        print_summary(report)

        # Also create a sources index
        index_path = OUTPUT_BASE_DIR / "index.json"
        index = {
            "generated": datetime.utcnow().isoformat() + "Z",
            "cases": {}
        }
        for result in all_results:
            folder = result["case"]
            index["cases"][folder] = {
                "case_citation": result["case_citation"],
                "documents": [
                    {
                        "ecf": d["ecf"],
                        "filename": d["filename"],
                        "available": d.get("status") in ["downloaded", "exists"],
                    }
                    for d in result["ecf_documents"]
                ]
            }
        with open(index_path, 'w') as f:
            json.dump(index, f, indent=2)
        logger.info("Index saved", path=str(index_path))
        print(f"Index saved to: {index_path}")
    else:
        # Print dry run summary
        print("\n" + "=" * 60)
        print("DRY RUN SUMMARY")
        print("=" * 60)
        total_ecf = sum(len(r["ecf_documents"]) for r in all_results)
        total_non_ecf = sum(len(r["non_ecf_documents"]) for r in all_results)
        print(f"Would export {total_ecf} ECF documents")
        print(f"Would skip {total_non_ecf} documents without ECF numbers")

    logger.info("Export complete", dry_run=args.dry_run, cases=len(all_results))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Export cancelled by user")
        print("\nCancelled.")
        sys.exit(1)
    except PaperlessError as e:
        logger.error("Paperless error", error=str(e))
        print(f"\nError: {e}")
        print("Check your PAPERLESS_TOKEN in .env file")
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error", error=str(e))
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
