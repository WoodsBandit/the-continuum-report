#!/usr/bin/env python3
"""
Entity Matcher for Breaking News Intelligence System (BNIS)
Fuzzy-matches news mentions to 2,008+ entities from entities-master.json

Matching Strategy:
1. Exact match -> confidence: "documented"
2. Alias match -> confidence: "referenced"
3. Fuzzy match (>85% similarity) -> confidence: "interpreted"
4. No match -> track for auto-add threshold
"""

import json
import os
import re
from pathlib import Path
from difflib import SequenceMatcher
from typing import Optional
from dataclasses import dataclass, field

# Base directory for continuum project
BASE_DIR = Path(__file__).parent.parent.parent

@dataclass
class EntityMatch:
    """Represents a matched entity from news content."""
    mentioned_name: str
    matched_id: str
    confidence: str  # documented, referenced, interpreted, provisional
    similarity: float
    in_manifest: bool
    network: Optional[str] = None
    entity_type: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "mentioned_name": self.mentioned_name,
            "matched_id": self.matched_id,
            "confidence": self.confidence,
            "similarity": round(self.similarity, 3),
            "in_manifest": self.in_manifest,
            "network": self.network,
            "entity_type": self.entity_type
        }

@dataclass
class ProvisionalEntity:
    """Tracks entities not yet in the system awaiting threshold."""
    name: str
    mention_count: int = 1
    story_ids: list = field(default_factory=list)
    first_seen: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "mention_count": self.mention_count,
            "story_ids": self.story_ids,
            "first_seen": self.first_seen
        }

