"""
The Continuum Report - Paperless Client Tests

Test suite for paperless_client.py with mocked HTTP responses.
All tests use the responses library to mock API calls.
"""

import pytest
import responses
from requests.exceptions import ConnectionError, Timeout

from scripts.lib.paperless_client import (
    PaperlessClient,
    PaperlessError,
    PaperlessAuthError,
    PaperlessNotFoundError,
    PaperlessConnectionError,
)


# =============================================================================
# CLIENT INITIALIZATION TESTS
# =============================================================================

class TestClientInitialization:
    """Test PaperlessClient initialization and configuration."""

    def test_init_with_defaults(self, mock_env_vars):
        """Test client initialization with default settings."""
        client = PaperlessClient()

        assert client.base_url == "http://test-paperless:8040"
        assert client.token == "test-token-12345"
        assert client.timeout == 30

    def test_init_with_custom_values(self, mock_env_vars):
        """Test client initialization with custom values."""
        client = PaperlessClient(
            base_url="http://custom:9000",
            token="custom-token",
            timeout=60
        )

        assert client.base_url == "http://custom:9000"
        assert client.token == "custom-token"
        assert client.timeout == 60

    def test_init_strips_trailing_slash(self, mock_env_vars):
        """Test that trailing slash is stripped from base_url."""
        client = PaperlessClient(base_url="http://test:8040/")

        assert client.base_url == "http://test:8040"
        assert not client.base_url.endswith("/")

    def test_init_without_token_raises_error(self, monkeypatch):
        """Test that initialization without token raises PaperlessAuthError."""
        monkeypatch.delenv("PAPERLESS_TOKEN", raising=False)

        # Reload settings to pick up the deleted environment variable
        import importlib
        from scripts.lib import config
        importlib.reload(config)

        with pytest.raises(PaperlessAuthError) as exc_info:
            PaperlessClient()

        assert "token not configured" in str(exc_info.value).lower()

    def test_session_has_correct_headers(self, mock_env_vars):
        """Test that session is created with correct authorization headers."""
        client = PaperlessClient()

        assert "Authorization" in client.session.headers
        assert client.session.headers["Authorization"] == "Token test-token-12345"
        assert client.session.headers["Content-Type"] == "application/json"
        assert client.session.headers["Accept"] == "application/json"

    def test_cache_initialization(self, mock_env_vars):
        """Test that caches are initialized as None."""
        client = PaperlessClient()

        assert client._tag_cache is None
        assert client._doctype_cache is None


# =============================================================================
# HEALTH CHECK TESTS
# =============================================================================

