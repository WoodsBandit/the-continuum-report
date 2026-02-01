#!/usr/bin/env python3
"""
GDELT Adapter for BNIS v2

Fetches global news from the GDELT Project (Global Database of Events,
Language, and Tone). GDELT monitors news media worldwide and provides
free, unlimited API access.

API Documentation: https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/

No API key required - completely free and unlimited.
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta
from typing import Optional
import ssl
import time

try:
    from .base import SourceAdapter, RawItem
except ImportError:
    from base import SourceAdapter, RawItem


class GDELTAdapter(SourceAdapter):
    """
    GDELT 2.0 DOC API adapter.

    Features:
    - Global news coverage (65+ languages, 150+ countries)
    - No API key required
    - No rate limits
    - Real-time updates (15-minute delay from publication)
    - Full article metadata and source information
    """

    BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

    def __init__(self, config: dict):
        super().__init__(config)
        self.max_records = config.get("max_records", 250)
        self.source_lang = config.get("source_lang", "eng")
        self.themes = config.get("themes", [])
        self.timeout = config.get("timeout_seconds", 30)

    @property
    def source_type(self) -> str:
        return "gdelt"

    @property
    def rate_limits(self) -> dict:
        # GDELT has no rate limits
        return {
            "requests_per_minute": None,  # Unlimited
            "requests_per_day": None,  # Unlimited
            "note": "GDELT is free and unlimited"
        }

    def _build_query(self, keywords: list[str]) -> str:
        """
        Build GDELT query string.

        Args:
            keywords: List of search terms

        Returns:
            Properly formatted query string for GDELT API
        """
        if not keywords:
            return ""

        # For single keyword, just return it
        if len(keywords) == 1:
            kw = keywords[0]
            if ' ' in kw:
                return f'"{kw}"'
            return kw

        # For multiple keywords, join with OR and wrap in parentheses
        # GDELT requires: (term1 OR term2 OR term3)
        query_parts = []
        for kw in keywords:
            if ' ' in kw:
                query_parts.append(f'"{kw}"')
            else:
                query_parts.append(kw)

        query = '(' + ' OR '.join(query_parts) + ')'
        return query

    def _build_url(self, query: str, timespan: str = "24h",
                   max_records: Optional[int] = None,
                   mode: str = "artlist") -> str:
        """
        Build full GDELT API URL.

        Args:
            query: Search query string
            timespan: Time range
            max_records: Maximum results (default from config)
            mode: API mode (artlist, timeline, etc.)

        Returns:
            Full API URL
        """
        # GDELT requires query to be properly URL encoded
        # The query parameter needs special handling - encode separately
        base_params = {
            "mode": mode,
            "format": "json",
            "timespan": timespan,
            "maxrecords": str(max_records or self.max_records),
            "sourcelang": self.source_lang
        }

        # Add theme filter if configured
        if self.themes:
            base_params["theme"] = ",".join(self.themes)

        # Build URL with query encoded separately
        # GDELT expects the query as a URL-encoded parameter
        query_encoded = urllib.parse.quote(query, safe='')
        params_string = urllib.parse.urlencode(base_params)

        return f"{self.BASE_URL}?query={query_encoded}&{params_string}"

    def _fetch_url(self, url: str) -> Optional[dict]:
        """
        Fetch and parse JSON from URL.

        Args:
            url: Full API URL

        Returns:
            Parsed JSON dict or None on error
        """
        try:
            # Create SSL context (GDELT uses HTTPS)
            ctx = ssl.create_default_context()

            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "BNIS/2.0 (Continuum Report Intelligence)",
                    "Accept": "application/json"
                }
            )

            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                raw_data = response.read()
                data = raw_data.decode('utf-8')

                # Check for empty response
                if not data or not data.strip():
                    print(f"GDELT: Empty response received")
                    self._increment_stat("errors")
                    return None

                return json.loads(data)

        except urllib.error.HTTPError as e:
            print(f"GDELT HTTP Error {e.code}: {e.reason}")
            try:
                error_body = e.read().decode('utf-8')
                print(f"GDELT Error body: {error_body[:200]}")
            except:
                pass
            self._increment_stat("errors")
            return None
        except urllib.error.URLError as e:
            print(f"GDELT URL Error: {e.reason}")
            self._increment_stat("errors")
            return None
        except json.JSONDecodeError as e:
            print(f"GDELT JSON Error: {e}")
            print(f"GDELT Raw response (first 200 chars): {data[:200] if data else '(empty)'}")
            self._increment_stat("errors")
            return None
        except Exception as e:
            print(f"GDELT Error: {type(e).__name__}: {e}")
            self._increment_stat("errors")
            return None

    def _parse_article(self, article: dict) -> RawItem:
        """
        Parse GDELT article into RawItem.

        Args:
            article: Raw article dict from GDELT API

        Returns:
            Normalized RawItem
        """
        # Extract fields with defaults
        url = article.get("url", "")
        title = article.get("title", "")
        source_name = article.get("domain", article.get("sourcecountry", "unknown"))

        # GDELT provides seendate in YYYYMMDDTHHMMSSZ format
        seen_date = article.get("seendate", "")
        if seen_date:
            try:
                # Parse GDELT date format: 20260131T143000Z
                dt = datetime.strptime(seen_date, "%Y%m%dT%H%M%SZ")
                dt = dt.replace(tzinfo=timezone.utc)
                published_at = dt.isoformat()
            except ValueError:
                published_at = seen_date
        else:
            published_at = None

        # Extract location info
        location = None
        if article.get("sourcecountry"):
            location = {"country": article.get("sourcecountry")}

        # Build text from available fields
        # GDELT artlist mode only returns title, not full text
        # For full text, would need to fetch the actual article
        text = title

        # Extract image if available
        images = []
        if article.get("socialimage"):
            images.append(article["socialimage"])

        # Generate unique ID
        item_id = RawItem.generate_id("gdelt", f"{url}{title}")

        return RawItem(
            id=item_id,
            source_type="gdelt",
            source_adapter="gdelt_v2",
            source_name=source_name,
            source_url=url,
            title=title,
            text=text,
            language=article.get("language", "English"),
            published_at=published_at,
            location=location,
            images=images,
            tags=[],  # Could extract from GDELT themes
            category="news"
        )

    def fetch(self, keywords: list[str], since_hours: int = 24) -> list[RawItem]:
        """
        Fetch news articles matching keywords.

        Args:
            keywords: List of search terms
            since_hours: How far back to search (1-720 hours)

        Returns:
            List of RawItem objects
        """
        if not self.is_enabled():
            print("GDELT adapter is disabled")
            return []

        if not keywords:
            print("No keywords provided")
            return []

        # Convert hours to GDELT timespan format
        if since_hours <= 24:
            timespan = f"{since_hours}h"
        elif since_hours <= 168:  # 7 days
            timespan = f"{since_hours // 24}d"
        else:
            timespan = f"{min(since_hours // 24, 30)}d"  # Max 30 days

        print(f"GDELT: Fetching news for keywords: {keywords}")
        print(f"GDELT: Timespan: {timespan}, Max records: {self.max_records}")

        # Build and execute query
        query = self._build_query(keywords)
        url = self._build_url(query, timespan)

        print(f"GDELT: Full Query URL: {url}")

        data = self._fetch_url(url)
        if not data:
            return []

        # Parse articles
        articles = data.get("articles", [])
        print(f"GDELT: Found {len(articles)} articles")

        items = []
        for article in articles:
            try:
                item = self._parse_article(article)
                items.append(item)
                self._increment_stat("fetched")
            except Exception as e:
                print(f"GDELT: Error parsing article: {e}")
                self._increment_stat("errors")

        return items

    def fetch_topic_context(self, topic: str, depth: str = "standard") -> list[RawItem]:
        """
        Deep fetch for topic context aggregation.

        Searches GDELT with expanded queries to gather comprehensive
        coverage of a topic from multiple angles.

        Args:
            topic: Topic string or story summary
            depth: "quick" (25), "standard" (100), "deep" (250)

        Returns:
            List of RawItem objects
        """
        # Determine max records based on depth
        depth_limits = {
            "quick": 25,
            "standard": 100,
            "deep": 250
        }
        max_records = depth_limits.get(depth, 100)

        print(f"GDELT: Topic context fetch - depth: {depth}, max: {max_records}")

        # Extract key terms from topic
        # Simple extraction - split on common words
        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'is', 'are', 'was', 'were'}
        words = topic.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2][:10]

        if not keywords:
            keywords = [topic]

        # Build query
        query = self._build_query(keywords)

        # Fetch with extended timespan for context
        url = self._build_url(query, timespan="7d", max_records=max_records)

        print(f"GDELT: Context query: {query}")

        data = self._fetch_url(url)
        if not data:
            return []

        articles = data.get("articles", [])
        print(f"GDELT: Found {len(articles)} context articles")

        items = []
        for article in articles:
            try:
                item = self._parse_article(article)
                items.append(item)
                self._increment_stat("fetched")
            except Exception as e:
                print(f"GDELT: Error parsing context article: {e}")
                self._increment_stat("errors")

        return items

    def fetch_by_theme(self, themes: list[str], since_hours: int = 24) -> list[RawItem]:
        """
        Fetch articles by GDELT theme codes.

        GDELT themes include:
        - TAX_FNCACT_ARREST: Arrests
        - TAX_FNCACT_LAWSUIT: Lawsuits
        - TAX_FNCACT_INVESTIGATION: Investigations
        - CRISISLEX_C07_CRIME: Crime-related

        Args:
            themes: List of GDELT theme codes
            since_hours: How far back to search

        Returns:
            List of RawItem objects
        """
        if not themes:
            return []

        # Build theme query
        theme_query = " OR ".join([f"theme:{t}" for t in themes])

        timespan = f"{min(since_hours, 720)}h"
        url = self._build_url(theme_query, timespan)

        data = self._fetch_url(url)
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


def test_gdelt():
    """Test the GDELT adapter."""
    config = {
        "enabled": True,
        "max_records": 10,
        "source_lang": "eng",
        "timeout_seconds": 30
    }

    adapter = GDELTAdapter(config)

    print("\n" + "="*60)
    print("GDELT Adapter Test")
    print("="*60)

    # Test basic fetch
    keywords = ["Epstein", "documents"]
    items = adapter.fetch(keywords, since_hours=72)

    print(f"\nFetched {len(items)} items")
    print(f"Stats: {adapter.get_stats()}")

    if items:
        print("\nFirst item:")
        item = items[0]
        print(f"  ID: {item.id}")
        print(f"  Title: {item.title[:80]}...")
        print(f"  Source: {item.source_name}")
        print(f"  URL: {item.source_url[:60]}...")
        print(f"  Published: {item.published_at}")

    return items


if __name__ == "__main__":
    test_gdelt()
