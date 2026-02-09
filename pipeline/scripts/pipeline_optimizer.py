#!/usr/bin/env python3
"""
Pipeline Optimizer for Continuum Report
Executes all 7 phases of entity/connection pipeline optimization
"""

import json
from pathlib import Path
from collections import defaultdict
import re
from datetime import datetime, timezone

# Define paths
BASE_PATH = Path(r"C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum")
INDEXES_PATH = BASE_PATH / "indexes"
REPORTS_PATH = BASE_PATH / "reports"
WORK_PATH = BASE_PATH / "work"
WEBSITE_DATA_PATH = BASE_PATH / "website" / "data"

# Ensure work directory exists
WORK_PATH.mkdir(exist_ok=True, parents=True)

# Log file
log_lines = []

def log(message):
    """Log a message with timestamp"""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{timestamp}] {message}"
    print(line)
    log_lines.append(line)

def save_log():
    """Save log to file"""
    log_path = WORK_PATH / "pipeline_optimization_log.md"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("# Pipeline Optimization Log\n\n")
        f.write("\n".join(log_lines))
    log(f"Log saved to {log_path}")

# PHASE 1: Review Gap Analysis & Extract Priority Pairs
def phase1_extract_priority_pairs():
    log("\n=== PHASE 1: Extract Priority Pairs ===")

    # Load data
    with open(INDEXES_PATH / "entity_registry.json", 'r', encoding='utf-8') as f:
        entity_data = json.load(f)
        entities = entity_data.get('entities', {})

    with open(INDEXES_PATH / "co_occurrence.json", 'r', encoding='utf-8') as f:
        co_occurrence_data = json.load(f)
        pairs = co_occurrence_data.get('pairs', {})

    log(f"Loaded {len(entities)} entities and {len(pairs)} co-occurrence pairs")

    # Define boilerplate patterns
    boilerplate_keywords = {
        # Legal jargon
        'respectfully-submitted', 'pro-hac-vice', 'notary-public', 'filed-under-seal',
        'electronic-filing', 'composite-exhibit', 'protective-order', 'federal-rules',
        'civil-procedure', 'federal-rule', 'local-rules', 'local-civil-rule',
        'interrogatory-no', 'request-no', 'discovery-requests', 'first-set',
        'reported-by', 'professional-reporter', 'my-commission-no',
        'see-fed', 'see-motion', 'this-court', 'case-no',
        'all-documents', 'while-ms', 'exceed-presumptive-ten',
        'alleged-defamation', 'health-care-provider',

        # Addresses/locations (non-substantive)
        'fort-lauderdale', 'east-las-olas', 'las-olas-blvd', 'las-olas-boulevard',
        'north-andrews-avenue', 'north-andrews-ave', 'main-street',
        'university-st', 'university-street', 'little-st',
        'salt-lake-city', 'west-palm-beach', 'broward-county',
        'lake-worth', 'palm-beach-county', 'palm-beach-gardens',
        'south-salem', 'twin-lakes-rd', 'berkeley-square',

        # Legal entities (law firms - unless specific to case)
        'boies-schiller', 'quinney-college',

        # Generic/procedural
        'jane-doe-no', 'jane-does', 'appear-pro-hac',
        'crime-victims', 'rights-act', 'fifth-amendment', 'second-circuit',
        'prime-minister',  # too generic unless specific person
    }

    def is_boilerplate(entity_id):
        """Check if entity is boilerplate"""
        # Exact match
        if entity_id in boilerplate_keywords:
            return True

        # Pattern matches
        patterns = [
            r'^ecf-\d+',  # ECF references
            r'^\d+.*street$',
            r'^\d+.*avenue$',
            r'^\d+.*blvd$',
            r'.*-street$',
            r'.*-avenue$',
            r'.*-blvd$',
            r'^case-',
            r'^filed-',
            r'^see-',
            r'^all-',
        ]

        for pattern in patterns:
            if re.match(pattern, entity_id):
                return True

        return False

    def is_substantive(entity_id):
        """Check if entity is substantive (person, org, specific case)"""
        # Known substantive entities (key players)
        substantive_keywords = {
            'ghislaine-maxwell', 'jeffrey-epstein', 'virginia-giuffre',
            'alan-dershowitz', 'prince-andrew', 'bill-clinton', 'donald-trump',
            'sarah-kellen', 'nadia-marcinkova', 'jean-luc-brunel',
            'juan-alessi', 'johanna-sjoberg', 'emmy-taylor',
            'brad-edwards', 'bradley-edwards', 'paul-cassell', 'david-boies',
            'jeffrey-pagliuca', 'philip-barden', 'ross-gow', 'laura-menninger',
            'rinaldo-rizzo', 'alfredo-rodriguez', 'jack-scarola',
            'bill-richardson', 'les-wexner', 'al-gore',
            'david-rodgers', 'sharon-churcher', 'robert-giuffre',
            'meredith-schultz', 'meridith-schultz', 'kelli-ann-willis',
            'nicole-simmons', 'stanley-pottinger', 'stan-pottinger',
            'john-harris', 'royal-oaks-medical', 'westmead-hospital',
            'daily-mail', 'palm-beach-police',
            'defendant-ghislaine-maxwell', 'plaintiff-virginia-giuffre',
            'defendant-maxwell', 'president-clinton',
            'jane-doe',  # Keep this as it may refer to specific victims
            'mar-a-lago',  # Specific location relevant to case
            'virgin-islands', 'london', 'new-york', 'palm-beach', 'new-mexico',
        }

        return entity_id in substantive_keywords

    # Filter and score pairs
    priority_pairs = []

    for pair_key, pair_data in pairs.items():
        co_count = pair_data['co_mention_count']

        # Only consider pairs with 3+ co-mentions
        if co_count < 3:
            continue

        # Skip if already documented
        if pair_data.get('in_connections_json', False):
            continue

        # Parse entity IDs
        entities_in_pair = pair_key.split('|')
        if len(entities_in_pair) != 2:
            continue

        entity1, entity2 = entities_in_pair

        # Skip if either is boilerplate
        if is_boilerplate(entity1) or is_boilerplate(entity2):
            continue

        # Calculate substantiveness score
        substantive_score = 0
        if is_substantive(entity1):
            substantive_score += 1
        if is_substantive(entity2):
            substantive_score += 1

        # Get mention counts for both entities
        entity1_mentions = entities.get(entity1, {}).get('mention_count', 0)
        entity2_mentions = entities.get(entity2, {}).get('mention_count', 0)

        # Calculate priority score
        # Higher co-mentions + higher individual mentions + substantive = higher priority
        priority_score = (
            co_count * 10 +  # Co-occurrence is most important
            (entity1_mentions + entity2_mentions) * 0.5 +  # Individual mentions matter too
            substantive_score * 20  # Substantive entities get bonus
        )

        priority_pairs.append({
            'pair_key': pair_key,
            'entity1': entity1,
            'entity2': entity2,
            'co_mentions': co_count,
            'entity1_mentions': entity1_mentions,
            'entity2_mentions': entity2_mentions,
            'substantive_score': substantive_score,
            'priority_score': priority_score,
            'shared_sources': pair_data['shared_sources']
        })

    # Sort by priority score
    priority_pairs.sort(key=lambda x: x['priority_score'], reverse=True)

    log(f"Found {len(priority_pairs)} substantive undocumented pairs")
    log(f"Top priority pair: {priority_pairs[0]['pair_key']} (score: {priority_pairs[0]['priority_score']:.1f})")

    # Write to queue file
    queue_path = WORK_PATH / "priority_connections_queue.md"
    with open(queue_path, 'w', encoding='utf-8') as f:
        f.write("# Priority Connections Queue\n\n")
        f.write(f"**Generated:** {datetime.now(timezone.utc).isoformat()}\n\n")
        f.write(f"**Total undocumented substantive pairs:** {len(priority_pairs)}\n\n")
        f.write("---\n\n")
        f.write("## Scoring Methodology\n\n")
        f.write("Priority Score = (co_mentions × 10) + (total_mentions × 0.5) + (substantive_bonus × 20)\n\n")
        f.write("- **Co-mentions:** How often entities appear together in source documents\n")
        f.write("- **Total mentions:** Sum of individual entity mention counts\n")
        f.write("- **Substantive bonus:** +20 per entity that is a key person/org/location\n\n")
        f.write("---\n\n")
        f.write("## Top 50 Priority Connections\n\n")

        for i, pair in enumerate(priority_pairs[:50], 1):
            f.write(f"### {i}. {pair['entity1']} ↔ {pair['entity2']}\n\n")
            f.write(f"- **Priority Score:** {pair['priority_score']:.1f}\n")
            f.write(f"- **Co-mentions:** {pair['co_mentions']}\n")
            f.write(f"- **Entity Mentions:** {pair['entity1']} ({pair['entity1_mentions']}), {pair['entity2']} ({pair['entity2_mentions']})\n")
            f.write(f"- **Substantive Score:** {pair['substantive_score']}/2\n")
            f.write(f"- **Shared Sources:** {', '.join(pair['shared_sources'][:5])}")
            if len(pair['shared_sources']) > 5:
                f.write(f" (+{len(pair['shared_sources'])-5} more)")
            f.write("\n\n")

        if len(priority_pairs) > 50:
            f.write(f"\n---\n\n## Additional Pairs\n\n")
            f.write(f"*{len(priority_pairs) - 50} more pairs available in full data.*\n\n")

    log(f"Priority queue saved to {queue_path}")

    return priority_pairs, entities, pairs

