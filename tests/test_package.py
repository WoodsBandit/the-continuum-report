"""
Test package structure and imports for continuum-report.

Run with: pytest tests/test_package.py -v
"""

import pytest


class TestPackageImports:
    """Verify that the package can be imported correctly."""

    def test_import_main_package(self) -> None:
        """Test importing the main package."""
        import continuum_report

        assert hasattr(continuum_report, "__version__")
        assert continuum_report.__version__ == "1.0.0"

    def test_import_settings(self) -> None:
        """Test importing settings from the package."""
        from continuum_report import settings

        assert hasattr(settings, "paperless_url")
        assert hasattr(settings, "ollama_url")
        assert hasattr(settings, "ollama_model")

    def test_import_logger(self) -> None:
        """Test importing logging utilities."""
        from continuum_report import get_logger, with_context, clear_context

        logger = get_logger(__name__)
        assert logger is not None

    def test_import_paperless_client(self) -> None:
        """Test importing Paperless client classes."""
        from continuum_report import (
            PaperlessClient,
            PaperlessError,
            PaperlessAuthError,
            PaperlessNotFoundError,
            PaperlessConnectionError,
        )

        # Verify these are actual classes
        assert issubclass(PaperlessAuthError, PaperlessError)
        assert issubclass(PaperlessNotFoundError, PaperlessError)
        assert issubclass(PaperlessConnectionError, PaperlessError)

    def test_import_ollama_client(self) -> None:
        """Test importing Ollama client classes."""
        from continuum_report import (
            OllamaClient,
            OllamaError,
            OllamaConnectionError,
            OllamaModelError,
            OllamaTimeoutError,
        )

        # Verify these are actual classes
        assert issubclass(OllamaConnectionError, OllamaError)
        assert issubclass(OllamaModelError, OllamaError)
        assert issubclass(OllamaTimeoutError, OllamaError)

    def test_import_from_lib(self) -> None:
        """Test importing directly from lib subpackage."""
        from continuum_report.lib import settings, get_logger
        from continuum_report.lib import PaperlessClient, OllamaClient

        assert settings is not None
        assert get_logger is not None


class TestSettingsConfiguration:
    """Verify settings are properly configured."""

    def test_settings_has_required_fields(self) -> None:
        """Test that settings has all required configuration fields."""
        from continuum_report import settings

        # Core services
        assert hasattr(settings, "paperless_url")
        assert hasattr(settings, "paperless_token")
        assert hasattr(settings, "paperless_timeout")
        assert hasattr(settings, "ollama_url")
        assert hasattr(settings, "ollama_model")
        assert hasattr(settings, "ollama_timeout")

        # Directories
        assert hasattr(settings, "continuum_base_dir")
        assert hasattr(settings, "data_dir")
        assert hasattr(settings, "reports_dir")
        assert hasattr(settings, "checkpoint_dir")

        # Processing settings
        assert hasattr(settings, "max_documents_to_search")
        assert hasattr(settings, "max_chunk_size")

    def test_settings_default_values(self) -> None:
        """Test that settings have sensible defaults."""
        from continuum_report import settings

        assert settings.paperless_timeout > 0
        assert settings.ollama_timeout > 0
        assert settings.max_chunk_size > 0

    def test_settings_repr_hides_secrets(self) -> None:
        """Test that settings repr doesn't expose token."""
        from continuum_report import settings

        repr_str = repr(settings)
        # Token should not appear in repr
        assert "token" not in repr_str.lower() or "paperless_token" not in repr_str


class TestExceptionHierarchy:
    """Verify exception hierarchy is correct."""

    def test_paperless_exceptions(self) -> None:
        """Test Paperless exception inheritance."""
        from continuum_report import (
            PaperlessError,
            PaperlessAuthError,
            PaperlessNotFoundError,
            PaperlessConnectionError,
        )

        # All specific exceptions should inherit from base
        with pytest.raises(PaperlessError):
            raise PaperlessAuthError("test")

        with pytest.raises(PaperlessError):
            raise PaperlessNotFoundError("test")

        with pytest.raises(PaperlessError):
            raise PaperlessConnectionError("test")

    def test_ollama_exceptions(self) -> None:
        """Test Ollama exception inheritance."""
        from continuum_report import (
            OllamaError,
            OllamaConnectionError,
            OllamaModelError,
            OllamaTimeoutError,
        )

        # All specific exceptions should inherit from base
        with pytest.raises(OllamaError):
            raise OllamaConnectionError("test")

        with pytest.raises(OllamaError):
            raise OllamaModelError("test")

        with pytest.raises(OllamaError):
            raise OllamaTimeoutError("test")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
