# BNIS v2 - Multi-Source Intelligence Architecture

> Expanding from Twitter-only to comprehensive multi-source news intelligence

**Created:** 2026-01-31
**Status:** Design Phase

---

## Vision

Transform BNIS from a Twitter-only monitor into a **comprehensive intelligence aggregation platform** that:

1. Monitors **multiple source types** (news, social, video, local)
2. **Aggregates context** on topics across all sources
3. **Triangulates** information for credibility assessment
4. Maintains entity matching and connection building
5. Feeds the hierarchical framework (Ground → Events → Systems → Macro)

---

## Architecture Overview

```
                    ┌─────────────────────────────────────────────────────────────┐
                    │                    SOURCE ADAPTERS                           │
                    │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│
                    │  │ Twitter │ │ NewsAPI │ │ YouTube │ │ Reddit  │ │  RSS    ││
                    │  │ Adapter │ │ Adapter │ │ Adapter │ │ Adapter │ │ Adapter ││
                    │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘│
                    └───────┼──────────┼──────────┼──────────┼──────────┼────────┘
                            │          │          │          │          │
                            └──────────┴──────────┴──────────┴──────────┘
                                                  │
                                                  ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │                    UNIFIED COLLECTOR                         │
                    │  • Normalize all sources to common schema                    │
                    │  • Deduplicate across sources                                │
                    │  • Calculate cross-source relevance                          │
                    │  • Trigger topic fan-out                                     │
                    └─────────────────────────────┬───────────────────────────────┘
                                                  │
                                                  ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │                    TOPIC AGGREGATOR                          │
                    │  • Detect emerging topics                                    │
                    │  • Fan out to all sources for context                        │
                    │  • Build topic dossiers                                      │
                    │  • Merge related stories                                     │
                    └─────────────────────────────┬───────────────────────────────┘
                                                  │
                                                  ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │                  EXISTING BNIS PIPELINE                      │
                    │  raw_news/ → news_processor.py → entity_matcher.py →        │
                    │  approval_daemon.py → publish.py → website/                  │
                    └─────────────────────────────────────────────────────────────┘
```

---

## Source Adapters

### Design Principle: Pluggable Adapters

Each source type gets an adapter that implements a common interface:

```python
class SourceAdapter(ABC):
    """Base class for all source adapters."""

    @abstractmethod
    def fetch(self, keywords: list[str], since: datetime) -> list[RawItem]:
        """Fetch items matching keywords since timestamp."""
        pass

    @abstractmethod
    def fetch_topic_context(self, topic: str, depth: str = "standard") -> list[RawItem]:
        """Deep fetch for topic context aggregation."""
        pass

    @property
    @abstractmethod
    def source_type(self) -> str:
        """Return source type identifier (twitter, news, youtube, etc.)"""
        pass

    @property
    @abstractmethod
    def rate_limits(self) -> dict:
        """Return rate limit configuration."""
        pass
```

### Adapter Implementations

| Adapter | Source | API/Method | Rate Limits | Cost |
|---------|--------|------------|-------------|------|
| `TwitterAdapter` | X/Twitter | RSSHub/Nitter | 100/15min | Free |
| `NewsAPIAdapter` | News articles | NewsAPI.org | 100/day (free) | Free/$449/mo |
| `GDELTAdapter` | Global news | GDELT 2.0 API | Unlimited | Free |
| `YouTubeAdapter` | Videos | YouTube Data API v3 | 10,000 units/day | Free |
| `RedditAdapter` | Reddit | Reddit API | 60/min | Free |
| `RSSAdapter` | Generic RSS | feedparser | N/A | Free |
| `LocalNewsAdapter` | Local markets | RSS aggregation | N/A | Free |
| `PodcastAdapter` | Podcasts | RSS + Whisper | N/A | Free (compute) |

---

## Unified Item Schema

All adapters normalize to a common schema:

