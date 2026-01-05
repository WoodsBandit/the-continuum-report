"""
The Continuum Report - Shared Library

BACKWARD COMPATIBILITY NOTICE:
This module now re-exports from the main package at continuum_report.lib.
For new code, prefer importing directly:
    from continuum_report.lib import settings, PaperlessClient, OllamaClient

Legacy import style (still works):
    from lib.config import settings
    from lib.paperless_client import PaperlessClient
    from lib.ollama_client import OllamaClient
    from lib.logging_config import get_logger

This package provides centralized utilities for The Continuum Report pipeline:
- Configuration management (config.py)
- Paperless-ngx API client (paperless_client.py)
- Ollama LLM client (ollama_client.py)
- Structured logging (logging_config.py)

Usage:
    from lib import settings, get_logger, PaperlessClient, OllamaClient

    # Check configuration
    print(settings.paperless_url)
    print(settings.ollama_model)

    # Use clients
    with PaperlessClient() as paperless:
        docs = paperless.get_all_documents()

    with OllamaClient() as ollama:
        response = ollama.generate("Hello!")
"""

# Re-export from local modules for backward compatibility
# These modules use relative imports within scripts/lib/
from .config import settings
from .logging_config import clear_context, get_logger, with_context
from .ollama_client import (
    OllamaClient,
    OllamaConnectionError,
    OllamaError,
    OllamaModelError,
    OllamaTimeoutError,
)
from .paperless_client import (
    PaperlessAuthError,
    PaperlessClient,
    PaperlessConnectionError,
    PaperlessError,
    PaperlessNotFoundError,
)

__version__ = "1.0.0"
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
