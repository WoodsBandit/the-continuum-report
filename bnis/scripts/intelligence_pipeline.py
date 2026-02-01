#!/usr/bin/env python3
"""
Intelligence Pipeline for BNIS v2

Unified pipeline that orchestrates:
1. Multi-source news fetching (GDELT, RSS, NewsAPI, YouTube, Reddit, LocalNews)
2. Relevance scoring and deduplication
3. Entity matching against 2,008+ entities
4. Topic aggregation and context gathering
5. Preparation for approval workflow

This is the main entry point for automated news intelligence gathering.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from unified_fetcher import UnifiedFetcher
from entity_matcher import EntityMatcher, EntityMatch
from adapters import RawItem

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent


class IntelligencePipeline:
    """
    Main orchestrator for BNIS v2 intelligence gathering.

    Combines multi-source fetching with entity matching and
    prepares output for the approval workflow.
    """

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or BASE_DIR / "bnis" / "config" / "news_config_v2.json"

        # Output directories
        self.raw_news_dir = BASE_DIR / "raw_news"
        self.pending_dir = BASE_DIR / "pending_summaries"
        self.output_dir = BASE_DIR / "bnis" / "data" / "pipeline_output"
        self.logs_dir = BASE_DIR / "bnis" / "logs"

        # Create directories
        for d in [self.raw_news_dir, self.pending_dir, self.output_dir, self.logs_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # Initialize components
        print("Initializing Intelligence Pipeline...")
        self.fetcher = UnifiedFetcher(config_path)
        self.matcher = EntityMatcher()

        # Load config
        self.config = self._load_json(self.config_path)

        # Statistics
        self.stats = {
            "run_id": datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "items_fetched": 0,
            "items_relevant": 0,
            "entities_matched": 0,
            "high_value_items": 0,
            "by_source": {},
            "entities_found": {},
            "topics_detected": []
        }

    def _load_json(self, path: Path) -> dict:
        """Load JSON file."""
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_json(self, path: Path, data: dict) -> None:
        """Save JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def enrich_with_entities(self, item: RawItem) -> dict:
        """
        Run entity matching on an item.

        Args:
            item: RawItem to enrich

        Returns:
            Enriched item dict with entity matches
        """
        # Combine title and text for matching
        full_text = f"{item.title} {item.text}"

        # Run matcher
        matches = self.matcher.match_all(full_text)

        # Convert matches to dicts
        entity_matches = [m.to_dict() for m in matches]

        # Get entity IDs for context
        entity_ids = [m.matched_id for m in matches]
        context = self.matcher.get_entity_context(entity_ids)

        # Build enriched item
        item_dict = item.to_dict()
        item_dict["entity_enrichment"] = {
            "matches": entity_matches,
            "match_count": len(matches),
            "manifest_entities": sum(1 for m in matches if m.in_manifest),
            "networks": context.get("networks", []),
            "entity_types": context.get("types", {}),
            "high_value": any(m.in_manifest and m.confidence in ["documented", "referenced"] for m in matches)
        }

        # Track entities in stats
        for match in matches:
            self.stats["entities_matched"] += 1
            entity_id = match.matched_id
            if entity_id not in self.stats["entities_found"]:
                self.stats["entities_found"][entity_id] = {
                    "name": match.mentioned_name,
                    "count": 0,
                    "sources": []
                }
            self.stats["entities_found"][entity_id]["count"] += 1
            if item.source_type not in self.stats["entities_found"][entity_id]["sources"]:
                self.stats["entities_found"][entity_id]["sources"].append(item.source_type)

        return item_dict

    def calculate_intelligence_value(self, enriched_item: dict) -> float:
        """
        Calculate overall intelligence value of an item.

        Factors:
        - Relevance score (from keywords)
        - Entity matches (especially manifest entities)
        - Source type priority
        - Recency

        Returns:
            Float between 0 and 1
        """
        base_score = enriched_item.get("analysis", {}).get("relevance_score", 0)

        # Entity bonus
        entity_info = enriched_item.get("entity_enrichment", {})
        manifest_count = entity_info.get("manifest_entities", 0)
        total_matches = entity_info.get("match_count", 0)

        entity_bonus = min(manifest_count * 0.1 + total_matches * 0.02, 0.3)

        # High value bonus (documented entities)
        if entity_info.get("high_value"):
            entity_bonus += 0.1

        # Source type priority
        source_priorities = {
            "gdelt": 0.05,
            "rss": 0.08,
            "newsapi": 0.07,
            "youtube": 0.03,
            "reddit": 0.02,
            "local_news": 0.06
        }
        source_type = enriched_item.get("source_type", "")
        source_bonus = source_priorities.get(source_type, 0)

        total = min(base_score + entity_bonus + source_bonus, 1.0)
        return total

    def run(self, keywords: Optional[list[str]] = None,
            since_hours: int = 24,
            save_all: bool = True) -> dict:
        """
        Run the full intelligence pipeline.

        Args:
            keywords: Optional keyword filter (uses config if None)
            since_hours: Time window for fetching
            save_all: Whether to save all output files

        Returns:
            Pipeline run summary
        """
        print("\n" + "=" * 70)
        print("BNIS v2 Intelligence Pipeline")
        print(f"Run ID: {self.stats['run_id']}")
        print(f"Timestamp: {self.stats['timestamp']}")
        print("=" * 70)

        # Step 1: Fetch from all sources
        print("\n[STEP 1] Multi-source Fetch")
        print("-" * 40)

        items = self.fetcher.fetch_all(keywords, since_hours)
        self.stats["items_fetched"] = self.fetcher.stats["total_fetched"]
        self.stats["items_relevant"] = len(items)
        self.stats["by_source"] = self.fetcher.stats["by_source"]

        print(f"\nFetched: {self.stats['items_fetched']} total")
        print(f"Relevant: {self.stats['items_relevant']} after filtering")

        if not items:
            print("\nNo relevant items found. Pipeline complete.")
            return self._finalize_run([])

        # Step 2: Entity enrichment
        print("\n[STEP 2] Entity Matching")
        print("-" * 40)

        enriched_items = []
        for item in items:
            enriched = self.enrich_with_entities(item)
            enriched["intelligence_value"] = self.calculate_intelligence_value(enriched)
            enriched_items.append(enriched)

            # Track high value
            if enriched["entity_enrichment"]["high_value"]:
                self.stats["high_value_items"] += 1

        print(f"Entities matched: {self.stats['entities_matched']}")
        print(f"Unique entities: {len(self.stats['entities_found'])}")
        print(f"High-value items: {self.stats['high_value_items']}")

        # Sort by intelligence value
        enriched_items.sort(key=lambda x: x.get("intelligence_value", 0), reverse=True)

        # Step 3: Topic detection (simple clustering)
        print("\n[STEP 3] Topic Detection")
        print("-" * 40)

        topics = self._detect_topics(enriched_items)
        self.stats["topics_detected"] = topics
        print(f"Topics detected: {len(topics)}")
        for topic in topics[:5]:
            print(f"  - {topic['name']} ({topic['item_count']} items)")

        # Step 4: Save outputs
        print("\n[STEP 4] Saving Outputs")
        print("-" * 40)

        if save_all:
            self._save_outputs(enriched_items, topics)

        return self._finalize_run(enriched_items)

    def _detect_topics(self, items: list[dict]) -> list[dict]:
        """
        Simple topic detection based on entity co-occurrence.

        Returns list of topic dicts with name, entities, and items.
        """
        topics = []

        # Group by network/entity combinations
        network_groups = {}
        for item in items:
            networks = item.get("entity_enrichment", {}).get("networks", [])
            entities = [m["matched_id"] for m in item.get("entity_enrichment", {}).get("matches", [])]

            if networks:
                key = tuple(sorted(networks))
                if key not in network_groups:
                    network_groups[key] = {
                        "networks": list(key),
                        "items": [],
                        "entities": set()
                    }
                network_groups[key]["items"].append(item["id"])
                network_groups[key]["entities"].update(entities)

        # Convert to topic list
        for key, group in network_groups.items():
            if len(group["items"]) >= 2:  # At least 2 items to form a topic
                topics.append({
                    "name": " + ".join(group["networks"]),
                    "networks": group["networks"],
                    "entities": list(group["entities"]),
                    "item_count": len(group["items"]),
                    "item_ids": group["items"]
                })

        # Sort by item count
        topics.sort(key=lambda x: x["item_count"], reverse=True)

        return topics

    def _save_outputs(self, items: list[dict], topics: list[dict]) -> None:
        """Save all output files."""
        run_id = self.stats["run_id"]

        # Save enriched items
        items_file = self.output_dir / f"enriched_items_{run_id}.json"
        self._save_json(items_file, {"items": items, "count": len(items)})
        print(f"Saved: {items_file.name}")

        # Save topics
        topics_file = self.output_dir / f"topics_{run_id}.json"
        self._save_json(topics_file, {"topics": topics, "count": len(topics)})
        print(f"Saved: {topics_file.name}")

        # Save high-value items for approval
        high_value = [i for i in items if i.get("entity_enrichment", {}).get("high_value")]
        if high_value:
            pending_file = self.pending_dir / f"pending_{run_id}.json"
            self._save_json(pending_file, {
                "items": high_value,
                "count": len(high_value),
                "awaiting_approval": True,
                "generated_at": self.stats["timestamp"]
            })
            print(f"Saved for approval: {pending_file.name} ({len(high_value)} items)")

        # Save run log
        log_file = self.logs_dir / f"pipeline_{run_id}.json"
        self._save_json(log_file, self.stats)
        print(f"Saved: {log_file.name}")

        # Update latest symlink / reference
        latest_file = self.output_dir / "latest_run.json"
        self._save_json(latest_file, {
            "run_id": run_id,
            "timestamp": self.stats["timestamp"],
            "items_file": str(items_file),
            "topics_file": str(topics_file),
            "stats": self.stats
        })

    def _finalize_run(self, items: list[dict]) -> dict:
        """Finalize and return run summary."""
        summary = {
            "run_id": self.stats["run_id"],
            "timestamp": self.stats["timestamp"],
            "success": True,
            "stats": self.stats,
            "top_items": [],
            "top_entities": []
        }

        # Top 5 items by intelligence value
        for item in items[:5]:
            summary["top_items"].append({
                "id": item.get("id"),
                "title": item.get("content", {}).get("title", "")[:80],
                "source": item.get("source_type"),
                "intelligence_value": round(item.get("intelligence_value", 0), 3),
                "entities": [m["matched_id"] for m in item.get("entity_enrichment", {}).get("matches", [])]
            })

        # Top entities by mention count
        entity_list = [
            {"id": k, "name": v["name"], "count": v["count"], "sources": v["sources"]}
            for k, v in self.stats["entities_found"].items()
        ]
        entity_list.sort(key=lambda x: x["count"], reverse=True)
        summary["top_entities"] = entity_list[:10]

        print("\n" + "=" * 70)
        print("Pipeline Run Complete")
        print("=" * 70)
        print(f"\nSummary:")
        print(f"  Items fetched: {self.stats['items_fetched']}")
        print(f"  Items relevant: {self.stats['items_relevant']}")
        print(f"  Entities matched: {self.stats['entities_matched']}")
        print(f"  High-value items: {self.stats['high_value_items']}")
        print(f"  Topics detected: {len(self.stats['topics_detected'])}")

        if summary["top_entities"]:
            print(f"\nTop Entities:")
            for e in summary["top_entities"][:5]:
                print(f"  - {e['name']}: {e['count']} mentions")

        return summary


def main():
    """Run the intelligence pipeline."""
    pipeline = IntelligencePipeline()

    # Run with default config
    result = pipeline.run(since_hours=72)

    # Print final summary
    print("\n" + "=" * 70)
    print("Final Run Summary")
    print("=" * 70)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
