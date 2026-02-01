#!/usr/bin/env python3
"""
Test script for GDELT adapter.
"""

import sys
from pathlib import Path

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from adapters.base import SourceAdapter, RawItem
from adapters.gdelt import GDELTAdapter
import json
import urllib.request


def debug_gdelt_api():
    """Debug raw GDELT API response."""
    print("\n[DEBUG] Testing raw GDELT API...")

    # Simple test query
    url = "https://api.gdeltproject.org/api/v2/doc/doc?query=Epstein&mode=artlist&format=json&timespan=7d&maxrecords=5"

    print(f"URL: {url}")

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BNIS/2.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
            print(f"Response length: {len(raw)} bytes")
            print(f"First 500 chars: {raw[:500]}")

            # Try to parse
            data = json.loads(raw.decode('utf-8'))
            print(f"Parsed successfully! Keys: {list(data.keys())}")

            if "articles" in data:
                print(f"Articles count: {len(data['articles'])}")
                if data['articles']:
                    print(f"First article: {json.dumps(data['articles'][0], indent=2)[:500]}")

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")


def test_gdelt():
    """Test the GDELT adapter with Epstein-related keywords."""

    config = {
        "enabled": True,
        "max_records": 25,
        "source_lang": "eng",
        "timeout_seconds": 30
    }

    adapter = GDELTAdapter(config)

    print("\n" + "="*70)
    print("GDELT Adapter Test - Breaking News Intelligence System v2")
    print("="*70)

    # Debug first
    debug_gdelt_api()

    # Test 1: Basic keyword fetch
    print("\n" + "-"*70)
    print("\n[TEST 1] Fetching news for: Epstein, Maxwell")
    keywords = ["Epstein", "Maxwell"]
    items = adapter.fetch(keywords, since_hours=168)  # Past week

    print(f"\n[OK] Fetched {len(items)} items")
    print(f"  Stats: {adapter.get_stats()}")

    if items:
        print("\n[SAMPLE RESULTS]")
        for i, item in enumerate(items[:5]):
            title = item.title[:70] if item.title else "(no title)"
            print(f"\n  [{i+1}] {title}...")
            print(f"      Source: {item.source_name}")
            print(f"      URL: {item.source_url[:60] if item.source_url else '(none)'}...")
            print(f"      Published: {item.published_at}")

    # Test 2: Topic context fetch
    print("\n" + "-"*70)
    print("\n[TEST 2] Topic context aggregation: 'DOJ releases Epstein documents'")

    adapter.reset_stats()
    context_items = adapter.fetch_topic_context(
        "DOJ releases new Epstein documents court filings",
        depth="quick"
    )

    print(f"\n[OK] Context items: {len(context_items)}")
    print(f"  Stats: {adapter.get_stats()}")

    # Test 3: Check data structure
    if items:
        print("\n" + "-"*70)
        print("\n[TEST 3] Verifying RawItem structure")
        item = items[0]
        item_dict = item.to_dict()

        print(f"  [OK] ID: {item_dict['id']}")
        print(f"  [OK] source_type: {item_dict['source_type']}")
        print(f"  [OK] content.title present: {bool(item_dict['content']['title'])}")
        print(f"  [OK] metadata.published_at: {item_dict['metadata']['published_at']}")

        # Save sample item
        sample_path = Path(__file__).parent.parent / "data" / "gdelt_sample.json"
        sample_path.parent.mkdir(parents=True, exist_ok=True)
        with open(sample_path, 'w', encoding='utf-8') as f:
            json.dump(item_dict, f, indent=2, ensure_ascii=False)
        print(f"\n  Sample saved: {sample_path}")

    print("\n" + "="*70)
    print("GDELT adapter test complete!")
    print("="*70 + "\n")

    return items


if __name__ == "__main__":
    test_gdelt()
