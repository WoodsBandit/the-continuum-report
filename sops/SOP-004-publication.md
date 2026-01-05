# SOP-004: Publication

**Document Version:** 1.0
**Last Updated:** 2025-12-25
**Pipeline Stage:** 4 of 4 (Final)
**Trigger:** Files detected in approved/ directory
**Execution Mode:** Autonomous (Claude Code)

---

## 1. Purpose

Publish human-approved analytical briefs to The Continuum Report website by updating data indexes, copying files to web directories, and archiving published content. This is the final autonomous stage before content goes live.

## 2. Trigger Condition

**Primary Trigger:** Files detected in `\\192.168.1.139\continuum\approved\` directories
**Monitoring Method:** Directory watch or periodic polling (every 60 seconds)
**Trigger Script:**
```python
# Watch approved/ directories for new files
import os
import time
from pathlib import Path

approved_entities = Path(r"\\192.168.1.139\continuum\approved\entities")
approved_connections = Path(r"\\192.168.1.139\continuum\approved\connections")

def check_for_approved_files():
    entity_files = list(approved_entities.glob("*.md"))
    connection_files = list(approved_connections.glob("*.md"))

    if entity_files or connection_files:
        execute_stage4(entity_files, connection_files)
        return True
    return False

while True:
    check_for_approved_files()
    time.sleep(60)
```

**Fallback Trigger:** Manual execution via command line
**Alternative Trigger:** Scheduled daily publication run (e.g., 6 AM daily)

## 3. Prerequisites

### Required Files Must Exist
- `\\192.168.1.139\continuum\website\data\entities.json`
- `\\192.168.1.139\continuum\website\data\connections.json`
- `\\192.168.1.139\continuum\website\continuum.html`

### Required Directories Must Exist
- `\\192.168.1.139\continuum\approved\entities\`
- `\\192.168.1.139\continuum\approved\connections\`
- `\\192.168.1.139\continuum\website\briefs\entity\`
- `\\192.168.1.139\continuum\website\briefs\connections\`
- `\\192.168.1.139\continuum\website\sources\`
- `\\192.168.1.139\continuum\archive\published\entities\`
- `\\192.168.1.139\continuum\archive\published\connections\`

### System Requirements
- Write access to website/ directory
- Write access to archive/ directory
- Sufficient disk space for brief and source file copies

## 4. Inputs

### Primary Inputs

**Approved Entity Briefs:**
`\\192.168.1.139\continuum\approved\entities\*.md`
- Human-approved entity analytical briefs
- Must have valid YAML frontmatter
- Legal review must be resolved

**Approved Connection Briefs:**
`\\192.168.1.139\continuum\approved\connections\*.md`
- Human-approved connection briefs
- Must have valid YAML frontmatter
- Legal review must be resolved

### Reference Inputs

**Entity Registry:** `\\192.168.1.139\continuum\indexes\entity_registry.json`
**Source Mentions:** `\\192.168.1.139\continuum\indexes\source_mentions.json`

### Website Data Files (Existing)

**Entities Data:** `\\192.168.1.139\continuum\website\data\entities.json`
```json
{
  "_schema_version": "1.0",
  "_last_updated": "2025-12-25T10:00:00Z",
  "entities": [
    {
      "id": "john_doe",
      "name": "John Doe",
      "type": "PERSON",
      "brief_path": "/briefs/entity/analytical_brief_John_Doe.md",
      "mention_count": 42,
      "connection_count": 8,
      "last_updated": "2025-12-20T15:30:00Z",
      "preview": "John Doe is a prominent figure in...",
      "tags": ["business", "legal"]
    }
  ]
}
```

**Connections Data:** `\\192.168.1.139\continuum\website\data\connections.json`
```json
{
  "_schema_version": "1.0",
  "_last_updated": "2025-12-25T10:00:00Z",
  "connections": [
    {
      "id": "john_doe_acme_corporation",
      "entity1": "John Doe",
      "entity2": "Acme Corporation",
      "brief_path": "/briefs/connections/John_Doe_Acme_Corporation.md",
      "relationship_type": "employment",
      "strength": 0.85,
      "last_updated": "2025-12-20T15:45:00Z",
      "preview": "John Doe served as CFO of Acme Corporation..."
    }
  ]
}
```

## 5. Process Steps

### Step 1: Scan Approved Directories

**Action:** Identify all approved briefs awaiting publication

```
# Scan for approved entity briefs
approved_entity_briefs = []
entity_dir = \\192.168.1.139\continuum\approved\entities\

