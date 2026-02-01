#!/usr/bin/env python3
"""
Reddit Adapter for BNIS v2

Fetches posts and comments from Reddit via the official API.

API Documentation: https://www.reddit.com/dev/api
Rate limit: 60 requests/minute with OAuth2

Requires app registration at: https://www.reddit.com/prefs/apps
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
import os
import base64
from datetime import datetime, timezone, timedelta
from typing import Optional

try:
    from .base import SourceAdapter, RawItem
except ImportError:
    from base import SourceAdapter, RawItem


class RedditAdapter(SourceAdapter):
    """
    Reddit API adapter using OAuth2.

    Features:
    - Fetch from multiple subreddits
    - Search across Reddit
    - Include top comments
    - Filter by score and age
    - Rate limit: 60 req/min
    """

    AUTH_URL = "https://www.reddit.com/api/v1/access_token"
    API_URL = "https://oauth.reddit.com"

    def __init__(self, config: dict):
        super().__init__(config)

        # OAuth credentials
        self.client_id = config.get("client_id", "").replace("${REDDIT_CLIENT_ID}", "")
        if not self.client_id or self.client_id.startswith("$"):
            self.client_id = os.environ.get("REDDIT_CLIENT_ID", "")

        self.client_secret = config.get("client_secret", "").replace("${REDDIT_SECRET}", "")
        if not self.client_secret or self.client_secret.startswith("$"):
            self.client_secret = os.environ.get("REDDIT_SECRET", "")

        self.user_agent = config.get("user_agent", "BNIS/2.0 (continuum intelligence)")
        self.subreddits = config.get("subreddits", [])
        self.include_comments = config.get("include_comments", True)
        self.comment_depth = config.get("comment_depth", 2)
        self.min_score = config.get("min_score", 10)
        self.timeout = config.get("timeout_seconds", 30)

        # OAuth token
        self._access_token = None
        self._token_expires = None

    @property
    def source_type(self) -> str:
        return "reddit"

    @property
    def rate_limits(self) -> dict:
        return {
            "requests_per_minute": 60,
            "requests_per_day": None,  # No daily limit
            "note": "OAuth2 required, 60 req/min"
        }

    def is_enabled(self) -> bool:
        """Check if adapter is enabled AND has credentials."""
        if not super().is_enabled():
            return False
        if not self.client_id or not self.client_secret:
            print("Reddit: Missing credentials (set REDDIT_CLIENT_ID and REDDIT_SECRET)")
            return False
        return True

    def _get_access_token(self) -> Optional[str]:
        """
        Get OAuth2 access token.

        Returns:
            Access token or None on error
        """
        # Check if we have a valid token
        if self._access_token and self._token_expires:
            if datetime.now(timezone.utc) < self._token_expires:
                return self._access_token

        # Request new token
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

        data = urllib.parse.urlencode({
            "grant_type": "client_credentials"
        }).encode('utf-8')

        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(
                self.AUTH_URL,
                data=data,
                headers={
                    "Authorization": f"Basic {auth_bytes}",
                    "User-Agent": self.user_agent,
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )

            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                result = json.loads(response.read().decode('utf-8'))

                self._access_token = result.get("access_token")
                expires_in = result.get("expires_in", 3600)
                self._token_expires = datetime.now(timezone.utc) + timedelta(seconds=expires_in - 60)

                return self._access_token

        except urllib.error.HTTPError as e:
            print(f"Reddit Auth Error {e.code}: {e.reason}")
            self._increment_stat("errors")
            return None
        except Exception as e:
            print(f"Reddit Auth Error: {type(e).__name__}: {e}")
            self._increment_stat("errors")
            return None

    def _make_request(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """
        Make authenticated request to Reddit API.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Parsed JSON response or None on error
        """
        token = self._get_access_token()
        if not token:
            return None

        url = f"{self.API_URL}/{endpoint}"
        if params:
            url += "?" + urllib.parse.urlencode(params)

        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "User-Agent": self.user_agent
                }
            )

            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                return json.loads(response.read().decode('utf-8'))

        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("Reddit: Rate limited")
                self._increment_stat("rate_limited")
            else:
                print(f"Reddit HTTP {e.code}: {e.reason}")
            self._increment_stat("errors")
            return None
        except Exception as e:
            print(f"Reddit Error: {type(e).__name__}: {e}")
            self._increment_stat("errors")
            return None

    def _parse_post(self, post_data: dict, subreddit_info: dict = None) -> RawItem:
        """
        Parse Reddit post into RawItem.

        Args:
            post_data: Post data dict
            subreddit_info: Subreddit configuration

        Returns:
            Normalized RawItem
        """
        data = post_data.get("data", post_data)

        post_id = data.get("id", "")
        title = data.get("title", "")
        selftext = data.get("selftext", "")
        url = data.get("url", "")
        permalink = f"https://www.reddit.com{data.get('permalink', '')}"
        subreddit = data.get("subreddit", "")
        author = data.get("author", "[deleted]")

        # Timestamp
        created_utc = data.get("created_utc", 0)
        published_at = datetime.fromtimestamp(created_utc, tz=timezone.utc).isoformat() if created_utc else None

        # Engagement
        score = data.get("score", 0)
        num_comments = data.get("num_comments", 0)
        upvote_ratio = data.get("upvote_ratio", 0)

        # Images
        images = []
        if data.get("thumbnail") and data["thumbnail"].startswith("http"):
            images.append(data["thumbnail"])

        # Preview images
        preview = data.get("preview", {})
        if preview.get("images"):
            for img in preview["images"][:1]:
                source = img.get("source", {})
                if source.get("url"):
                    # Unescape URL
                    images.append(source["url"].replace("&amp;", "&"))

        # Build text
        text = f"{title}\n\n{selftext}" if selftext else title

        # Determine if it's a link post
        is_self = data.get("is_self", True)
        category = subreddit_info.get("category", "discussion") if subreddit_info else "discussion"

        # Generate ID
        item_id = RawItem.generate_id("reddit", f"{post_id}{title}")

        return RawItem(
            id=item_id,
            source_type="reddit",
            source_adapter="reddit_oauth",
            source_name=f"r/{subreddit}",
            source_url=permalink if is_self else url,
            title=title,
            text=text,
            language="en",
            author=author,
            published_at=published_at,
            category=category,
            tags=[subreddit],
            images=images,
            engagement={
                "score": score,
                "comments": num_comments,
                "upvote_ratio": upvote_ratio
            }
        )

    def _fetch_subreddit(self, subreddit_config: dict, since_hours: int = 24) -> list[RawItem]:
        """
        Fetch posts from a subreddit.

        Args:
            subreddit_config: Subreddit configuration dict
            since_hours: Time window

        Returns:
            List of RawItem objects
        """
        name = subreddit_config.get("name")
        sort = subreddit_config.get("sort", "hot")
        limit = subreddit_config.get("limit", 25)

        if not name:
            return []

        endpoint = f"r/{name}/{sort}"
        params = {"limit": limit}

        data = self._make_request(endpoint, params)
        if not data:
            return []

        posts = data.get("data", {}).get("children", [])
        cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)

        items = []
        for post in posts:
            try:
                # Check age
                created_utc = post.get("data", {}).get("created_utc", 0)
                if created_utc:
                    post_time = datetime.fromtimestamp(created_utc, tz=timezone.utc)
                    if post_time < cutoff:
                        continue

                # Check score
                score = post.get("data", {}).get("score", 0)
                if score < self.min_score:
                    continue

                item = self._parse_post(post, subreddit_config)
                items.append(item)
                self._increment_stat("fetched")

            except Exception as e:
                print(f"Reddit: Error parsing post: {e}")
                self._increment_stat("errors")

        return items

    def _search_reddit(self, query: str, since_hours: int = 24,
                       subreddit: str = None, limit: int = 25) -> list[RawItem]:
        """
        Search Reddit.

        Args:
            query: Search query
            since_hours: Time window
            subreddit: Optional subreddit to search within
            limit: Max results

        Returns:
            List of RawItem objects
        """
        if subreddit:
            endpoint = f"r/{subreddit}/search"
            params = {
                "q": query,
                "restrict_sr": "on",
                "sort": "new",
                "limit": limit,
                "t": "week"
            }
        else:
            endpoint = "search"
            params = {
                "q": query,
                "sort": "new",
                "limit": limit,
                "t": "week"
            }

        data = self._make_request(endpoint, params)
        if not data:
            return []

        posts = data.get("data", {}).get("children", [])
        cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)

        items = []
        for post in posts:
            try:
                created_utc = post.get("data", {}).get("created_utc", 0)
                if created_utc:
                    post_time = datetime.fromtimestamp(created_utc, tz=timezone.utc)
                    if post_time < cutoff:
                        continue

                item = self._parse_post(post)
                items.append(item)
                self._increment_stat("fetched")

            except Exception as e:
                print(f"Reddit: Error parsing search result: {e}")
                self._increment_stat("errors")

        return items

    def fetch(self, keywords: list[str], since_hours: int = 24) -> list[RawItem]:
        """
        Fetch posts from subreddits and search.

        Args:
            keywords: Search keywords
            since_hours: Time window

        Returns:
            List of RawItem objects
        """
        if not self.is_enabled():
            return []

        all_items = []

        # Fetch from configured subreddits
        if self.subreddits:
            print(f"Reddit: Fetching from {len(self.subreddits)} subreddits")

            for sub_config in self.subreddits:
                sub_name = sub_config.get("name", "")
                print(f"Reddit:   Fetching r/{sub_name}...")

                items = self._fetch_subreddit(sub_config, since_hours)
                print(f"Reddit:     Got {len(items)} posts")
                all_items.extend(items)

        # Search if keywords provided
        if keywords:
            query = " ".join(keywords)
            print(f"Reddit: Searching for: {query}")

            search_items = self._search_reddit(query, since_hours)
            print(f"Reddit:   Found {len(search_items)} results")
            all_items.extend(search_items)

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
            "quick": {"hours": 48, "limit": 10},
            "standard": {"hours": 168, "limit": 25},
            "deep": {"hours": 336, "limit": 50}
        }

        config = depth_config.get(depth, depth_config["standard"])

        # Extract keywords
        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or'}
        words = topic.lower().split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2][:5]

        return self.fetch(keywords, since_hours=config["hours"])


def test_reddit():
    """Test the Reddit adapter."""
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    config = {
        "enabled": True,
        "client_id": os.environ.get("REDDIT_CLIENT_ID", ""),
        "client_secret": os.environ.get("REDDIT_SECRET", ""),
        "user_agent": "BNIS/2.0 (continuum intelligence)",
        "subreddits": [
            {"name": "news", "sort": "hot", "limit": 10},
            {"name": "law", "sort": "new", "limit": 10}
        ],
        "min_score": 10,
        "timeout_seconds": 30
    }

    adapter = RedditAdapter(config)

    print("\n" + "=" * 60)
    print("Reddit Adapter Test")
    print("=" * 60)

    if not adapter.client_id or not adapter.client_secret:
        print("\n[SKIP] No credentials found.")
        print("Set REDDIT_CLIENT_ID and REDDIT_SECRET environment variables.")
        print("Register app at: https://www.reddit.com/prefs/apps")
        return []

    # Test fetch
    print("\n[TEST 1] Fetch from subreddits + search")
    items = adapter.fetch(["Epstein", "Maxwell"], since_hours=168)

    print(f"\nFetched {len(items)} items")
    print(f"Stats: {adapter.get_stats()}")

    if items:
        print("\nSample items:")
        for i, item in enumerate(items[:3]):
            title = item.title[:60] if item.title else "(no title)"
            print(f"\n  [{i+1}] {title}...")
            print(f"      Subreddit: {item.source_name}")
            print(f"      Score: {item.engagement.get('score', 0) if item.engagement else 0}")
            print(f"      Published: {item.published_at}")

    print("\n" + "=" * 60)
    print("Reddit adapter test complete!")
    print("=" * 60 + "\n")

    return items


if __name__ == "__main__":
    test_reddit()
