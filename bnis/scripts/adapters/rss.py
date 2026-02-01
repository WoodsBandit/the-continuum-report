#!/usr/bin/env python3
"""
RSS Adapter for BNIS v2

Fetches news from RSS/Atom feeds. Supports multiple feeds with
priority levels and category tagging.

No external dependencies - uses stdlib xml.etree for parsing.
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


class RSSAdapter(SourceAdapter):
    """
    RSS/Atom feed adapter.

    Features:
    - Supports both RSS 2.0 and Atom formats
    - Multiple feeds with priority levels
    - Category tagging per feed
    - Keyword filtering
    - No external dependencies
    """

    # Common RSS namespaces
    NAMESPACES = {
        'atom': 'http://www.w3.org/2005/Atom',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'media': 'http://search.yahoo.com/mrss/'
    }

    def __init__(self, config: dict):
        super().__init__(config)
        self.feeds = config.get("feeds", [])
        self.timeout = config.get("timeout_seconds", 30)
        self.max_items_per_feed = config.get("max_items_per_feed", 50)

    @property
    def source_type(self) -> str:
        return "rss"

    @property
    def rate_limits(self) -> dict:
        return {
            "requests_per_minute": None,  # Self-hosted feeds have no limits
            "requests_per_day": None,
            "note": "RSS feeds - respect robots.txt and feed owner policies"
        }

    def _fetch_feed(self, url: str) -> Optional[str]:
        """
        Fetch raw XML from feed URL.

        Args:
            url: Feed URL

        Returns:
            Raw XML string or None on error
        """
        try:
            ctx = ssl.create_default_context()

            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "BNIS/2.0 (Continuum Report Intelligence)",
                    "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml"
                }
            )

            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                return response.read().decode('utf-8')

        except urllib.error.HTTPError as e:
            print(f"RSS HTTP Error {e.code} for {url}: {e.reason}")
            self._increment_stat("errors")
            return None
        except urllib.error.URLError as e:
            print(f"RSS URL Error for {url}: {e.reason}")
            self._increment_stat("errors")
            return None
        except Exception as e:
            print(f"RSS Error for {url}: {type(e).__name__}: {e}")
            self._increment_stat("errors")
            return None

    def _parse_date(self, date_str: str) -> Optional[str]:
        """
        Parse various date formats to ISO format.

        Args:
            date_str: Date string in various formats

        Returns:
            ISO format datetime string or None
        """
        if not date_str:
            return None

        # Try RFC 2822 (common in RSS)
        try:
            dt = parsedate_to_datetime(date_str)
            return dt.isoformat()
        except (ValueError, TypeError):
            pass

        # Try ISO 8601 (common in Atom)
        try:
            # Handle various ISO formats
            date_str = date_str.replace('Z', '+00:00')
            if '.' in date_str:
                # Truncate microseconds if present
                parts = date_str.split('.')
                if '+' in parts[1]:
                    date_str = parts[0] + '+' + parts[1].split('+')[1]
                elif '-' in parts[1]:
                    date_str = parts[0] + '-' + parts[1].split('-')[1]
                else:
                    date_str = parts[0]
            dt = datetime.fromisoformat(date_str)
            return dt.isoformat()
        except (ValueError, TypeError):
            pass

        return date_str  # Return as-is if parsing fails

    def _parse_rss_item(self, item: ET.Element, feed_info: dict) -> Optional[RawItem]:
        """
        Parse RSS 2.0 item element.

        Args:
            item: XML Element for <item>
            feed_info: Feed configuration dict

        Returns:
            RawItem or None if parsing fails
        """
        try:
            # Extract basic fields
            title_elem = item.find('title')
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""

            link_elem = item.find('link')
            url = link_elem.text.strip() if link_elem is not None and link_elem.text else ""

            # Description/content
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

            # Categories/tags
            tags = []
            for cat in item.findall('category'):
                if cat.text:
                    tags.append(cat.text.strip())

            # Media/images
            images = []
            enclosure = item.find('enclosure')
            if enclosure is not None:
                enc_type = enclosure.get('type', '')
                if 'image' in enc_type:
                    images.append(enclosure.get('url', ''))

            media_content = item.find('{http://search.yahoo.com/mrss/}content')
            if media_content is not None:
                media_url = media_content.get('url', '')
                if media_url:
                    images.append(media_url)

            # Generate ID
            item_id = RawItem.generate_id("rss", f"{url}{title}")

            return RawItem(
                id=item_id,
                source_type="rss",
                source_adapter="rss_v2",
                source_name=feed_info.get("name", "Unknown Feed"),
                source_url=url,
                title=title,
                text=text,
                language="en",
                author=author,
                published_at=published_at,
                category=feed_info.get("category", "news"),
                tags=tags,
                images=images
            )

        except Exception as e:
            print(f"RSS: Error parsing item: {e}")
            self._increment_stat("errors")
            return None

    def _parse_atom_entry(self, entry: ET.Element, feed_info: dict, ns: dict) -> Optional[RawItem]:
        """
        Parse Atom entry element.

        Args:
            entry: XML Element for <entry>
            feed_info: Feed configuration dict
            ns: Namespace dict

        Returns:
            RawItem or None if parsing fails
        """
        try:
            # Title
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""

            # Link - prefer alternate, fall back to any href
            url = ""
            for link in entry.findall('atom:link', ns):
                rel = link.get('rel', 'alternate')
                if rel == 'alternate':
                    url = link.get('href', '')
                    break
                elif not url:
                    url = link.get('href', '')

            # Content
            content_elem = entry.find('atom:content', ns)
            summary_elem = entry.find('atom:summary', ns)

            if content_elem is not None and content_elem.text:
                text = self._strip_html(content_elem.text)
            elif summary_elem is not None and summary_elem.text:
                text = self._strip_html(summary_elem.text)
            else:
                text = title

            # Date
            updated_elem = entry.find('atom:updated', ns)
            published_elem = entry.find('atom:published', ns)
            published_at = None

            if published_elem is not None and published_elem.text:
                published_at = self._parse_date(published_elem.text.strip())
            elif updated_elem is not None and updated_elem.text:
                published_at = self._parse_date(updated_elem.text.strip())

            # Author
            author = None
            author_elem = entry.find('atom:author/atom:name', ns)
            if author_elem is not None and author_elem.text:
                author = author_elem.text.strip()

            # Categories
            tags = []
            for cat in entry.findall('atom:category', ns):
                term = cat.get('term', '')
                if term:
                    tags.append(term)

            # Generate ID
            item_id = RawItem.generate_id("rss", f"{url}{title}")

            return RawItem(
                id=item_id,
                source_type="rss",
                source_adapter="rss_v2",
                source_name=feed_info.get("name", "Unknown Feed"),
                source_url=url,
                title=title,
                text=text,
                language="en",
                author=author,
                published_at=published_at,
                category=feed_info.get("category", "news"),
                tags=tags,
                images=[]
            )

        except Exception as e:
            print(f"RSS: Error parsing Atom entry: {e}")
            self._increment_stat("errors")
            return None

    def _strip_html(self, text: str) -> str:
        """Remove HTML tags from text."""
        if not text:
            return ""
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', text)
        # Decode common entities
        clean = clean.replace('&amp;', '&')
        clean = clean.replace('&lt;', '<')
        clean = clean.replace('&gt;', '>')
        clean = clean.replace('&quot;', '"')
        clean = clean.replace('&#39;', "'")
        clean = clean.replace('&nbsp;', ' ')
        # Normalize whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean

    def _parse_feed(self, xml_content: str, feed_info: dict) -> list[RawItem]:
        """
        Parse RSS or Atom feed XML.

        Args:
            xml_content: Raw XML string
            feed_info: Feed configuration dict

        Returns:
            List of RawItem objects
        """
        items = []

        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            print(f"RSS: XML parse error for {feed_info.get('name')}: {e}")
            self._increment_stat("errors")
            return []

        # Detect feed type and parse accordingly
        if root.tag == 'rss' or root.tag == 'rdf:RDF':
            # RSS 2.0 or RSS 1.0
            channel = root.find('channel')
            if channel is None:
                channel = root

            for item in channel.findall('item')[:self.max_items_per_feed]:
                parsed = self._parse_rss_item(item, feed_info)
                if parsed:
                    items.append(parsed)
                    self._increment_stat("fetched")

        elif root.tag == '{http://www.w3.org/2005/Atom}feed':
            # Atom
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('atom:entry', ns)[:self.max_items_per_feed]:
                parsed = self._parse_atom_entry(entry, feed_info, ns)
                if parsed:
                    items.append(parsed)
                    self._increment_stat("fetched")

        else:
            print(f"RSS: Unknown feed format for {feed_info.get('name')}: {root.tag}")
            self._increment_stat("errors")

        return items

    def _matches_keywords(self, item: RawItem, keywords: list[str]) -> bool:
        """Check if item matches any keywords."""
        if not keywords:
            return True  # No filter = match all

        text = f"{item.title} {item.text}".lower()
        for kw in keywords:
            if kw.lower() in text:
                return True
        return False

    def _is_recent(self, item: RawItem, since_hours: int) -> bool:
        """Check if item is within time window."""
        if not item.published_at:
            return True  # No date = assume recent

        try:
            # Parse ISO format
            pub_date = item.published_at.replace('Z', '+00:00')
            dt = datetime.fromisoformat(pub_date)
            cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)
            return dt >= cutoff
        except (ValueError, TypeError):
            return True  # Parse error = assume recent

    def fetch(self, keywords: list[str], since_hours: int = 24) -> list[RawItem]:
        """
        Fetch articles from all configured RSS feeds.

        Args:
            keywords: List of keywords to filter by
            since_hours: Only return items from past N hours

        Returns:
            List of RawItem objects matching criteria
        """
        if not self.is_enabled():
            print("RSS adapter is disabled")
            return []

        if not self.feeds:
            print("RSS: No feeds configured")
            return []

        print(f"RSS: Fetching from {len(self.feeds)} feeds")
        print(f"RSS: Keywords filter: {keywords if keywords else '(none)'}")
        print(f"RSS: Time window: {since_hours}h")

        all_items = []

        for feed_info in self.feeds:
            feed_url = feed_info.get("url")
            feed_name = feed_info.get("name", feed_url)

            if not feed_url:
                continue

            print(f"RSS: Fetching {feed_name}...")

            xml_content = self._fetch_feed(feed_url)
            if not xml_content:
                continue

            items = self._parse_feed(xml_content, feed_info)
            print(f"RSS:   Got {len(items)} items from {feed_name}")

            # Filter by keywords and time
            for item in items:
                if self._is_recent(item, since_hours):
                    if self._matches_keywords(item, keywords):
                        all_items.append(item)

        print(f"RSS: Total items after filtering: {len(all_items)}")
        return all_items

    def fetch_topic_context(self, topic: str, depth: str = "standard") -> list[RawItem]:
        """
        Fetch items related to a topic.

        For RSS, this just fetches recent items and filters by topic words.

        Args:
            topic: Topic string
            depth: "quick" (1 day), "standard" (3 days), "deep" (7 days)

        Returns:
            List of RawItem objects
        """
        depth_hours = {
            "quick": 24,
            "standard": 72,
            "deep": 168
        }
        hours = depth_hours.get(depth, 72)

        # Extract keywords from topic
        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'is', 'are', 'was', 'were'}
        words = topic.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2][:5]

        return self.fetch(keywords, since_hours=hours)


def test_rss():
    """Test the RSS adapter."""
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    config = {
        "enabled": True,
        "feeds": [
            {
                "name": "Courthouse News",
                "url": "https://www.courthousenews.com/feed/",
                "category": "legal",
                "priority": "high"
            },
            {
                "name": "Law & Crime",
                "url": "https://lawandcrime.com/feed/",
                "category": "legal",
                "priority": "high"
            }
        ],
        "timeout_seconds": 30,
        "max_items_per_feed": 20
    }

    adapter = RSSAdapter(config)

    print("\n" + "=" * 60)
    print("RSS Adapter Test")
    print("=" * 60)

    # Test basic fetch (no keyword filter)
    print("\n[TEST 1] Fetch all recent items (no filter)")
    items = adapter.fetch([], since_hours=48)
    print(f"Fetched {len(items)} items")
    print(f"Stats: {adapter.get_stats()}")

    if items:
        print("\nSample items:")
        for i, item in enumerate(items[:3]):
            title = item.title[:60] if item.title else "(no title)"
            print(f"\n  [{i+1}] {title}...")
            print(f"      Source: {item.source_name}")
            print(f"      URL: {item.source_url[:50]}...")
            print(f"      Published: {item.published_at}")

    # Test keyword filter
    print("\n" + "-" * 60)
    print("\n[TEST 2] Fetch with keyword filter: 'court', 'lawsuit'")
    adapter.reset_stats()
    filtered = adapter.fetch(["court", "lawsuit"], since_hours=72)
    print(f"Filtered items: {len(filtered)}")

    if filtered:
        print("\nMatched items:")
        for i, item in enumerate(filtered[:3]):
            title = item.title[:60] if item.title else "(no title)"
            print(f"  [{i+1}] {title}...")

    print("\n" + "=" * 60)
    print("RSS adapter test complete!")
    print("=" * 60 + "\n")

    return items


if __name__ == "__main__":
    test_rss()