# PHASE 2: Build Entity Normalization Map
def phase2_build_normalization_map(entities):
    log("\n=== PHASE 2: Build Entity Normalization Map ===")

    # Identify variant clusters
    normalization_map = {
        'canonical': {},
        'lookup': {}
    }

    # Define known variants manually (conservative approach)
    known_variants = {
        'ghislaine-maxwell': {
            'variants': ['defendant-ghislaine-maxwell', 'defendant-maxwell'],
            'display_name': 'Ghislaine Maxwell'
        },
        'jeffrey-epstein': {
            'variants': ['defendant-epstein'],
            'display_name': 'Jeffrey Epstein'
        },
        'virginia-giuffre': {
            'variants': ['plaintiff-virginia-giuffre'],
            'display_name': 'Virginia Giuffre'
        },
        'david-boies': {
            'variants': [],
            'display_name': 'David Boies'
        },
        'brad-edwards': {
            'variants': ['bradley-edwards'],
            'display_name': 'Brad Edwards'
        },
        'bill-clinton': {
            'variants': ['president-clinton'],
            'display_name': 'Bill Clinton'
        },
        'meredith-schultz': {
            'variants': ['meridith-schultz'],
            'display_name': 'Meredith Schultz'
        },
        'stanley-pottinger': {
            'variants': ['stan-pottinger'],
            'display_name': 'Stanley Pottinger'
        },
        'north-andrews-avenue': {
            'variants': ['north-andrews-ave'],
            'display_name': 'North Andrews Avenue'
        },
        'las-olas-blvd': {
            'variants': ['las-olas-boulevard'],
            'display_name': 'Las Olas Boulevard'
        },
        'university-st': {
            'variants': ['university-street'],
            'display_name': 'University Street'
        },
    }

    # Build normalization map
    for canonical, data in known_variants.items():
        # Add canonical entry
        normalization_map['canonical'][canonical] = {
            'variants': data['variants'],
            'display_name': data['display_name'],
            'merged_mention_count': entities.get(canonical, {}).get('mention_count', 0),
            'merged_source_count': entities.get(canonical, {}).get('source_count', 0)
        }

        # Aggregate mentions from variants
        for variant in data['variants']:
            if variant in entities:
                normalization_map['canonical'][canonical]['merged_mention_count'] += entities[variant]['mention_count']
                normalization_map['canonical'][canonical]['merged_source_count'] += entities[variant]['source_count']

                # Add to lookup
                normalization_map['lookup'][variant] = canonical

    log(f"Created normalization map with {len(normalization_map['canonical'])} canonical entities")
    log(f"Total variants mapped: {len(normalization_map['lookup'])}")

    # Save normalization map
    norm_path = INDEXES_PATH / "entity_normalization.json"
    with open(norm_path, 'w', encoding='utf-8') as f:
        json.dump(normalization_map, f, indent=2)

    log(f"Normalization map saved to {norm_path}")

    return normalization_map

