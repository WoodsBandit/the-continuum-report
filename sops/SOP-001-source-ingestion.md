# SOP-001: Source Ingestion

  ## Purpose
  Extract entities from source documents.

  ## Entity Types
  - PERSON: Named individuals
  - ORGANIZATION: Companies, agencies
  - LOCATION: Addresses, places
  - LEGAL: Case numbers, courts

  ## Output
  Return JSON with document_id, entities list, and summary.

  ## Standards
  - Only extract documented entities
  - Note context for mentions
  - Maintain source attribution