FOR EACH file IN entity_dir:
    IF file.endswith('.md'):
        approved_entity_briefs.append(file)
        LOG INFO: "Found approved entity brief: {file}"

# Scan for approved connection briefs
approved_connection_briefs = []
connection_dir = \\192.168.1.139\continuum\approved\connections\

FOR EACH file IN connection_dir:
    IF file.endswith('.md'):
        approved_connection_briefs.append(file)
        LOG INFO: "Found approved connection brief: {file}"

total_briefs = len(approved_entity_briefs) + len(approved_connection_briefs)

LOG INFO: "Found {total_briefs} approved briefs for publication"

IF total_briefs == 0:
    LOG INFO: "No approved briefs to publish, Stage 4 complete"
    HALT processing (success)
```

### Step 2: Validate Approved Briefs

**Action:** Ensure all approved briefs are properly formatted and ready for publication

```
validation_errors = []

FOR EACH brief_path IN (approved_entity_briefs + approved_connection_briefs):
    TRY:
        # Read brief
        brief_content = READ file at brief_path

        # Parse YAML frontmatter
        metadata = PARSE_YAML_FRONTMATTER(brief_content)

        # Validate required fields exist
        required_fields = ["last_updated", "legal_review"]

        FOR EACH field IN required_fields:
            IF field NOT IN metadata:
                validation_errors.append({
                    "brief": brief_path,
                    "error": f"Missing required field: {field}"
                })

        # Check legal review status
        legal_status = metadata.get("legal_review", "UNKNOWN")

        IF legal_status == "ISSUES FOUND" AND "manual_legal_approval" NOT IN metadata:
            validation_errors.append({
                "brief": brief_path,
                "error": "Legal issues not resolved - missing manual approval"
            })

        # Validate content body exists
        content_body = EXTRACT_CONTENT_BODY(brief_content)
        IF len(content_body.strip()) < 100:
            validation_errors.append({
                "brief": brief_path,
                "error": "Brief content too short (< 100 chars)"
            })

    CATCH Exception as e:
        validation_errors.append({
            "brief": brief_path,
            "error": f"Validation failed: {e}"
        })

IF len(validation_errors) > 0:
    LOG ERROR: "Validation failed for {len(validation_errors)} briefs"

    FOR EACH error IN validation_errors:
        LOG ERROR: "  {error.brief}: {error.error}"

    # Move invalid briefs back to pending_approval with error notes
    FOR EACH error IN validation_errors:
        MOVE error.brief BACK TO pending_approval/
        CREATE error_note: {error.brief}.ERROR with error details

    # Remove invalid briefs from processing queue
    approved_entity_briefs = REMOVE invalid briefs
    approved_connection_briefs = REMOVE invalid briefs

    LOG WARNING: "Continuing with {remaining} valid briefs"
```

### Step 3: Process Entity Brief Publications

**Action:** Publish each approved entity brief

```
READ: \\192.168.1.139\continuum\website\data\entities.json
PARSE as entities_data

published_entities = []

FOR EACH brief_path IN approved_entity_briefs:
    LOG INFO: "Publishing entity brief: {brief_path}"

    # Read and parse brief
    brief_content = READ file at brief_path
    metadata = PARSE_YAML_FRONTMATTER(brief_content)
    content_body = EXTRACT_CONTENT_BODY(brief_content)

    entity_name = metadata.entity_name
    entity_type = metadata.entity_type

    # Get additional data from entity registry
    entity_registry_data = entity_registry.entities.get(entity_name, {})

    # Generate entity ID (normalized name)
    entity_id = GENERATE_ENTITY_ID(entity_name)

    # Generate preview (first paragraph of Executive Summary)
    preview = EXTRACT_PREVIEW(content_body, max_chars=200)

    # Determine tags (based on entity type and content analysis)
    tags = GENERATE_TAGS(entity_type, content_body)

    # Count connections for this entity
    connection_count = COUNT_CONNECTIONS_FOR_ENTITY(entity_name)

    # Create/update entity entry for website data
    entity_entry = {
        "id": entity_id,
        "name": entity_name,
        "type": entity_type,
        "brief_path": f"/briefs/entity/{BASENAME(brief_path)}",
        "mention_count": entity_registry_data.get("mention_count", 0),
        "connection_count": connection_count,
        "last_updated": metadata.last_updated,
        "preview": preview,
        "tags": tags
    }

    # Check if entity already exists in website data
    existing_entity = FIND in entities_data.entities where id == entity_id

    IF existing_entity:
        # UPDATE existing entry
        UPDATE existing_entity with entity_entry values
        LOG INFO: "Updated existing entity entry: {entity_name}"
    ELSE:
        # ADD new entry
        entities_data.entities.append(entity_entry)
        LOG INFO: "Added new entity entry: {entity_name}"

    # Copy brief to website
    website_brief_path = \\192.168.1.139\continuum\website\briefs\entity\{BASENAME(brief_path)}
    COPY brief from brief_path to website_brief_path
    LOG INFO: "Copied brief to website: {website_brief_path}"

    # Track for archival
    published_entities.append({
        "brief_path": brief_path,
        "entity_name": entity_name,
        "entity_id": entity_id
    })

