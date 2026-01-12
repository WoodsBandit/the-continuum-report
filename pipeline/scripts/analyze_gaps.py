#!/usr/bin/env python3
"""
Gap Analysis: Compare indexes against curated data

Identifies:
1. High co-occurrence pairs missing from connections.json
2. Connections with weak source evidence
3. Entities with many sources but no brief
"""

import json
from pathlib import Path
from datetime import datetime, timezone


def load_json(filepath):
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_undocumented_connections(co_occurrence, threshold=3):
    """Find high co-occurrence pairs not in connections.json"""

    undocumented = []

    for pair_key, data in co_occurrence['pairs'].items():
        if not data['in_connections_json'] and data['co_mention_count'] >= threshold:
            entity1, entity2 = pair_key.split('|')

            # Filter out obvious boilerplate/legal jargon
            skip_keywords = [
                'case-no', 'fort-lauderdale', 'las-olas', 'main-street',
                'north-andrews', 'respectfully-submitted', 'pro-hac',
                'civil-procedure', 'electronic-filing', 'notary-public',
                'composite-exhibit', 'appear-pro', 'documents-you',
                'income-you', 'your-attorneys', 'your-complaint',
                'defendant-', 'plaintiff-', 'court-', 'exhibit-',
                'page-', 'line-', 'docket-'
            ]

            skip = False
            for keyword in skip_keywords:
                if keyword in entity1 or keyword in entity2:
                    skip = True
                    break

            if not skip:
                undocumented.append({
                    'entity1': entity1,
                    'entity2': entity2,
                    'co_mention_count': data['co_mention_count'],
                    'shared_sources': data['shared_sources']
                })

    # Sort by co-mention count
    undocumented.sort(key=lambda x: x['co_mention_count'], reverse=True)

    return undocumented


def analyze_weak_connections(connections, co_occurrence):
    """Find connections with low co-occurrence evidence"""

    weak_connections = []

    for conn in connections['connections']:
        source = conn['source']
        target = conn['target']

        # Create normalized pair key
        entities = sorted([source, target])
        pair_key = f"{entities[0]}|{entities[1]}"

        # Check co-occurrence
        if pair_key in co_occurrence['pairs']:
            co_count = co_occurrence['pairs'][pair_key]['co_mention_count']
        else:
            co_count = 0

        # Flag connections with few co-occurrences (co-count < 2)
        if co_count < 2:
            weak_connections.append({
                'source': source,
                'target': target,
                'co_occurrence': co_count,
                'sources_count': conn.get('sources_count', 0),  # Binary model: no strength scoring
                'type': conn.get('type', 'unknown'),
                'evidence': conn.get('evidence', [])
            })

    # Sort by co-occurrence (ascending - weakest first)
    weak_connections.sort(key=lambda x: x['co_occurrence'])

    return weak_connections


def analyze_entities_without_briefs(entity_registry, entities_with_briefs, threshold=10):
    """Find high-mention entities without briefs"""

    entities_needing_briefs = []

    # Get set of entity IDs with briefs
    brief_ids = set()
    for entity in entities_with_briefs.get('entities', []):
        entity_id = entity.get('id', '').lower()
        if entity.get('brief_file') or entity.get('brief_url'):
            brief_ids.add(entity_id)

    # Check all entities
    for entity_id, data in entity_registry['entities'].items():
        if entity_id not in brief_ids and data['mention_count'] >= threshold:

            # Filter out obvious boilerplate
            skip_keywords = [
                'case-no', 'fort-lauderdale', 'las-olas', 'main-street',
                'notary-public', 'civil-procedure', 'electronic-filing',
                'respectfully-submitted', 'pro-hac', 'composite-exhibit',
                'new-york', 'palm-beach', 'salt-lake-city'  # Generic locations
            ]

            if not any(keyword in entity_id for keyword in skip_keywords):
                entities_needing_briefs.append({
                    'entity_id': entity_id,
                    'name': data['name'],
                    'mention_count': data['mention_count'],
                    'source_count': data['source_count']
                })

    # Sort by mention count
    entities_needing_briefs.sort(key=lambda x: x['mention_count'], reverse=True)

    return entities_needing_briefs


