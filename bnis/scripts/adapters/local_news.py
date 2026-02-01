#!/usr/bin/env python3
"""
Local News Adapter for BNIS v2

Aggregates local/regional news from configured markets.
Uses RSS feeds from local newspapers and TV stations.

No API keys required - uses public RSS feeds.
"""

import re
import urllib.request
import urllib.error
import ssl
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from typing import Optional
from email.utils import parsedate_to_datetime

try:
    from .base import SourceAdapter, RawItem
except ImportError:
    from base import SourceAdapter, RawItem


class LocalNewsAdapter(SourceAdapter):
    """
    Local/regional news aggregator.

    Features:
    - Multiple geographic markets
    - Priority-based market weighting
    - RSS feed aggregation per market
    - No API keys required
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.markets = config.get("markets", [])
        self.timeout = config.get("timeout_seconds", 30)
        self.max_items_per_outlet = config.get("max_items_per_outlet", 20)

    @property
    def source_type(self) -> str:
        return "local_news"

    @property
    def rate_limits(self) -> dict:
        return {
            "requests_per_minute": None,
            "requests_per_day": None,
            "note": "RSS feeds - no rate limits, respect server policies"
        }

    def _fetch_feed(self, url: str) -> Optional[str]:
        """Fetch raw XML from feed URL."""
        try:
            ctx = ssl.create_default_context()

            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "BNIS/2.0 (Continuum Report Intelligence)",
                    "Accept": "application/rss+xml, application/atom+xml, text/xml"
                }
            )

            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                return response.read().decode('utf-8', errors='replace')

        except urllib.error.HTTPError as e:
            print(f"LocalNews HTTP {e.code} for {url}")
            self._increment_stat("errors")
            return None
        except Exception as e:
            print(f"LocalNews Error for {url}: {type(e).__name__}")
            self._increment_stat("errors")
            return None

    def _parse_date(self, date_str: str) -> Optional[str]:
        """Parse date to ISO format."""
        if not date_str:
            return None

        try:
            dt = parsedate_to_datetime(date_str)
            return dt.isoformat()
        except (ValueError, TypeError):
            pass

        try:
            date_str = date_str.replace('Z', '+00:00')
            dt = datetime.fromisoformat(date_str)
            return dt.isoformat()
        except (ValueError, TypeError):
            pass

        return date_str

    def _strip_html(self, text: str) -> str:
        """Remove HTML tags."""
        if not text:
            return ""
        clean = re.sub(r'<[^>]+>', '', text)
        clean = clean.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        clean = clean.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean

    def _parse_rss_item(self, item: ET.Element, outlet_info: dict, market_info: dict) -> Optional[RawItem]:
        """Parse RSS item into RawItem."""
        try:
            title_elem = item.find('title')
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""

            link_elem = item.find('link')
            url = link_elem.text.strip() if link_elem is not None and link_elem.text else ""

            # Description
            desc_elem = item.find('description')
            content_elem = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')

            if content_elem is not None and content_elem.text:
                text = self._strip_html(content_elem.text)
            elif desc_elem is not None and desc_elem.text:
                text = self._strip_html(desc_elem.text)
            else:
                text = title

            # Date
            pub_date_elem = item.find('pubDate')
            published_at = None
            if pub_date_elem is not None and pub_date_elem.text:
                published_at = self._parse_date(pub_date_elem.text.strip())

            # Author
            author_elem = item.find('author')
            dc_creator = item.find('{http://purl.org/dc/elements/1.1/}creator')
            author = None
            if author_elem is not None and author_elem.text:
                author = author_elem.text.strip()
            elif dc_creator is not None and dc_creator.text:
                author = dc_creator.text.strip()

            # Categories
            tags = [market_info.get("name", "")]
            for cat in item.findall('category'):
                if cat.text:
                    tags.append(cat.text.strip())

            # Images
            images = []
            enclosure = item.find('enclosure')
            if enclosure is not None:
                if 'image' in enclosure.get('type', ''):
                    images.append(enclosure.get('url', ''))

            media_content = item.find('{http://search.yahoo.com/mrss/}content')
            if media_content is not None:
                media_url = media_content.get('url', '')
                if media_url:
                    images.append(media_url)

            # Location from market
            location = {"region": market_info.get("name", "")}

            item_id = RawItem.generate_id("local_news", f"{url}{title}")

            return RawItem(
                id=item_id,
                source_type="local_news",
                source_adapter="local_news_rss",
                source_name=outlet_info.get("name", "Unknown"),
                source_url=url,
                title=title,
                text=text,
                language="en",
                author=author,
                published_at=published_at,
                category="local_news",
                tags=tags,
                location=location,
                images=images
            )

        except Exception as e:
            print(f"LocalNews: Error parsing item: {e}")
            self._increment_stat("errors")
            return None

    def _parse_atom_entry(self, entry: ET.Element, outlet_info: dict, market_info: dict) -> Optional[RawItem]:
        """Parse Atom entry into RawItem."""
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        try:
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""

            url = ""
            for link in entry.findall('atom:link', ns):
                if link.get('rel', 'alternate') == 'alternate':
                    url = link.get('href', '')
                    break
                elif not url:
                    url = link.get('href', '')

            content_elem = entry.find('atom:content', ns)
            summary_elem = entry.find('atom:summary', ns)

            if content_elem is not None and content_elem.text:
                text = self._strip_html(content_elem.text)
            elif summary_elem is not None and summary_elem.text:
                text = self._strip_html(summary_elem.text)
            else:
                text = title

            published_elem = entry.find('atom:published', ns)
            updated_elem = entry.find('atom:updated', ns)
            published_at = None

            if published_elem is not None and published_elem.text:
                published_at = self._parse_date(published_elem.text.strip())
            elif updated_elem is not None and updated_elem.text:
                published_at = self._parse_date(updated_elem.text.strip())

            author = None
            author_elem = entry.find('atom:author/atom:name', ns)
            if author_elem is not None and author_elem.text:
                author = author_elem.text.strip()

            tags = [market_info.get("name", "")]

            location = {"region": market_info.get("name", "")}

            item_id = RawItem.generate_id("local_news", f"{url}{title}")

            return RawItem(
                id=item_id,
                source_type="local_news",
                source_adapter="local_news_rss",
                source_name=outlet_info.get("name", "Unknown"),
                source_url=url,
                title=title,
                text=text,
                language="en",
                author=author,
                published_at=published_at,
                category="local_news",
                tags=tags,
                location=location,
                images=[]
            )

        except Exception as e:
            print(f"LocalNews: Error parsing Atom entry: {e}")
            self._increment_stat("errors")
            return None

    def _parse_feed(self, xml_content: str, outlet_info: dict, market_info: dict) -> list[RawItem]:
        """Parse RSS or Atom feed."""
        items = []

        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            print(f"LocalNews: XML parse error for {outlet_info.get('name')}: {e}")
            self._increment_stat("errors")
            return []

        if root.tag == 'rss':
            channel = root.find('channel')
            if channel is None:
                channel = root

            for item in channel.findall('item')[:self.max_items_per_outlet]:
                parsed = self._parse_rss_item(item, outlet_info, market_info)
                if parsed:
                    items.append(parsed)
                    self._increment_stat("fetched")

        elif root.tag == '{http://www.w3.org/2005/Atom}feed':
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('atom:entry', ns)[:self.max_items_per_outlet]:
                parsed = self._parse_atom_entry(entry, outlet_info, market_info)
                if parsed:
                    items.append(parsed)
                    self._increment_stat("fetched")

        return items

    def _matches_keywords(self, item: RawItem, keywords: list[str]) -> bool:
        """Check if item matches keywords."""
        if not keywords:
            return True

        text = f"{item.title} {item.text}".lower()
        for kw in keywords:
            if kw.lower() in text:
                return True
        return False

    def _is_recent(self, item: RawItem, since_hours: int) -> bool:
        """Check if item is recent enough."""
        if not item.published_at:
            return True

        try:
            pub_date = item.published_at.replace('Z', '+00:00')
            dt = datetime.fromisoformat(pub_date)
            cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)
            return dt >= cutoff
        except (ValueError, TypeError):
            return True

    def fetch(self, keywords: list[str], since_hours: int = 24) -> list[RawItem]:
        """
        Fetch from all configured local news markets.

        Args:
            keywords: Filter keywords
            since_hours: Time window

        Returns:
            List of RawItem objects
        """
        if not self.is_enabled():
            print("LocalNews adapter is disabled")
            return []

        if not self.markets:
            print("LocalNews: No markets configured")
            return []

        print(f"LocalNews: Fetching from {len(self.markets)} markets")
        print(f"LocalNews: Keywords: {keywords if keywords else '(none)'}")

        all_items = []

        for market in self.markets:
            market_name = market.get("name", "Unknown")
            priority = market.get("priority", "medium")
            outlets = market.get("outlets", [])

            print(f"\nLocalNews: Market: {market_name} (priority: {priority})")

            for outlet in outlets:
                outlet_name = outlet.get("name", "Unknown")
                rss_url = outlet.get("rss")

                if not rss_url:
                    continue

                print(f"LocalNews:   Fetching {outlet_name}...")

                xml_content = self._fetch_feed(rss_url)
                if not xml_content:
                    continue

                items = self._parse_feed(xml_content, outlet, market)
                print(f"LocalNews:     Got {len(items)} items")

                # Filter
                for item in items:
                    if self._is_recent(item, since_hours):
                        if self._matches_keywords(item, keywords):
                            all_items.append(item)

        print(f"\nLocalNews: Total items after filtering: {len(all_items)}")
        return all_items

    def fetch_topic_context(self, topic: str, depth: str = "standard") -> list[RawItem]:
        """
        Fetch items related to a topic.

        Args:
            topic: Topic string
            depth: "quick", "standard", "deep"

        Returns:
            List of RawItem objects
        """
        depth_hours = {
            "quick": 24,
            "standard": 72,
            "deep": 168
        }
        hours = depth_hours.get(depth, 72)

        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or'}
        words = topic.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2][:5]

        return self.fetch(keywords, since_hours=hours)

    def fetch_by_market(self, market_name: str, since_hours: int = 24) -> list[RawItem]:
        """
        Fetch from a specific market.

        Args:
            market_name: Market name to fetch from
            since_hours: Time window

        Returns:
            List of RawItem objects
        """
        for market in self.markets:
            if market.get("name", "").lower() == market_name.lower():
                # Temporarily filter to just this market
                original_markets = self.markets
                self.markets = [market]

                items = self.fetch([], since_hours)

                self.markets = original_markets
                return items

        print(f"LocalNews: Market not found: {market_name}")
        return []


def test_local_news():
    """Test the LocalNews adapter."""
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    config = {
        "enabled": True,
        "markets": [
            {
                "name": "New York",
                "priority": "high",
                "outlets": [
                    {"name": "NY Times", "rss": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"},
                    {"name": "NY Post", "rss": "https://nypost.com/feed/"}
                ]
            },
            {
                "name": "South Florida",
                "priority": "critical",
                "note": "Key Epstein jurisdiction",
                "outlets": [
                    {"name": "Miami Herald", "rss": "https://www.miamiherald.com/latest-news/rss"}
                ]
            }
        ],
        "timeout_seconds": 30,
        "max_items_per_outlet": 10
    }

    adapter = LocalNewsAdapter(config)

    print("\n" + "=" * 60)
    print("Local News Adapter Test")
    print("=" * 60)

    # Test fetch all
    print("\n[TEST 1] Fetch all markets (no filter)")
    items = adapter.fetch([], since_hours=48)
    print(f"Fetched {len(items)} items")
    print(f"Stats: {adapter.get_stats()}")

    if items:
        print("\nSample items:")
        for i, item in enumerate(items[:3]):
            title = item.title[:60] if item.title else "(no title)"
            print(f"\n  [{i+1}] {title}...")
            print(f"      Source: {item.source_name}")
            print(f"      Market: {item.location.get('region') if item.location else 'N/A'}")
            print(f"      Published: {item.published_at}")

    # Test keyword filter
    print("\n" + "-" * 60)
    print("\n[TEST 2] Fetch with keyword filter: 'court'")
    adapter.reset_stats()
    filtered = adapter.fetch(["court"], since_hours=72)
    print(f"Filtered items: {len(filtered)}")

    print("\n" + "=" * 60)
    print("Local News adapter test complete!")
    print("=" * 60 + "\n")

    return items


if __name__ == "__main__":
    test_local_news()