# PHASE 3: Build Boilerplate Filter List
def phase3_build_boilerplate_filter():
    log("\n=== PHASE 3: Build Boilerplate Filter ===")

    boilerplate_filter = {
        'exclude_exact': [],
        'exclude_patterns': [],
        'reason': {}
    }

    # Legal jargon
    legal_jargon = [
        'respectfully-submitted', 'pro-hac-vice', 'notary-public', 'filed-under-seal',
        'electronic-filing', 'composite-exhibit', 'protective-order', 'federal-rules',
        'civil-procedure', 'federal-rule', 'local-rules', 'local-civil-rule',
        'interrogatory-no', 'request-no', 'discovery-requests', 'first-set',
        'reported-by', 'professional-reporter', 'my-commission-no',
        'see-fed', 'see-motion', 'this-court', 'case-no',
        'all-documents', 'while-ms', 'exceed-presumptive-ten',
        'alleged-defamation', 'health-care-provider', 'appear-pro-hac',
        'crime-victims', 'rights-act', 'fifth-amendment', 'second-circuit',
    ]

    for term in legal_jargon:
        boilerplate_filter['exclude_exact'].append(term)
        boilerplate_filter['reason'][term] = 'legal_jargon'

    # Address components (non-specific)
    address_components = [
        'fort-lauderdale', 'east-las-olas', 'west-palm-beach',
        'salt-lake-city', 'broward-county', 'lake-worth',
        'palm-beach-county', 'palm-beach-gardens',
        'south-salem', 'twin-lakes-rd', 'berkeley-square',
        'main-street', 'little-st',
    ]

    for term in address_components:
        boilerplate_filter['exclude_exact'].append(term)
        boilerplate_filter['reason'][term] = 'address_component'

    # Law firms (unless they play substantive role)
    law_firms = [
        'boies-schiller', 'quinney-college',
    ]

    for term in law_firms:
        boilerplate_filter['exclude_exact'].append(term)
        boilerplate_filter['reason'][term] = 'law_firm_boilerplate'

    # Generic procedural terms
    generic_terms = [
        'jane-doe-no', 'jane-does', 'prime-minister',
    ]

    for term in generic_terms:
        boilerplate_filter['exclude_exact'].append(term)
        boilerplate_filter['reason'][term] = 'generic_procedural'

    # Patterns
    boilerplate_filter['exclude_patterns'] = [
        '^ecf-\\d+',  # ECF document references
        '^\\d+.*street$',  # Numbered streets
        '^\\d+.*avenue$',  # Numbered avenues
        '^\\d+.*blvd$',  # Numbered boulevards
        '.*-street$',  # Generic streets
        '.*-avenue$',  # Generic avenues
        '.*-blvd$',  # Generic boulevards
        '^case-',  # Case procedural terms
        '^filed-',  # Filing procedural terms
        '^see-',  # Cross-reference terms
        '^all-',  # Generic "all" terms
    ]

    log(f"Created boilerplate filter with {len(boilerplate_filter['exclude_exact'])} exact matches")
    log(f"Created {len(boilerplate_filter['exclude_patterns'])} exclusion patterns")

    # Save filter
    filter_path = INDEXES_PATH / "boilerplate_filter.json"
    with open(filter_path, 'w', encoding='utf-8') as f:
        json.dump(boilerplate_filter, f, indent=2)

    log(f"Boilerplate filter saved to {filter_path}")

    return boilerplate_filter