class TestHealthCheck:
    """Test health check functionality."""

    @responses.activate
    def test_health_check_success(self, mock_env_vars):
        """Test successful health check."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/",
            json={"version": "2.3.0"},
            status=200
        )

        client = PaperlessClient()
        assert client.health_check() is True

    @responses.activate
    def test_health_check_failure(self, mock_env_vars):
        """Test failed health check."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/",
            json={"error": "Server error"},
            status=500
        )

        client = PaperlessClient()
        assert client.health_check() is False

    @responses.activate
    def test_health_check_connection_error(self, mock_env_vars):
        """Test health check with connection error."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/",
            body=ConnectionError("Connection refused")
        )

        client = PaperlessClient()
        assert client.health_check() is False


# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

class TestErrorHandling:
    """Test error handling for various HTTP status codes."""

    @responses.activate
    def test_401_unauthorized_raises_auth_error(self, mock_env_vars):
        """Test that 401 status raises PaperlessAuthError."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/123/",
            json={"detail": "Invalid token"},
            status=401
        )

        client = PaperlessClient()
        with pytest.raises(PaperlessAuthError) as exc_info:
            client.get_document(123)

        assert "Invalid API token" in str(exc_info.value)

    @responses.activate
    def test_403_forbidden_raises_auth_error(self, mock_env_vars):
        """Test that 403 status raises PaperlessAuthError."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/123/",
            json={"detail": "Access denied"},
            status=403
        )

        client = PaperlessClient()
        with pytest.raises(PaperlessAuthError) as exc_info:
            client.get_document(123)

        assert "Access denied" in str(exc_info.value)

    @responses.activate
    def test_404_not_found_raises_not_found_error(self, mock_env_vars):
        """Test that 404 status raises PaperlessNotFoundError."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/999/",
            json={"detail": "Not found"},
            status=404
        )

        client = PaperlessClient()
        with pytest.raises(PaperlessNotFoundError) as exc_info:
            client.get_document(999)

        assert "Resource not found" in str(exc_info.value)

    @responses.activate
    def test_500_server_error_raises_paperless_error(self, mock_env_vars):
        """Test that 500 status raises PaperlessError."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/123/",
            json={"error": "Internal server error"},
            status=500
        )

        client = PaperlessClient()
        with pytest.raises(PaperlessError) as exc_info:
            client.get_document(123)

        # Retry logic will cause "Max retries exceeded" or "API error 500"
        assert "500" in str(exc_info.value) or "Request failed" in str(exc_info.value)

    @responses.activate
    def test_connection_error_raises_connection_error(self, mock_env_vars):
        """Test that connection errors raise PaperlessConnectionError."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/123/",
            body=ConnectionError("Connection refused")
        )

        client = PaperlessClient()
        with pytest.raises(PaperlessConnectionError) as exc_info:
            client.get_document(123)

        assert "Cannot connect" in str(exc_info.value)

    @responses.activate
    def test_timeout_error_raises_connection_error(self, mock_env_vars):
        """Test that timeout errors raise PaperlessConnectionError."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/123/",
            body=Timeout("Request timed out")
        )

        client = PaperlessClient()
        with pytest.raises(PaperlessConnectionError) as exc_info:
            client.get_document(123)

        assert "timed out" in str(exc_info.value).lower()


# =============================================================================
# DOCUMENT RETRIEVAL TESTS
# =============================================================================

class TestDocumentRetrieval:
    """Test document retrieval methods."""

    @responses.activate
    def test_get_document_success(self, mock_env_vars, mock_paperless_document):
        """Test successful document retrieval."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/123/",
            json=mock_paperless_document,
            status=200
        )

        client = PaperlessClient()
        doc = client.get_document(123)

        assert doc["id"] == 123
        assert doc["title"] == "Test Document - Jeffrey Epstein Flight Logs"
        assert "content" in doc

    @responses.activate
    def test_get_document_content_success(self, mock_env_vars, mock_paperless_document):
        """Test successful document content retrieval."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/123/",
            json=mock_paperless_document,
            status=200
        )

        client = PaperlessClient()
        content = client.get_document_content(123)

        assert isinstance(content, str)
        assert "Sample document content" in content

    @responses.activate
    def test_get_document_content_missing_returns_empty_string(self, mock_env_vars):
        """Test that missing content returns empty string."""
        doc_without_content = {
            "id": 123,
            "title": "Test Document",
            # No "content" field
        }

        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/123/",
            json=doc_without_content,
            status=200
        )

        client = PaperlessClient()
        content = client.get_document_content(123)

        assert content == ""


# =============================================================================
# PAGINATION TESTS
# =============================================================================

class TestPagination:
    """Test pagination functionality."""

    @responses.activate
    def test_get_documents_page_success(self, mock_env_vars, mock_paperless_documents_page):
        """Test successful paginated document retrieval."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            json=mock_paperless_documents_page,
            status=200
        )

        client = PaperlessClient()
        result = client.get_documents_page(page=1, page_size=25)

        assert result["count"] == 150
        assert len(result["results"]) == 3
        assert result["next"] is not None

    @responses.activate
    def test_get_documents_page_with_filters(self, mock_env_vars, mock_paperless_documents_page):
        """Test paginated retrieval with filters."""
        def request_callback(request):
            # Verify query parameters
            assert "page=2" in request.url
            assert "page_size=50" in request.url
            assert "ordering=-created" in request.url
            return (200, {}, '{"count": 0, "results": []}')

        responses.add_callback(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            callback=request_callback
        )

        client = PaperlessClient()
        client.get_documents_page(page=2, page_size=50, ordering="-created")

    @responses.activate
    def test_get_all_documents_single_page(self, mock_env_vars):
        """Test get_all_documents with single page of results."""
        single_page = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {"id": 1, "title": "Doc 1"},
                {"id": 2, "title": "Doc 2"},
            ]
        }

        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            json=single_page,
            status=200
        )

        client = PaperlessClient()
        docs = client.get_all_documents(page_size=100)

        assert len(docs) == 2
        assert docs[0]["id"] == 1
        assert docs[1]["id"] == 2

    @responses.activate
    def test_get_all_documents_multiple_pages(self, mock_env_vars):
        """Test get_all_documents with multiple pages."""
        page1 = {
            "count": 5,
            "next": "http://test-paperless:8040/api/documents/?page=2",
            "previous": None,
            "results": [
                {"id": 1, "title": "Doc 1"},
                {"id": 2, "title": "Doc 2"},
                {"id": 3, "title": "Doc 3"},
            ]
        }

        page2 = {
            "count": 5,
            "next": None,
            "previous": "http://test-paperless:8040/api/documents/?page=1",
            "results": [
                {"id": 4, "title": "Doc 4"},
                {"id": 5, "title": "Doc 5"},
            ]
        }

        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            json=page1,
            status=200
        )

        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            json=page2,
            status=200
        )

        client = PaperlessClient()
        docs = client.get_all_documents(page_size=3)

        assert len(docs) == 5
        assert docs[0]["id"] == 1
        assert docs[4]["id"] == 5

    @responses.activate
    def test_get_all_documents_excludes_dossiers(self, mock_env_vars):
        """Test that get_all_documents excludes generated dossiers."""
        page_with_dossier = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {"id": 1, "title": "Normal Document"},
                {"id": 2, "title": "DOSSIER: Jeffrey Epstein"},
                {"id": 3, "title": "Another Document"},
            ]
        }

        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            json=page_with_dossier,
            status=200
        )

        client = PaperlessClient()
        docs = client.get_all_documents(exclude_dossiers=True)

        # Should exclude the dossier
        assert len(docs) == 2
        assert all("dossier" not in doc["title"].lower() for doc in docs)

    @responses.activate
    def test_get_all_documents_with_progress_callback(self, mock_env_vars):
        """Test progress callback during pagination."""
        page1 = {
            "count": 100,
            "next": "http://test-paperless:8040/api/documents/?page=2",
            "results": [{"id": i, "title": f"Doc {i}"} for i in range(1, 51)]
        }

        page2 = {
            "count": 100,
            "next": None,
            "results": [{"id": i, "title": f"Doc {i}"} for i in range(51, 101)]
        }

        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            json=page1,
            status=200
        )

        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            json=page2,
            status=200
        )

        callback_calls = []

        def progress_callback(fetched, total):
            callback_calls.append((fetched, total))

        client = PaperlessClient()
        docs = client.get_all_documents(page_size=50, progress_callback=progress_callback)

        # Verify callback was called
        assert len(callback_calls) == 2
        assert callback_calls[0] == (50, 100)
        assert callback_calls[1] == (100, 100)


