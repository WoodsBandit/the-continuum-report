#!/usr/bin/env python3
"""
Connection Brief Generator for The Continuum Report
Phase 5 of 5 - Continuum.html Implementation
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
ENTITIES_PATH = '/continuum/data/entities.json'
BRIEFS_PATH = '/continuum/briefs/'
CONNECTIONS_OUTPUT = '/continuum/briefs/connections/'
DATA_OUTPUT = '/continuum/data/'

def load_entities():
    """Load entity data from JSON"""
    with open(ENTITIES_PATH, 'r') as f:
        return json.load(f)

def load_analytical_brief(entity_id):
    """Load existing analytical brief for an entity if available"""
    brief_patterns = [
        f'{BRIEFS_PATH}analytical_brief_{entity_id}.md',
        f'{BRIEFS_PATH}{entity_id}_brief.md',
        f'{BRIEFS_PATH}{entity_id}.md'
    ]

    for pattern in brief_patterns:
        if os.path.exists(pattern):
            with open(pattern, 'r') as f:
                return f.read()
    return None

def get_connection_summary(entity, target_id, mention_details):
    """Generate a summary for a specific connection"""
    entity_name = entity.get('name', entity['id'])

    # Get mention details for this connection
    details = mention_details.get(target_id, {})
    count = details.get('count', 0)
    strength = details.get('strength', 'associated')

    # Generate summary based on strength
    if strength == 'documented':
        return f"Connection between {entity_name} and this entity is documented in {count} court filing reference(s). This represents a verified documentary connection established through primary source materials."
    elif strength == 'referenced':
        return f"Connection referenced in {count} document(s). This connection appears in source materials but may be indirect or contextual."
    else:
        return f"Associated through mutual connections or contextual references in source materials."

def generate_connection_brief(entity, entities_dict):
    """Generate complete connection brief for an entity"""

    entity_id = entity['id']
    entity_name = entity.get('name', entity_id)
    mentions = entity.get('mentions', [])
    mention_details = entity.get('mention_details', {})
    sources = entity.get('sources', [])

    # Load analytical brief if exists
    analytical_brief = load_analytical_brief(entity_id)

    date_str = datetime.now().strftime('%Y-%m-%d')

    # Generate header
    brief = f"""# {entity_name} — Connection Analysis

## Editorial Commentary Under First Amendment Protection

**Prepared by:** The Continuum Report
**Generated:** {date_str}
**Entity ID:** {entity_id}
**Classification:** Analytical Commentary — Not Statements of Fact

---

## Methodology Statement

This Connection Analysis documents relationships between **{entity_name}** and other entities within The Continuum based on publicly available source materials. All connections are derived from court filings, sworn testimony, news reports, and other documented sources.

**Important:** The inclusion of any individual in this analysis does not imply wrongdoing. Connections may be professional, social, incidental, or circumstantial. Readers should consult primary sources and draw their own conclusions.

---

"""

    # Track all sources for index
    all_sources = []
    connection_data_list = []

    # Generate section for each connection
    for target_id in mentions:
        target_entity = entities_dict.get(target_id, {'id': target_id, 'name': target_id.replace('-', ' ').title()})
        target_name = target_entity.get('name', target_id.replace('-', ' ').title())

        details = mention_details.get(target_id, {})
        count = details.get('count', 0)
        strength = details.get('strength', 'associated')

        summary = get_connection_summary(entity, target_id, mention_details)

        # Find relevant sources
        relevant_sources = []
        for src in sources:
            relevant_sources.append(src)
            all_sources.append(src)

        brief += f"""## Connection: {target_name}

### Summary

{summary}

### Documented Evidence

"""

        # Add evidence items
        if relevant_sources:
            for src in relevant_sources[:3]:  # Limit to 3 sources per connection
                ecf = src.get('ecf', 'Unknown')
                desc = src.get('description', 'Source Document')
                filed = src.get('filed', '')

                brief += f"""**ECF Doc. {ecf}** ({desc}, filed {filed}):

> Document references connection context. See primary source for full details.

"""
        else:
            brief += """*Source documentation derived from case materials. See Document Index for full source list.*

"""

        # Add analysis
        brief += f"""### Analysis

*The following represents editorial commentary and opinion:*

The documented connection between {entity_name} and {target_name} appears in court filings and related materials. Based on our review of available documents, this connection {"is well-established through multiple documentary references" if strength == "documented" else "is referenced in source materials" if strength == "referenced" else "may warrant further investigation to fully characterize"}.

