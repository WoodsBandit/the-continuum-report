# SOP-002: Context Extraction

**Document Version:** 1.0
**Last Updated:** 2025-12-25
**Pipeline Stage:** 2 of 4
**Trigger:** Change to entity_registry.json
**Execution Mode:** Autonomous (Claude Code)

---

## 1. Purpose

Extract contextual information around entity mentions to identify relationships, co-occurrences, and interaction patterns. This stage bridges raw entity extraction with analytical brief generation by capturing the semantic context in which entities appear together.

## 2. Trigger Condition

**Primary Trigger:** Modification timestamp change on `entity_registry.json`
**Monitoring Method:** File system watch or periodic polling (every 30 seconds)
**Trigger Script:**
```python
# Watch entity_registry.json for changes
import os
import time

registry_path = r"project_root/indexes\entity_registry.json"
last_modified = os.path.getmtime(registry_path)

while True:
    current_modified = os.path.getmtime(registry_path)
    if current_modified > last_modified:
        # File changed - trigger Stage 2
        execute_stage2()
        last_modified = current_modified
    time.sleep(30)
```

**Fallback Trigger:** Manual execution via command line with optional entity filter

## 3. Prerequisites

### Required Files Must Exist
- `project_root/indexes\entity_registry.json` (recently updated by Stage 1)
- `project_root/indexes\source_mentions.json`
- `project_root/indexes\co_occurrence.json`
- `project_root/indexes\connection_contexts.json`

### Required Directories Must Exist
- `project_root/sources\paperless_mirror\` (containing source documents)

### System Requirements
- Claude Code must have read access to source documents
- Claude Code must have read/write access to index files
- Sufficient memory to process context windows (estimate 10MB per 100 entities)

## 4. Inputs

### Primary Input
**Entity Registry:** `project_root/indexes\entity_registry.json`
- Focus on entities with `last_seen` == today (newly mentioned in Stage 1)
- OR entities in new sources from last Stage 1 run

### Reference Inputs

**Source Mentions:** `project_root/indexes\source_mentions.json`
- Maps entities to specific sources where they appear
- Provides source file paths for context extraction

**Co-Occurrence Index (Existing):** `project_root/indexes\co_occurrence.json`
```json
{
  "_schema_version": "1.0",
  "_last_updated": "2025-12-25T10:00:00Z",
  "pairs": {
    "John Doe|Acme Corporation": {
      "entity1": "John Doe",
      "entity2": "Acme Corporation",
      "co_mention_count": 5,
      "sources": ["src_000042", "src_000103", "src_000245"],
      "first_co_mention": "2025-01-15",
      "last_co_mention": "2025-12-20"
    }
  }
}
```

**Connection Contexts (Existing):** `project_root/indexes\connection_contexts.json`
```json
{
  "_schema_version": "1.0",
  "_last_updated": "2025-12-25T10:00:00Z",
  "connections": {
    "John Doe|Acme Corporation": {
      "entity1": "John Doe",
      "entity2": "Acme Corporation",
      "contexts": [
        {
          "source_id": "src_000042",
          "snippet": "...John Doe, representing Acme Corporation, testified before the committee regarding the proposed merger. The CEO stated...",
          "context_type": "representation",
          "date": "2025-01-15",
          "entities_in_context": ["John Doe", "Acme Corporation", "committee"],
          "action_verbs": ["representing", "testified", "stated"],
          "relevance_score": 0.92
        }
      ],
      "last_updated": "2025-12-20T15:30:00Z"
    }
  }
}
```

## 5. Process Steps

### Step 1: Identify Changed Entities

**Action:** Determine which entities have new source mentions since last run

```
READ: project_root/indexes\entity_registry.json
READ: project_root/indexes\connection_contexts.json

# Get last processing timestamp
last_run_timestamp = connection_contexts._last_updated

# Identify entities with updates
changed_entities = []

