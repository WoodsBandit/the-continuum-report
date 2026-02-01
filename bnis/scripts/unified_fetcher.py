#!/usr/bin/env python3
"""
Unified Fetcher for BNIS v2

Orchestrates all source adapters to fetch news from multiple sources,
normalize to common format, and deduplicate across sources.

Features:
- Parallel fetching from multiple sources
- Cross-source deduplication
- Unified relevance scoring
- Topic detection and fan-out triggering
"""

import json
import hashlib
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import adapters
from adapters import (
    GDELTAdapter, RSSAdapter, NewsAPIAdapter,
    YouTubeAdapter, RedditAdapter, LocalNewsAdapter, RawItem
)

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent


class UnifiedFetcher:
    """
    Orchestrates multi-source news fetching.
    """

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or BASE_DIR / "bnis" / "config" / "news_config_v2.json"
        self.raw_news_dir = BASE_DIR / "raw_news"
        self.dedup_file = BASE_DIR / "bnis" / "data" / "unified_hashes.json"

        # Create directories
        self.raw_news_dir.mkdir(parents=True, exist_ok=True)
        (BASE_DIR / "bnis" / "data").mkdir(parents=True, exist_ok=True)

        # Load config
        self.config = self._load_json(self.config_path)

        # Initialize adapters
        self.adapters = self._init_adapters()

        # Load dedup hashes
        self.seen_hashes = self._load_dedup_hashes()

        # Build keyword sets
        self.keywords = self._build_keywords()

        # Stats
        self.stats = {
            "total_fetched": 0,
            "duplicates": 0,
            "relevant": 0,
            "saved": 0,
            "by_source": {}
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

    def _init_adapters(self) -> dict:
        """Initialize all enabled adapters."""
        adapters = {}
        adapter_configs = self.config.get("adapters", {})

        # GDELT adapter (free, no API key)
        if "gdelt" in adapter_configs:
            gdelt_config = adapter_configs["gdelt"]
            if gdelt_config.get("enabled", False):
                adapters["gdelt"] = GDELTAdapter(gdelt_config)
                print("Initialized: GDELT adapter")

        # RSS adapter (free, no API key)
        if "rss" in adapter_configs:
            rss_config = adapter_configs["rss"]
            if rss_config.get("enabled", False):
                adapters["rss"] = RSSAdapter(rss_config)
                print("Initialized: RSS adapter")

        # NewsAPI adapter (requires API key)
        if "newsapi" in adapter_configs:
            newsapi_config = adapter_configs["newsapi"]
            if newsapi_config.get("enabled", False):
                adapter = NewsAPIAdapter(newsapi_config)
                if adapter.is_enabled():
                    adapters["newsapi"] = adapter
                    print("Initialized: NewsAPI adapter")

        # YouTube adapter (requires API key)
        if "youtube" in adapter_configs:
            youtube_config = adapter_configs["youtube"]
            if youtube_config.get("enabled", False):
                adapter = YouTubeAdapter(youtube_config)
                if adapter.is_enabled():
                    adapters["youtube"] = adapter
                    print("Initialized: YouTube adapter")

        # Reddit adapter (requires OAuth credentials)
        if "reddit" in adapter_configs:
            reddit_config = adapter_configs["reddit"]
            if reddit_config.get("enabled", False):
                adapter = RedditAdapter(reddit_config)
                if adapter.is_enabled():
                    adapters["reddit"] = adapter
                    print("Initialized: Reddit adapter")

        # Local News adapter (free, RSS-based)
        if "local_news" in adapter_configs:
            local_config = adapter_configs["local_news"]
            if local_config.get("enabled", False):
                adapters["local_news"] = LocalNewsAdapter(local_config)
                print("Initialized: LocalNews adapter")

        # TODO: Add Twitter adapter (RSSHub-based, already exists in v1)

        return adapters

    def _load_dedup_hashes(self) -> dict:
        """Load seen hashes for deduplication."""
        data = self._load_json(self.dedup_file)

        # Clean old hashes
        window_hours = self.config.get("global", {}).get("dedup_window_hours", 48)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
        cutoff_str = cutoff.isoformat()

        return {h: ts for h, ts in data.items() if ts > cutoff_str}

    def _save_dedup_hashes(self) -> None:
        """Save dedup hashes."""
        self._save_json(self.dedup_file, self.seen_hashes)

    def _build_keywords(self) -> dict:
        """Build keyword sets from config."""
        kw_config = self.config.get("keywords", {})
        return {
            "high": set(k.lower() for k in kw_config.get("high_priority", [])),
            "medium": set(k.lower() for k in kw_config.get("medium_priority", [])),
            "low": set(k.lower() for k in kw_config.get("low_priority", [])),
            "all": set(
                k.lower() for k in
                kw_config.get("high_priority", []) +
                kw_config.get("medium_priority", []) +
                kw_config.get("low_priority", [])
            )
        }

    def content_hash(self, text: str) -> str:
        """Generate hash for deduplication."""
        normalized = re.sub(r'\s+', ' ', text.strip().lower())
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()[:16]

    def is_duplicate(self, item: RawItem) -> bool:
        """Check if item is duplicate."""
        # Hash on title + source URL
        content = f"{item.title}{item.source_url}"
        hash_val = self.content_hash(content)
        return hash_val in self.seen_hashes

    def mark_seen(self, item: RawItem) -> str:
        """Mark item as seen."""
        content = f"{item.title}{item.source_url}"
        hash_val = self.content_hash(content)
        self.seen_hashes[hash_val] = datetime.now(timezone.utc).isoformat()
        return hash_val

    def calculate_relevance(self, item: RawItem) -> tuple[float, list[str]]:
        """
        Calculate relevance score for an item.

        Returns:
            (score, matched_keywords)
        """
        text = f"{item.title} {item.text}".lower()
        matched = []

        # Check all keywords
        for kw in self.keywords["all"]:
            if kw in text:
                matched.append(kw)

        if not matched:
            return 0.0, []

        # Score based on priority
        high_matches = sum(1 for kw in matched if kw in self.keywords["high"])
        med_matches = sum(1 for kw in matched if kw in self.keywords["medium"])

        # Base score from quantity
        base_score = min(len(matched) / 5, 0.4)

        # Priority bonuses
        high_bonus = min(high_matches * 0.2, 0.4)
        med_bonus = min(med_matches * 0.1, 0.2)

        total = min(base_score + high_bonus + med_bonus, 1.0)

        return total, matched

    def fetch_from_adapter(self, adapter_name: str, keywords: list[str],
                           since_hours: int = 24) -> list[RawItem]:
        """Fetch from a single adapter."""
        adapter = self.adapters.get(adapter_name)
        if not adapter:
            return []

        try:
            items = adapter.fetch(keywords, since_hours)
            self.stats["by_source"][adapter_name] = len(items)
            return items
        except Exception as e:
            print(f"Error fetching from {adapter_name}: {e}")
            self.stats["by_source"][adapter_name] = 0
            return []

    def fetch_all(self, keywords: Optional[list[str]] = None,
                  since_hours: int = 24) -> list[RawItem]:
        """
        Fetch from all enabled adapters.

        Args:
            keywords: Keywords to search (uses config if None)
            since_hours: Time window

        Returns:
            Deduplicated, scored list of RawItem
        """
        if keywords is None:
            keywords = list(self.keywords["high"])[:10]  # Top 10 high priority

        all_items = []

        print(f"\n{'='*60}")
        print(f"Unified Fetcher - {datetime.now(timezone.utc).isoformat()}")
        print(f"Keywords: {keywords}")
        print(f"Adapters: {list(self.adapters.keys())}")
        print(f"{'='*60}\n")

        # Fetch from each adapter
        for adapter_name in self.adapters:
            print(f"\nFetching from {adapter_name}...")
            items = self.fetch_from_adapter(adapter_name, keywords, since_hours)
            all_items.extend(items)
            print(f"  Got {len(items)} items")

        self.stats["total_fetched"] = len(all_items)
        print(f"\nTotal fetched: {len(all_items)}")

        # Deduplicate and score
        processed = []
        for item in all_items:
            if self.is_duplicate(item):
                self.stats["duplicates"] += 1
                continue

            # Calculate relevance
            score, matched = self.calculate_relevance(item)
            item.relevance_score = score
            item.keywords_matched = matched

            # Check threshold
            min_score = self.config.get("thresholds", {}).get("min_relevance_score", 0.6)
            if score >= min_score:
                self.mark_seen(item)
                processed.append(item)
                self.stats["relevant"] += 1

        print(f"After dedup/scoring: {len(processed)} relevant items")
        print(f"Duplicates skipped: {self.stats['duplicates']}")

        # Sort by relevance
        processed.sort(key=lambda x: x.relevance_score, reverse=True)

        return processed

    def save_items(self, items: list[RawItem]) -> list[Path]:
        """Save items to raw_news directory."""
        saved = []

        for item in items:
            filename = f"{item.id}.json"
            filepath = self.raw_news_dir / filename

            self._save_json(filepath, item.to_dict())
            saved.append(filepath)
            self.stats["saved"] += 1

        return saved

    def run(self, keywords: Optional[list[str]] = None,
            since_hours: int = 24) -> dict:
        """
        Run full fetch cycle.

        Returns:
            Stats and saved item IDs
        """
        # Fetch
        items = self.fetch_all(keywords, since_hours)

        # Save
        saved_paths = self.save_items(items)

        # Save dedup hashes
        self._save_dedup_hashes()

        # Summary
        print(f"\n{'='*60}")
        print("Fetch Summary:")
        print(f"  Total fetched: {self.stats['total_fetched']}")
        print(f"  Duplicates: {self.stats['duplicates']}")
        print(f"  Relevant: {self.stats['relevant']}")
        print(f"  Saved: {self.stats['saved']}")
        print(f"  By source: {self.stats['by_source']}")
        print(f"{'='*60}\n")

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "stats": self.stats,
            "saved_items": [str(p) for p in saved_paths]
        }


def main():
    """Run the unified fetcher."""
    fetcher = UnifiedFetcher()

    # Use high priority keywords from config
    result = fetcher.run(since_hours=72)

    # Save run log
    log_dir = BASE_DIR / "bnis" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"unified_fetch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

    print(f"Log saved: {log_file}")


if __name__ == "__main__":
    main()