# PHASE 4: Create Filtered Entity Registry
def phase4_create_filtered_registry(entities, normalization_map, boilerplate_filter):
    log("\n=== PHASE 4: Create Filtered Entity Registry ===")

    def should_exclude(entity_id):
        """Check if entity should be excluded"""
        # Check exact matches
        if entity_id in boilerplate_filter['exclude_exact']:
            return True

        # Check patterns
        for pattern in boilerplate_filter['exclude_patterns']:
            if re.match(pattern, entity_id):
                return True

        return False

    def normalize_entity_id(entity_id):
        """Get canonical ID for an entity"""
        return normalization_map['lookup'].get(entity_id, entity_id)

    # Process entities
    clean_entities = {}
    stats = {
        'original_count': len(entities),
        'excluded_count': 0,
        'normalized_count': 0,
        'final_count': 0
    }

    # First pass: normalize and aggregate
    for entity_id, entity_data in entities.items():
        # Skip if should be excluded
        if should_exclude(entity_id):
            stats['excluded_count'] += 1
            continue

        # Get canonical ID
        canonical_id = normalize_entity_id(entity_id)

        if canonical_id != entity_id:
            stats['normalized_count'] += 1

        # Initialize or update canonical entry
        if canonical_id not in clean_entities:
            # Check if this is a canonical entity with predefined data
            if canonical_id in normalization_map['canonical']:
                clean_entities[canonical_id] = {
                    'name': normalization_map['canonical'][canonical_id]['display_name'],
                    'mention_count': normalization_map['canonical'][canonical_id]['merged_mention_count'],
                    'source_count': normalization_map['canonical'][canonical_id]['merged_source_count'],
                    'sources': set(),
                    'variants_merged': normalization_map['canonical'][canonical_id]['variants']
                }
            else:
                clean_entities[canonical_id] = {
                    'name': entity_data['name'],
                    'mention_count': entity_data['mention_count'],
                    'source_count': entity_data['source_count'],
                    'sources': set(entity_data.get('sources', [])),
                    'variants_merged': []
                }

        # Add sources
        if 'sources' in entity_data:
            clean_entities[canonical_id]['sources'].update(entity_data['sources'])

    # Second pass: convert sources back to lists and finalize
    for entity_id in clean_entities:
        clean_entities[entity_id]['sources'] = sorted(list(clean_entities[entity_id]['sources']))
        clean_entities[entity_id]['source_count'] = len(clean_entities[entity_id]['sources'])

    stats['final_count'] = len(clean_entities)

    # Sort by mention count
    sorted_entities = dict(sorted(clean_entities.items(), key=lambda x: x[1]['mention_count'], reverse=True))

    # Save clean registry
    clean_registry = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'count': len(sorted_entities),
        'stats': stats,
        'entities': sorted_entities
    }

    clean_path = INDEXES_PATH / "entity_registry_clean.json"
    with open(clean_path, 'w', encoding='utf-8') as f:
        json.dump(clean_registry, f, indent=2)

    log(f"Original entities: {stats['original_count']}")
    log(f"Excluded (boilerplate): {stats['excluded_count']}")
    log(f"Normalized (merged): {stats['normalized_count']}")
    log(f"Final clean entities: {stats['final_count']}")
    log(f"Clean registry saved to {clean_path}")

    return clean_entities, stats

