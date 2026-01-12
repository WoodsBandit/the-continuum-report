# TASK: Generate All Connection Briefs

## OBJECTIVE
Generate connection brief markdown files for every entity in entities.json so the "View Brief" button works in the detail panel.

## OUTPUT LOCATION
```
/continuum/briefs/connections/
```

Each file should be named: `{entityId}_connections.md`

## STEP 1: Setup

```bash
# Create the briefs directory if it doesn't exist
mkdir -p /continuum/briefs/connections

# Check what entities exist
cat /continuum/data/entities.json | head -200
```

## STEP 2: Read Entity Data

Parse entities.json to get:
- Entity ID
- Entity name
- Entity type
- Entity connections array (with targetId, summary, sources)

## STEP 3: Generate Brief for Each Entity

For each entity that has connections, create a markdown file with this structure:

```markdown
# [Entity Name] — Connections Brief

**Entity Type:** [Person/Organization/Case]  
**Total Connections:** [count]  
**Generated:** [date]

---

## Connection Summary

[2-3 sentence overview of this entity's role and significance in the network]

---

## Documented Connections

### 1. [Connected Entity Name]
**Type:** [Person/Organization/Case]  
**Relationship:** [Brief description of the connection]

[Expanded summary of the connection - what documents show, nature of relationship, timeline if known]

**Sources:**
- [Source document title/description]
- [Source document title/description]

---

### 2. [Next Connected Entity Name]
...

---

## Analysis Notes

[Any patterns, significance, or analytical observations about this entity's connections]

---

*This brief is part of The Continuum Report's documented analysis of the Epstein network. All connections are derived from court documents, depositions, flight logs, and other primary source materials.*
```

## STEP 4: Python Script to Generate Briefs

Create and run this script:

```python
#!/usr/bin/env python3
"""
Generate connection briefs for all entities in The Continuum Report.
"""

import json
import os
from datetime import datetime

# Paths
ENTITIES_FILE = '/continuum/data/entities.json'
BRIEFS_DIR = '/continuum/briefs/connections'

# Ensure output directory exists
os.makedirs(BRIEFS_DIR, exist_ok=True)

def load_entities():
    """Load entities from JSON file."""
    with open(ENTITIES_FILE, 'r') as f:
        data = json.load(f)
    return data.get('entities', data) if isinstance(data, dict) else data

def get_entity_by_id(entities, entity_id):
    """Find entity by ID."""
    for e in entities:
        if e.get('id') == entity_id:
            return e
    return None

def generate_brief(entity, all_entities):
    """Generate markdown brief for an entity."""
    name = entity.get('name', entity.get('id', 'Unknown'))
    entity_type = entity.get('type', 'Unknown').title()
    connections = entity.get('connections', [])
    
    if not connections:
        return None
    
    # Build the brief
    lines = []
    lines.append(f"# {name} — Connections Brief\n")
    lines.append(f"**Entity Type:** {entity_type}  ")
    lines.append(f"**Total Connections:** {len(connections)}  ")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Connection Summary")
    lines.append("")
    
    # Generate summary based on entity type and connections
    conn_types = {}
    for c in connections:
        target = get_entity_by_id(all_entities, c.get('targetId', c.get('target', '')))
        if target:
            t = target.get('type', 'unknown')
            conn_types[t] = conn_types.get(t, 0) + 1
    
    type_summary = ', '.join([f"{v} {k}s" for k, v in conn_types.items()])
    lines.append(f"{name} has {len(connections)} documented connections in The Continuum Report database ({type_summary}). These connections are derived from court documents, depositions, and other primary source materials.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Documented Connections")
    lines.append("")
    
    # Each connection
    for i, conn in enumerate(connections, 1):
        target_id = conn.get('targetId', conn.get('target', ''))
        target = get_entity_by_id(all_entities, target_id)
        target_name = target.get('name', target_id) if target else target_id
        target_type = target.get('type', 'Unknown').title() if target else 'Unknown'
        
        summary = conn.get('summary', 'Connection documented in source materials.')
        sources = conn.get('sources', [])
        
        lines.append(f"### {i}. {target_name}")
        lines.append(f"**Type:** {target_type}  ")
        lines.append("")
        lines.append(summary)
        lines.append("")
        
        if sources:
            lines.append("**Sources:**")
            for src in sources:
                if isinstance(src, dict):
                    title = src.get('title', src.get('description', 'Source Document'))
                    lines.append(f"- {title}")
                else:
                    lines.append(f"- {src}")
        else:
            lines.append("**Sources:** Primary source documentation pending verification")
        
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Analysis notes
    lines.append("## Analysis Notes")
    lines.append("")
    if len(connections) > 5:
        lines.append(f"{name} appears to be a significant node in the network with {len(connections)} documented connections. Further analysis may reveal additional patterns.")
    else:
        lines.append(f"{name} has {len(connections)} documented connections. Additional connections may be revealed as more documents are processed.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*This brief is part of The Continuum Report's documented analysis. All connections are derived from court documents, depositions, flight logs, and other primary source materials.*")
    
    return '\n'.join(lines)

def main():
    print("Loading entities...")
    entities = load_entities()
    print(f"Found {len(entities)} entities")
    
    generated = 0
    skipped = 0
    
    for entity in entities:
        entity_id = entity.get('id', '')
        if not entity_id:
            continue
        
        connections = entity.get('connections', [])
        if not connections:
            print(f"  Skipping {entity.get('name', entity_id)}: no connections")
            skipped += 1
            continue
        
        brief = generate_brief(entity, entities)
        if brief:
            # Sanitize filename
            safe_id = entity_id.replace(' ', '-').replace('/', '-').lower()
            filepath = os.path.join(BRIEFS_DIR, f"{safe_id}_connections.md")
            
            with open(filepath, 'w') as f:
                f.write(brief)
            
            print(f"  Generated: {filepath}")
            generated += 1
    
    print(f"\nComplete! Generated {generated} briefs, skipped {skipped} entities without connections")
    print(f"Briefs saved to: {BRIEFS_DIR}")

if __name__ == '__main__':
    main()
```