```json
{
  "id": "2026-01-31_abc123def",
  "source_type": "news",
  "source_adapter": "newsapi",
  "source_name": "Reuters",
  "source_url": "https://reuters.com/article/...",

  "content": {
    "title": "New Epstein Documents Released by DOJ",
    "text": "Full article text or transcript...",
    "summary": "AI-generated summary if available",
    "language": "en"
  },

  "metadata": {
    "author": "John Smith",
    "published_at": "2026-01-31T14:30:00Z",
    "fetched_at": "2026-01-31T14:35:22Z",
    "category": "legal",
    "tags": ["epstein", "doj", "documents"],
    "location": {"country": "US", "region": "New York"},
    "engagement": {"views": 50000, "shares": 1200}
  },

  "media": {
    "images": ["https://..."],
    "video_url": null,
    "video_transcript": null
  },

  "analysis": {
    "relevance_score": 0.92,
    "keywords_matched": ["Epstein", "DOJ", "documents"],
    "entities_detected": ["jeffrey-epstein", "doj"],
    "sentiment": "neutral",
    "credibility_signals": ["official_source", "primary_document"]
  }
}
```

---

## Topic Aggregator

### Concept: Topic-Driven Context Gathering

When a relevant story is detected, **fan out to all sources** to build comprehensive context:

```
Story Detected: "DOJ releases new Epstein documents"
    │
    ├─▶ TWITTER: Search "Epstein documents", monitor reactions
    ├─▶ NEWSAPI: Search major outlets for coverage
    ├─▶ YOUTUBE: Find video explainers, news segments
    ├─▶ REDDIT: Check r/news, r/politics, r/conspiracy discussions
    ├─▶ LOCAL: Check NY Times, Miami Herald (key jurisdictions)
    │
    ▼
Topic Dossier: {
  "topic_id": "epstein-doj-release-2026-01",
  "primary_story": {...},
  "related_coverage": [
    {"source": "nytimes", "angle": "legal analysis"},
    {"source": "youtube", "angle": "document walkthrough"},
    {"source": "reddit", "angle": "public discussion"}
  ],
  "timeline": [...],
  "entities_mentioned": [...],
  "source_credibility": 0.87
}
```

### Topic Detection Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| High-priority keyword match | relevance > 0.8 | Immediate fan-out |
| Multiple sources same story | 3+ sources in 1hr | Topic creation |
| Existing entity mentioned | any mention | Context enrichment |
| Breaking news signal | "BREAKING" + keyword | Priority fan-out |

---

## Source-Specific Configurations

### 1. News Articles (NewsAPI)

```json
{
  "newsapi": {
    "api_key": "${NEWSAPI_KEY}",
    "sources": [
      "reuters", "associated-press", "bbc-news",
      "the-new-york-times", "the-washington-post",
      "the-guardian-us", "cnn", "fox-news"
    ],
    "domains": [
      "courthousenews.com", "lawandcrime.com",
      "dropsitenesw.com", "mintpressnews.com"
    ],
    "refresh_interval_minutes": 30
  }
}
```

### 2. GDELT (Global News)

```json
{
  "gdelt": {
    "base_url": "https://api.gdeltproject.org/api/v2/doc/doc",
    "modes": ["artlist", "timeline"],
    "filters": {
      "theme": ["TAX_FNCACT_ARREST", "TAX_FNCACT_LAWSUIT"],
      "sourcelang": "eng"
    },
    "refresh_interval_minutes": 60
  }
}
```

### 3. YouTube

```json
{
  "youtube": {
    "api_key": "${YOUTUBE_API_KEY}",
    "channels": [
      {"id": "UCxxxxx", "name": "Law & Crime Network"},
      {"id": "UCyyyyy", "name": "Court TV"}
    ],
    "search_queries": [
      "Epstein documents",
      "Maxwell trial"
    ],
    "fetch_transcripts": true,
    "transcript_method": "youtube_api",
    "max_video_age_days": 7
  }
}
```

### 4. Reddit

```json
{
  "reddit": {
    "client_id": "${REDDIT_CLIENT_ID}",
    "client_secret": "${REDDIT_SECRET}",
    "subreddits": [
      {"name": "news", "priority": "high"},
      {"name": "politics", "priority": "medium"},
      {"name": "law", "priority": "high"},
      {"name": "conspiracy", "priority": "low", "note": "monitor for disinfo"}
    ],
    "search_queries": ["Epstein", "Maxwell", "DOJ"],
    "include_comments": true,
    "comment_depth": 2
  }
}
```

