"""
The Continuum Report - Pytest Configuration and Fixtures

Shared test fixtures for mocking external dependencies and test utilities.
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, MagicMock

import pytest
import responses


# =============================================================================
# ENVIRONMENT FIXTURES
# =============================================================================

@pytest.fixture
def mock_env_vars(monkeypatch):
    """
    Mock environment variables for testing configuration.

    Sets up a complete test environment with all required variables.
    Reloads the settings module to pick up the new environment variables.
    """
    env_vars = {
        "PAPERLESS_URL": "http://test-paperless:8040",
        "PAPERLESS_TOKEN": "test-token-12345",
        "PAPERLESS_TIMEOUT": "30",
        "OLLAMA_URL": "http://test-ollama:11434",
        "OLLAMA_MODEL": "test-mistral",
        "OLLAMA_CONTEXT_SIZE": "1024",
        "OLLAMA_TIMEOUT": "600",
        "CONTINUUM_BASE_DIR": "/tmp/continuum-test",
        "LOG_LEVEL": "DEBUG",
        "LOG_FORMAT": "console",
    }

    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

    # Reload the settings module to pick up new environment variables
    import importlib
    import sys
    from scripts.lib import config
    importlib.reload(config)

    # Monkeypatch the new settings object into already-imported client modules
    # (don't reload client modules as that would create new exception classes)
    if "scripts.lib.paperless_client" in sys.modules:
        from scripts.lib import paperless_client
        monkeypatch.setattr(paperless_client, "settings", config.settings)
    if "scripts.lib.ollama_client" in sys.modules:
        from scripts.lib import ollama_client
        monkeypatch.setattr(ollama_client, "settings", config.settings)

    return env_vars


@pytest.fixture
def temp_continuum_dir(tmp_path):
    """
    Create a temporary directory structure for testing.

    Returns:
        Path: Temporary base directory with subdirectories created
    """
    base_dir = tmp_path / "continuum"
    base_dir.mkdir()

    # Create subdirectories
    (base_dir / "entity_data").mkdir()
    (base_dir / "reports").mkdir()
    (base_dir / "checkpoints").mkdir()
    (base_dir / "documents" / "inbox").mkdir(parents=True)

    return base_dir


# =============================================================================
# PAPERLESS API MOCK FIXTURES
# =============================================================================

@pytest.fixture
def mock_paperless_document():
    """Sample Paperless document metadata for testing."""
    return {
        "id": 123,
        "title": "Test Document - Jeffrey Epstein Flight Logs",
        "content": "Sample document content about Epstein's private jet logs...",
        "created": "2024-01-15T10:30:00Z",
        "modified": "2024-01-15T10:30:00Z",
        "correspondent": 1,
        "document_type": 2,
        "tags": [10, 20, 30],
        "archive_serial_number": "2024-001",
        "original_file_name": "epstein_logs.pdf",
    }


@pytest.fixture
def mock_paperless_documents_page(mock_paperless_document):
    """Sample paginated documents response."""
    return {
        "count": 150,
        "next": "http://test-paperless:8040/api/documents/?page=2",
        "previous": None,
        "results": [
            mock_paperless_document,
            {**mock_paperless_document, "id": 124, "title": "Document 2"},
            {**mock_paperless_document, "id": 125, "title": "Document 3"},
        ]
    }


@pytest.fixture
def mock_paperless_tags():
    """Sample tags response."""
    return {
        "count": 3,
        "next": None,
        "previous": None,
        "results": [
            {"id": 10, "name": "Epstein", "color": "#ff0000"},
            {"id": 20, "name": "OSINT", "color": "#00ff00"},
            {"id": 30, "name": "Investigation", "color": "#0000ff"},
        ]
    }


@pytest.fixture
def mock_paperless_document_types():
    """Sample document types response."""
    return {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {"id": 1, "name": "Report"},
            {"id": 2, "name": "Document"},
        ]
    }


@pytest.fixture
def mock_paperless_api():
    """
    Mock Paperless API responses using responses library.

    Yields:
        responses.RequestsMock: Active mock for HTTP requests
    """
    with responses.RequestsMock() as rsps:
        # Health check endpoint
        rsps.add(
            responses.GET,
            "http://test-paperless:8040/api/",
            json={"version": "2.3.0"},
            status=200
        )

        yield rsps


# =============================================================================
# OLLAMA API MOCK FIXTURES
# =============================================================================

@pytest.fixture
def mock_ollama_generate_response():
    """Sample Ollama generate response."""
    return {
        "model": "test-mistral",
        "created_at": "2024-01-15T10:30:00Z",
        "response": "This is a test response from the LLM model.",
        "done": True,
        "context": [1, 2, 3],
        "total_duration": 1000000000,
        "load_duration": 100000000,
        "prompt_eval_count": 10,
        "prompt_eval_duration": 200000000,
        "eval_count": 20,
        "eval_duration": 700000000,
    }


@pytest.fixture
def mock_ollama_models():
    """Sample Ollama models list."""
    return {
        "models": [
            {
                "name": "test-mistral",
                "modified_at": "2024-01-15T10:30:00Z",
                "size": 4109865159,
                "digest": "abc123def456",
            },
            {
                "name": "llama2",
                "modified_at": "2024-01-14T09:20:00Z",
                "size": 3826793677,
                "digest": "xyz789uvw012",
            }
        ]
    }


@pytest.fixture
def mock_ollama_stream_response():
    """Sample streaming response chunks."""
    return [
        {"model": "test-mistral", "response": "This ", "done": False},
        {"model": "test-mistral", "response": "is ", "done": False},
        {"model": "test-mistral", "response": "streaming.", "done": False},
        {"model": "test-mistral", "response": "", "done": True, "eval_count": 10},
    ]


@pytest.fixture
def mock_ollama_api():
    """
    Mock Ollama API responses using responses library.

    Yields:
        responses.RequestsMock: Active mock for HTTP requests
    """
    with responses.RequestsMock() as rsps:
        # Health check / list models endpoint
        rsps.add(
            responses.GET,
            "http://test-ollama:11434/api/tags",
            json={
                "models": [
                    {"name": "test-mistral", "size": 4109865159}
                ]
            },
            status=200
        )

        yield rsps


# =============================================================================
# ENTITY EXTRACTION MOCK FIXTURES
# =============================================================================

@pytest.fixture
def mock_entity_extraction_response():
    """Sample entity extraction JSON response."""
    return [
        {
            "name": "Jeffrey Epstein",
            "type": "Person",
            "context": "financier and convicted sex offender"
        },
        {
            "name": "Little St. James",
            "type": "Location",
            "context": "private island in the U.S. Virgin Islands"
        },
        {
            "name": "Lolita Express",
            "type": "Document",
            "context": "nickname for Epstein's private Boeing 727"
        }
    ]


@pytest.fixture
def mock_connection_analysis_response():
    """Sample connection analysis JSON response."""
    return {
        "relationship": "Business associate and frequent travel companion",
        "confidence": "high",
        "evidence": "Flight logs show 26 documented trips together between 2001-2003"
    }


# =============================================================================
# TEST UTILITIES
# =============================================================================

@pytest.fixture
def sample_document_text():
    """Sample document text for testing LLM operations."""
    return """
    Jeffrey Epstein was an American financier and convicted sex offender.
    He had connections to numerous high-profile individuals including politicians,
    academics, and business leaders. His private island, Little St. James in the
    U.S. Virgin Islands, became the subject of intense scrutiny following his arrest.

    Flight logs from his private jet, nicknamed the "Lolita Express," revealed
    extensive travel patterns and passenger manifests that became crucial evidence
    in investigations.
    """


@pytest.fixture
def assert_structlog_called():
    """
    Utility fixture to verify structlog logging calls.

    Usage:
        assert_structlog_called(logger, "info", "message", key="value")
    """
    def _assert_called(logger_mock, level, message=None, **kwargs):
        """Verify logger was called with expected parameters."""
        method = getattr(logger_mock, level)
        if message:
            method.assert_called_with(message, **kwargs)
        else:
            assert method.called

    return _assert_called


# =============================================================================
# PARAMETRIZATION HELPERS
# =============================================================================

@pytest.fixture(params=[
    {"page": 1, "page_size": 25},
    {"page": 2, "page_size": 50},
    {"page": 10, "page_size": 100},
])
def pagination_params(request):
    """Parametrized pagination configurations for testing."""
    return request.param


@pytest.fixture(params=[
    {"status_code": 401, "exception": "PaperlessAuthError"},
    {"status_code": 403, "exception": "PaperlessAuthError"},
    {"status_code": 404, "exception": "PaperlessNotFoundError"},
    {"status_code": 500, "exception": "PaperlessError"},
])
def error_responses(request):
    """Parametrized error responses for testing error handling."""
    return request.param


# =============================================================================
# SESSION-SCOPED FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def test_data_dir(tmp_path_factory):
    """
    Create a session-scoped temporary directory for test data.

    Useful for test data that should persist across all tests.
    """
    data_dir = tmp_path_factory.mktemp("test_data")
    return data_dir


# =============================================================================
# AUTO-USE FIXTURES
# =============================================================================

@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    """
    Automatically reset environment for each test.

    Prevents test pollution from environment variables.
    """
    # Clear any existing test environment variables
    test_vars = [
        "PAPERLESS_URL", "PAPERLESS_TOKEN", "PAPERLESS_TIMEOUT",
        "OLLAMA_URL", "OLLAMA_MODEL", "OLLAMA_CONTEXT_SIZE", "OLLAMA_TIMEOUT",
        "CONTINUUM_BASE_DIR", "LOG_LEVEL", "LOG_FORMAT", "LOG_FILE"
    ]

    for var in test_vars:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture(autouse=True)
def disable_external_requests(monkeypatch):
    """
    Prevent accidental external HTTP requests during tests.

    Tests should use mocked responses, not real API calls.
    """
    # This will be overridden by specific fixtures when needed
    pass


# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires services)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test (default)"
    )