FOR EACH entity IN entity_registry.entities:
    IF entity.last_seen > last_run_timestamp:
        # Entity has new mentions
        changed_entities.append(entity.name)
        LOG INFO: "Entity '{entity.name}' has new mentions"

    ELSE:
        # Check if any of entity's sources are new
        FOR EACH source_id IN entity.sources:
            source_processed_date = GET from source_mentions.sources[source_id].processed_date

            IF source_processed_date > last_run_timestamp:
                # Entity appears in newly processed source
                changed_entities.append(entity.name)
                LOG INFO: "Entity '{entity.name}' in new source {source_id}"
                BREAK

LOG INFO: "Identified {len(changed_entities)} entities with new mentions"

IF len(changed_entities) == 0:
    LOG INFO: "No entities to process, Stage 2 complete"
    HALT processing (success)
```

### Step 2: Build Entity-Source Mapping

**Action:** Create lookup table of which sources to examine for each entity

```
entity_source_map = {}

FOR EACH entity_name IN changed_entities:
    entity_data = entity_registry.entities[entity_name]

    # Get ALL sources mentioning this entity
    # (not just new ones - need full context for co-occurrence)
    entity_source_map[entity_name] = entity_data.sources

    LOG INFO: "Entity '{entity_name}' appears in {len(entity_data.sources)} sources"

EXAMPLE:
{
  "John Doe": ["src_000042", "src_000103", "src_000245"],
  "Jane Smith": ["src_000103", "src_000201"]
}
```

### Step 3: Extract Context Windows

**Action:** For each entity, read ±500 characters around each mention in each source

```
entity_contexts = {}  # Will store all context windows per entity

FOR EACH entity_name IN changed_entities:
    entity_contexts[entity_name] = []

    FOR EACH source_id IN entity_source_map[entity_name]:
        # Get source file path
        source_data = source_mentions.sources[source_id]
        source_file_path = source_data.file_path

        TRY:
            # Read source document
            source_text = READ file at source_file_path

        CATCH FileNotFoundError:
            LOG ERROR: "Source file not found: {source_file_path}"
            CONTINUE to next source

        # Find all mentions of entity in source text
        entity_aliases = entity_registry.entities[entity_name].aliases
        search_terms = [entity_name] + entity_aliases

        mentions = []
        FOR EACH term IN search_terms:
            # Case-insensitive search
            positions = FIND_ALL_POSITIONS(term in source_text, ignore_case=True)
            mentions.extend(positions)

        # Remove duplicates and sort
        mentions = UNIQUE_SORTED(mentions)

        LOG INFO: "Found {len(mentions)} mentions of '{entity_name}' in {source_id}"

        # Extract context window for each mention
        FOR EACH position IN mentions:
            # Get ±500 chars (but don't exceed document boundaries)
            start = max(0, position - 500)
            end = min(len(source_text), position + len(entity_name) + 500)

            context_snippet = source_text[start:end]

            # Clean up snippet (remove excessive whitespace, newlines)
            context_snippet = CLEAN_TEXT(context_snippet)

            # Store context
            entity_contexts[entity_name].append({
                "source_id": source_id,
                "position": position,
                "snippet": context_snippet,
                "mention_term": term
            })

LOG INFO: "Extracted context windows for {len(changed_entities)} entities"
```

**Text Cleaning Function:**
```python
def CLEAN_TEXT(text):
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    # Trim leading/trailing whitespace
    text = text.strip()
    # Ensure snippet doesn't start/end mid-word
    if not text[0].isupper() and ' ' in text:
        text = text.split(' ', 1)[1]  # Remove partial first word
    if not text[-1] in '.!?':
        text = ' '.join(text.split(' ')[:-1])  # Remove partial last word
    return text
```

### Step 4: Identify Co-Occurring Entities

**Action:** Find other entities mentioned within each context window

```
co_occurrences = {}  # Will store entity pairs and their co-mention details