# Update website entities.json timestamp
entities_data._last_updated = current_timestamp

# Write updated entities data
WRITE entities_data to \\192.168.1.139\continuum\website\data\entities.json
LOG INFO: "Updated website entities.json"
```

**Generate Entity ID Function:**
```
FUNCTION GENERATE_ENTITY_ID(entity_name):
    # Convert to lowercase
    id = entity_name.lower()

    # Replace spaces and special chars with underscores
    id = REPLACE non-alphanumeric chars with '_'

    # Remove consecutive underscores
    while '__' in id:
        id = id.replace('__', '_')

    # Trim underscores from ends
    id = id.strip('_')

    RETURN id

EXAMPLES:
"John Doe" → "john_doe"
"Acme Corporation" → "acme_corporation"
"New York, NY" → "new_york_ny"
```

**Extract Preview Function:**
```
FUNCTION EXTRACT_PREVIEW(content_body, max_chars=200):
    # Find Executive Summary section
    lines = content_body.split('\n')

    in_exec_summary = False
    preview_lines = []

    FOR EACH line IN lines:
        IF "## Executive Summary" in line:
            in_exec_summary = True
            CONTINUE

        IF in_exec_summary:
            IF line.startswith('#'):  # Next section
                BREAK

            IF line.strip():  # Non-empty line
                preview_lines.append(line.strip())

    preview = ' '.join(preview_lines)

    # Truncate to max_chars
    IF len(preview) > max_chars:
        preview = preview[:max_chars] + "..."

    RETURN preview
```

**Generate Tags Function:**
```
FUNCTION GENERATE_TAGS(entity_type, content_body):
    # Base tag from entity type
    tags = [entity_type.lower()]

    # Content-based tags (keyword matching)
    tag_keywords = {
        "legal": ["lawsuit", "court", "litigation", "attorney", "case"],
        "business": ["company", "corporation", "transaction", "business"],
        "government": ["agency", "department", "official", "government"],
        "financial": ["financial", "money", "investment", "funds"],
        "real_estate": ["property", "real estate", "building", "land"]
    }

    content_lower = content_body.lower()

    FOR EACH tag, keywords IN tag_keywords:
        FOR EACH keyword IN keywords:
            IF keyword IN content_lower:
                tags.append(tag)
                BREAK  # One match per tag sufficient

    # Remove duplicates and limit to 5 tags
    tags = UNIQUE(tags)[:5]

    RETURN tags
```

### Step 4: Process Connection Brief Publications

**Action:** Publish each approved connection brief

```
READ: \\192.168.1.139\continuum\website\data\connections.json
PARSE as connections_data

published_connections = []

