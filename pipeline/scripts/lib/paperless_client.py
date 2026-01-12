"""
The Continuum Report - Paperless-ngx API Client

A robust, type-safe client for interacting with Paperless-ngx.
Features retry logic, connection pooling, and structured error handling.

Usage:
    from lib.paperless_client import PaperlessClient

    client = PaperlessClient()

    # Fetch documents
    docs = client.get_all_documents()
    doc = client.get_document(123)
    content = client.get_document_content(123)

    # Search
    results = client.search("Epstein")

    # Tags and document types
    tags = client.get_all_tags()
    doc_types = client.get_all_document_types()
"""

from typing import Any, Dict, Generator, List, Optional

import requests
from requests.adapters import HTTPAdapter
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from urllib3.util.retry import Retry

try:
    from .config import settings
    from .logging_config import get_logger
except ImportError:
    from config import settings
    from logging_config import get_logger

logger = get_logger(__name__)


class PaperlessError(Exception):
    """Base exception for Paperless client errors."""
    pass


class PaperlessAuthError(PaperlessError):
    """Authentication failed - check API token."""
    pass


class PaperlessNotFoundError(PaperlessError):
    """Requested resource not found."""
    pass


class PaperlessConnectionError(PaperlessError):
    """Failed to connect to Paperless server."""
    pass