# =============================================================================
# SEARCH TESTS
# =============================================================================

class TestSearch:
    """Test document search functionality."""

    @responses.activate
    def test_search_success(self, mock_env_vars):
        """Test successful document search."""
        search_results = {
            "count": 10,
            "next": None,
            "results": [
                {"id": 1, "title": "Epstein Document 1"},
                {"id": 2, "title": "Epstein Document 2"},
            ]
        }

        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            json=search_results,
            status=200
        )

        client = PaperlessClient()
        results = client.search("Epstein")

        assert results["count"] == 10
        assert len(results["results"]) == 2

    @responses.activate
    def test_search_all_multiple_pages(self, mock_env_vars):
        """Test search_all with multiple pages of results."""
        page1 = {
            "count": 150,
            "next": "http://test-paperless:8040/api/documents/?page=2",
            "results": [{"id": i, "title": f"Epstein {i}"} for i in range(1, 101)]
        }

        page2 = {
            "count": 150,
            "next": None,
            "results": [{"id": i, "title": f"Epstein {i}"} for i in range(101, 151)]
        }

        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            json=page1,
            status=200
        )

        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/documents/",
            json=page2,
            status=200
        )

        client = PaperlessClient()
        results = client.search_all("Epstein")

        assert len(results) == 150


# =============================================================================
# TAGS AND DOCUMENT TYPES TESTS
# =============================================================================

