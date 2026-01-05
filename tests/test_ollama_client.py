"""
The Continuum Report - Ollama Client Tests

Test suite for ollama_client.py with mocked HTTP responses.
All tests use the responses library to mock API calls.
"""

import json
import pytest
import responses
from requests.exceptions import ConnectionError, Timeout

from scripts.lib.ollama_client import (
    OllamaClient,
    OllamaError,
    OllamaConnectionError,
    OllamaModelError,
    OllamaTimeoutError,
)


# =============================================================================
# CLIENT INITIALIZATION TESTS
# =============================================================================

class TestClientInitialization:
    """Test OllamaClient initialization and configuration."""

    def test_init_with_defaults(self, mock_env_vars):
        """Test client initialization with default settings."""
        client = OllamaClient()

        assert client.base_url == "http://test-ollama:11434"
        assert client.model == "test-mistral"
        assert client.context_size == 1024
        assert client.timeout == 600

    def test_init_with_custom_values(self, mock_env_vars):
        """Test client initialization with custom values."""
        client = OllamaClient(
            base_url="http://custom-ollama:9999",
            model="llama3",
            context_size=2048,
            timeout=300
        )

        assert client.base_url == "http://custom-ollama:9999"
        assert client.model == "llama3"
        assert client.context_size == 2048
        assert client.timeout == 300

    def test_init_strips_trailing_slash(self, mock_env_vars):
        """Test that trailing slash is stripped from base_url."""
        client = OllamaClient(base_url="http://test-ollama:11434/")

        assert client.base_url == "http://test-ollama:11434"
        assert not client.base_url.endswith("/")

    def test_generation_counter_initialized(self, mock_env_vars):
        """Test that generation counter is initialized."""
        client = OllamaClient()

        assert client._generation_count == 0
        assert client._unload_every == 10  # From settings

    def test_session_created(self, mock_env_vars):
        """Test that requests session is created."""
        client = OllamaClient()

        assert client.session is not None


# =============================================================================
# HEALTH CHECK TESTS
# =============================================================================

class TestHealthCheck:
    """Test health check functionality."""

    @responses.activate
    def test_health_check_success(self, mock_env_vars, mock_ollama_models):
        """Test successful health check."""
        responses.add(
            responses.GET,
            "http://test-ollama:11434/api/tags",
            json=mock_ollama_models,
            status=200
        )

        client = OllamaClient()
        assert client.health_check() is True

    @responses.activate
    def test_health_check_failure(self, mock_env_vars):
        """Test failed health check."""
        responses.add(
            responses.GET,
            "http://test-ollama:11434/api/tags",
            json={"error": "Server error"},
            status=500
        )

        client = OllamaClient()
        assert client.health_check() is False

    @responses.activate
    def test_health_check_connection_error(self, mock_env_vars):
        """Test health check with connection error."""
        responses.add(
            responses.GET,
            "http://test-ollama:11434/api/tags",
            body=ConnectionError("Connection refused")
        )

        client = OllamaClient()
        assert client.health_check() is False


# =============================================================================
# GENERATE METHOD TESTS
# =============================================================================

class TestGenerate:
    """Test basic text generation functionality."""

    @responses.activate
    def test_generate_success(self, mock_env_vars, mock_ollama_generate_response):
        """Test successful text generation."""
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json=mock_ollama_generate_response,
            status=200
        )

        client = OllamaClient()
        response = client.generate("What is OSINT?")

        assert isinstance(response, str)
        assert response == "This is a test response from the LLM model."

    @responses.activate
    def test_generate_with_system_prompt(self, mock_env_vars, mock_ollama_generate_response):
        """Test generation with system prompt."""
        def request_callback(request):
            payload = json.loads(request.body)
            assert "system" in payload
            assert payload["system"] == "You are a helpful assistant."
            return (200, {}, json.dumps(mock_ollama_generate_response))

        responses.add_callback(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            callback=request_callback
        )

        client = OllamaClient()
        response = client.generate(
            "What is OSINT?",
            system="You are a helpful assistant."
        )

        assert isinstance(response, str)

    @responses.activate
    def test_generate_with_temperature(self, mock_env_vars, mock_ollama_generate_response):
        """Test generation with custom temperature."""
        def request_callback(request):
            payload = json.loads(request.body)
            assert payload["options"]["temperature"] == 0.3
            return (200, {}, json.dumps(mock_ollama_generate_response))

        responses.add_callback(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            callback=request_callback
        )

        client = OllamaClient()
        response = client.generate("Summarize this", temperature=0.3)

        assert isinstance(response, str)

    @responses.activate
    def test_generate_with_max_tokens(self, mock_env_vars, mock_ollama_generate_response):
        """Test generation with max tokens limit."""
        def request_callback(request):
            payload = json.loads(request.body)
            assert payload["options"]["num_predict"] == 100
            return (200, {}, json.dumps(mock_ollama_generate_response))

        responses.add_callback(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            callback=request_callback
        )

        client = OllamaClient()
        response = client.generate("Brief answer", max_tokens=100)

        assert isinstance(response, str)

    @responses.activate
    def test_generate_increments_counter(self, mock_env_vars, mock_ollama_generate_response):
        """Test that generation increments the counter."""
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json=mock_ollama_generate_response,
            status=200
        )

        client = OllamaClient()
        assert client._generation_count == 0

        client.generate("Test prompt")
        assert client._generation_count == 1


# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================

class TestGenerateErrorHandling:
    """Test error handling during generation."""

    @responses.activate
    def test_model_not_found_raises_error(self, mock_env_vars):
        """Test that 404 status raises OllamaModelError."""
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json={"error": "model not found"},
            status=404
        )

        client = OllamaClient()
        with pytest.raises(OllamaModelError) as exc_info:
            client.generate("Test prompt")

        assert "not found" in str(exc_info.value).lower()

    @responses.activate
    def test_server_error_raises_ollama_error(self, mock_env_vars):
        """Test that 500 status raises OllamaError."""
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json={"error": "Internal server error"},
            status=500
        )

        client = OllamaClient()
        with pytest.raises(OllamaError) as exc_info:
            client.generate("Test prompt")

        # Retry logic will cause "Max retries exceeded" or "API error 500"
        assert "500" in str(exc_info.value) or "Request failed" in str(exc_info.value)

    @responses.activate
    def test_timeout_raises_timeout_error(self, mock_env_vars):
        """Test that timeout raises OllamaTimeoutError."""
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            body=Timeout("Request timed out")
        )

        client = OllamaClient()
        with pytest.raises(OllamaTimeoutError) as exc_info:
            client.generate("Test prompt")

        assert "timed out" in str(exc_info.value).lower()

    @responses.activate
    def test_connection_error_raises_connection_error(self, mock_env_vars):
        """Test that connection error raises OllamaConnectionError or RetryError after retries."""
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            body=ConnectionError("Connection refused")
        )

        client = OllamaClient()
        # The retry decorator may wrap the exception in RetryError after 3 attempts
        from tenacity import RetryError
        with pytest.raises((OllamaConnectionError, RetryError)) as exc_info:
            client.generate("Test prompt")

        # Check that the error is related to connection
        error_str = str(exc_info.value)
        assert "Cannot connect" in error_str or "Connection" in error_str or "RetryError" in str(type(exc_info.value))


# =============================================================================
# STREAMING TESTS
# =============================================================================

class TestGenerateStream:
    """Test streaming generation functionality."""

    @responses.activate
    def test_generate_stream_success(self, mock_env_vars, mock_ollama_stream_response):
        """Test successful streaming generation."""
        # Mock streaming response
        stream_body = "\n".join([json.dumps(chunk) for chunk in mock_ollama_stream_response])

        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            body=stream_body,
            status=200,
            stream=True
        )

        client = OllamaClient()
        chunks = list(client.generate_stream("Test prompt"))

        # Should receive all non-empty chunks
        assert len(chunks) == 3
        assert chunks[0] == "This "
        assert chunks[1] == "is "
        assert chunks[2] == "streaming."

    @responses.activate
    def test_generate_stream_with_system_prompt(self, mock_env_vars, mock_ollama_stream_response):
        """Test streaming with system prompt."""
        def request_callback(request):
            payload = json.loads(request.body)
            assert "system" in payload
            assert payload["stream"] is True

            stream_body = "\n".join([json.dumps(chunk) for chunk in mock_ollama_stream_response])
            return (200, {}, stream_body)

        responses.add_callback(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            callback=request_callback
        )

        client = OllamaClient()
        chunks = list(client.generate_stream(
            "Test prompt",
            system="You are helpful."
        ))

        assert len(chunks) > 0

    @responses.activate
    def test_generate_stream_timeout(self, mock_env_vars):
        """Test streaming with timeout error."""
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            body=Timeout("Stream timed out")
        )

        client = OllamaClient()
        with pytest.raises(OllamaTimeoutError):
            list(client.generate_stream("Test prompt"))


# =============================================================================
# ENTITY EXTRACTION TESTS
# =============================================================================