FOR EACH brief_path IN approved_connection_briefs:
    LOG INFO: "Publishing connection brief: {brief_path}"

    # Read and parse brief
    brief_content = READ file at brief_path
    metadata = PARSE_YAML_FRONTMATTER(brief_content)
    content_body = EXTRACT_CONTENT_BODY(brief_content)

    entity1 = metadata.entity1
    entity2 = metadata.entity2
    connection_id_meta = metadata.get("connection_id", f"{entity1}|{entity2}")

    # Generate connection ID for website
    connection_id = GENERATE_CONNECTION_ID(entity1, entity2)

    # Generate preview
    preview = EXTRACT_PREVIEW(content_body, max_chars=200)

    # Determine primary relationship type
    relationship_type = DETERMINE_RELATIONSHIP_TYPE(content_body, metadata)

    # Get relationship strength
    strength = metadata.get("relationship_strength", 0.5)

    # Create/update connection entry
    connection_entry = {
        "id": connection_id,
        "entity1": entity1,
        "entity2": entity2,
        "brief_path": f"/briefs/connections/{BASENAME(brief_path)}",
        "relationship_type": relationship_type,
        "strength": strength,
        "last_updated": metadata.last_updated,
        "preview": preview
    }

    # Check if connection already exists
    existing_connection = FIND in connections_data.connections where id == connection_id

    IF existing_connection:
        # UPDATE existing entry
        UPDATE existing_connection with connection_entry values
        LOG INFO: "Updated existing connection entry: {entity1} ↔ {entity2}"
    ELSE:
        # ADD new entry
        connections_data.connections.append(connection_entry)
        LOG INFO: "Added new connection entry: {entity1} ↔ {entity2}"

    # Copy brief to website
    website_brief_path = \\192.168.1.139\continuum\website\briefs\connections\{BASENAME(brief_path)}
    COPY brief from brief_path to website_brief_path
    LOG INFO: "Copied brief to website: {website_brief_path}"

    # Track for archival
    published_connections.append({
        "brief_path": brief_path,
        "entity1": entity1,
        "entity2": entity2,
        "connection_id": connection_id
    })

# Update website connections.json timestamp
connections_data._last_updated = current_timestamp

# Write updated connections data
WRITE connections_data to \\192.168.1.139\continuum\website\data\connections.json
LOG INFO: "Updated website connections.json"
```

**Generate Connection ID Function:**
```
FUNCTION GENERATE_CONNECTION_ID(entity1, entity2):
    # Convert both entities to IDs
    id1 = GENERATE_ENTITY_ID(entity1)
    id2 = GENERATE_ENTITY_ID(entity2)

    # Alphabetical order
    sorted_ids = SORT([id1, id2])

    # Combine with underscore
    connection_id = f"{sorted_ids[0]}_{sorted_ids[1]}"

    RETURN connection_id

EXAMPLES:
"John Doe", "Acme Corporation" → "acme_corporation_john_doe"
"New York", "Jane Smith" → "jane_smith_new_york"
```

**Determine Relationship Type Function:**
```
FUNCTION DETERMINE_RELATIONSHIP_TYPE(content_body, metadata):
    # Check if metadata specifies type
    IF "relationship_type" IN metadata:
        RETURN metadata.relationship_type

    # Otherwise, analyze content
    type_keywords = {
        "employment": ["employee", "worked for", "employed by", "CFO", "CEO", "director"],
        "ownership": ["owns", "owner of", "shareholder", "equity"],
        "legal": ["lawsuit", "litigation", "represented", "attorney"],
        "transaction": ["purchased", "sold", "acquired", "transaction"],
        "family": ["married", "spouse", "family", "relative"],
        "association": ["associated with", "connected to", "member"]
    }

    content_lower = content_body.lower()

    # Score each type
    type_scores = {}
    FOR EACH rel_type, keywords IN type_keywords:
        score = 0
        FOR EACH keyword IN keywords:
            IF keyword IN content_lower:
                score += 1
        type_scores[rel_type] = score

    # Return type with highest score
    IF max(type_scores.values()) > 0:
        RETURN max(type_scores, key=type_scores.get)
    ELSE:
        RETURN "association"  # Default
```

### Step 5: Copy Source Documents to Website

**Action:** Ensure all referenced source PDFs are available on website

```
# Collect all sources referenced in published briefs
all_referenced_sources = set()

FOR EACH entity IN published_entities:
    brief_metadata = GET_METADATA(entity.brief_path)
    sources = brief_metadata.get("sources_covered", [])
    all_referenced_sources.update(sources)

FOR EACH connection IN published_connections:
    brief_metadata = GET_METADATA(connection.brief_path)
    sources = brief_metadata.get("context_sources", [])
    all_referenced_sources.update(sources)

LOG INFO: "Publishing {len(all_referenced_sources)} source documents"

