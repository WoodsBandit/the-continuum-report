"""
The Continuum Report - Structured Logging Configuration

Uses structlog for structured, JSON-capable logging with context propagation.

Usage:
    from lib.logging_config import get_logger

    logger = get_logger(__name__)
    logger.info("Processing document", doc_id=123, title="Example")
    logger.error("Failed to process", error=str(e), doc_id=123)

Features:
- Structured key-value logging
- Automatic timestamp and log level
- JSON output for production (LOG_FORMAT=json)
- Pretty console output for development (default)
- Context binding for request tracing
"""

import logging
import sys
from typing import Any, Optional

import structlog
from structlog.typing import Processor


def configure_logging(
    level: str = "INFO",
    json_format: bool = False,
    log_file: Optional[str] = None
) -> None:
    """
    Configure structlog with consistent formatting.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: If True, output JSON; otherwise pretty console output
        log_file: Optional file path to write logs to
    """
    # Determine log level
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Shared processors for all outputs
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if json_format:
        # JSON output for production/log aggregation
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ]
    else:
        # Pretty console output for development
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback
            )
        ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard logging
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # Add file handler if specified
    handlers = [handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        handlers.append(file_handler)

    logging.basicConfig(
        format="%(message)s",
        level=log_level,
        handlers=handlers,
        force=True
    )


def get_logger(name: str = None) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        A structlog BoundLogger instance
    """
    return structlog.get_logger(name)


def with_context(**kwargs: Any) -> None:
    """
    Bind context variables that will be included in all subsequent log messages.

    Useful for adding request IDs, user IDs, or other context that should
    appear in all related log messages.

    Args:
        **kwargs: Key-value pairs to bind to the logging context

    Usage:
        with_context(request_id="abc123", user="john")
        logger.info("Processing")  # Will include request_id and user
    """
    structlog.contextvars.bind_contextvars(**kwargs)


def clear_context() -> None:
    """Clear all bound context variables."""
    structlog.contextvars.clear_contextvars()


# =============================================================================
# INITIALIZATION
# =============================================================================

# Auto-configure on import based on environment
import os

_log_format = os.environ.get("LOG_FORMAT", "console").lower()
_log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
_log_file = os.environ.get("LOG_FILE")

configure_logging(
    level=_log_level,
    json_format=(_log_format == "json"),
    log_file=_log_file
)


# =============================================================================
# CLI UTILITY
# =============================================================================

if __name__ == "__main__":
    """Demo logging when run directly."""
    logger = get_logger("demo")

    print("=" * 60)
    print("The Continuum Report - Logging Demo")
    print("=" * 60)
    print()

    # Basic logging
    logger.info("Starting demo")
    logger.debug("Debug message", value=42)
    logger.warning("Warning message", reason="just a demo")

    # With context
    with_context(session_id="demo-123", component="logging_config")
    logger.info("Message with context")
    logger.info("Another message", extra_field="additional data")

    # Error logging
    try:
        raise ValueError("Example error for demo")
    except Exception as e:
        logger.error("Caught an error", error=str(e), exc_info=True)

    clear_context()
    logger.info("Context cleared")

    print()
    print("Try with different formats:")
    print("  LOG_FORMAT=json python logging_config.py")
    print("  LOG_LEVEL=DEBUG python logging_config.py")
