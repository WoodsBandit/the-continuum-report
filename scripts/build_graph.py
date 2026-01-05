#!/usr/bin/env python3
"""
build_graph.py - Build the complete knowledge graph from all analytical briefs
Version 2.1 - Binary Connection Model

ARCHITECTURAL PRINCIPLE:
    CONNECTION BRIEFS ARE THE SOURCE OF TRUTH.
    No connection exists without a corresponding brief.
    Each brief contains: quote + source + summary.
    No subjective "strength" scoring.

Usage:
    python build_graph.py [--briefs-dir PATH] [--output-dir PATH]

This script:
1. Scans all briefs in the briefs directory
2. Parses each brief using parse_brief.py
3. Generates entities.json (connections are built separately)
4. Generates manifest.json

IMPORTANT: Connections are built by build_connections_from_briefs.py, NOT this script.

Changes in v2.1:
- Removed strength scoring (binary model)
- Connections handled by separate brief-based script
- Strength-based functions marked DEPRECATED

Changes in v2.0:
- Structured logging with structlog (lib.logging_config)
- Better error handling
- Path handling improvements
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Import shared library for logging
from lib import get_logger

# Initialize logger
logger = get_logger(__name__)

# Import the parse_brief function from our parser
sys.path.insert(0, str(Path(__file__).parent))
from parse_brief import parse_brief, ENTITY_NAMES


def scan_briefs(briefs_dir: Path) -> List[Path]:
    """Find all analytical brief markdown files"""
    briefs = list(briefs_dir.glob("analytical_brief_*.md"))
    logger.info("Scanned briefs directory", path=str(briefs_dir), count=len(briefs))
    return sorted(briefs)


def build_entities(briefs: List[Path]) -> Dict[str, dict]:
    """Parse all briefs and build entities dictionary"""
    entities = {}
    errors = []

    logger.info("Building entities from briefs", total_briefs=len(briefs))

    for brief_path in briefs:
        try:
            entity = parse_brief(str(brief_path))
            entities[entity['id']] = entity
            logger.debug("Brief parsed", name=entity['name'], type=entity['type'])
            print(f"  Parsed: {entity['name']} ({entity['type']})")
        except Exception as e:
            errors.append((brief_path.name, str(e)))
            logger.error("Failed to parse brief", brief=brief_path.name, error=str(e))
            print(f"  ERROR: {brief_path.name} - {e}")

    if errors:
        logger.warning("Some briefs had errors", error_count=len(errors))
        print(f"\nWarnings: {len(errors)} briefs had errors")

    logger.info("Entities built", total_entities=len(entities))
    return entities


def calculate_connection_strength_DEPRECATED(
    entity_a: dict,
    entity_b: dict,
    a_mentions_b: dict,
    b_mentions_a: dict
) -> int:
    """
    DEPRECATED: Calculate connection strength (0-100) based on mutual mentions.

    DEPRECATED as of 2026-01:
    The binary connection model eliminates subjective strength scoring.
    Connections exist (in a brief) or they don't. No scoring.

    Use: python scripts/build_connections_from_briefs.py

    Keeping this code for reference only.
    """
    logger.warning("calculate_connection_strength_DEPRECATED called - this should not be used")
    strength = 0

    # Base points for any connection
    if a_mentions_b or b_mentions_a:
        strength += 20

    # Bidirectional bonus (both mention each other)
    if a_mentions_b and b_mentions_a:
        strength += 30

    # Strength from A mentioning B
    if a_mentions_b:
        if a_mentions_b.get('strength') == 'documented':
            strength += 20
        elif a_mentions_b.get('strength') == 'interpreted':
            strength += 10
        else:
            strength += 5

        # Count bonus (diminishing returns)
        count = a_mentions_b.get('count', 0)
        strength += min(count * 2, 10)

    # Strength from B mentioning A
    if b_mentions_a:
        if b_mentions_a.get('strength') == 'documented':
            strength += 20
        elif b_mentions_a.get('strength') == 'interpreted':
            strength += 10
        else:
            strength += 5

        count = b_mentions_a.get('count', 0)
        strength += min(count * 2, 10)

    return min(strength, 100)


def determine_connection_type_DEPRECATED(a_mentions_b: dict, b_mentions_a: dict) -> str:
    """
    DEPRECATED: Determine the connection type based on evidence quality.

    DEPRECATED as of 2026-01:
    Connection types now represent RELATIONSHIP NATURE (EMP, ATT, SOC, FIN, etc.),
    not evidence quality. The binary model eliminates documented/referenced/interpreted.

    Use: python scripts/build_connections_from_briefs.py

    Keeping this code for reference only.
    """
    logger.warning("determine_connection_type_DEPRECATED called - this should not be used")
    # If either side has documented evidence, it's documented
    if a_mentions_b and a_mentions_b.get('strength') == 'documented':
        return 'documented'
    if b_mentions_a and b_mentions_a.get('strength') == 'documented':
        return 'documented'

    # If either side has interpreted evidence
    if a_mentions_b and a_mentions_b.get('strength') == 'interpreted':
        return 'interpreted'
    if b_mentions_a and b_mentions_a.get('strength') == 'interpreted':
        return 'interpreted'

    return 'referenced'


def build_connections_from_mentions_DEPRECATED(entities: Dict[str, dict]) -> List[dict]:
    """
    DEPRECATED: Build connections from text mentions.

    This function is DEPRECATED as of 2026-01.
    Connections should ONLY be derived from connection briefs.

    Use: python scripts/build_connections_from_briefs.py

    Keeping this code for reference only.
    """
    logger.warning("build_connections_from_mentions_DEPRECATED called - this should not be used")
    connections = []
    processed_pairs = set()

    for entity_id, entity in entities.items():
        mentions = entity.get('mentions', [])
        mention_details = entity.get('mention_details', {})

        for mentioned_id in mentions:
            # Skip if we don't have this entity
            if mentioned_id not in entities:
                continue

            # Create a sorted pair to avoid duplicates
            pair = tuple(sorted([entity_id, mentioned_id]))
            if pair in processed_pairs:
                continue
            processed_pairs.add(pair)

            # Get mention data from both sides
            mentioned_entity = entities[mentioned_id]
            a_mentions_b = mention_details.get(mentioned_id)
            b_mentions_a = mentioned_entity.get('mention_details', {}).get(entity_id)

            # Calculate strength
            strength = calculate_connection_strength(
                entity, mentioned_entity, a_mentions_b, b_mentions_a
            )

            # Determine type
            conn_type = determine_connection_type(a_mentions_b, b_mentions_a)

            # Gather evidence (ECF citations that might be relevant)
            evidence = []
            if entity.get('ecf_citations'):
                evidence.extend([f"ECF {c}" for c in entity['ecf_citations'][:3]])
            if mentioned_entity.get('ecf_citations'):
                for c in mentioned_entity['ecf_citations'][:2]:
                    if f"ECF {c}" not in evidence:
                        evidence.append(f"ECF {c}")

            connection = {
                'source': pair[0],
                'target': pair[1],
                'strength': strength,
                'type': conn_type,
                'evidence': evidence[:5],  # Limit to 5 citations
                'bidirectional': bool(a_mentions_b and b_mentions_a),
                'source_mentions_target': bool(
                    mention_details.get(mentioned_id) if entity_id == pair[0]
                    else mentioned_entity.get('mention_details', {}).get(entity_id)
                ),
                'target_mentions_source': bool(
                    mentioned_entity.get('mention_details', {}).get(entity_id) if entity_id == pair[0]
                    else mention_details.get(mentioned_id)
                ),
            }

            connections.append(connection)

    # Sort by strength descending
    connections.sort(key=lambda x: -x['strength'])

    return connections


def build_manifest(entities: Dict[str, dict], briefs_dir: Path) -> dict:
    """Build manifest of processed briefs"""
    return {
        'generated': datetime.utcnow().isoformat() + 'Z',
        'briefs_directory': str(briefs_dir),
        'total_entities': len(entities),
        'entities_by_type': {
            'person': len([e for e in entities.values() if e['type'] == 'person']),
            'organization': len([e for e in entities.values() if e['type'] == 'organization']),
            'case': len([e for e in entities.values() if e['type'] == 'case']),
        },
        'briefs': [
            {
                'id': e['id'],
                'name': e['name'],
                'type': e['type'],
                'file': e['brief_file'],
                'parsed': e['last_updated'],
            }
            for e in sorted(entities.values(), key=lambda x: x['name'])
        ]
    }


def generate_summary(entities: Dict[str, dict], connections: List[dict]) -> str:
    """Generate a text summary of the knowledge graph"""
    lines = []
    lines.append("=" * 60)
    lines.append("CONTINUUM KNOWLEDGE GRAPH SUMMARY")
    lines.append("=" * 60)
    lines.append("")

    # Entity counts
    lines.append(f"Total Entities: {len(entities)}")
    type_counts = {}
    for e in entities.values():
        type_counts[e['type']] = type_counts.get(e['type'], 0) + 1
    for t, c in sorted(type_counts.items()):
        lines.append(f"  - {t.capitalize()}: {c}")
    lines.append("")

    # Connection stats
    lines.append(f"Total Connections: {len(connections)}")
    bidirectional = len([c for c in connections if c['bidirectional']])
    lines.append(f"  - Bidirectional: {bidirectional}")
    lines.append(f"  - One-way: {len(connections) - bidirectional}")
    lines.append("")

    # Connection type breakdown
    type_counts = {}
    for c in connections:
        type_counts[c['type']] = type_counts.get(c['type'], 0) + 1
    lines.append("Connection Types:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"  - {t.capitalize()}: {c}")
    lines.append("")

    # Top connections (by source count)
    lines.append("TOP 15 CONNECTIONS:")
    lines.append("-" * 50)
    if connections:
        for conn in connections[:15]:
            source_name = entities.get(conn['source'], {}).get('name', conn['source'])
            target_name = entities.get(conn['target'], {}).get('name', conn['target'])
            bidir = "<-->" if conn.get('bidirectional') else " --> "
            lines.append(f"  {source_name} {bidir} {target_name}")
            sources_count = conn.get('sources_count', 0)
            conn_type = conn.get('type', 'unknown')
            lines.append(f"    Sources: {sources_count} | Type: {conn_type}")
    else:
        lines.append("  (Run build_connections_from_briefs.py to generate connections)")
    lines.append("")

    # Most connected entities
    lines.append("MOST CONNECTED ENTITIES:")
    lines.append("-" * 50)
    connection_counts = {}
    for conn in connections:
        connection_counts[conn['source']] = connection_counts.get(conn['source'], 0) + 1
        connection_counts[conn['target']] = connection_counts.get(conn['target'], 0) + 1

    sorted_entities = sorted(connection_counts.items(), key=lambda x: -x[1])
    for entity_id, count in sorted_entities[:10]:
        entity = entities.get(entity_id, {})
        name = entity.get('name', entity_id)
        etype = entity.get('type', 'unknown')
        lines.append(f"  {name} ({etype}): {count} connections")
    lines.append("")

    # Entity list
    lines.append("ALL ENTITIES:")
    lines.append("-" * 50)
    for entity in sorted(entities.values(), key=lambda x: x['name']):
        mention_count = len(entity.get('mentions', []))
        lines.append(f"  [{entity['type'][:3].upper()}] {entity['name']}")
        lines.append(f"        Status: {entity['status'][:60]}...")
        lines.append(f"        Mentions: {mention_count} other entities")
    lines.append("")

    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Build Continuum knowledge graph')
    parser.add_argument('--briefs-dir', type=str, default='/continuum/briefs',
                        help='Directory containing analytical briefs')
    parser.add_argument('--output-dir', type=str, default='/continuum/data',
                        help='Directory for output JSON files')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress progress output')

    args = parser.parse_args()

    briefs_dir = Path(args.briefs_dir)
    output_dir = Path(args.output_dir)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Continuum Knowledge Graph Builder")
    print("=" * 40)
    print(f"Briefs directory: {briefs_dir}")
    print(f"Output directory: {output_dir}")
    print("")

    # Step 1: Find all briefs
    print("Scanning for briefs...")
    briefs = scan_briefs(briefs_dir)
    print(f"Found {len(briefs)} analytical briefs")
    print("")

    # Step 2: Parse all briefs
    print("Parsing briefs...")
    entities = build_entities(briefs)
    print(f"Parsed {len(entities)} entities")
    print("")

    # Step 3: Connections - HANDLED BY SEPARATE SCRIPT
    # =========================================================================
    # ARCHITECTURAL CHANGE (2026-01):
    # Connections are NO LONGER derived from text mentions in analytical briefs.
    # Connection briefs are the SOURCE OF TRUTH.
    #
    # Run: python scripts/build_connections_from_briefs.py
    #
    # This ensures: NO CONNECTION EXISTS WITHOUT A BRIEF.
    # =========================================================================
    print("NOTE: Connections are built separately from connection briefs.")
    print("      Run: python scripts/build_connections_from_briefs.py")
    print("")
    connections = []  # Empty - connections come from briefs, not mentions

    # Step 4: Build manifest
    manifest = build_manifest(entities, briefs_dir)

    # Step 5: Prepare output data

    # entities.json - list format for easier frontend consumption
    entities_output = {
        'generated': datetime.utcnow().isoformat() + 'Z',
        'count': len(entities),
        'entities': list(entities.values())
    }

    # connections.json
    connections_output = {
        'generated': datetime.utcnow().isoformat() + 'Z',
        'count': len(connections),
        'connections': connections
    }

    # Step 6: Write output files
    print("Writing output files...")

    entities_path = output_dir / 'entities.json'
    with open(entities_path, 'w', encoding='utf-8') as f:
        json.dump(entities_output, f, indent=2)
    print(f"  Written: {entities_path}")

    connections_path = output_dir / 'connections.json'
    with open(connections_path, 'w', encoding='utf-8') as f:
        json.dump(connections_output, f, indent=2)
    print(f"  Written: {connections_path}")

    manifest_path = output_dir / 'manifest.json'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    print(f"  Written: {manifest_path}")

    print("")

    # Step 7: Generate and print summary
    summary = generate_summary(entities, connections)
    print(summary)

    # Also save summary to file
    summary_path = output_dir / 'graph_summary.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"Summary saved to: {summary_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