class EntityMatcher:
    """
    Matches text mentions against the Continuum entity database.
    Supports exact, alias, and fuzzy matching with configurable thresholds.
    """

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or BASE_DIR / "bnis" / "config" / "news_config.json"
        self.manifest_path = BASE_DIR / "website" / "data" / "manifest.json"
        self.entities_master_path = BASE_DIR / "website" / "data" / "entities-master.json"
        self.hierarchy_path = BASE_DIR / "website" / "data" / "hierarchy.json"
        self.provisional_path = BASE_DIR / "bnis" / "data" / "provisional_entities.json"

        # Load configuration
        self.config = self._load_json(self.config_path)

        # Load entity data
        self.manifest = self._load_json(self.manifest_path)
        self.entities_master = self._load_json(self.entities_master_path)
        self.hierarchy = self._load_json(self.hierarchy_path)

        # Build lookup indexes
        self._build_indexes()

        # Load or create provisional entities tracker
        self.provisional_entities: dict[str, ProvisionalEntity] = {}
        self._load_provisional_entities()

    def _load_json(self, path: Path) -> dict:
        """Load JSON file, return empty dict if not found."""
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_json(self, path: Path, data: dict) -> None:
        """Save data to JSON file, creating directories if needed."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _build_indexes(self) -> None:
        """Build lookup indexes for fast matching."""
        # Index of manifest entity IDs -> entity info
        self.manifest_entities: dict[str, dict] = {}
        if "briefs" in self.manifest:
            for brief in self.manifest["briefs"]:
                self.manifest_entities[brief["id"]] = {
                    "name": brief["name"],
                    "type": brief.get("type"),
                    "file": brief.get("file")
                }

        # Index of entity ID -> network from hierarchy
        self.entity_networks: dict[str, str] = {}
        if "entityParents" in self.hierarchy:
            self.entity_networks = self.hierarchy["entityParents"]

        # Build aliases from config
        self.aliases: dict[str, str] = {}  # alias -> entity_id
        if "keywords" in self.config and "entity_aliases" in self.config["keywords"]:
            for entity_id, alias_list in self.config["keywords"]["entity_aliases"].items():
                for alias in alias_list:
                    self.aliases[alias.lower()] = entity_id

        # Build name to ID mapping for all manifest entities
        self.name_to_id: dict[str, str] = {}
        for entity_id, info in self.manifest_entities.items():
            self.name_to_id[info["name"].lower()] = entity_id

        # Extract all person names from entities-master for broader matching
        self.master_names: list[str] = []
        if "people" in self.entities_master:
            self.master_names = list(self.entities_master["people"].keys())

    def _load_provisional_entities(self) -> None:
        """Load provisional entities from disk."""
        if self.provisional_path.exists():
            data = self._load_json(self.provisional_path)
            for name, info in data.items():
                self.provisional_entities[name] = ProvisionalEntity(
                    name=name,
                    mention_count=info.get("mention_count", 1),
                    story_ids=info.get("story_ids", []),
                    first_seen=info.get("first_seen", "")
                )

    def save_provisional_entities(self) -> None:
        """Save provisional entities to disk."""
        data = {name: entity.to_dict() for name, entity in self.provisional_entities.items()}
        self._save_json(self.provisional_path, data)

    def normalize_text(self, text: str) -> str:
        """Normalize text for matching."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        return text

    def similarity(self, a: str, b: str) -> float:
        """Calculate similarity ratio between two strings."""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def match_entity(self, mention: str) -> Optional[EntityMatch]:
        """
        Match a mentioned name against the entity database.
        Returns EntityMatch or None if no match found.
        """
        mention_normalized = self.normalize_text(mention)
        mention_lower = mention_normalized.lower()

        # 1. Check exact match against manifest entity names
        if mention_lower in self.name_to_id:
            entity_id = self.name_to_id[mention_lower]
            return EntityMatch(
                mentioned_name=mention,
                matched_id=entity_id,
                confidence="documented",
                similarity=1.0,
                in_manifest=True,
                network=self.entity_networks.get(entity_id),
                entity_type=self.manifest_entities[entity_id].get("type")
            )

        # 2. Check alias match
        if mention_lower in self.aliases:
            entity_id = self.aliases[mention_lower]
            if entity_id in self.manifest_entities:
                return EntityMatch(
                    mentioned_name=mention,
                    matched_id=entity_id,
                    confidence="referenced",
                    similarity=0.95,
                    in_manifest=True,
                    network=self.entity_networks.get(entity_id),
                    entity_type=self.manifest_entities[entity_id].get("type")
                )

        # 3. Fuzzy match against manifest entity names
        best_match = None
        best_similarity = 0.0

        for entity_id, info in self.manifest_entities.items():
            sim = self.similarity(mention_normalized, info["name"])
            if sim > best_similarity:
                best_similarity = sim
                best_match = (entity_id, info)

        # Check threshold from config
        min_sim = self.config.get("confidence_levels", {}).get("interpreted", {}).get("min_similarity", 0.85)

        if best_match and best_similarity >= min_sim:
            entity_id, info = best_match
            return EntityMatch(
                mentioned_name=mention,
                matched_id=entity_id,
                confidence="interpreted",
                similarity=best_similarity,
                in_manifest=True,
                network=self.entity_networks.get(entity_id),
                entity_type=info.get("type")
            )

        # 4. Check against broader entities-master (not in manifest)
        for master_name in self.master_names:
            sim = self.similarity(mention_normalized, master_name)
            if sim > best_similarity:
                best_similarity = sim
                best_match = (master_name, {"name": master_name, "type": "person"})

        if best_match and best_similarity >= min_sim:
            name, info = best_match
            # Create a slug-style ID
            entity_id = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
            return EntityMatch(
                mentioned_name=mention,
                matched_id=entity_id,
                confidence="interpreted",
                similarity=best_similarity,
                in_manifest=False,  # Not in curated manifest
                network=None,
                entity_type=info.get("type")
            )

        # No match found
        return None

    def match_all(self, text: str) -> list[EntityMatch]:
        """
        Find all entity mentions in a text.
        Returns list of EntityMatch objects.
        """
        matches = []
        seen_ids = set()

        # Try matching against all known names and aliases
        all_search_terms = set()

        # Add manifest entity names
        for entity_id, info in self.manifest_entities.items():
            all_search_terms.add(info["name"])

        # Add aliases
        for alias in self.aliases.keys():
            all_search_terms.add(alias)

        # Add high priority keywords from config
        if "keywords" in self.config and "high_priority" in self.config["keywords"]:
            for keyword in self.config["keywords"]["high_priority"]:
                all_search_terms.add(keyword)

        # Search for each term in the text
        text_lower = text.lower()
        for term in all_search_terms:
            if term.lower() in text_lower:
                match = self.match_entity(term)
                if match and match.matched_id not in seen_ids:
                    matches.append(match)
                    seen_ids.add(match.matched_id)

        return matches

    def track_provisional(self, name: str, story_id: str, timestamp: str) -> Optional[dict]:
        """
        Track a new entity mention that didn't match existing entities.
        Returns entity info if it has crossed the auto-add threshold.
        """
        name_normalized = self.normalize_text(name)

        if name_normalized not in self.provisional_entities:
            self.provisional_entities[name_normalized] = ProvisionalEntity(
                name=name_normalized,
                mention_count=1,
                story_ids=[story_id],
                first_seen=timestamp
            )
        else:
            entity = self.provisional_entities[name_normalized]
            if story_id not in entity.story_ids:
                entity.mention_count += 1
                entity.story_ids.append(story_id)

        # Check threshold
        threshold = self.config.get("thresholds", {}).get("auto_add_entity_mentions", 3)
        entity = self.provisional_entities[name_normalized]

        if entity.mention_count >= threshold:
            return {
                "name": entity.name,
                "mention_count": entity.mention_count,
                "story_ids": entity.story_ids,
                "first_seen": entity.first_seen,
                "ready_for_promotion": True
            }

        return None

    def get_entity_context(self, entity_ids: list[str]) -> dict:
        """
        Get context information for a list of entity IDs.
        Useful for building Claude Code prompts.
        """
        context = {
            "entities": [],
            "networks": set(),
            "types": {}
        }

        for entity_id in entity_ids:
            if entity_id in self.manifest_entities:
                info = self.manifest_entities[entity_id]
                network = self.entity_networks.get(entity_id)

                context["entities"].append({
                    "id": entity_id,
                    "name": info["name"],
                    "type": info.get("type"),
                    "network": network,
                    "in_manifest": True
                })

                if network:
                    context["networks"].add(network)

                entity_type = info.get("type", "unknown")
                context["types"][entity_type] = context["types"].get(entity_type, 0) + 1

        context["networks"] = list(context["networks"])
        return context