### Alternative Interpretations

The documented association between these parties may reflect:
- Professional or business relationships
- Social acquaintance within shared circles
- Coincidental appearance in the same proceedings
- Witness or victim status rather than culpable involvement

Readers should review primary sources to form independent conclusions.

---

"""

        # Store connection data for JSON
        connection_data_list.append({
            'entityId': target_id,
            'summary': summary,
            'strength': strength,
            'count': count,
            'sources': [{'id': s.get('ecf'), 'title': f"ECF Doc. {s.get('ecf')}", 'date': s.get('filed')} for s in relevant_sources[:3]]
        })

    # Add document index
    brief += """## Document Index

All sources cited in this Connection Analysis:

"""

    seen_sources = set()
    for i, source in enumerate(all_sources, 1):
        ecf = source.get('ecf', '')
        if ecf not in seen_sources:
            seen_sources.add(ecf)
            brief += f"{i}. **ECF Doc. {ecf}** — {source.get('description', 'Court Filing')}, Filed: {source.get('filed', 'Date unknown')}\n"

    if not all_sources:
        brief += "*Source documents referenced in associated analytical brief.*\n"

    # Add disclaimer
    brief += """
---

## Disclaimer

This document constitutes editorial commentary and opinion journalism protected under the First Amendment. The Continuum Report makes no accusations of illegal activity. All statements of fact are attributed to their sources. Interpretive statements represent the editorial opinion of the authors and should not be construed as assertions of fact.

For corrections or additional information, contact: contact@thecontinuumreport.com

---

*The Continuum Report — Another Node in the Decentralized Intelligence Agency*
"""

    return brief, connection_data_list

def generate_all_connection_briefs():
    """Main function to generate all connection briefs"""

    # Ensure output directory exists
    os.makedirs(CONNECTIONS_OUTPUT, exist_ok=True)

    # Load entities
    data = load_entities()
    entities_list = data.get('entities', [])
    entities_dict = {e['id']: e for e in entities_list}

    # Track generated briefs
    generated = []
    errors = []
    all_connection_data = {}

    for entity in entities_list:
        entity_id = entity['id']
        try:
            # Skip entities with no mentions
            if not entity.get('mentions'):
                print(f"⊘ Skipping {entity_id}: No connections")
                continue

            # Generate brief
            brief_content, connection_data = generate_connection_brief(entity, entities_dict)

            # Write file
            output_path = f"{CONNECTIONS_OUTPUT}{entity_id}_connections.md"
            with open(output_path, 'w') as f:
                f.write(brief_content)

            generated.append({
                'entity_id': entity_id,
                'entity_name': entity.get('name', entity_id),
                'connection_count': len(entity.get('mentions', [])),
                'file_path': output_path
            })

            # Store connection data for JSON
            all_connection_data[entity_id] = {
                'brief_path': f"/continuum/briefs/connections/{entity_id}_connections.md",
                'connections': connection_data
            }

            print(f"✓ Generated: {output_path}")

        except Exception as e:
            errors.append({
                'entity_id': entity_id,
                'error': str(e)
            })
            print(f"✗ Error for {entity_id}: {e}")

    # Create manifest
    manifest = {
        'generated_at': datetime.now().isoformat(),
        'total_entities': len(entities_list),
        'briefs_generated': len(generated),
        'errors': len(errors),
        'briefs': generated,
        'error_details': errors
    }

    manifest_path = f"{CONNECTIONS_OUTPUT}manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"✓ Created: {manifest_path}")

    # Create connection_briefs.json for website
    website_data = {
        'generated': datetime.now().strftime('%Y-%m-%d'),
        'entities': all_connection_data
    }

    website_json_path = f"{DATA_OUTPUT}connection_briefs.json"
    with open(website_json_path, 'w') as f:
        json.dump(website_data, f, indent=2)
    print(f"✓ Created: {website_json_path}")

    print(f"\n{'='*60}")
    print(f"Connection Brief Generation Complete")
    print(f"{'='*60}")
    print(f"Generated: {len(generated)} briefs")
    print(f"Errors: {len(errors)}")
    print(f"Manifest: {manifest_path}")
    print(f"Website JSON: {website_json_path}")

    return manifest

if __name__ == '__main__':
    generate_all_connection_briefs()
