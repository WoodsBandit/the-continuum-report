#!/usr/bin/env python3
"""
NewsAPI Adapter for BNIS v2

Fetches news from NewsAPI.org - aggregates 80,000+ sources worldwide.

API Documentation: https://newsapi.org/docs
Free tier: 100 requests/day, 1 month old articles max

Requires API key - get free key at https://newsapi.org/register
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
import os
from datetime import datetime, timezone, timedelta
from typing import Optional

try:
    from .base import SourceAdapter, RawItem
except ImportError:
    from base import SourceAdapter, RawItem


class NewsAPIAdapter(SourceAdapter):
    """
    NewsAPI.org adapter.

    Features:
    - 80,000+ news sources worldwide
    - Search by keyword, source, or domain
    - Sort by relevance, popularity, or date
    - Free tier: 100 requests/day
    """

    BASE_URL = "https://newsapi.org/v2"

    def __init__(self, config: dict):
        super().__init__(config)
        # Try config first, then environment variable
        self.api_key = config.get("api_key", "").replace("${NEWSAPI_KEY}", "")
        if not self.api_key or self.api_key.startswith("$"):
            self.api_key = os.environ.get("NEWSAPI_KEY", "")

        self.sources = config.get("sources", [])
        self.domains = config.get("domains", [])
        self.language = config.get("language", "en")
        self.sort_by = config.get("sort_by", "publishedAt")
        self.page_size = config.get("page_size", 100)
        self.timeout = config.get("timeout_seconds", 30)

    @property
    def source_type(self) -> str:
        return "newsapi"

    @property
    def rate_limits(self) -> dict:
        return {
            "requests_per_day": 100,  # Free tier
            "requests_per_minute": 10,
            "note": "Free tier: 100/day, Developer: 500/day"
        }

    def is_enabled(self) -> bool:
        """Check if adapter is enabled AND has API key."""
        if not super().is_enabled():
            return False
        if not self.api_key:
            print("NewsAPI: No API key configured (set NEWSAPI_KEY env var or api_key in config)")
            return False
        return True

    def _make_request(self, endpoint: str, params: dict) -> Optional[dict]:
        """
        Make authenticated request to NewsAPI.

        Args:
            endpoint: API endpoint (everything, top-headlines, sources)
            params: Query parameters

        Returns:
            Parsed JSON response or None on error
        """
        params_string = urllib.parse.urlencode(params)
        url = f"{self.BASE_URL}/{endpoint}?{params_string}"

        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "BNIS/2.0",
                    "X-Api-Key": self.api_key,
                    "Accept": "application/json"
                }
            )

            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                data = json.loads(response.read().decode('utf-8'))

                if data.get("status") != "ok":
                    print(f"NewsAPI Error: {data.get('message', 'Unknown error')}")
                    self._increment_stat("errors")
                    return None

                return data

        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode('utf-8')
                error_data = json.loads(error_body)
                print(f"NewsAPI HTTP {e.code}: {error_data.get('message', e.reason)}")
            except:
                print(f"NewsAPI HTTP {e.code}: {e.reason}")

            if e.code == 401:
                print("NewsAPI: Invalid API key")
            elif e.code == 429:
                print("NewsAPI: Rate limit exceeded")
                self._increment_stat("rate_limited")

            self._increment_stat("errors")
            return None

        except Exception as e:
            print(f"NewsAPI Error: {type(e).__name__}: {e}")
            self._increment_stat("errors")
            return None

    def _parse_article(self, article: dict) -> RawItem:
        """
        Parse NewsAPI article into RawItem.

        Args:
            article: Article dict from NewsAPI

        Returns:
            Normalized RawItem
        """
        url = article.get("url", "")
        title = article.get("title", "")

        # Get source info
        source_info = article.get("source", {})
        source_name = source_info.get("name", "Unknown")

        # Content - NewsAPI provides description and truncated content
        description = article.get("description", "") or ""
        content = article.get("content", "") or ""
        # Content is truncated with "[+N chars]" - use description if more complete
        text = description if len(description) > len(content.split("[+")[0]) else content.split("[+")[0]

        # Date
        published_at = article.get("publishedAt")

        # Author
        author = article.get("author")

        # Image
        images = []
        if article.get("urlToImage"):
            images.append(article["urlToImage"])

        # Generate ID
        item_id = RawItem.generate_id("newsapi", f"{url}{title}")

        return RawItem(
            id=item_id,
            source_type="newsapi",
            source_adapter="newsapi_v2",
            source_name=source_name,
            source_url=url,
            title=title,
            text=text,
            summary=description,
            language=self.language,
            author=author,
            published_at=published_at,
            category="news",
            tags=[],
            images=images
        )

    def fetch(self, keywords: list[str], since_hours: int = 24) -> list[RawItem]:
        """
        Fetch articles matching keywords.

        Args:
            keywords: Search terms
            since_hours: Time window (max 720h for free tier)

        Returns:
            List of RawItem objects
        """
        if not self.is_enabled():
            return []

        if not keywords:
            print("NewsAPI: No keywords provided")
            return []

        # Build query
        query = " OR ".join(keywords)

        # Calculate from date (NewsAPI uses ISO format)
        from_date = (datetime.now(timezone.utc) - timedelta(hours=since_hours)).strftime("%Y-%m-%dT%H:%M:%S")

        params = {
            "q": query,
            "from": from_date,
            "language": self.language,
            "sortBy": self.sort_by,
            "pageSize": self.page_size
        }

        # Add source/domain filters if configured
        if self.sources:
            params["sources"] = ",".join(self.sources)
        if self.domains:
            params["domains"] = ",".join(self.domains)

        print(f"NewsAPI: Searching for: {query}")
        print(f"NewsAPI: Time window: {since_hours}h, Sort: {self.sort_by}")

        data = self._make_request("everything", params)
        if not data:
            return []

        articles = data.get("articles", [])
        total_results = data.get("totalResults", 0)
        print(f"NewsAPI: Found {total_results} total, fetched {len(articles)}")

        items = []
        for article in articles:
            try:
                item = self._parse_article(article)
                items.append(item)
                self._increment_stat("fetched")
            except Exception as e:
                print(f"NewsAPI: Error parsing article: {e}")
                self._increment_stat("errors")

        return items

    def fetch_top_headlines(self, category: str = None, country: str = "us") -> list[RawItem]:
        """
        Fetch top headlines.

        Args:
            category: business, entertainment, health, science, sports, technology
            country: 2-letter country code

        Returns:
            List of RawItem objects
        """
        if not self.is_enabled():
            return []

        params = {
            "country": country,
            "pageSize": self.page_size
        }

        if category:
            params["category"] = category

        print(f"NewsAPI: Fetching top headlines for {country}")

        data = self._make_request("top-headlines", params)
        if not data:
            return []

        articles = data.get("articles", [])
        items = []

        for article in articles:
            try:
                item = self._parse_article(article)
                items.append(item)
                self._increment_stat("fetched")
            except Exception as e:
                self._increment_stat("errors")

        return items

    def fetch_topic_context(self, topic: str, depth: str = "standard") -> list[RawItem]:
        """
        Deep fetch for topic context.

        Args:
            topic: Topic string
            depth: "quick" (1 day), "standard" (3 days), "deep" (7 days)

        Returns:
            List of RawItem objects
        """
        depth_config = {
            "quick": {"hours": 24, "page_size": 25},
            "standard": {"hours": 72, "page_size": 50},
            "deep": {"hours": 168, "page_size": 100}
        }

        config = depth_config.get(depth, depth_config["standard"])

        # Extract keywords from topic
        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'is', 'are'}
        words = topic.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2][:5]

        if not keywords:
            keywords = [topic]

        # Temporarily adjust page size
        original_page_size = self.page_size
        self.page_size = config["page_size"]

        items = self.fetch(keywords, since_hours=config["hours"])

        self.page_size = original_page_size
        return items


def test_newsapi():
    """Test the NewsAPI adapter."""
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    config = {
        "enabled": True,
        "api_key": os.environ.get("NEWSAPI_KEY", ""),
        "language": "en",
        "sort_by": "publishedAt",
        "page_size": 10,
        "timeout_seconds": 30
    }

    adapter = NewsAPIAdapter(config)

    print("\n" + "=" * 60)
    print("NewsAPI Adapter Test")
    print("=" * 60)

    if not adapter.api_key:
        print("\n[SKIP] No API key found. Set NEWSAPI_KEY environment variable.")
        print("Get free key at: https://newsapi.org/register")
        return []

    # Test search
    print("\n[TEST 1] Keyword search: Epstein, Maxwell")
    items = adapter.fetch(["Epstein", "Maxwell"], since_hours=168)

    print(f"\nFetched {len(items)} items")
    print(f"Stats: {adapter.get_stats()}")

    if items:
        print("\nSample items:")
        for i, item in enumerate(items[:3]):
            title = item.title[:60] if item.title else "(no title)"
            print(f"\n  [{i+1}] {title}...")
            print(f"      Source: {item.source_name}")
            print(f"      Published: {item.published_at}")

    print("\n" + "=" * 60)
    print("NewsAPI adapter test complete!")
    print("=" * 60 + "\n")

    return items


if __name__ == "__main__":
    test_newsapi()