def main():
    """Test the entity matcher."""
    matcher = EntityMatcher()

    # Test cases
    test_mentions = [
        "Jeffrey Epstein",
        "Epstein",
        "Ghislaine Maxwell",
        "Maxwell",
        "Virginia Giuffre",
        "Virginia Roberts",
        "Les Wexner",
        "Prince Andrew",
        "Duke of York",
        "Some Random Person",
        "court filing",
        "NXIVM"
    ]

    print("Entity Matcher Test Results")
    print("=" * 60)

    for mention in test_mentions:
        match = matcher.match_entity(mention)
        if match:
            print(f"\n'{mention}':")
            print(f"  -> {match.matched_id} ({match.confidence})")
            print(f"     Similarity: {match.similarity:.2%}")
            print(f"     In Manifest: {match.in_manifest}")
            print(f"     Network: {match.network}")
        else:
            print(f"\n'{mention}': No match found")

    # Test full text matching
    print("\n" + "=" * 60)
    print("Full Text Match Test")
    print("=" * 60)

    test_text = """
    Breaking: New court documents reveal Jeffrey Epstein met with
    Les Wexner multiple times in 2007. The filing also mentions
    Ghislaine Maxwell and references the NXIVM case.
    """

    matches = matcher.match_all(test_text)
    print(f"\nFound {len(matches)} entity matches in text:")
    for match in matches:
        print(f"  - {match.matched_id}: '{match.mentioned_name}' ({match.confidence})")

    # Get context for matched entities
    entity_ids = [m.matched_id for m in matches]
    context = matcher.get_entity_context(entity_ids)
    print(f"\nContext:")
    print(f"  Networks involved: {context['networks']}")
    print(f"  Entity types: {context['types']}")


if __name__ == "__main__":
    main()