class TestEntityExtraction:
    """Test entity extraction functionality."""

    @responses.activate
    def test_extract_entities_success(self, mock_env_vars, mock_entity_extraction_response):
        """Test successful entity extraction."""
        response_json = {
            "response": json.dumps(mock_entity_extraction_response),
            "done": True
        }

        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json=response_json,
            status=200
        )

        client = OllamaClient()
        entities = client.extract_entities("Sample document text about Epstein...")

        assert len(entities) == 3
        assert entities[0]["name"] == "Jeffrey Epstein"
        assert entities[0]["type"] == "Person"
        assert entities[1]["type"] == "Location"

    @responses.activate
    def test_extract_entities_with_custom_types(self, mock_env_vars, mock_entity_extraction_response):
        """Test entity extraction with custom entity types."""
        def request_callback(request):
            payload = json.loads(request.body)
            assert "Person" in payload["prompt"]
            assert "Organization" in payload["prompt"]

            response = {
                "response": json.dumps(mock_entity_extraction_response),
                "done": True
            }
            return (200, {}, json.dumps(response))

        responses.add_callback(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            callback=request_callback
        )

        client = OllamaClient()
        entities = client.extract_entities(
            "Sample text",
            entity_types=["Person", "Organization"]
        )

        assert isinstance(entities, list)

    @responses.activate
    def test_extract_entities_invalid_json_returns_empty(self, mock_env_vars):
        """Test that invalid JSON returns empty list."""
        response_json = {
            "response": "This is not valid JSON at all",
            "done": True
        }

        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json=response_json,
            status=200
        )

        client = OllamaClient()
        entities = client.extract_entities("Sample text")

        assert entities == []

    @responses.activate
    def test_extract_entities_no_json_array_returns_empty(self, mock_env_vars):
        """Test that response without JSON array returns empty list."""
        response_json = {
            "response": "Here are the entities: {not an array}",
            "done": True
        }

        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json=response_json,
            status=200
        )

        client = OllamaClient()
        entities = client.extract_entities("Sample text")

        assert entities == []


# =============================================================================
# SUMMARIZATION TESTS
# =============================================================================

class TestSummarization:
    """Test text summarization functionality."""

    @responses.activate
    def test_summarize_success(self, mock_env_vars):
        """Test successful text summarization."""
        response_json = {
            "response": "This is a concise summary of the provided text.",
            "done": True
        }

        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json=response_json,
            status=200
        )

        client = OllamaClient()
        summary = client.summarize("Long document text here...")

        assert isinstance(summary, str)
        assert "summary" in summary.lower()

    @responses.activate
    def test_summarize_with_custom_length(self, mock_env_vars):
        """Test summarization with custom max length."""
        def request_callback(request):
            payload = json.loads(request.body)
            assert "100 words" in payload["prompt"]

            response = {
                "response": "Brief summary.",
                "done": True
            }
            return (200, {}, json.dumps(response))

        responses.add_callback(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            callback=request_callback
        )

        client = OllamaClient()
        summary = client.summarize("Long text", max_length=100)

        assert isinstance(summary, str)


# =============================================================================
# CONNECTION ANALYSIS TESTS
# =============================================================================

class TestConnectionAnalysis:
    """Test connection analysis between entities."""

    @responses.activate
    def test_analyze_connections_success(self, mock_env_vars, mock_connection_analysis_response):
        """Test successful connection analysis."""
        response_json = {
            "response": json.dumps(mock_connection_analysis_response),
            "done": True
        }

        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json=response_json,
            status=200
        )

        client = OllamaClient()
        analysis = client.analyze_connections(
            "Jeffrey Epstein",
            "Bill Clinton",
            "Flight logs show multiple trips together..."
        )

        assert analysis["relationship"] == "Business associate and frequent travel companion"
        assert analysis["confidence"] == "high"
        assert "evidence" in analysis

    @responses.activate
    def test_analyze_connections_invalid_json(self, mock_env_vars):
        """Test connection analysis with invalid JSON returns default."""
        response_json = {
            "response": "Not valid JSON response",
            "done": True
        }

        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json=response_json,
            status=200
        )

        client = OllamaClient()
        analysis = client.analyze_connections("Entity1", "Entity2", "Context")

        assert analysis["relationship"] == "Unknown"
        assert analysis["confidence"] == "low"
        assert "evidence" in analysis


# =============================================================================
# MODEL MANAGEMENT TESTS
# =============================================================================