# PHASE 5: Update Co-occurrence with Clean Data
def phase5_update_cooccurrence(pairs, clean_entities, normalization_map, boilerplate_filter):
    log("\n=== PHASE 5: Update Co-occurrence with Clean Data ===")

    def should_exclude(entity_id):
        """Check if entity should be excluded"""
        if entity_id in boilerplate_filter['exclude_exact']:
            return True
        for pattern in boilerplate_filter['exclude_patterns']:
            if re.match(pattern, entity_id):
                return True
        return False

    def normalize_entity_id(entity_id):
        """Get canonical ID for an entity"""
        return normalization_map['lookup'].get(entity_id, entity_id)

    # Rebuild co-occurrence with clean entities
    clean_pairs = {}
    stats = {
        'original_pairs': len(pairs),
        'excluded_pairs': 0,
        'normalized_pairs': 0,
        'final_pairs': 0
    }

    for pair_key, pair_data in pairs.items():
        entities_in_pair = pair_key.split('|')
        if len(entities_in_pair) != 2:
            continue

        entity1, entity2 = entities_in_pair

        # Skip if either entity should be excluded
        if should_exclude(entity1) or should_exclude(entity2):
            stats['excluded_pairs'] += 1
            continue

        # Normalize entity IDs
        canonical1 = normalize_entity_id(entity1)
        canonical2 = normalize_entity_id(entity2)

        # Ensure consistent ordering
        if canonical1 > canonical2:
            canonical1, canonical2 = canonical2, canonical1

        # Create new pair key
        new_pair_key = f"{canonical1}|{canonical2}"

        # Track if normalization occurred
        if new_pair_key != pair_key:
            stats['normalized_pairs'] += 1

        # Initialize or update pair
        if new_pair_key not in clean_pairs:
            clean_pairs[new_pair_key] = {
                'co_mention_count': pair_data['co_mention_count'],
                'shared_sources': set(pair_data['shared_sources']),
                'in_connections_json': pair_data.get('in_connections_json', False),
                'has_brief': pair_data.get('has_brief', False)
            }
        else:
            # Merge with existing pair
            clean_pairs[new_pair_key]['co_mention_count'] += pair_data['co_mention_count']
            clean_pairs[new_pair_key]['shared_sources'].update(pair_data['shared_sources'])

    # Convert sources back to lists
    for pair_key in clean_pairs:
        clean_pairs[pair_key]['shared_sources'] = sorted(list(clean_pairs[pair_key]['shared_sources']))
        clean_pairs[pair_key]['co_mention_count'] = len(clean_pairs[pair_key]['shared_sources'])

    # Sort by co-mention count
    sorted_pairs = dict(sorted(clean_pairs.items(), key=lambda x: x[1]['co_mention_count'], reverse=True))

    stats['final_pairs'] = len(sorted_pairs)

    # Save clean co-occurrence
    clean_cooccurrence = {
        'generated': datetime.now(timezone.utc).isoformat(),
        'pair_count': len(sorted_pairs),
        'stats': stats,
        'pairs': sorted_pairs
    }

    clean_path = INDEXES_PATH / "co_occurrence_clean.json"
    with open(clean_path, 'w', encoding='utf-8') as f:
        json.dump(clean_cooccurrence, f, indent=2)

    log(f"Original pairs: {stats['original_pairs']}")
    log(f"Excluded pairs: {stats['excluded_pairs']}")
    log(f"Normalized pairs: {stats['normalized_pairs']}")
    log(f"Final clean pairs: {stats['final_pairs']}")
    log(f"Reduction: {((stats['original_pairs'] - stats['final_pairs']) / stats['original_pairs'] * 100):.1f}%")
    log(f"Clean co-occurrence saved to {clean_path}")

    return sorted_pairs, stats

