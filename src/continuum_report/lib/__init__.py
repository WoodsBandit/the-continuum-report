"""
The Continuum Report - Core Library

This package provides core utilities for The Continuum Report pipeline:
- Configuration management (config.py)
- Paperless-ngx API client (paperless_client.py)
- Ollama LLM client (ollama_client.py)
- Structured logging (logging_config.py)

Usage:
    from continuum_report.lib import settings
    from continuum_report.lib import PaperlessClient, OllamaClient
    from continuum_report.lib import get_logger

    # Check configuration
    print(settings.paperless_url)
    print(settings.ollama_model)

    # Use clients
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

__all__ = [
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
