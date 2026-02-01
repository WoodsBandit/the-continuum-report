# BNIS v2 Source Adapters
# Pluggable adapters for multi-source news intelligence

from .base import SourceAdapter, RawItem
from .gdelt import GDELTAdapter
from .rss import RSSAdapter
from .newsapi import NewsAPIAdapter
from .youtube import YouTubeAdapter
from .reddit import RedditAdapter
from .local_news import LocalNewsAdapter

__all__ = [
    'SourceAdapter',
    'RawItem',
    'GDELTAdapter',
    'RSSAdapter',
    'NewsAPIAdapter',
    'YouTubeAdapter',
    'RedditAdapter',
    'LocalNewsAdapter'
]