FOR EACH entity_name IN changed_entities:
    FOR EACH context IN entity_contexts[entity_name]:
        snippet = context.snippet
        source_id = context.source_id

        # Get list of ALL entities to check
        all_entities = entity_registry.entities.keys()

        # Find which other entities appear in this context
        for other_entity IN all_entities:
            IF other_entity == entity_name:
                CONTINUE  # Skip self

            # Check if other entity appears in snippet
            other_aliases = entity_registry.entities[other_entity].aliases
            search_terms = [other_entity] + other_aliases

            found = False
            for term IN search_terms:
                IF term IN snippet (case-insensitive):
                    found = True
                    BREAK

            IF found:
                # Co-occurrence detected!
                # Create canonical pair key (alphabetical order)
                pair_key = CANONICAL_PAIR_KEY(entity_name, other_entity)

                # Initialize pair if not exists
                IF pair_key NOT IN co_occurrences:
                    co_occurrences[pair_key] = {
                        "entity1": MIN(entity_name, other_entity),
                        "entity2": MAX(entity_name, other_entity),
                        "contexts": [],
                        "sources": set()
                    }

                # Add this context
                co_occurrences[pair_key]["contexts"].append({
                    "source_id": source_id,
                    "snippet": snippet,
                    "primary_entity": entity_name
                })

                co_occurrences[pair_key]["sources"].add(source_id)

                LOG DEBUG: "Co-occurrence: {entity_name} + {other_entity} in {source_id}"

LOG INFO: "Identified {len(co_occurrences)} entity pair co-occurrences"
```

**Canonical Pair Key Function:**
```python
def CANONICAL_PAIR_KEY(entity1, entity2):
    # Always alphabetical order, pipe-separated
    sorted_pair = sorted([entity1, entity2])
    return f"{sorted_pair[0]}|{sorted_pair[1]}"
```

### Step 5: Extract Relationship Signals

**Action:** Analyze context snippets for relationship indicators

```
FOR EACH pair_key IN co_occurrences:
    pair_data = co_occurrences[pair_key]

    FOR EACH context IN pair_data["contexts"]:
        snippet = context["snippet"]

        # Analyze snippet for relationship signals
        analysis = ANALYZE_RELATIONSHIP_CONTEXT(snippet, pair_data.entity1, pair_data.entity2)

        # Add analysis to context
        context["context_type"] = analysis.context_type
        context["action_verbs"] = analysis.action_verbs
        context["entities_in_context"] = analysis.all_entities
        context["relevance_score"] = analysis.relevance_score
        context["date_mentions"] = analysis.dates
```

**Relationship Context Analysis Function:**
```
FUNCTION ANALYZE_RELATIONSHIP_CONTEXT(snippet, entity1, entity2):
    # Use Claude to analyze relationship signals

    prompt = f'''
Analyze this text snippet for relationship signals between "{entity1}" and "{entity2}".

Text:
---
{snippet}
---

Provide:
1. context_type: The nature of the relationship (e.g., "employment", "representation", "transaction", "association", "opposition", "family", "legal_matter", "collaboration")
2. action_verbs: List of verbs indicating interaction (e.g., ["testified", "represented", "negotiated"])
3. all_entities: All entities mentioned in snippet (including entity1 and entity2)
4. relevance_score: How substantive is this connection? (0.0-1.0)
   - 0.9-1.0: Direct interaction, strong evidence
   - 0.7-0.89: Clear association, moderate evidence
   - 0.5-0.69: Weak association, minimal evidence
   - Below 0.5: Likely coincidental co-mention
5. dates: Any dates or time periods mentioned

Return JSON:
{
  "context_type": "employment",
  "action_verbs": ["worked", "employed"],
  "all_entities": ["John Doe", "Acme Corp", "New York"],
  "relevance_score": 0.85,
  "dates": ["2023-01-15"]
}
'''

    result = CALL_CLAUDE(prompt)
    RETURN result
```

### Step 6: Update Co-Occurrence Index

**Action:** Merge new co-occurrence data with existing index

```
READ: project_root/indexes\co_occurrence.json
PARSE as co_occurrence_index

