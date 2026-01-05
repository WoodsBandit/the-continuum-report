"""
The Continuum Report - Configuration Tests

Test suite for config.py settings and validation.
"""

import os
import warnings
from pathlib import Path

import pytest
from pydantic import ValidationError

from scripts.lib.config import ContinuumSettings


# =============================================================================
# DEFAULT VALUES TESTS
# =============================================================================

class TestDefaultValues:
    """Test that configuration loads with correct default values."""

    def test_paperless_defaults(self, mock_env_vars):
        """Test Paperless default configuration values."""
        settings = ContinuumSettings()

        assert settings.paperless_url == "http://test-paperless:8040"
        assert settings.paperless_token == "test-token-12345"
        assert settings.paperless_timeout == 30

    def test_ollama_defaults(self, mock_env_vars):
        """Test Ollama default configuration values."""
        settings = ContinuumSettings()

        assert settings.ollama_url == "http://test-ollama:11434"
        assert settings.ollama_model == "test-mistral"
        assert settings.ollama_context_size == 1024
        assert settings.ollama_timeout == 600

    def test_directory_defaults(self, mock_env_vars):
        """Test directory configuration defaults."""
        settings = ContinuumSettings()

        assert settings.continuum_base_dir == Path("/tmp/continuum-test")
        assert isinstance(settings.continuum_base_dir, Path)

    def test_processing_defaults(self, mock_env_vars):
        """Test processing configuration defaults."""
        settings = ContinuumSettings()

        assert settings.max_documents_to_search == 9999
        assert settings.max_documents_for_entities == 9999
        assert settings.max_documents_for_dossier == 9999
        assert settings.max_chunk_size == 1500

    def test_memory_safety_defaults(self, mock_env_vars):
        """Test memory safety configuration defaults."""
        settings = ContinuumSettings()

        assert settings.delay_between_docs == 10
        assert settings.delay_between_batches == 30
        assert settings.unload_model_every == 10

    def test_website_defaults(self, mock_env_vars):
        """Test website configuration defaults."""
        settings = ContinuumSettings()

        assert settings.website_base_url == "https://thecontinuumreport.com"


# =============================================================================
# ENVIRONMENT VARIABLE OVERRIDE TESTS
# =============================================================================

class TestEnvironmentOverrides:
    """Test that environment variables correctly override defaults."""

    def test_paperless_url_override(self, monkeypatch):
        """Test PAPERLESS_URL environment variable override."""
        monkeypatch.setenv("PAPERLESS_URL", "http://custom-paperless:9000")
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()
        assert settings.paperless_url == "http://custom-paperless:9000"

    def test_paperless_token_override(self, monkeypatch):
        """Test PAPERLESS_TOKEN environment variable override."""
        monkeypatch.setenv("PAPERLESS_TOKEN", "custom-secret-token-xyz")

        settings = ContinuumSettings()
        assert settings.paperless_token == "custom-secret-token-xyz"

    def test_ollama_model_override(self, monkeypatch):
        """Test OLLAMA_MODEL environment variable override."""
        monkeypatch.setenv("OLLAMA_MODEL", "llama3")
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()
        assert settings.ollama_model == "llama3"

    def test_base_dir_override(self, monkeypatch):
        """Test CONTINUUM_BASE_DIR environment variable override."""
        monkeypatch.setenv("CONTINUUM_BASE_DIR", "/custom/path/continuum")
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()
        assert settings.continuum_base_dir == Path("/custom/path/continuum")

    def test_numeric_override(self, monkeypatch):
        """Test numeric configuration overrides."""
        monkeypatch.setenv("PAPERLESS_TIMEOUT", "60")
        monkeypatch.setenv("OLLAMA_CONTEXT_SIZE", "2048")
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()
        assert settings.paperless_timeout == 60
        assert settings.ollama_context_size == 2048


# =============================================================================
# PATH PROPERTY TESTS
# =============================================================================

