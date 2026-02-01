#!/usr/bin/env python3
"""
YouTube Adapter for BNIS v2

Fetches videos and metadata from YouTube Data API v3.
Optionally fetches auto-generated captions/transcripts.

API Documentation: https://developers.google.com/youtube/v3
Free tier: 10,000 units/day (search = 100 units, video details = 1 unit)

Requires API key from Google Cloud Console.
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
import os
import re
from datetime import datetime, timezone, timedelta
from typing import Optional

try:
    from .base import SourceAdapter, RawItem
except ImportError:
    from base import SourceAdapter, RawItem


class YouTubeAdapter(SourceAdapter):
    """
    YouTube Data API v3 adapter.

    Features:
    - Search videos by keyword
    - Fetch from specific channels
    - Get video metadata and statistics
    - Extract auto-generated captions (when available)
    - Free tier: 10,000 units/day
    """

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, config: dict):
        super().__init__(config)
        # Try config first, then environment variable
        self.api_key = config.get("api_key", "").replace("${YOUTUBE_API_KEY}", "")
        if not self.api_key or self.api_key.startswith("$"):
            self.api_key = os.environ.get("YOUTUBE_API_KEY", "")

        self.channels = config.get("channels", [])
        self.search_queries = config.get("search_queries", [])
        self.fetch_transcripts = config.get("fetch_transcripts", False)
        self.max_results = config.get("max_results_per_query", 10)
        self.max_video_age_days = config.get("max_video_age_days", 7)
        self.timeout = config.get("timeout_seconds", 30)

        # Track API quota usage
        self.quota_used = 0

    @property
    def source_type(self) -> str:
        return "youtube"

    @property
    def rate_limits(self) -> dict:
        return {
            "units_per_day": 10000,
            "search_cost": 100,
            "video_details_cost": 1,
            "captions_cost": 50,
            "note": "Free tier: 10,000 units/day"
        }

    def is_enabled(self) -> bool:
        """Check if adapter is enabled AND has API key."""
        if not super().is_enabled():
            return False
        if not self.api_key:
            print("YouTube: No API key configured (set YOUTUBE_API_KEY env var)")
            return False
        return True

    def _make_request(self, endpoint: str, params: dict) -> Optional[dict]:
        """
        Make authenticated request to YouTube API.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Parsed JSON response or None on error
        """
        params["key"] = self.api_key
        params_string = urllib.parse.urlencode(params)
        url = f"{self.BASE_URL}/{endpoint}?{params_string}"

        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "BNIS/2.0",
                    "Accept": "application/json"
                }
            )

            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                return json.loads(response.read().decode('utf-8'))

        except urllib.error.HTTPError as e:
            try:
                error_body = e.read().decode('utf-8')
                error_data = json.loads(error_body)
                error_msg = error_data.get("error", {}).get("message", e.reason)
                print(f"YouTube HTTP {e.code}: {error_msg}")

                if e.code == 403:
                    errors = error_data.get("error", {}).get("errors", [])
                    for err in errors:
                        if err.get("reason") == "quotaExceeded":
                            print("YouTube: Daily quota exceeded")
                            self._increment_stat("rate_limited")
            except:
                print(f"YouTube HTTP {e.code}: {e.reason}")

            self._increment_stat("errors")
            return None

        except Exception as e:
            print(f"YouTube Error: {type(e).__name__}: {e}")
            self._increment_stat("errors")
            return None

    def _search_videos(self, query: str, max_results: int = None,
                       published_after: str = None) -> list[dict]:
        """
        Search for videos.

        Args:
            query: Search query
            max_results: Maximum results
            published_after: ISO 8601 datetime filter

        Returns:
            List of search result items
        """
        params = {
            "part": "snippet",
            "type": "video",
            "q": query,
            "maxResults": max_results or self.max_results,
            "order": "date"
        }

        if published_after:
            params["publishedAfter"] = published_after

        self.quota_used += 100  # Search costs 100 units

        data = self._make_request("search", params)
        if not data:
            return []

        return data.get("items", [])

    def _get_video_details(self, video_ids: list[str]) -> dict:
        """
        Get detailed info for videos.

        Args:
            video_ids: List of video IDs

        Returns:
            Dict mapping video ID to details
        """
        if not video_ids:
            return {}

        params = {
            "part": "snippet,statistics,contentDetails",
            "id": ",".join(video_ids)
        }

        self.quota_used += len(video_ids)  # 1 unit per video

        data = self._make_request("videos", params)
        if not data:
            return {}

        return {item["id"]: item for item in data.get("items", [])}

    def _get_channel_videos(self, channel_id: str, max_results: int = None) -> list[dict]:
        """
        Get recent videos from a channel.

        Args:
            channel_id: YouTube channel ID
            max_results: Maximum results

        Returns:
            List of video items
        """
        # First get the uploads playlist ID
        params = {
            "part": "contentDetails",
            "id": channel_id
        }

        data = self._make_request("channels", params)
        if not data or not data.get("items"):
            return []

        uploads_id = data["items"][0].get("contentDetails", {}).get(
            "relatedPlaylists", {}).get("uploads")

        if not uploads_id:
            return []

        # Get playlist items
        params = {
            "part": "snippet",
            "playlistId": uploads_id,
            "maxResults": max_results or self.max_results
        }

        self.quota_used += 1

        data = self._make_request("playlistItems", params)
        if not data:
            return []

        return data.get("items", [])

    def _parse_duration(self, duration: str) -> int:
        """Parse ISO 8601 duration to seconds."""
        if not duration:
            return 0

        # Format: PT1H2M3S or PT2M30S or PT45S
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
        if not match:
            return 0

        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)

        return hours * 3600 + minutes * 60 + seconds

    def _parse_video(self, item: dict, details: dict = None) -> RawItem:
        """
        Parse YouTube video into RawItem.

        Args:
            item: Search result or playlist item
            details: Optional video details

        Returns:
            Normalized RawItem
        """
        snippet = item.get("snippet", {})

        # Get video ID (different structure for search vs playlist)
        if "videoId" in item.get("id", {}):
            video_id = item["id"]["videoId"]
        elif "resourceId" in snippet:
            video_id = snippet["resourceId"].get("videoId", "")
        else:
            video_id = item.get("id", "")

        url = f"https://www.youtube.com/watch?v={video_id}"
        title = snippet.get("title", "")
        description = snippet.get("description", "")
        channel_title = snippet.get("channelTitle", "")
        published_at = snippet.get("publishedAt")

        # Thumbnails
        thumbnails = snippet.get("thumbnails", {})
        images = []
        for quality in ["high", "medium", "default"]:
            if quality in thumbnails:
                images.append(thumbnails[quality].get("url", ""))
                break

        # Get additional details if available
        engagement = None
        duration = None
        if details:
            stats = details.get("statistics", {})
            engagement = {
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0))
            }

            content_details = details.get("contentDetails", {})
            duration = self._parse_duration(content_details.get("duration", ""))

        # Build text from title and description
        text = f"{title}\n\n{description}"

        # Generate ID
        item_id = RawItem.generate_id("youtube", f"{video_id}{title}")

        return RawItem(
            id=item_id,
            source_type="youtube",
            source_adapter="youtube_v3",
            source_name=channel_title,
            source_url=url,
            title=title,
            text=text,
            summary=description[:500] if description else None,
            language="en",
            author=channel_title,
            published_at=published_at,
            category="video",
            tags=snippet.get("tags", []),
            images=images,
            video_url=url,
            engagement=engagement
        )

    def fetch(self, keywords: list[str], since_hours: int = 24) -> list[RawItem]:
        """
        Search for videos matching keywords.

        Args:
            keywords: Search terms
            since_hours: Time window

        Returns:
            List of RawItem objects
        """
        if not self.is_enabled():
            return []

        if not keywords:
            print("YouTube: No keywords provided")
            return []

        # Calculate published after date
        published_after = (datetime.now(timezone.utc) - timedelta(hours=since_hours)).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Build combined query
        query = " ".join(keywords)

        print(f"YouTube: Searching for: {query}")
        print(f"YouTube: Time window: {since_hours}h")

        search_results = self._search_videos(query, published_after=published_after)
        print(f"YouTube: Found {len(search_results)} videos")

        if not search_results:
            return []

        # Get video IDs for details
        video_ids = []
        for item in search_results:
            vid_id = item.get("id", {}).get("videoId")
            if vid_id:
                video_ids.append(vid_id)

        # Fetch details
        details_map = self._get_video_details(video_ids)

        # Parse videos
        items = []
        for item in search_results:
            try:
                vid_id = item.get("id", {}).get("videoId")
                details = details_map.get(vid_id)
                parsed = self._parse_video(item, details)
                items.append(parsed)
                self._increment_stat("fetched")
            except Exception as e:
                print(f"YouTube: Error parsing video: {e}")
                self._increment_stat("errors")

        print(f"YouTube: Quota used this session: {self.quota_used} units")
        return items

    def fetch_from_channels(self) -> list[RawItem]:
        """
        Fetch recent videos from configured channels.

        Returns:
            List of RawItem objects
        """
        if not self.is_enabled():
            return []

        if not self.channels:
            print("YouTube: No channels configured")
            return []

        all_items = []

        for channel_info in self.channels:
            channel_id = channel_info.get("id")
            channel_name = channel_info.get("name", channel_id)

            if not channel_id:
                continue

            print(f"YouTube: Fetching from channel: {channel_name}")

            videos = self._get_channel_videos(channel_id)
            print(f"YouTube:   Got {len(videos)} videos")

            for item in videos:
                try:
                    parsed = self._parse_video(item)
                    all_items.append(parsed)
                    self._increment_stat("fetched")
                except Exception as e:
                    print(f"YouTube: Error parsing video: {e}")
                    self._increment_stat("errors")

        return all_items

    def fetch_topic_context(self, topic: str, depth: str = "standard") -> list[RawItem]:
        """
        Deep fetch for topic context.

        Args:
            topic: Topic string
            depth: "quick", "standard", "deep"

        Returns:
            List of RawItem objects
        """
        depth_config = {
            "quick": {"hours": 72, "max_results": 5},
            "standard": {"hours": 168, "max_results": 15},
            "deep": {"hours": 336, "max_results": 25}
        }

        config = depth_config.get(depth, depth_config["standard"])

        # Extract keywords
        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or'}
        words = topic.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2][:5]

        if not keywords:
            keywords = [topic]

        original_max = self.max_results
        self.max_results = config["max_results"]

        items = self.fetch(keywords, since_hours=config["hours"])

        self.max_results = original_max
        return items


def test_youtube():
    """Test the YouTube adapter."""
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    config = {
        "enabled": True,
        "api_key": os.environ.get("YOUTUBE_API_KEY", ""),
        "max_results_per_query": 5,
        "max_video_age_days": 7,
        "timeout_seconds": 30,
        "channels": [
            {"id": "UCYwVLVsVfD6A5kdGIH-9MCg", "name": "Law & Crime Network"}
        ]
    }

    adapter = YouTubeAdapter(config)

    print("\n" + "=" * 60)
    print("YouTube Adapter Test")
    print("=" * 60)

    if not adapter.api_key:
        print("\n[SKIP] No API key found. Set YOUTUBE_API_KEY environment variable.")
        print("Get key from: https://console.cloud.google.com/apis/credentials")
        return []

    # Test search
    print("\n[TEST 1] Keyword search: Epstein documents")
    items = adapter.fetch(["Epstein", "documents"], since_hours=168)

    print(f"\nFetched {len(items)} items")
    print(f"Stats: {adapter.get_stats()}")
    print(f"Quota used: {adapter.quota_used} units")

    if items:
        print("\nSample items:")
        for i, item in enumerate(items[:3]):
            title = item.title[:60] if item.title else "(no title)"
            print(f"\n  [{i+1}] {title}...")
            print(f"      Channel: {item.source_name}")
            print(f"      URL: {item.source_url}")
            print(f"      Published: {item.published_at}")
            if item.engagement:
                print(f"      Views: {item.engagement.get('views', 0):,}")

    print("\n" + "=" * 60)
    print("YouTube adapter test complete!")
    print("=" * 60 + "\n")

    return items


if __name__ == "__main__":
    test_youtube()