# Copy each source to website
FOR EACH source_id IN all_referenced_sources:
    # Get source file path
    source_data = source_mentions.sources.get(source_id)

    IF source_data is None:
        LOG WARNING: "Source {source_id} not found in source_mentions.json"
        CONTINUE

    source_file_path = source_data.file_path

    # Check if source file exists
    IF NOT FILE_EXISTS(source_file_path):
        LOG ERROR: "Source file not found: {source_file_path}"
        CONTINUE

    # Generate website source path
    website_source_path = \\192.168.1.139\continuum\website\sources\{BASENAME(source_file_path)}

    # Check if already published
    IF FILE_EXISTS(website_source_path):
        LOG DEBUG: "Source {source_id} already on website"
        CONTINUE

    # Copy source to website
    COPY file from source_file_path to website_source_path
    LOG INFO: "Published source: {source_id} → {website_source_path}"
```

### Step 6: Update Website HTML (Optional)

**Action:** Trigger website rebuild or update navigation

```
# Check if continuum.html needs updating
html_path = \\192.168.1.139\continuum\website\continuum.html

# Option 1: Static HTML that loads JSON dynamically (no update needed)
LOG INFO: "Website uses dynamic JSON loading, no HTML update required"

# Option 2: If HTML needs timestamp update
TRY:
    html_content = READ file at html_path

    # Update "Last Updated" timestamp in HTML
    updated_html = REPLACE in html_content:
        pattern = r'Last Updated: [\d\-]+ [\d:]+'
        replacement = f'Last Updated: {current_date} {current_time}'

    WRITE updated_html to html_path
    LOG INFO: "Updated continuum.html timestamp"

CATCH Exception as e:
    LOG WARNING: "Could not update HTML: {e}"
    # Non-critical, continue
```

### Step 7: Archive Published Briefs

**Action:** Move published briefs to archive with timestamp

```
archive_timestamp = current_timestamp.replace(':', '-')  # Filesystem-safe

# Archive entity briefs
FOR EACH entity IN published_entities:
    brief_path = entity.brief_path
    entity_id = entity.entity_id

    # Create archive filename with timestamp
    archive_filename = f"{entity_id}_{archive_timestamp}.md"
    archive_path = \\192.168.1.139\continuum\archive\published\entities\{archive_filename}

    # Move brief to archive
    MOVE brief from brief_path to archive_path
    LOG INFO: "Archived entity brief: {archive_path}"

# Archive connection briefs
FOR EACH connection IN published_connections:
    brief_path = connection.brief_path
    connection_id = connection.connection_id

    # Create archive filename with timestamp
    archive_filename = f"{connection_id}_{archive_timestamp}.md"
    archive_path = \\192.168.1.139\continuum\archive\published\connections\{archive_filename}

    # Move brief to archive
    MOVE brief from brief_path to archive_path
    LOG INFO: "Archived connection brief: {archive_path}"
```

### Step 8: Clean Up Approved Directory

**Action:** Verify approved/ directories are empty

```
# Check entity approved directory
remaining_entity_files = LIST files in \\192.168.1.139\continuum\approved\entities\

IF len(remaining_entity_files) > 0:
    LOG WARNING: "{len(remaining_entity_files)} files remain in approved/entities/"
    FOR EACH file IN remaining_entity_files:
        LOG WARNING: "  Remaining file: {file}"
ELSE:
    LOG INFO: "Approved entities directory empty"

# Check connection approved directory
remaining_connection_files = LIST files in \\192.168.1.139\continuum\approved\connections\

IF len(remaining_connection_files) > 0:
    LOG WARNING: "{len(remaining_connection_files)} files remain in approved/connections/"
    FOR EACH file IN remaining_connection_files:
        LOG WARNING: "  Remaining file: {file}"
ELSE:
    LOG INFO: "Approved connections directory empty"
```

### Step 9: Generate Publication Report

**Action:** Create summary of publication activity

```
publication_report = f'''
# Publication Report - {current_date}

**Generated:** {current_timestamp}
**Stage 4 Completion Summary**

## Published Content

### Entity Briefs Published: {len(published_entities)}
{LIST published entity names}

### Connection Briefs Published: {len(published_connections)}
{LIST published connection pairs}

### Source Documents Published: {len(all_referenced_sources)}

## Website Updates

**entities.json:** Updated with {count_new_entities} new + {count_updated_entities} updated entries
**connections.json:** Updated with {count_new_connections} new + {count_updated_connections} updated entries

## Archive

All published briefs archived to:
- \\192.168.1.139\continuum\archive\published\entities\
- \\192.168.1.139\continuum\archive\published\connections\

Archive timestamp: {archive_timestamp}

## Website Status

**Live URL:** http://continuum.local/continuum.html
**Last Updated:** {current_timestamp}
**Total Entities:** {total_entity_count}
**Total Connections:** {total_connection_count}

---
*Auto-generated by Stage 4: Publication*
'''