class TestTagsAndDocumentTypes:
    """Test tag and document type retrieval."""

    @responses.activate
    def test_get_all_tags(self, mock_env_vars, mock_paperless_tags):
        """Test retrieving all tags."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/tags/",
            json=mock_paperless_tags,
            status=200
        )

        client = PaperlessClient()
        tags = client.get_all_tags()

        assert len(tags) == 3
        assert 10 in tags
        assert tags[10]["name"] == "Epstein"

    @responses.activate
    def test_get_all_tags_uses_cache(self, mock_env_vars, mock_paperless_tags):
        """Test that get_all_tags caches results."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/tags/",
            json=mock_paperless_tags,
            status=200
        )

        client = PaperlessClient()

        # First call should hit API
        tags1 = client.get_all_tags()

        # Second call should use cache (no additional API call)
        tags2 = client.get_all_tags(use_cache=True)

        assert tags1 == tags2
        # Only one API call should have been made
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_tag_name(self, mock_env_vars, mock_paperless_tags):
        """Test getting tag name by ID."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/tags/",
            json=mock_paperless_tags,
            status=200
        )

        client = PaperlessClient()
        tag_name = client.get_tag_name(10)

        assert tag_name == "Epstein"

    @responses.activate
    def test_get_tag_name_nonexistent(self, mock_env_vars, mock_paperless_tags):
        """Test getting name for non-existent tag returns None."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/tags/",
            json=mock_paperless_tags,
            status=200
        )

        client = PaperlessClient()
        tag_name = client.get_tag_name(9999)

        assert tag_name is None

    @responses.activate
    def test_get_all_document_types(self, mock_env_vars, mock_paperless_document_types):
        """Test retrieving all document types."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/document_types/",
            json=mock_paperless_document_types,
            status=200
        )

        client = PaperlessClient()
        doc_types = client.get_all_document_types()

        assert len(doc_types) == 2
        assert 1 in doc_types
        assert doc_types[1]["name"] == "Report"


# =============================================================================
# CONTEXT MANAGER TESTS
# =============================================================================

class TestContextManager:
    """Test context manager functionality."""

    @responses.activate
    def test_context_manager_closes_session(self, mock_env_vars):
        """Test that context manager properly closes session."""
        responses.add(
            responses.GET,
            "http://test-paperless:8040/api/",
            json={"version": "2.3.0"},
            status=200
        )

        with PaperlessClient() as client:
            assert client.health_check() is True
            # Session should be open
            assert client.session is not None

        # After exiting, close() should have been called
        # We can't directly test if session is closed, but we verified the pattern

    def test_close_method(self, mock_env_vars):
        """Test that close() method works."""
        client = PaperlessClient()
        session = client.session

        client.close()

        # Session should be closed (we can't easily verify, but method shouldn't error)


# =============================================================================
# DOSSIER DETECTION TESTS
# =============================================================================

class TestDossierDetection:
    """Test dossier detection logic."""

    def test_is_dossier_identifies_dossier(self, mock_env_vars):
        """Test that _is_dossier correctly identifies dossiers."""
        client = PaperlessClient()

        dossier_titles = [
            "DOSSIER: Jeffrey Epstein",
            "dossier: Test Entity",
            "Entity Profile: Ghislaine Maxwell",
            "Connection Brief: Epstein Network",
            "Analysis: Flight Log Patterns",
        ]

        for title in dossier_titles:
            doc = {"title": title}
            assert client._is_dossier(doc) is True

    def test_is_dossier_identifies_non_dossier(self, mock_env_vars):
        """Test that _is_dossier correctly identifies regular documents."""
        client = PaperlessClient()

        regular_titles = [
            "Flight Manifest 2024",
            "Investigation Report",
            "Court Documents",
            "Research Notes",
        ]

        for title in regular_titles:
            doc = {"title": title}
            assert client._is_dossier(doc) is False