def generate_report(entity_registry, source_mentions, co_occurrence, connections, entities):
    """Generate comprehensive gap analysis report"""

    # Run analyses
    undocumented = analyze_undocumented_connections(co_occurrence, threshold=3)
    weak = analyze_weak_connections(connections, co_occurrence)
    no_briefs = analyze_entities_without_briefs(entity_registry, entities, threshold=10)

    # Build report
    report = []
    report.append("# Index Pipeline - Gap Analysis Report")
    report.append(f"\n**Generated:** {datetime.now(timezone.utc).isoformat()}")
    report.append(f"\n**Data Sources:**")
    report.append(f"- Entity Registry: {entity_registry['count']} entities")
    report.append(f"- Source Mentions: {source_mentions['source_count']} sources")
    report.append(f"- Co-occurrence: {co_occurrence['pair_count']} pairs")
    report.append(f"- Connections: {connections['count']} documented")
    report.append(f"- Entities with Briefs: {entities['count']} curated")

    report.append("\n---\n")
    report.append("## Executive Summary\n")
    report.append(f"This report identifies gaps between raw entity extractions and curated documentation.\n")
    report.append(f"\n**Key Findings:**")
    report.append(f"- {len(undocumented)} high co-occurrence pairs are undocumented")
    report.append(f"- {len(weak)} documented connections have weak evidence")
    report.append(f"- {len(no_briefs)} high-mention entities lack briefs")

    report.append("\n---\n")
    report.append("## 1. High Co-occurrence Pairs Missing from connections.json\n")
    report.append("These entity pairs appear together frequently but are not documented in connections.json.\n")

    if undocumented:
        report.append(f"\n**Found {len(undocumented)} undocumented pairs with ≥3 co-mentions:**\n")

        # Top 20
        for item in undocumented[:20]:
            report.append(f"\n### {item['entity1']} × {item['entity2']}")
            report.append(f"- **Co-mentions:** {item['co_mention_count']}")
            report.append(f"- **Shared Sources:** {', '.join(item['shared_sources'][:5])}")
            if len(item['shared_sources']) > 5:
                report.append(f"  (and {len(item['shared_sources']) - 5} more)")

        if len(undocumented) > 20:
            report.append(f"\n*...and {len(undocumented) - 20} more pairs*")
    else:
        report.append("\nNo high co-occurrence undocumented pairs found.")

    report.append("\n---\n")
    report.append("## 2. Connections with Weak Source Evidence\n")
    report.append("These connections are documented but have low co-occurrence in source documents.\n")

    if weak:
        report.append(f"\n**Found {len(weak)} connections with <2 co-mentions:**\n")

        for item in weak[:20]:
            report.append(f"\n### {item['source']} → {item['target']}")
            report.append(f"- **Co-occurrence:** {item['co_occurrence']}")
            report.append(f"- **Sources:** {item['sources_count']}")
            report.append(f"- **Type:** {item['type']}")
            report.append(f"- **Evidence:** {', '.join(item['evidence'][:3])}")

        if len(weak) > 20:
            report.append(f"\n*...and {len(weak) - 20} more weak connections*")

        report.append("\n**Note:** Low co-occurrence may be expected for:")
        report.append("- Connections based on external sources (not in this corpus)")
        report.append("- Indirect connections (via intermediaries)")
        report.append("- Parallel cases (structural comparisons)")

    else:
        report.append("\nAll documented connections have strong co-occurrence evidence.")

    report.append("\n---\n")
    report.append("## 3. Entities with Many Sources but No Brief\n")
    report.append("These entities appear frequently but lack curated profiles in entities.json.\n")

    if no_briefs:
        report.append(f"\n**Found {len(no_briefs)} high-mention entities without briefs (≥10 mentions):**\n")

        for item in no_briefs[:30]:
            report.append(f"\n### {item['name']}")
            report.append(f"- **Entity ID:** `{item['entity_id']}`")
            report.append(f"- **Mentions:** {item['mention_count']} across {item['source_count']} sources")

        if len(no_briefs) > 30:
            report.append(f"\n*...and {len(no_briefs) - 30} more entities*")

        report.append("\n**Recommendation:** Review top entities to determine which merit analytical briefs.")

    else:
        report.append("\nAll high-mention entities have curated briefs.")

    report.append("\n---\n")
    report.append("## Recommendations\n")

    report.append("\n### Priority 1: Document High Co-occurrence Pairs")
    if undocumented:
        report.append(f"\nReview the top {min(10, len(undocumented))} undocumented pairs listed above.")
        report.append("Determine which represent substantive relationships worthy of documentation.")

    report.append("\n### Priority 2: Validate Weak Connections")
    if weak:
        report.append(f"\nReview {len(weak)} connections with low co-occurrence.")
        report.append("Verify evidence sources and consider adding supporting documentation.")

    report.append("\n### Priority 3: Expand Entity Coverage")
    if no_briefs:
        report.append(f"\nConsider creating briefs for high-value entities without current documentation.")
        report.append("Focus on entities with substantive roles (people, organizations, cases).")

    report.append("\n### Data Quality Improvements")
    report.append("\n- **Entity Normalization:** Merge variants (e.g., 'ghislaine-maxwell' vs 'defendant-ghislaine-maxwell')")
    report.append("- **Boilerplate Filtering:** Improve extraction to exclude legal boilerplate")
    report.append("- **Source Expansion:** Process additional documents to increase co-occurrence counts")
    report.append("- **Manual Review:** Validate top undocumented pairs for substantive relationships")

    report.append("\n---\n")
    report.append("## Next Steps\n")
    report.append("\n1. **Human Review:** Analyst reviews undocumented high co-occurrence pairs")
    report.append("2. **Documentation:** Add valid connections to connections.json")
    report.append("3. **Brief Writing:** Create entity briefs for high-priority entities")
    report.append("4. **Index Rebuild:** Re-run pipeline after updates")
    report.append("5. **Iteration:** Repeat analysis to track progress")

    report.append("\n---\n")
    report.append("## Appendix: Statistics\n")

    # Co-occurrence distribution
    counts = [p['co_mention_count'] for p in co_occurrence['pairs'].values()]
    report.append(f"\n### Co-occurrence Distribution")
    report.append(f"- Total pairs: {len(counts)}")
    report.append(f"- Average co-mentions: {sum(counts)/len(counts):.1f}")
    report.append(f"- Max co-mentions: {max(counts)}")
    report.append(f"- Pairs with ≥3 co-mentions: {sum(1 for c in counts if c >= 3)}")
    report.append(f"- Pairs with ≥5 co-mentions: {sum(1 for c in counts if c >= 5)}")
    report.append(f"- Pairs with ≥10 co-mentions: {sum(1 for c in counts if c >= 10)}")

    # Entity distribution
    mention_counts = [e['mention_count'] for e in entity_registry['entities'].values()]
    report.append(f"\n### Entity Mention Distribution")
    report.append(f"- Total entities: {len(mention_counts)}")
    report.append(f"- Average mentions: {sum(mention_counts)/len(mention_counts):.1f}")
    report.append(f"- Max mentions: {max(mention_counts)}")
    report.append(f"- Entities with ≥10 mentions: {sum(1 for c in mention_counts if c >= 10)}")
    report.append(f"- Entities with ≥20 mentions: {sum(1 for c in mention_counts if c >= 20)}")
    report.append(f"- Entities with ≥50 mentions: {sum(1 for c in mention_counts if c >= 50)}")

    return '\n'.join(report)


def main():
    base_dir = Path(r'\\192.168.1.139\continuum')

    print("Loading data files...")

    # Load all data
    entity_registry = load_json(base_dir / 'indexes' / 'entity_registry.json')
    source_mentions = load_json(base_dir / 'indexes' / 'source_mentions.json')
    co_occurrence = load_json(base_dir / 'indexes' / 'co_occurrence.json')
    connections = load_json(base_dir / 'website' / 'data' / 'connections.json')
    entities = load_json(base_dir / 'website' / 'data' / 'entities.json')

    print("Generating gap analysis report...")

    # Generate report
    report = generate_report(entity_registry, source_mentions, co_occurrence, connections, entities)

    # Write report
    output_dir = base_dir / 'reports'
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / 'index_pipeline_report.md'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport written to: {output_file}")
    print(f"Report length: {len(report)} characters")


if __name__ == '__main__':
    main()