WRITE publication_report to \\192.168.1.139\continuum\logs\publication_report_{archive_timestamp}.md

LOG INFO: "Publication report generated"
```

### Step 10: Update Processing Timestamp

**Action:** Record completion for monitoring

```
WRITE current_timestamp to \\192.168.1.139\continuum\logs\stage4_last_run.txt

LOG INFO: "Stage 4 complete. Published {total_briefs} briefs to website."
```

## 6. Decision Logic

### 6.1 Handling Duplicate Entity Entries

**Decision:** What to do when entity already exists in entities.json?

```
IF entity_id exists in entities_data.entities:

    # Compare timestamps
    existing_timestamp = existing_entry.last_updated
    new_timestamp = metadata.last_updated

    IF new_timestamp > existing_timestamp:
        # UPDATE with newer data
        UPDATE existing_entry with new values
        LOG INFO: "Updated entity entry (newer data)"

    ELSE IF new_timestamp == existing_timestamp:
        # Same version, merge data
        MERGE new data into existing (keep higher mention counts, etc.)
        LOG INFO: "Merged entity entry (same timestamp)"

    ELSE:
        # Older data trying to overwrite newer
        LOG WARNING: "Approved brief has older timestamp than published version"
        LOG WARNING: "Existing: {existing_timestamp}, New: {new_timestamp}"

        # Still update (human approved this version)
        UPDATE existing_entry with new values
        LOG INFO: "Updated entity entry (human override)"
```

### 6.2 Missing Source File Handling

**Decision:** What to do when source PDF is missing?

```
IF source_file NOT found:

    LOG ERROR: "Source file missing: {source_file_path}"

    # Don't halt publication of brief
    # Brief can be published without source PDF

    # Add to error log
    ADD to publication_errors: {
        "type": "missing_source",
        "source_id": source_id,
        "file_path": source_file_path,
        "referenced_in": [list of briefs referencing this source]
    }

    # Create placeholder in website/sources/
    placeholder_content = f"Source document {source_id} not available"
    WRITE placeholder to website\sources\{source_id}_MISSING.txt

    LOG WARNING: "Created placeholder for missing source {source_id}"

    CONTINUE processing other sources
```

### 6.3 Invalid JSON Structure

**Decision:** What to do if entities.json or connections.json is corrupted?

```
TRY:
    entities_data = PARSE_JSON(entities.json)

CATCH JSONDecodeError:
    LOG CRITICAL: "entities.json is corrupted"

    # Attempt recovery from backup
    backup_path = GET_LATEST_BACKUP("entities.json")

    IF backup_path exists:
        LOG INFO: "Restoring entities.json from backup: {backup_path}"
        COPY backup to entities.json
        entities_data = PARSE_JSON(entities.json)

    ELSE:
        LOG CRITICAL: "No backup available for entities.json"

        # Create new structure from scratch
        LOG INFO: "Rebuilding entities.json from existing briefs"
        entities_data = REBUILD_ENTITIES_JSON_FROM_BRIEFS()

    # Retry publication
    RETRY publication process
```

### 6.4 Website Directory Not Accessible

**Decision:** What to do if cannot write to website/ directory?

```
TRY:
    COPY brief to website_path

CATCH PermissionError OR IOError:
    LOG CRITICAL: "Cannot write to website directory: {website_path}"

    # Try alternate publication location
    alternate_path = \\192.168.1.139\continuum\website_staging\

    IF alternate_path is accessible:
        LOG INFO: "Publishing to staging location: {alternate_path}"
        COPY brief to alternate_path
        # Alert operator to move from staging to live
        SEND alert: "Published to staging, manual move required"

    ELSE:
        LOG CRITICAL: "No accessible publication location"
        # Move brief back to approved/ for retry
        LOG INFO: "Moving brief back to approved/ for later retry"
        # Don't archive (publication incomplete)

        SEND URGENT alert: "Publication failed - website directory inaccessible"