### 5. Local News (RSS Aggregation)

```json
{
  "local_news": {
    "markets": [
      {
        "name": "New York",
        "outlets": [
          {"name": "NY Times", "rss": "https://rss.nytimes.com/..."},
          {"name": "NY Post", "rss": "https://nypost.com/feed/"}
        ]
      },
      {
        "name": "South Florida",
        "outlets": [
          {"name": "Miami Herald", "rss": "https://..."},
          {"name": "Palm Beach Post", "rss": "https://..."}
        ],
        "priority": "high",
        "note": "Key Epstein jurisdiction"
      }
    ]
  }
}
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Create adapter base class and interface
- [ ] Refactor existing Twitter fetcher to adapter pattern
- [ ] Build unified collector
- [ ] Update config schema for multi-source

### Phase 2: News Integration (Week 3-4)
- [ ] Implement NewsAPI adapter
- [ ] Implement GDELT adapter
- [ ] Add local news RSS aggregation
- [ ] Test news → entity matching

### Phase 3: Social & Video (Week 5-6)
- [ ] Implement YouTube adapter + transcript extraction
- [ ] Implement Reddit adapter
- [ ] Add comment/discussion analysis
- [ ] Test social → entity matching

### Phase 4: Topic Aggregation (Week 7-8)
- [ ] Build topic detection system
- [ ] Implement fan-out logic
- [ ] Create topic dossier format
- [ ] Integration testing

### Phase 5: Polish & Scale (Week 9-10)
- [ ] Rate limit optimization
- [ ] Caching layer
- [ ] Performance tuning
- [ ] Documentation

---

## API Requirements Summary

| Service | Cost | Rate Limits | Signup |
|---------|------|-------------|--------|
| **NewsAPI** | Free (100/day) or $449/mo | 100/day free | newsapi.org |
| **GDELT** | Free | Unlimited | No signup needed |
| **YouTube Data API** | Free (10k units/day) | 10,000 units/day | Google Cloud Console |
| **Reddit API** | Free | 60 req/min | Reddit app registration |
| **RSS Feeds** | Free | N/A | N/A |

### Recommended First Steps

1. **GDELT** - No API key needed, start immediately
2. **NewsAPI** - Free tier for development
3. **YouTube** - Create Google Cloud project
4. **Reddit** - Register Reddit app

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           BNIS v2 DATA FLOW                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  SOURCES                    COLLECTION                    PROCESSING          │
│  ────────                   ──────────                    ──────────          │
│                                                                               │
│  ┌─────────┐                                                                  │
│  │ Twitter │─┐                                                                │
│  └─────────┘ │              ┌──────────────┐                                  │
│  ┌─────────┐ │              │   Unified    │              ┌──────────────┐   │
│  │ NewsAPI │─┼──────────────│  Collector   │──────────────│   Topic      │   │
│  └─────────┘ │              │              │              │  Aggregator  │   │
│  ┌─────────┐ │              │  • Normalize │              │              │   │
│  │ YouTube │─┼──────────────│  • Dedup     │──────────────│  • Detect    │   │
│  └─────────┘ │              │  • Score     │              │  • Fan-out   │   │
│  ┌─────────┐ │              │  • Trigger   │              │  • Aggregate │   │
│  │ Reddit  │─┤              └──────────────┘              └──────┬───────┘   │
│  └─────────┘ │                                                   │            │
│  ┌─────────┐ │                                                   │            │
│  │  RSS    │─┘                                                   │            │
│  └─────────┘                                                     │            │
│                                                                  ▼            │
│                          ┌────────────────────────────────────────────────┐  │
│                          │              EXISTING PIPELINE                  │  │
│                          │  raw_news/ → processor → matcher → approval →  │  │
│                          │  publish → website/                             │  │
│                          └────────────────────────────────────────────────┘  │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Next Steps

1. **Review this design** - Does this match your vision?
2. **Set up API access** - Start with free tiers (GDELT, NewsAPI free, YouTube)
3. **Begin Phase 1** - Refactor to adapter pattern
4. **Iterate** - Add sources incrementally

---

*Part of The Continuum Report - Another Node in the Decentralized Intelligence Agency*