FOR EACH pair_key IN co_occurrences:
    new_pair = co_occurrences[pair_key]

    IF pair_key IN co_occurrence_index.pairs:
        # UPDATE existing pair
        existing_pair = co_occurrence_index.pairs[pair_key]

        # Merge sources
        existing_sources = set(existing_pair.sources)
        new_sources = new_pair["sources"]
        merged_sources = list(existing_sources.union(new_sources))

        existing_pair.sources = merged_sources
        existing_pair.co_mention_count = len(merged_sources)
        existing_pair.last_co_mention = current_date

        # NOTE: No strength scoring - binary model
        # Connection exists (in a brief with quote+source+summary) or it doesn't

        LOG INFO: "Updated co-occurrence: {pair_key} (now {len(merged_sources)} sources)"

    ELSE:
        # CREATE new pair
        # NOTE: No strength scoring - binary model
        co_occurrence_index.pairs[pair_key] = {
            "entity1": new_pair["entity1"],
            "entity2": new_pair["entity2"],
            "co_mention_count": len(new_pair["sources"]),
            "sources": list(new_pair["sources"]),
            "first_co_mention": current_date,
            "last_co_mention": current_date
        }

        LOG INFO: "Created new co-occurrence: {pair_key}"

# Update metadata
co_occurrence_index._last_updated = current_timestamp

# Write updated index
WRITE co_occurrence_index to project_root/indexes\co_occurrence.json
LOG INFO: "Co-occurrence index updated"
```

**Note on Relationship Strength (DEPRECATED):**

As of 2026-01, The Continuum Report uses a **binary connection model**:
- A connection EXISTS (documented with quote + source + summary in a connection brief)
- Or it DOESN'T EXIST (no connection brief)

No subjective strength scoring. The source documents speak for themselves.

### Step 7: Update Connection Contexts

**Action:** Add new context snippets to connection_contexts.json

```
READ: project_root/indexes\connection_contexts.json
PARSE as connection_contexts

FOR EACH pair_key IN co_occurrences:
    pair_contexts = co_occurrences[pair_key]["contexts"]

    IF pair_key IN connection_contexts.connections:
        # UPDATE existing connection
        existing_connection = connection_contexts.connections[pair_key]

        # Get existing context source IDs (to avoid duplicates)
        existing_source_ids = set([ctx.source_id for ctx in existing_connection.contexts])

        # Add new contexts
        new_contexts_added = 0
        FOR EACH context IN pair_contexts:
            # Only add if relevance_score meets threshold
            IF context.relevance_score >= 0.5:
                # Check if we already have context from this source
                IF context.source_id NOT IN existing_source_ids:
                    existing_connection.contexts.append({
                        "source_id": context.source_id,
                        "snippet": context.snippet,
                        "context_type": context.context_type,
                        "date": source_mentions.sources[context.source_id].date,
                        "entities_in_context": context.entities_in_context,
                        "action_verbs": context.action_verbs,
                        "relevance_score": context.relevance_score
                    })
                    new_contexts_added += 1
                ELSE:
                    LOG DEBUG: "Skipping duplicate context from {context.source_id}"
            ELSE:
                LOG DEBUG: "Skipping low relevance context (score: {context.relevance_score})"

        existing_connection.last_updated = current_timestamp

        LOG INFO: "Updated connection contexts for {pair_key}: added {new_contexts_added} new contexts"

    ELSE:
        # CREATE new connection
        # Filter contexts by relevance
        high_relevance_contexts = [
            ctx for ctx in pair_contexts if ctx.relevance_score >= 0.5
        ]

        IF len(high_relevance_contexts) > 0:
            connection_contexts.connections[pair_key] = {
                "entity1": co_occurrences[pair_key]["entity1"],
                "entity2": co_occurrences[pair_key]["entity2"],
                "contexts": [
                    {
                        "source_id": ctx.source_id,
                        "snippet": ctx.snippet,
                        "context_type": ctx.context_type,
                        "date": source_mentions.sources[ctx.source_id].date,
                        "entities_in_context": ctx.entities_in_context,
                        "action_verbs": ctx.action_verbs,
                        "relevance_score": ctx.relevance_score
                    }
                    for ctx in high_relevance_contexts
                ],
                "last_updated": current_timestamp
            }

            LOG INFO: "Created new connection contexts for {pair_key}: {len(high_relevance_contexts)} contexts"
        ELSE:
            LOG INFO: "Skipping {pair_key}: no high-relevance contexts found"

