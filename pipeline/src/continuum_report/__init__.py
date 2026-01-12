"""
The Continuum Report - AI Document Analysis Pipeline

This package provides tools for intelligent document analysis, entity extraction,
and dossier generation using Paperless-ngx and Ollama LLM integration.

Modules:
    lib: Core library components (config, clients, logging)
    scripts: CLI tools and pipeline scripts

Quick Start:
    from continuum_report import settings, get_logger
    from continuum_report import PaperlessClient, OllamaClient

    # Use configured settings
    print(settings.paperless_url)

    # Get a structured logger
    logger = get_logger(__name__)

    # Use API clients
    with PaperlessClient() as paperless:
        docs = paperless.get_all_documents()

    with OllamaClient() as ollama:
        response = ollama.generate("Hello!")
"""

from continuum_report.lib.config import settings
from continuum_report.lib.logging_config import clear_context, get_logger, with_context
from continuum_report.lib.ollama_client import (
    OllamaClient,
    OllamaConnectionError,
    OllamaError,
    OllamaModelError,
    OllamaTimeoutError,
)
from continuum_report.lib.paperless_client import (
    PaperlessAuthError,
    PaperlessClient,
    PaperlessConnectionError,
    PaperlessError,
    PaperlessNotFoundError,
)

__version__ = "1.0.0"
__all__ = [
    # Version
    "__version__",
    # Configuration
    "settings",
    # Logging
    "get_logger",
    "with_context",
    "clear_context",
    # Paperless
    "PaperlessClient",
    "PaperlessError",
    "PaperlessAuthError",
    "PaperlessNotFoundError",
    "PaperlessConnectionError",
    # Ollama
    "OllamaClient",
    "OllamaError",
    "OllamaConnectionError",
    "OllamaModelError",
    "OllamaTimeoutError",
]