# PHASE 6: Cross-Reference with Curated Data
def phase6_cross_reference_curated(clean_entities, curated_entities_path):
    log("\n=== PHASE 6: Cross-Reference with Curated Data ===")

    # Load curated entities
    with open(curated_entities_path, 'r', encoding='utf-8') as f:
        curated_data = json.load(f)
        curated_entities = {e['id']: e for e in curated_data.get('entities', [])}

    log(f"Loaded {len(curated_entities)} curated entities")

    # Identify gaps
    gaps = {
        'high_mention_not_curated': [],
        'curated_low_mention': [],
        'curated_not_in_registry': []
    }

    # Find high-mention entities not in curated (threshold: 10+ mentions)
    for entity_id, entity_data in clean_entities.items():
        if entity_data['mention_count'] >= 10:
            if entity_id not in curated_entities:
                gaps['high_mention_not_curated'].append({
                    'id': entity_id,
                    'name': entity_data['name'],
                    'mentions': entity_data['mention_count'],
                    'sources': entity_data['source_count']
                })

    # Find curated entities with low mentions
    for entity_id, entity_data in curated_entities.items():
        if entity_id in clean_entities:
            registry_mentions = clean_entities[entity_id]['mention_count']
            if registry_mentions < 5:
                gaps['curated_low_mention'].append({
                    'id': entity_id,
                    'name': entity_data['name'],
                    'mentions': registry_mentions,
                    'reason': 'May need more source documents'
                })
        else:
            gaps['curated_not_in_registry'].append({
                'id': entity_id,
                'name': entity_data['name'],
                'reason': 'Not found in entity registry (may be from external sources)'
            })

    # Sort by mentions
    gaps['high_mention_not_curated'].sort(key=lambda x: x['mentions'], reverse=True)
    gaps['curated_low_mention'].sort(key=lambda x: x['mentions'])

    log(f"Found {len(gaps['high_mention_not_curated'])} high-mention entities needing briefs")
    log(f"Found {len(gaps['curated_low_mention'])} curated entities with low mentions")
    log(f"Found {len(gaps['curated_not_in_registry'])} curated entities not in registry")

    # Write report
    report_path = REPORTS_PATH / "entity_curation_gaps.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Entity Curation Gaps Report\n\n")
        f.write(f"**Generated:** {datetime.now(timezone.utc).isoformat()}\n\n")
        f.write("---\n\n")

        f.write("## High-Mention Entities Without Briefs\n\n")
        f.write(f"**Total:** {len(gaps['high_mention_not_curated'])} entities with ≥10 mentions\n\n")
        f.write("These entities appear frequently in source documents but lack curated analytical briefs.\n\n")

        for i, entity in enumerate(gaps['high_mention_not_curated'][:30], 1):
            f.write(f"### {i}. {entity['name']}\n\n")
            f.write(f"- **Entity ID:** `{entity['id']}`\n")
            f.write(f"- **Mentions:** {entity['mentions']}\n")
            f.write(f"- **Source Documents:** {entity['sources']}\n")
            f.write(f"- **Recommendation:** Create analytical brief\n\n")

        if len(gaps['high_mention_not_curated']) > 30:
            f.write(f"\n*...and {len(gaps['high_mention_not_curated']) - 30} more entities*\n\n")

        f.write("---\n\n")

        f.write("## Curated Entities with Low Registry Mentions\n\n")
        f.write(f"**Total:** {len(gaps['curated_low_mention'])} entities\n\n")
        f.write("These entities have analytical briefs but few mentions in the current document corpus.\n\n")

        for entity in gaps['curated_low_mention']:
            f.write(f"### {entity['name']}\n\n")
            f.write(f"- **Entity ID:** `{entity['id']}`\n")
            f.write(f"- **Registry Mentions:** {entity['mentions']}\n")
            f.write(f"- **Note:** {entity['reason']}\n\n")

        f.write("---\n\n")

        f.write("## Curated Entities Not in Registry\n\n")
        f.write(f"**Total:** {len(gaps['curated_not_in_registry'])} entities\n\n")
        f.write("These entities have briefs but don't appear in the entity registry.\n\n")

        for entity in gaps['curated_not_in_registry']:
            f.write(f"### {entity['name']}\n\n")
            f.write(f"- **Entity ID:** `{entity['id']}`\n")
            f.write(f"- **Note:** {entity['reason']}\n\n")

    log(f"Curation gaps report saved to {report_path}")

    return gaps