## STEP 5: Run the Script

```bash
cd /continuum
python3 scripts/generate_briefs.py
```

Or run inline:
```bash
python3 << 'EOF'
# [paste the script above]
EOF
```

## STEP 6: Verify Output

```bash
# Check briefs were created
ls -la /continuum/briefs/connections/

# Check a sample brief
cat /continuum/briefs/connections/jeffrey-epstein_connections.md | head -50

# Count briefs
ls /continuum/briefs/connections/*.md | wc -l
```

## STEP 7: Verify Web Path

The code in continuum.html fetches briefs from:
```javascript
const briefPath = `/continuum/briefs/connections/${entityId}_connections.md`;
```

Ensure your web server (nginx/cloudflare) serves `/continuum/briefs/` from the correct directory.

If the web root is `/continuum/website/`, you may need to:

**Option A:** Symlink briefs into website directory
```bash
ln -s /continuum/briefs /continuum/website/briefs
```

**Option B:** Update nginx config to serve briefs directory

**Option C:** Update the code path to match your actual structure

## ENTITY ID FORMAT CHECK

The script normalizes entity IDs to lowercase with hyphens. Verify this matches how the code calls them:

```bash
# Check how entity IDs appear in entities.json
grep -o '"id":\s*"[^"]*"' /continuum/data/entities.json | head -20
```

If IDs in the JSON use different format (spaces, caps), update the script's `safe_id` logic or the code's fetch path.

## VERIFICATION

1. Run the script
2. Confirm files created in `/continuum/briefs/connections/`
3. Open continuum.html in browser
4. Navigate to an entity (e.g., Jeffrey Epstein)
5. Click "View Brief" button
6. Verify brief content displays in modal

## TROUBLESHOOTING

**Brief not found (404):**
- Check file exists: `ls /continuum/briefs/connections/ | grep epstein`
- Check web server serves the path
- Check entity ID format matches filename

**Empty connections in brief:**
- Check entities.json has `connections` array populated
- Run the enrichment phase if connections are missing

## BACKUP
```bash
# Backup existing briefs if any
cp -r /continuum/briefs /continuum/briefs_backup_$(date +%Y%m%d)
```