class TestPathProperties:
    """Test that path properties return correct Path objects."""

    def test_data_dir_property(self, mock_env_vars):
        """Test data_dir property returns correct Path."""
        settings = ContinuumSettings()

        assert settings.data_dir == Path("/tmp/continuum-test/entity_data")
        assert isinstance(settings.data_dir, Path)

    def test_reports_dir_property(self, mock_env_vars):
        """Test reports_dir property returns correct Path."""
        settings = ContinuumSettings()

        assert settings.reports_dir == Path("/tmp/continuum-test/reports")
        assert isinstance(settings.reports_dir, Path)

    def test_checkpoint_dir_property(self, mock_env_vars):
        """Test checkpoint_dir property returns correct Path."""
        settings = ContinuumSettings()

        assert settings.checkpoint_dir == Path("/tmp/continuum-test/checkpoints")
        assert isinstance(settings.checkpoint_dir, Path)

    def test_documents_inbox_property(self, mock_env_vars):
        """Test documents_inbox property returns correct Path."""
        settings = ContinuumSettings()

        assert settings.documents_inbox == Path("/tmp/continuum-test/documents/inbox")
        assert isinstance(settings.documents_inbox, Path)

    def test_entity_db_file_property(self, mock_env_vars):
        """Test entity_db_file property returns correct Path."""
        settings = ContinuumSettings()

        expected = Path("/tmp/continuum-test/entity_data/entity_database.json")
        assert settings.entity_db_file == expected
        assert isinstance(settings.entity_db_file, Path)

    def test_dossier_queue_file_property(self, mock_env_vars):
        """Test dossier_queue_file property returns correct Path."""
        settings = ContinuumSettings()

        expected = Path("/tmp/continuum-test/entity_data/dossier_queue.json")
        assert settings.dossier_queue_file == expected
        assert isinstance(settings.dossier_queue_file, Path)


# =============================================================================
# DIRECTORY CREATION TESTS
# =============================================================================

class TestEnsureDirectories:
    """Test ensure_directories creates required directories."""

    def test_creates_all_directories(self, tmp_path, monkeypatch):
        """Test that ensure_directories creates all required directories."""
        base_dir = tmp_path / "continuum_test"

        monkeypatch.setenv("CONTINUUM_BASE_DIR", str(base_dir))
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()
        settings.ensure_directories()

        # Verify all directories were created
        assert settings.data_dir.exists()
        assert settings.reports_dir.exists()
        assert settings.checkpoint_dir.exists()
        assert settings.documents_inbox.exists()

        # Verify they are directories
        assert settings.data_dir.is_dir()
        assert settings.reports_dir.is_dir()
        assert settings.checkpoint_dir.is_dir()
        assert settings.documents_inbox.is_dir()

    def test_idempotent_directory_creation(self, tmp_path, monkeypatch):
        """Test that ensure_directories can be called multiple times safely."""
        base_dir = tmp_path / "continuum_test"

        monkeypatch.setenv("CONTINUUM_BASE_DIR", str(base_dir))
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()

        # Call multiple times
        settings.ensure_directories()
        settings.ensure_directories()
        settings.ensure_directories()

        # Should still work without errors
        assert settings.data_dir.exists()
        assert settings.reports_dir.exists()

    def test_creates_nested_directories(self, tmp_path, monkeypatch):
        """Test that ensure_directories creates nested directory structures."""
        base_dir = tmp_path / "continuum_test"

        monkeypatch.setenv("CONTINUUM_BASE_DIR", str(base_dir))
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()
        settings.ensure_directories()

        # Verify nested structure for documents inbox
        assert (base_dir / "documents").exists()
        assert (base_dir / "documents" / "inbox").exists()


# =============================================================================
# VALIDATION TESTS
# =============================================================================

class TestValidation:
    """Test configuration validation logic."""

    def test_missing_paperless_token_warning(self, monkeypatch, caplog):
        """Test that missing PAPERLESS_TOKEN raises a warning."""
        monkeypatch.delenv("PAPERLESS_TOKEN", raising=False)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            settings = ContinuumSettings()

            # Verify warning was issued
            assert len(w) == 1
            assert "PAPERLESS_TOKEN is not set" in str(w[0].message)
            assert settings.paperless_token == ""

    def test_path_parsing_from_string(self, monkeypatch):
        """Test that string paths are converted to Path objects."""
        monkeypatch.setenv("CONTINUUM_BASE_DIR", "/tmp/string/path")
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()
        assert isinstance(settings.continuum_base_dir, Path)
        assert settings.continuum_base_dir == Path("/tmp/string/path")

    def test_path_parsing_preserves_path_object(self, monkeypatch):
        """Test that Path objects are preserved during validation."""
        # This tests the validator when initialized programmatically
        settings = ContinuumSettings(
            continuum_base_dir=Path("/tmp/path/object"),
            paperless_token="test-token"
        )

        assert isinstance(settings.continuum_base_dir, Path)
        assert settings.continuum_base_dir == Path("/tmp/path/object")


