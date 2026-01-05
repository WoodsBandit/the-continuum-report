#!/usr/bin/env python3
"""
Batch processor for multiple PDF documents
Processes directories of PDFs in parallel
"""

import sys
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from extract_pdf import PDFExtractor
from datetime import datetime

def process_single_pdf(pdf_path, output_dir):
    """Process a single PDF file"""
    try:
        output_path = output_dir / f"{pdf_path.stem}.md"
        extractor = PDFExtractor(pdf_path)
        result = extractor.process(output_path)
        return result
    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}", file=sys.stderr)
        return None

def batch_process(input_dir, output_dir, max_workers=4):
    """Process all PDFs in a directory"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Get all PDF files
    pdf_files = list(input_path.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files in {input_dir}")

    results = []
    completed = 0

    # Process in parallel
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_single_pdf, pdf, output_path): pdf for pdf in pdf_files}

        for future in as_completed(futures):
            pdf = futures[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
                    completed += 1
                    print(f"Progress: {completed}/{len(pdf_files)} files processed")
            except Exception as e:
                print(f"Failed to process {pdf.name}: {e}", file=sys.stderr)

    # Generate summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'input_dir': str(input_dir),
        'output_dir': str(output_dir),
        'total_files': len(pdf_files),
        'processed': len(results),
        'failed': len(pdf_files) - len(results),
        'total_people': sum(r['people'] for r in results),
        'total_orgs': sum(r['orgs'] for r in results),
        'total_locations': sum(r['locations'] for r in results),
        'total_dates': sum(r['dates'] for r in results),
        'total_quotes': sum(r['quotes'] for r in results),
        'files': results
    }

    # Save summary
    summary_path = output_path / '_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print(f"BATCH PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Files processed: {summary['processed']}/{summary['total_files']}")
    print(f"Total people: {summary['total_people']}")
    print(f"Total organizations: {summary['total_orgs']}")
    print(f"Total locations: {summary['total_locations']}")
    print(f"Total dates: {summary['total_dates']}")
    print(f"Total quotes: {summary['total_quotes']}")
    print(f"Summary saved to: {summary_path}")

    return summary

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python batch_process.py <input_dir> <output_dir> [max_workers]")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    max_workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    summary = batch_process(input_dir, output_dir, max_workers)