# Update metadata
connection_contexts._last_updated = current_timestamp

# Write updated contexts
WRITE connection_contexts to project_root/indexes\connection_contexts.json
LOG INFO: "Connection contexts index updated"
```

### Step 8: Generate Processing Summary

**Action:** Create summary of what was processed

```
summary = {
    "processing_date": current_timestamp,
    "entities_processed": len(changed_entities),
    "entity_names": changed_entities,
    "co_occurrences_found": len(co_occurrences),
    "new_connections": count of new connections created,
    "updated_connections": count of connections updated,
    "context_snippets_added": total count of new context snippets
}

WRITE summary to project_root/logs\stage2_summary_{timestamp}.json

LOG INFO: "Stage 2 complete: Processed {len(changed_entities)} entities, found {len(co_occurrences)} co-occurrences"
```

### Step 9: Trigger Next Stage

**Action:** Signal Stage 3 (Brief Generation) to begin

```
# Stage 3 monitors connection_contexts.json for changes
# Since we just updated connection_contexts.json in Step 7, Stage 3 will auto-trigger

LOG INFO: "Stage 2 complete. Stage 3 will auto-trigger on connection_contexts.json change."

# Optional: Write trigger file for explicit signaling
trigger_file = project_root/triggers\stage3_trigger.json
WRITE {
    "triggered_by": "stage2",
    "timestamp": current_timestamp,
    "entities_processed": changed_entities,
    "new_connections": list of new connection pair_keys,
    "updated_connections": list of updated connection pair_keys
} to trigger_file
```

## 6. Decision Logic

### 6.1 Context Relevance Filtering

**Scenario:** Entity pair appears in same document but no real relationship

```
EXAMPLE: Both "John Doe" and "Jane Smith" appear in author byline of report

Context snippet: "Report prepared by John Doe and Jane Smith, Research Analysts"

Analysis result:
{
  "context_type": "authorship",
  "relevance_score": 0.3
}

DECISION:
IF relevance_score < 0.5:
    LOG DEBUG: "Low relevance co-mention, not adding to connection_contexts"
    # Still add to co_occurrence.json (increment count)
    # But don't create context snippet
    SKIP context snippet creation
```

### 6.2 Handling Missing Source Files

**Scenario:** Source file referenced in source_mentions.json doesn't exist

```
source_file_path = "project_root/sources\paperless_mirror\doc_000042.pdf"

TRY:
    source_text = READ file at source_file_path

CATCH FileNotFoundError:
    LOG ERROR: "Source file missing: {source_file_path} (referenced by src_000042)"

    # Don't halt entire stage for one missing file
    # Skip this source for all entities
    FOR EACH entity referencing this source:
        LOG WARNING: "Skipping context extraction for {entity} from {source_id}"

    # Record the error
    ADD to error_log: {
        "timestamp": current_timestamp,
        "error_type": "missing_source_file",
        "source_id": "src_000042",
        "file_path": source_file_path,
        "affected_entities": list of entities
    }

    # Continue processing other sources
    CONTINUE to next source
```

### 6.3 Duplicate Context Detection

**Scenario:** Same entity pair co-occurs multiple times in same source

```
Entity pair: "John Doe|Acme Corporation"
Source: src_000042

Found 5 mentions of pair in same source document

DECISION:
# Don't create 5 separate context snippets
# Instead, merge into representative samples

