#!/usr/bin/env python3
"""
Base adapter class for BNIS v2 multi-source intelligence.

All source adapters (Twitter, GDELT, NewsAPI, YouTube, Reddit, etc.)
implement this interface for unified data collection.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import hashlib
import re


@dataclass
class RawItem:
    """
    Unified schema for items from any source.
    All adapters normalize their data to this format.
    """
    # Identity
    id: str
    source_type: str  # twitter, gdelt, newsapi, youtube, reddit, rss
    source_adapter: str  # specific adapter name
    source_name: str  # outlet/account name
    source_url: str  # original URL

    # Content
    title: str
    text: str
    summary: Optional[str] = None
    language: str = "en"

    # Metadata
    author: Optional[str] = None
    published_at: Optional[str] = None
    fetched_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    category: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    location: Optional[dict] = None  # {"country": "US", "region": "NY"}

    # Engagement (if available)
    engagement: Optional[dict] = None  # {"views": 1000, "shares": 50}

    # Media
    images: list[str] = field(default_factory=list)
    video_url: Optional[str] = None
    video_transcript: Optional[str] = None

    # Analysis (populated by processor)
    relevance_score: float = 0.0
    keywords_matched: list[str] = field(default_factory=list)
    entities_detected: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "source_type": self.source_type,
            "source_adapter": self.source_adapter,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "content": {
                "title": self.title,
                "text": self.text,
                "summary": self.summary,
                "language": self.language
            },
            "metadata": {
                "author": self.author,
                "published_at": self.published_at,
                "fetched_at": self.fetched_at,
                "category": self.category,
                "tags": self.tags,
                "location": self.location,
                "engagement": self.engagement
            },
            "media": {
                "images": self.images,
                "video_url": self.video_url,
                "video_transcript": self.video_transcript
            },
            "analysis": {
                "relevance_score": self.relevance_score,
                "keywords_matched": self.keywords_matched,
                "entities_detected": self.entities_detected
            }
        }

    @staticmethod
    def generate_id(source_type: str, content: str) -> str:
        """Generate unique ID from source type and content hash."""
        normalized = re.sub(r'\s+', ' ', content.strip().lower())
        content_hash = hashlib.md5(normalized.encode('utf-8')).hexdigest()[:12]
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return f"{date_str}_{source_type}_{content_hash}"


class SourceAdapter(ABC):
    """
    Abstract base class for all source adapters.

    Each adapter must implement:
    - fetch(): Get items matching keywords
    - fetch_topic_context(): Deep fetch for topic aggregation
    - source_type: Identifier string
    - rate_limits: Rate limit configuration
    """

    def __init__(self, config: dict):
        """
        Initialize adapter with configuration.

        Args:
            config: Adapter-specific configuration from news_config_v2.json
        """
        self.config = config
        self.enabled = config.get("enabled", False)
        self._stats = {
            "fetched": 0,
            "errors": 0,
            "rate_limited": 0
        }

    @property
    @abstractmethod
    def source_type(self) -> str:
        """Return source type identifier (twitter, gdelt, newsapi, etc.)"""
        pass

    @property
    @abstractmethod
    def rate_limits(self) -> dict:
        """
        Return rate limit configuration.

        Example:
            {"requests_per_minute": 60, "requests_per_day": 1000}
        """
        pass

    @abstractmethod
    def fetch(self, keywords: list[str], since_hours: int = 24) -> list[RawItem]:
        """
        Fetch items matching keywords from the past N hours.

        Args:
            keywords: List of keywords to search for
            since_hours: How far back to search (default 24h)

        Returns:
            List of RawItem objects
        """
        pass

    @abstractmethod
    def fetch_topic_context(self, topic: str, depth: str = "standard") -> list[RawItem]:
        """
        Deep fetch for topic context aggregation.

        Called when a high-relevance story is detected to gather
        comprehensive context from this source.

        Args:
            topic: Topic string or primary story summary
            depth: "quick" (5 items), "standard" (25 items), "deep" (100 items)

        Returns:
            List of RawItem objects providing context
        """
        pass

    def is_enabled(self) -> bool:
        """Check if adapter is enabled in config."""
        return self.enabled

    def get_stats(self) -> dict:
        """Return fetch statistics."""
        return self._stats.copy()

    def reset_stats(self) -> None:
        """Reset fetch statistics."""
        self._stats = {"fetched": 0, "errors": 0, "rate_limited": 0}

    def _increment_stat(self, stat: str, count: int = 1) -> None:
        """Increment a statistic counter."""
        if stat in self._stats:
            self._stats[stat] += count