class TestModelManagement:
    """Test model listing and management."""

    @responses.activate
    def test_list_models_success(self, mock_env_vars, mock_ollama_models):
        """Test successful model listing."""
        responses.add(
            responses.GET,
            "http://test-ollama:11434/api/tags",
            json=mock_ollama_models,
            status=200
        )

        client = OllamaClient()
        models = client.list_models()

        assert len(models) == 2
        assert models[0]["name"] == "test-mistral"
        assert models[1]["name"] == "llama2"

    @responses.activate
    def test_list_models_error_returns_empty(self, mock_env_vars):
        """Test that error during listing returns empty list."""
        responses.add(
            responses.GET,
            "http://test-ollama:11434/api/tags",
            body=ConnectionError("Connection failed")
        )

        client = OllamaClient()
        models = client.list_models()

        assert models == []

    @responses.activate
    def test_model_exists_true(self, mock_env_vars, mock_ollama_models):
        """Test model_exists returns True for existing model."""
        responses.add(
            responses.GET,
            "http://test-ollama:11434/api/tags",
            json=mock_ollama_models,
            status=200
        )

        client = OllamaClient()
        assert client.model_exists() is True
        assert client.model_exists("llama2") is True

    @responses.activate
    def test_model_exists_false(self, mock_env_vars, mock_ollama_models):
        """Test model_exists returns False for non-existent model."""
        responses.add(
            responses.GET,
            "http://test-ollama:11434/api/tags",
            json=mock_ollama_models,
            status=200
        )

        client = OllamaClient()
        assert client.model_exists("nonexistent-model") is False


# =============================================================================
# MEMORY MANAGEMENT TESTS
# =============================================================================

class TestMemoryManagement:
    """Test memory management and model unloading."""

    @responses.activate
    def test_unload_model_success(self, mock_env_vars):
        """Test successful model unloading."""
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json={"response": "", "done": True},
            status=200
        )

        client = OllamaClient()
        result = client.unload_model()

        assert result is True

        # Verify the request payload
        request_body = json.loads(responses.calls[0].request.body)
        assert request_body["keep_alive"] == 0

    @responses.activate
    def test_unload_model_failure(self, mock_env_vars):
        """Test model unload failure handling."""
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            body=ConnectionError("Connection failed")
        )

        client = OllamaClient()
        result = client.unload_model()

        # Should return False but not raise exception
        assert result is False

    @responses.activate
    def test_auto_unload_after_threshold(self, mock_env_vars, mock_ollama_generate_response):
        """Test automatic model unloading after generation threshold."""
        # Mock both generate and unload endpoints
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json=mock_ollama_generate_response,
            status=200
        )

        client = OllamaClient()
        client._unload_every = 3  # Set low threshold for testing

        # Generate 3 times to trigger unload
        for _ in range(3):
            client.generate("Test prompt")

        # Counter should reset after unload
        assert client._generation_count == 0


# =============================================================================
# CONTEXT MANAGER TESTS
# =============================================================================

class TestContextManager:
    """Test context manager functionality."""

    @responses.activate
    def test_context_manager_unloads_model(self, mock_env_vars):
        """Test that context manager unloads model on exit."""
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json={"response": "", "done": True},
            status=200
        )

        with OllamaClient() as client:
            assert client.session is not None

        # Unload should have been called (verify by checking responses calls)
        assert len(responses.calls) >= 1

    def test_close_method(self, mock_env_vars):
        """Test that close() method works."""
        client = OllamaClient()
        session = client.session

        # close() should not raise error
        client.close()


# =============================================================================
# RETRY LOGIC TESTS
# =============================================================================

class TestRetryLogic:
    """Test retry logic for transient failures."""

    @responses.activate
    def test_generate_retries_on_connection_error(self, mock_env_vars, mock_ollama_generate_response):
        """Test that generate retries on connection errors."""
        # First call fails, second succeeds
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            body=ConnectionError("Connection refused")
        )

        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json=mock_ollama_generate_response,
            status=200
        )

        client = OllamaClient()
        # Should retry and eventually succeed
        response = client.generate("Test prompt")

        assert isinstance(response, str)
        # Verify multiple calls were made
        assert len(responses.calls) == 2


# =============================================================================
# INTEGRATION-STYLE TESTS
# =============================================================================

class TestIntegrationScenarios:
    """Test realistic usage scenarios."""

    @responses.activate
    def test_full_document_processing_workflow(
        self, mock_env_vars, mock_ollama_generate_response, mock_entity_extraction_response
    ):
        """Test complete document processing workflow."""
        # Mock entity extraction
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json={
                "response": json.dumps(mock_entity_extraction_response),
                "done": True
            },
            status=200
        )

        # Mock summarization
        responses.add(
            responses.POST,
            "http://test-ollama:11434/api/generate",
            json={
                "response": "Brief summary of document.",
                "done": True
            },
            status=200
        )

        client = OllamaClient()

        # Extract entities
        entities = client.extract_entities("Document about Epstein...")
        assert len(entities) == 3

        # Summarize document
        summary = client.summarize("Long document text...")
        assert isinstance(summary, str)

        # Verify both calls were made
        assert len(responses.calls) == 2