IF mentions > 3:
    # Take first mention, middle mention, last mention
    representative_contexts = [
        contexts[0],
        contexts[len(contexts) // 2],
        contexts[-1]
    ]

    LOG INFO: "Multiple co-mentions in {source_id}, using 3 representative contexts"

ELSE:
    # Use all contexts
    representative_contexts = contexts
```

### 6.4 Context Window Overlap

**Scenario:** Entity A at position 100, Entity B at position 200 (within ±500 window)

```
IF windows overlap:
    # Merge into single context covering both
    merged_window_start = min(pos_A - 500, pos_B - 500)
    merged_window_end = max(pos_A + 500, pos_B + 500)

    context_snippet = source_text[merged_window_start:merged_window_end]

    LOG DEBUG: "Merged overlapping context windows for {entity1} and {entity2}"
```

## 7. Outputs

### Primary Outputs

**Updated Co-Occurrence Index:**
`project_root/indexes\co_occurrence.json`
- New entity pairs added
- Existing pairs updated with new sources
- Co-mention counts updated

**Updated Connection Contexts:**
`project_root/indexes\connection_contexts.json`
- New connection entries created
- Existing connections updated with new context snippets
- Relationship type classifications added
- Relevance scores calculated

### Secondary Outputs

**Processing Summary:**
`project_root/logs\stage2_summary_{timestamp}.json`
- List of entities processed
- Count of co-occurrences found
- Count of new vs updated connections
- Processing statistics

**Stage 3 Trigger:**
`project_root/triggers\stage3_trigger.json`
- Signal for Stage 3 to begin
- List of affected connections

### Log Outputs

**Processing Log:**
`project_root/logs\stage2_context_extraction.log`

Example:
```
2025-12-25T10:16:00Z | INFO | Stage 2 triggered by entity_registry.json change
2025-12-25T10:16:01Z | INFO | Identified 23 entities with new mentions
2025-12-25T10:16:02Z | INFO | Found 5 mentions of 'John Doe' in src_012345
2025-12-25T10:16:15Z | INFO | Extracted context windows for 23 entities
2025-12-25T10:16:20Z | DEBUG | Co-occurrence: John Doe + Acme Corporation in src_012345
2025-12-25T10:16:45Z | INFO | Identified 12 entity pair co-occurrences
2025-12-25T10:16:50Z | INFO | Updated co-occurrence: John Doe|Acme Corporation (now 6 sources)
2025-12-25T10:16:51Z | INFO | Updated connection contexts for John Doe|Acme Corporation: added 1 new context
2025-12-25T10:16:55Z | INFO | Co-occurrence index updated
2025-12-25T10:16:56Z | INFO | Connection contexts index updated
2025-12-25T10:16:56Z | INFO | Stage 2 complete. Stage 3 will auto-trigger.
```

## 8. Success Criteria

### Mandatory Criteria

1. **Entities Processed:** All changed entities identified and processed
2. **Contexts Extracted:** Context windows extracted for all entity mentions
3. **Co-Occurrences Identified:** Entity pairs with overlap detected
4. **Indexes Updated:** Both co_occurrence.json and connection_contexts.json updated
5. **No Data Corruption:** All JSON files remain valid

### Quality Criteria

1. **Context Quality:** Average relevance_score > 0.6 for added contexts
2. **Coverage:** At least 80% of changed entities have co-occurrences found
3. **No Excessive Contexts:** No connection has > 100 context snippets (indicates noise)
4. **Relationship Diversity:** Multiple context_types identified (not all "association")

### Validation Commands

```bash
# Verify JSON validity
python -m json.tool project_root/indexes\co_occurrence.json > /dev/null

# Check update timestamp
jq '._last_updated' project_root/indexes\connection_contexts.json

# Count new connections
jq '.connections | length' project_root/indexes\connection_contexts.json

# Check average relevance score
jq '[.connections[].contexts[].relevance_score] | add / length' project_root/indexes\connection_contexts.json
```

## 9. Error Handling

### 9.1 Context Analysis Failure

**Error:** Claude API fails during relationship analysis

```
CATCH APIError during ANALYZE_RELATIONSHIP_CONTEXT:
    LOG ERROR: "Relationship analysis failed for context: {error}"

    # Use fallback analysis
    context["context_type"] = "association"  # Generic type
    context["action_verbs"] = []  # Empty list
    context["entities_in_context"] = [entity1, entity2]  # Minimum
    context["relevance_score"] = 0.5  # Neutral score
    context["date_mentions"] = []

    LOG WARNING: "Using fallback analysis for context from {source_id}"

    # Continue processing (don't fail entire stage)
    CONTINUE
```

### 9.2 Excessive Co-Occurrences

**Error:** Entity pair has > 100 co-mentions (likely common terms)

```
IF co_mention_count > 100:
    LOG WARNING: "Excessive co-mentions for {pair_key}: {co_mention_count}"
    LOG WARNING: "This may indicate overly broad entity matching"

    # Still process, but flag for review
    ADD to review_queue: {
        "issue": "excessive_co_mentions",
        "pair": pair_key,
        "count": co_mention_count
    }

    # Limit contexts to most relevant (top 20 by relevance_score)
    contexts_sorted = SORT contexts by relevance_score DESC
    contexts_to_keep = contexts_sorted[:20]

    LOG INFO: "Limiting {pair_key} to top 20 contexts by relevance"
```

### 9.3 JSON Write Failure

**Error:** Cannot write updated index file

```
CATCH IOError OR PermissionError during WRITE:
    LOG CRITICAL: "Cannot write to {file_path}: {error}"

    # Save to backup location
    backup_path = "project_root/backups\emergency\{filename}_{timestamp}"
    WRITE data to backup_path
    LOG INFO: "Saved to emergency backup: {backup_path}"

    # Alert operator
    SEND alert: "Stage 2 cannot write to primary index location"

    # Retry once after 10 seconds
    WAIT 10 seconds
    RETRY write to primary location

    IF retry fails:
        LOG CRITICAL: "Write retry failed, data in emergency backup only"
        HALT processing
```

## 10. Next Stage

**Stage 3: Brief Generation (SOP-003)**

**Trigger Condition:** Modification of `connection_contexts.json`

**What Stage 3 Will Do:**
- Check for existing entity briefs (CREATE vs UPDATE decision)
- Check for existing connection briefs (CREATE vs UPDATE decision)
- Generate/update analytical briefs using templates
- Run legal-auditor agent for compliance checks
- Output briefs to pending_approval/ for human review

**Handoff Requirements:**
- connection_contexts.json must be valid JSON
- co_occurrence.json must be valid JSON
- All referenced sources must be accessible
- entity_registry.json must be current

**Timing:** Stage 3 should begin within 30 seconds of Stage 2 completion

---

## Appendix A: Context Type Classifications

| Context Type | Description | Example |
|-------------|-------------|---------|
| employment | Work relationship | "John worked for Acme Corp as CFO" |
| representation | Legal/official representation | "Attorney Jane represented client John" |
| transaction | Business transaction | "Acme purchased property from John" |
| association | General association | "John and Jane attended the conference" |
| opposition | Adversarial relationship | "John sued Acme Corporation" |
| family | Family relationship | "John is married to Jane" |
| legal_matter | Involvement in legal case | "Both named in case #12345" |
| collaboration | Working together | "John and Jane co-authored the report" |
| ownership | Ownership relationship | "John owns 40% of Acme Corp" |
| location | Geographic connection | "John resides in New York" |

## Appendix B: Relevance Score Guidelines

**0.9 - 1.0 (Very High):**
- Direct quotes or statements
- Specific named actions
- Documented transactions
- Official roles/titles

**0.7 - 0.89 (High):**
- Clear associations
- Indirect but specific connections
- Timeline events
- Multiple entity interactions

**0.5 - 0.69 (Moderate):**
- General mentions
- Weak associations
- Contextual proximity
- Single mentions

**Below 0.5 (Low - Exclude):**
- Coincidental co-mention
- No clear relationship
- Both in metadata only (e.g., tags)
- No substantive context

---

**Document Control**
- **Related SOPs:** SOP-001 (Source Ingestion), SOP-003 (Brief Generation)
- **Next Review Date:** 2026-03-25
- **Change Authority:** Pipeline Administrator