# PHASE 7: Summary Report
def phase7_summary_report(priority_pairs, entity_stats, cooccurrence_stats, gaps):
    log("\n=== PHASE 7: Generate Summary Report ===")

    report_path = REPORTS_PATH / "pipeline_optimization_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Pipeline Optimization Report\n\n")
        f.write(f"**Generated:** {datetime.now(timezone.utc).isoformat()}\n\n")
        f.write("---\n\n")

        f.write("## Executive Summary\n\n")
        f.write("This report documents the optimization of the entity/connection pipeline for The Continuum Report. ")
        f.write("The optimization focused on reducing noise from boilerplate entities, normalizing variant entity names, ")
        f.write("and identifying priority connections for documentation.\n\n")

        f.write("### Key Achievements\n\n")
        f.write(f"- **Entity Registry:** Reduced from {entity_stats['original_count']:,} to {entity_stats['final_count']:,} entities ({entity_stats['excluded_count']:,} boilerplate removed, {entity_stats['normalized_count']:,} variants merged)\n")
        f.write(f"- **Co-occurrence Pairs:** Reduced from {cooccurrence_stats['original_pairs']:,} to {cooccurrence_stats['final_pairs']:,} pairs ({((cooccurrence_stats['original_pairs'] - cooccurrence_stats['final_pairs']) / cooccurrence_stats['original_pairs'] * 100):.1f}% reduction)\n")
        f.write(f"- **Priority Connections:** Identified {len(priority_pairs)} substantive undocumented entity pairs\n")
        f.write(f"- **Curation Gaps:** Found {len(gaps['high_mention_not_curated'])} high-priority entities needing analytical briefs\n\n")

        f.write("---\n\n")

        f.write("## Phase 1: Priority Connections Queue\n\n")
        f.write(f"Extracted and prioritized {len(priority_pairs)} undocumented entity pairs with substantive relationships.\n\n")
        f.write("**Top 20 Priority Pairs:**\n\n")

        for i, pair in enumerate(priority_pairs[:20], 1):
            f.write(f"{i}. **{pair['entity1']}** ↔ **{pair['entity2']}** ")
            f.write(f"(Priority Score: {pair['priority_score']:.1f}, Co-mentions: {pair['co_mentions']})\n")

        f.write(f"\n*Full queue available at: `/work/priority_connections_queue.md`*\n\n")

        f.write("---\n\n")

        f.write("## Phase 2: Entity Normalization\n\n")
        f.write(f"**Variants Merged:** {entity_stats['normalized_count']}\n\n")
        f.write("**Key Normalizations:**\n\n")
        f.write("- `ghislaine-maxwell` ← `defendant-ghislaine-maxwell`, `defendant-maxwell`\n")
        f.write("- `jeffrey-epstein` ← `defendant-epstein`\n")
        f.write("- `virginia-giuffre` ← `plaintiff-virginia-giuffre`\n")
        f.write("- `brad-edwards` ← `bradley-edwards`\n")
        f.write("- `bill-clinton` ← `president-clinton`\n")
        f.write("- `meredith-schultz` ← `meridith-schultz`\n")
        f.write("- `stanley-pottinger` ← `stan-pottinger`\n\n")
        f.write("*Full normalization map available at: `/indexes/entity_normalization.json`*\n\n")

        f.write("---\n\n")

        f.write("## Phase 3: Boilerplate Filtering\n\n")
        f.write(f"**Entities Excluded:** {entity_stats['excluded_count']}\n\n")
        f.write("**Categories Filtered:**\n\n")
        f.write("- **Legal Jargon:** `respectfully-submitted`, `pro-hac-vice`, `notary-public`, `filed-under-seal`, etc.\n")
        f.write("- **Generic Addresses:** `fort-lauderdale`, `salt-lake-city`, `north-andrews-avenue`, etc.\n")
        f.write("- **Procedural Terms:** `case-no`, `interrogatory-no`, `discovery-requests`, `see-fed`, etc.\n")
        f.write("- **Law Firm Boilerplate:** `boies-schiller`, `quinney-college`\n\n")
        f.write("*Full filter list available at: `/indexes/boilerplate_filter.json`*\n\n")

        f.write("---\n\n")

        f.write("## Phase 4: Clean Entity Registry\n\n")
        f.write("**Statistics:**\n\n")
        f.write(f"- Original entities: {entity_stats['original_count']:,}\n")
        f.write(f"- Excluded (boilerplate): {entity_stats['excluded_count']:,}\n")
        f.write(f"- Normalized (merged): {entity_stats['normalized_count']:,}\n")
        f.write(f"- **Final clean entities: {entity_stats['final_count']:,}**\n\n")
        f.write("*Clean registry available at: `/indexes/entity_registry_clean.json`*\n\n")

        f.write("---\n\n")

        f.write("## Phase 5: Clean Co-occurrence Index\n\n")
        f.write("**Statistics:**\n\n")
        f.write(f"- Original pairs: {cooccurrence_stats['original_pairs']:,}\n")
        f.write(f"- Excluded pairs: {cooccurrence_stats['excluded_pairs']:,}\n")
        f.write(f"- Normalized pairs: {cooccurrence_stats['normalized_pairs']:,}\n")
        f.write(f"- **Final clean pairs: {cooccurrence_stats['final_pairs']:,}**\n")
        f.write(f"- **Reduction: {((cooccurrence_stats['original_pairs'] - cooccurrence_stats['final_pairs']) / cooccurrence_stats['original_pairs'] * 100):.1f}%**\n\n")
        f.write("This dramatic reduction in noise pairs makes manual review and connection documentation much more feasible.\n\n")
        f.write("*Clean co-occurrence index available at: `/indexes/co_occurrence_clean.json`*\n\n")

        f.write("---\n\n")

        f.write("## Phase 6: Entity Curation Gaps\n\n")
        f.write(f"**High-Mention Entities Without Briefs:** {len(gaps['high_mention_not_curated'])}\n\n")
        f.write("**Top 10 Entities Needing Briefs:**\n\n")

        for i, entity in enumerate(gaps['high_mention_not_curated'][:10], 1):
            f.write(f"{i}. **{entity['name']}** (`{entity['id']}`) - {entity['mentions']} mentions\n")

        f.write(f"\n**Curated Entities with Low Mentions:** {len(gaps['curated_low_mention'])}\n")
        f.write(f"**Curated Entities Not in Registry:** {len(gaps['curated_not_in_registry'])}\n\n")
        f.write("*Full curation gaps report available at: `/reports/entity_curation_gaps.md`*\n\n")

        f.write("---\n\n")

        f.write("## Recommendations\n\n")
        f.write("### Immediate Next Steps\n\n")
        f.write("1. **Review Priority Connections Queue**\n")
        f.write("   - Start with top 20 pairs in `/work/priority_connections_queue.md`\n")
        f.write("   - Document substantive relationships in `connections.json`\n\n")
        f.write("2. **Create Analytical Briefs for High-Priority Entities**\n")
        f.write("   - Focus on top 10 from curation gaps report\n")
        f.write("   - Prioritize: Lawyers (Boies, Pagliuca, Cassell), Witnesses (Alessi, Rizzo, Rodriguez)\n\n")
        f.write("3. **Use Clean Indexes for Future Analysis**\n")
        f.write("   - Switch to `entity_registry_clean.json` and `co_occurrence_clean.json`\n")
        f.write("   - Apply normalization map to future entity extractions\n\n")
        f.write("### Long-Term Improvements\n\n")
        f.write("1. **Expand Source Corpus**\n")
        f.write("   - Process additional court documents to increase co-occurrence counts\n")
        f.write("   - Target documents mentioning low-coverage curated entities\n\n")
        f.write("2. **Refine Entity Extraction**\n")
        f.write("   - Apply boilerplate filter during initial extraction\n")
        f.write("   - Use normalization map to prevent variant proliferation\n\n")
        f.write("3. **Automated Connection Suggestions**\n")
        f.write("   - Build agent to auto-generate connection drafts from priority queue\n")
        f.write("   - Human review and approval before adding to `connections.json`\n\n")

        f.write("---\n\n")

        f.write("## Files Generated\n\n")
        f.write("### Work Files\n")
        f.write("- `/work/priority_connections_queue.md` - Top 50 undocumented entity pairs\n")
        f.write("- `/work/pipeline_optimization_log.md` - Detailed execution log\n\n")
        f.write("### Index Files\n")
        f.write("- `/indexes/entity_normalization.json` - Entity variant mapping\n")
        f.write("- `/indexes/boilerplate_filter.json` - Noise entity filter\n")
        f.write("- `/indexes/entity_registry_clean.json` - Cleaned entity registry\n")
        f.write("- `/indexes/co_occurrence_clean.json` - Cleaned co-occurrence index\n\n")
        f.write("### Reports\n")
        f.write("- `/reports/entity_curation_gaps.md` - Entities needing analytical briefs\n")
        f.write("- `/reports/pipeline_optimization_report.md` - This file\n\n")

    log(f"Summary report saved to {report_path}")