```

## 7. Outputs

### Primary Outputs

**Updated Website Data:**
- `\\192.168.1.139\continuum\website\data\entities.json` (new/updated entity entries)
- `\\192.168.1.139\continuum\website\data\connections.json` (new/updated connection entries)

**Published Briefs:**
- `\\192.168.1.139\continuum\website\briefs\entity\*.md`
- `\\192.168.1.139\continuum\website\briefs\connections\*.md`

**Published Sources:**
- `\\192.168.1.139\continuum\website\sources\*.pdf`

**Archived Content:**
- `\\192.168.1.139\continuum\archive\published\entities\*_{timestamp}.md`
- `\\192.168.1.139\continuum\archive\published\connections\*_{timestamp}.md`

### Secondary Outputs

**Publication Report:**
`\\192.168.1.139\continuum\logs\publication_report_{timestamp}.md`
- Summary of what was published
- Website statistics
- Archive locations

**Processing Timestamp:**
`\\192.168.1.139\continuum\logs\stage4_last_run.txt`

### Log Outputs

**Processing Log:**
`\\192.168.1.139\continuum\logs\stage4_publication.log`

Example:
```
2025-12-25T12:00:00Z | INFO | Stage 4 triggered - files detected in approved/
2025-12-25T12:00:01Z | INFO | Found 5 approved entity briefs
2025-12-25T12:00:01Z | INFO | Found 3 approved connection briefs
2025-12-25T12:00:05Z | INFO | Publishing entity brief: analytical_brief_John_Doe.md
2025-12-25T12:00:06Z | INFO | Added new entity entry: John Doe
2025-12-25T12:00:07Z | INFO | Copied brief to website
2025-12-25T12:00:30Z | INFO | Updated website entities.json
2025-12-25T12:00:45Z | INFO | Updated website connections.json
2025-12-25T12:00:50Z | INFO | Publishing 15 source documents
2025-12-25T12:01:10Z | INFO | Archived entity brief
2025-12-25T12:01:30Z | INFO | Publication report generated
2025-12-25T12:01:30Z | INFO | Stage 4 complete. Published 8 briefs to website.
```

## 8. Success Criteria

### Mandatory Criteria

1. **All Briefs Published:** Every approved brief copied to website/briefs/
2. **Website Data Updated:** entities.json and connections.json contain all published entries
3. **Briefs Archived:** All published briefs moved to archive/ with timestamp
4. **Approved Directory Empty:** No briefs remain in approved/ directories
5. **No Data Corruption:** All JSON files remain valid after updates

### Quality Criteria

1. **Source Availability:** > 95% of referenced sources published to website
2. **Data Consistency:** Entity/connection counts match between briefs and JSON
3. **Archive Integrity:** All archived briefs readable and complete
4. **Website Accessibility:** Published content accessible via web interface

### Validation Commands

```bash
# Verify website JSON validity
python -m json.tool \\192.168.1.139\continuum\website\data\entities.json > /dev/null

# Count published briefs
ls \\192.168.1.139\continuum\website\briefs\entity\ | wc -l
ls \\192.168.1.139\continuum\website\briefs\connections\ | wc -l

# Verify approved directories empty
ls \\192.168.1.139\continuum\approved\entities\
ls \\192.168.1.139\continuum\approved\connections\

# Check archive created
ls -lh \\192.168.1.139\continuum\archive\published\entities\ | tail -5

# Test website accessibility
curl http://continuum.local/briefs/entity/analytical_brief_John_Doe.md
```

## 9. Error Handling

### 9.1 Brief Validation Failure

**Error:** Approved brief has invalid structure

```
# Handled in Step 2