class PaperlessClient:
    """
    Client for Paperless-ngx API with retry logic and connection pooling.

    All methods use automatic retry with exponential backoff for transient failures.
    Connection pooling improves performance for multiple requests.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        """
        Initialize Paperless client.

        Args:
            base_url: Paperless server URL (defaults to settings.paperless_url)
            token: API token (defaults to settings.paperless_token)
            timeout: Request timeout in seconds (defaults to settings.paperless_timeout)
        """
        self.base_url = (base_url or settings.paperless_url).rstrip("/")
        self.token = token or settings.paperless_token
        self.timeout = timeout or settings.paperless_timeout

        if not self.token:
            raise PaperlessAuthError(
                "Paperless API token not configured. "
                "Set PAPERLESS_TOKEN in your .env file."
            )

        # Create session with connection pooling and retry
        self.session = self._create_session()

        # Caches for tags and document types
        self._tag_cache: Optional[Dict[int, Dict]] = None
        self._doctype_cache: Optional[Dict[int, Dict]] = None

        logger.debug("Paperless client initialized", url=self.base_url)

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic and pooling."""
        session = requests.Session()

        # Set default headers
        session.headers.update({
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

        # Configure retry strategy for transient failures
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=10,
        )

        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Make an API request with error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., "/api/documents/")
            params: Query parameters
            json_data: JSON body for POST/PUT requests

        Returns:
            Response JSON as dictionary

        Raises:
            PaperlessAuthError: If authentication fails
            PaperlessNotFoundError: If resource not found
            PaperlessConnectionError: If connection fails
            PaperlessError: For other API errors
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout,
            )

            # Handle specific error codes
            if response.status_code == 401:
                raise PaperlessAuthError("Invalid API token")
            elif response.status_code == 403:
                raise PaperlessAuthError("Access denied - check token permissions")
            elif response.status_code == 404:
                raise PaperlessNotFoundError(f"Resource not found: {endpoint}")
            elif response.status_code >= 400:
                raise PaperlessError(
                    f"API error {response.status_code}: {response.text}"
                )

            # Return JSON for successful responses
            if response.content:
                return response.json()
            return {}

        except requests.exceptions.ConnectionError as e:
            logger.error("Connection failed", url=url, error=str(e))
            raise PaperlessConnectionError(f"Cannot connect to {self.base_url}") from e
        except requests.exceptions.Timeout as e:
            logger.error("Request timeout", url=url, timeout=self.timeout)
            raise PaperlessConnectionError(f"Request timed out after {self.timeout}s") from e
        except requests.exceptions.RequestException as e:
            logger.error("Request failed", url=url, error=str(e))
            raise PaperlessError(f"Request failed: {e}") from e

    # =========================================================================
    # DOCUMENTS
    # =========================================================================

    def get_document(self, doc_id: int) -> Dict[str, Any]:
        """
        Fetch a single document by ID.

        Args:
            doc_id: Document ID

        Returns:
            Document metadata dictionary
        """
        logger.debug("Fetching document", doc_id=doc_id)
        return self._request("GET", f"/api/documents/{doc_id}/")

    def get_document_content(self, doc_id: int) -> str:
        """
        Fetch the text content of a document.

        Args:
            doc_id: Document ID

        Returns:
            Document text content
        """
        logger.debug("Fetching document content", doc_id=doc_id)
        doc = self.get_document(doc_id)
        return doc.get("content", "")

    def get_documents_page(
        self,
        page: int = 1,
        page_size: int = 25,
        ordering: str = "-created",
        **filters,
    ) -> Dict[str, Any]:
        """
        Fetch a page of documents.

        Args:
            page: Page number (1-indexed)
            page_size: Documents per page
            ordering: Sort order (e.g., "-created", "title")
            **filters: Additional filters (tags__id, document_type, etc.)

        Returns:
            Paginated response with 'results', 'count', 'next', 'previous'
        """
        params = {
            "page": page,
            "page_size": page_size,
            "ordering": ordering,
            **filters,
        }
        return self._request("GET", "/api/documents/", params=params)

    def get_all_documents(
        self,
        page_size: int = 100,
        exclude_dossiers: bool = True,
        progress_callback: Optional[callable] = None,
        **filters,
    ) -> List[Dict[str, Any]]:
        """
        Fetch all documents with pagination.

        Args:
            page_size: Documents per page
            exclude_dossiers: If True, exclude generated dossiers
            progress_callback: Optional callback(fetched, total) for progress
            **filters: Additional filters

        Returns:
            List of all document metadata
        """
        all_docs = []
        page = 1

        logger.info("Fetching all documents", exclude_dossiers=exclude_dossiers)

        while True:
            data = self.get_documents_page(page=page, page_size=page_size, **filters)

            results = data.get("results", [])
            if not results:
                break

            # Optionally filter out dossiers
            if exclude_dossiers:
                results = [
                    doc for doc in results
                    if not self._is_dossier(doc)
                ]

            all_docs.extend(results)

            total = data.get("count", 0)
            if progress_callback:
                progress_callback(len(all_docs), total)

            logger.debug(
                "Fetched page",
                page=page,
                fetched=len(all_docs),
                total=total
            )

            if not data.get("next"):
                break

            page += 1

        logger.info("Fetched all documents", count=len(all_docs))
        return all_docs

    def iter_all_documents(
        self,
        page_size: int = 100,
        **filters,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Iterate over all documents without loading all into memory.

        Args:
            page_size: Documents per page
            **filters: Additional filters

        Yields:
            Document metadata dictionaries
        """
        page = 1

        while True:
            data = self.get_documents_page(page=page, page_size=page_size, **filters)
            results = data.get("results", [])

            if not results:
                break

            yield from results

            if not data.get("next"):
                break

            page += 1

    def _is_dossier(self, doc: Dict) -> bool:
        """Check if a document is a generated dossier (not a source document)."""
        title = doc.get("title", "").lower()

        # Check title patterns that indicate generated content
        dossier_patterns = [
            "dossier:",
            "entity profile:",
            "connection brief:",
            "analysis:",
        ]

        return any(pattern in title for pattern in dossier_patterns)

    # =========================================================================
    # SEARCH
    # =========================================================================

    def search(
        self,
        query: str,
        page: int = 1,
        page_size: int = 25,
    ) -> Dict[str, Any]:
        """
        Search documents by query string.

        Args:
            query: Search query
            page: Page number
            page_size: Results per page

        Returns:
            Paginated search results
        """
        logger.debug("Searching documents", query=query)
        return self._request(
            "GET",
            "/api/documents/",
            params={"query": query, "page": page, "page_size": page_size}
        )

    def search_all(self, query: str) -> List[Dict[str, Any]]:
        """
        Search and return all matching documents.

        Args:
            query: Search query

        Returns:
            List of all matching documents
        """
        results = []
        page = 1

        while True:
            data = self.search(query, page=page, page_size=100)
            page_results = data.get("results", [])

            if not page_results:
                break

            results.extend(page_results)

            if not data.get("next"):
                break

            page += 1

        logger.info("Search complete", query=query, results=len(results))
        return results

    # =========================================================================
    # TAGS
    # =========================================================================

    def get_all_tags(self, use_cache: bool = True) -> Dict[int, Dict]:
        """
        Fetch all tags as a dictionary keyed by ID.

        Args:
            use_cache: If True, return cached results if available

        Returns:
            Dict mapping tag ID to tag metadata
        """
        if use_cache and self._tag_cache is not None:
            return self._tag_cache

        logger.debug("Fetching all tags")
        tags = {}
        page = 1

        while True:
            data = self._request(
                "GET",
                "/api/tags/",
                params={"page": page, "page_size": 100}
            )

            for tag in data.get("results", []):
                tags[tag["id"]] = tag

            if not data.get("next"):
                break
            page += 1

        self._tag_cache = tags
        logger.info("Fetched tags", count=len(tags))
        return tags

    def get_tag_name(self, tag_id: int) -> Optional[str]:
        """Get tag name by ID from cache."""
        tags = self.get_all_tags()
        tag = tags.get(tag_id)
        return tag["name"] if tag else None

    # =========================================================================
    # DOCUMENT TYPES
    # =========================================================================

    def get_all_document_types(self, use_cache: bool = True) -> Dict[int, Dict]:
        """
        Fetch all document types as a dictionary keyed by ID.

        Args:
            use_cache: If True, return cached results if available

        Returns:
            Dict mapping document type ID to metadata
        """
        if use_cache and self._doctype_cache is not None:
            return self._doctype_cache

        logger.debug("Fetching all document types")
        doc_types = {}
        page = 1

        while True:
            data = self._request(
                "GET",
                "/api/document_types/",
                params={"page": page, "page_size": 100}
            )

            for dt in data.get("results", []):
                doc_types[dt["id"]] = dt

            if not data.get("next"):
                break
            page += 1

        self._doctype_cache = doc_types
        logger.info("Fetched document types", count=len(doc_types))
        return doc_types

    def get_document_type_name(self, type_id: int) -> Optional[str]:
        """Get document type name by ID from cache."""
        doc_types = self.get_all_document_types()
        dt = doc_types.get(type_id)
        return dt["name"] if dt else None

    # =========================================================================
    # CORRESPONDENTS
    # =========================================================================

    def get_all_correspondents(self) -> Dict[int, Dict]:
        """Fetch all correspondents as a dictionary keyed by ID."""
        logger.debug("Fetching all correspondents")
        correspondents = {}
        page = 1

        while True:
            data = self._request(
                "GET",
                "/api/correspondents/",
                params={"page": page, "page_size": 100}
            )

            for corr in data.get("results", []):
                correspondents[corr["id"]] = corr

            if not data.get("next"):
                break
            page += 1

        logger.info("Fetched correspondents", count=len(correspondents))
        return correspondents

    # =========================================================================
    # HEALTH CHECK
    # =========================================================================

    def health_check(self) -> bool:
        """
        Check if Paperless server is reachable and authenticated.

        Returns:
            True if healthy, False otherwise
        """
        try:
            self._request("GET", "/api/")
            return True
        except PaperlessError:
            return False

    def close(self) -> None:
        """Close the session and release resources."""
        self.session.close()
        logger.debug("Paperless client closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# =============================================================================
# CLI UTILITY
# =============================================================================

if __name__ == "__main__":
    """Demo the client when run directly."""
    print("=" * 60)
    print("The Continuum Report - Paperless Client Demo")
    print("=" * 60)
    print()

    try:
        with PaperlessClient() as client:
            # Health check
            if client.health_check():
                print("Connection: OK")
            else:
                print("Connection: FAILED")
                sys.exit(1)

            # Fetch stats
            tags = client.get_all_tags()
            doc_types = client.get_all_document_types()

            print(f"Tags: {len(tags)}")
            print(f"Document Types: {len(doc_types)}")

            # Fetch first page of documents
            docs = client.get_documents_page(page_size=5)
            print(f"Documents (total): {docs.get('count', 0)}")
            print()

            # Show first few docs
            print("Recent documents:")
            for doc in docs.get("results", [])[:5]:
                print(f"  [{doc['id']}] {doc['title'][:50]}")

    except PaperlessAuthError as e:
        print(f"Authentication error: {e}")
        print("Check your PAPERLESS_TOKEN in .env")
    except PaperlessConnectionError as e:
        print(f"Connection error: {e}")
        print("Is Paperless running?")
    except PaperlessError as e:
        print(f"Error: {e}")