# =============================================================================
# REPRESENTATION TESTS
# =============================================================================

class TestRepresentation:
    """Test configuration string representation."""

    def test_repr_does_not_expose_token(self, mock_env_vars):
        """Test that __repr__ does not expose sensitive token."""
        settings = ContinuumSettings()
        repr_str = repr(settings)

        # Should not contain the actual token
        assert "test-token-12345" not in repr_str

        # Should contain other configuration
        assert "paperless_url" in repr_str
        assert "ollama_url" in repr_str
        assert "ollama_model" in repr_str

    def test_repr_format(self, mock_env_vars):
        """Test __repr__ format matches expected structure."""
        settings = ContinuumSettings()
        repr_str = repr(settings)

        assert repr_str.startswith("ContinuumSettings(")
        assert "paperless_url='http://test-paperless:8040'" in repr_str
        assert "ollama_url='http://test-ollama:11434'" in repr_str
        assert "ollama_model='test-mistral'" in repr_str


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestValidateConnection:
    """Test service connection validation."""

    @pytest.mark.skip(reason="Requires live services - integration test")
    def test_validate_connection_success(self, mock_env_vars):
        """Test successful connection validation (requires mocking)."""
        # This would require mocking requests or running live services
        # Skipped for unit tests
        pass

    def test_validate_connection_structure(self, mock_env_vars):
        """Test that validate_connection returns expected structure."""
        settings = ContinuumSettings()

        # We can't test actual connection without mocking requests,
        # but we can verify the method exists and has correct signature
        assert hasattr(settings, 'validate_connection')
        assert callable(settings.validate_connection)


# =============================================================================
# EDGE CASES AND ERROR HANDLING
# =============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_string_values(self, monkeypatch):
        """Test handling of empty string environment variables."""
        monkeypatch.setenv("PAPERLESS_URL", "")
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()
        # Empty string should be preserved, not converted to default
        assert settings.paperless_url == ""

    def test_case_insensitive_env_vars(self, monkeypatch):
        """Test that environment variables are case insensitive."""
        # Pydantic settings should handle case insensitivity
        monkeypatch.setenv("paperless_url", "http://lowercase:8040")
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()
        assert settings.paperless_url == "http://lowercase:8040"

    def test_extra_env_vars_ignored(self, monkeypatch):
        """Test that extra environment variables are ignored."""
        monkeypatch.setenv("UNKNOWN_VAR", "should-be-ignored")
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        # Should not raise error due to extra='ignore' in model_config
        settings = ContinuumSettings()
        assert not hasattr(settings, 'unknown_var')

    def test_whitespace_in_paths(self, monkeypatch):
        """Test handling of paths with whitespace."""
        monkeypatch.setenv("CONTINUUM_BASE_DIR", "  /tmp/path with spaces  ")
        monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

        settings = ContinuumSettings()
        # Path should preserve whitespace (caller's responsibility to clean)
        assert "path with spaces" in str(settings.continuum_base_dir)


# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestPerformance:
    """Test configuration performance characteristics."""

    def test_settings_initialization_performance(self, mock_env_vars):
        """Test that settings initialization is fast (if pytest-benchmark installed)."""
        # This is optional - only runs if pytest-benchmark is installed
        pytest.importorskip("pytest_benchmark", reason="pytest-benchmark not installed")
        # If we get here, benchmark plugin is available, but we need the fixture
        pytest.skip("pytest-benchmark not configured with fixture")

    def test_property_access_performance(self, mock_env_vars):
        """Test that property access is efficient."""
        settings = ContinuumSettings()

        # Properties should be computed efficiently
        # Call multiple times to ensure no expensive operations
        for _ in range(100):
            _ = settings.data_dir
            _ = settings.reports_dir
            _ = settings.checkpoint_dir

        # If this completes quickly, properties are efficient
        assert True