IF validation fails:
    MOVE brief BACK TO pending_approval/

    CREATE error note file: {brief_filename}.ERROR
    WRITE error details to error note

    LOG ERROR: "Brief validation failed, returned to pending_approval"

    # Alert human reviewer
    ADD to REVIEW_LOG.md:
    "ERROR: {brief_filename} failed validation - {error_details}"

    CONTINUE with other briefs (don't halt entire publication)
```

### 9.2 Website Data Corruption

**Error:** entities.json or connections.json is corrupted and no backup available

```
IF JSON corrupted AND no backup:

    LOG CRITICAL: "Website data corrupted, rebuilding from source"

    # Rebuild from all published briefs
    entities_data = {
        "_schema_version": "1.0",
        "_last_updated": current_timestamp,
        "entities": []
    }

    # Scan website/briefs/entity/ directory
    FOR EACH brief IN website\briefs\entity\:
        metadata = PARSE_YAML_FRONTMATTER(brief)
        entity_entry = BUILD_ENTITY_ENTRY_FROM_METADATA(metadata)
        entities_data.entities.append(entity_entry)

    WRITE entities_data to website\data\entities.json

    LOG INFO: "Rebuilt entities.json from {count} existing briefs"

    # Similar process for connections.json
```

### 9.3 Disk Full During Publication

**Error:** Insufficient disk space to copy briefs

```
CATCH DiskFullError:
    LOG CRITICAL: "Disk full - cannot complete publication"

    # Halt publication immediately
    WRITE halt signal to \\192.168.1.139\continuum\PUBLICATION_HALTED

    # Don't move briefs out of approved/ (incomplete publication)

    SEND URGENT alert: "Publication halted - disk full"

    # Log partial completion
    LOG INFO: "Published {completed_count} of {total_count} briefs before halt"

    HALT processing

# Operator must:
# 1. Free disk space
# 2. Remove PUBLICATION_HALTED file
# 3. Re-trigger Stage 4
```

### 9.4 Archive Move Failure

**Error:** Cannot move brief to archive

```
TRY:
    MOVE brief to archive_path

CATCH Exception as e:
    LOG ERROR: "Archive move failed: {e}"

    # Copy instead of move
    TRY:
        COPY brief to archive_path
        DELETE brief from approved/

        LOG INFO: "Archived via copy (move failed)"

    CATCH Exception as e2:
        LOG CRITICAL: "Archive copy also failed: {e2}"

        # Leave brief in approved/ with .PUBLISHED marker
        CREATE file: {brief_path}.PUBLISHED with timestamp

        LOG WARNING: "Brief published but not archived, marked with .PUBLISHED"

        # Continue (publication successful, archival can be fixed later)
```

## 10. Next Stage

**End of Pipeline** - This is the final autonomous stage.

**Post-Publication:**
1. Website is live with new content
2. Approved briefs are archived
3. Pipeline awaits new source documents to begin cycle again

**Return to Stage 1:**
- When new document uploaded to Paperless
- Webhook triggers Stage 1 (Source Ingestion)
- Cycle repeats

**Manual Operations:**
- Monitor website for accuracy
- Respond to user feedback
- Perform periodic data quality audits
- Review archived content for patterns

---

## Appendix A: Website JSON Schema Validation

### entities.json Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["_schema_version", "_last_updated", "entities"],
  "properties": {
    "_schema_version": {"type": "string"},
    "_last_updated": {"type": "string", "format": "date-time"},
    "entities": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "type", "brief_path"],
        "properties": {
          "id": {"type": "string"},
          "name": {"type": "string"},
          "type": {"type": "string"},
          "brief_path": {"type": "string"},
          "mention_count": {"type": "integer"},
          "connection_count": {"type": "integer"},
          "last_updated": {"type": "string", "format": "date-time"},
          "preview": {"type": "string"},
          "tags": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

### connections.json Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["_schema_version", "_last_updated", "connections"],
  "properties": {
    "_schema_version": {"type": "string"},
    "_last_updated": {"type": "string", "format": "date-time"},
    "connections": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "entity1", "entity2", "brief_path"],
        "properties": {
          "id": {"type": "string"},
          "entity1": {"type": "string"},
          "entity2": {"type": "string"},
          "brief_path": {"type": "string"},
          "relationship_type": {"type": "string"},
          "strength": {"type": "number", "minimum": 0, "maximum": 1},
          "last_updated": {"type": "string", "format": "date-time"},
          "preview": {"type": "string"}
        }
      }
    }
  }
}
```

## Appendix B: Archive Naming Convention

**Format:** `{entity_id}_{timestamp}.md`

**Examples:**
- `john_doe_2025-12-25T12-00-00Z.md`
- `acme_corporation_john_doe_2025-12-25T12-01-30Z.md`

**Benefits:**
- Sortable by entity then by time
- Easy to find all versions of specific entity/connection
- Filesystem-safe (no colons in timestamp)

## Appendix C: Rebuilding Website Data from Scratch

If both entities.json and connections.json are lost/corrupted:

```bash
# Run rebuild script
python \\192.168.1.139\continuum\scripts\rebuild_website_data.py

# Script will:
# 1. Scan website/briefs/ for all published briefs
# 2. Extract metadata from each brief
# 3. Rebuild entities.json and connections.json
# 4. Validate against schema
# 5. Create backup of rebuilt files
```

---

**Document Control**
- **Related SOPs:** SOP-003 (Brief Generation), SOP-000 (Master Pipeline)
- **Next Review Date:** 2026-03-25
- **Change Authority:** Pipeline Administrator