# Main execution
def main():
    log("="*80)
    log("CONTINUUM REPORT - PIPELINE OPTIMIZATION")
    log("="*80)

    try:
        # Phase 1
        priority_pairs, entities, pairs = phase1_extract_priority_pairs()

        # Phase 2
        normalization_map = phase2_build_normalization_map(entities)

        # Phase 3
        boilerplate_filter = phase3_build_boilerplate_filter()

        # Phase 4
        clean_entities, entity_stats = phase4_create_filtered_registry(
            entities, normalization_map, boilerplate_filter
        )

        # Phase 5
        clean_pairs, cooccurrence_stats = phase5_update_cooccurrence(
            pairs, clean_entities, normalization_map, boilerplate_filter
        )

        # Phase 6
        gaps = phase6_cross_reference_curated(
            clean_entities, WEBSITE_DATA_PATH / "entities.json"
        )

        # Phase 7
        phase7_summary_report(priority_pairs, entity_stats, cooccurrence_stats, gaps)

        # Save log
        save_log()

        log("\n" + "="*80)
        log("PIPELINE OPTIMIZATION COMPLETE")
        log("="*80)

    except Exception as e:
        log(f"\nERROR: {str(e)}")
        import traceback
        log(traceback.format_exc())
        save_log()
        raise

if __name__ == "__main__":
    main()
