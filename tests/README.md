# The Continuum Report - Test Suite

Comprehensive test coverage for all library components in The Continuum Report project.

## Overview

This test suite provides robust testing infrastructure with:
- **100% mocked external dependencies** (no live API calls required)
- **High test coverage** for all core library modules
- **Fast execution** (all tests run in seconds)
- **Clear test organization** following best practices

## Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── conftest.py                    # Shared pytest fixtures and configuration
├── test_config.py                 # Configuration and settings tests
├── test_paperless_client.py       # Paperless API client tests (mocked)
└── test_ollama_client.py          # Ollama LLM client tests (mocked)
```

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test File

```bash
pytest tests/test_config.py
pytest tests/test_paperless_client.py
pytest tests/test_ollama_client.py
```

### Run Specific Test Class or Method

```bash
# Run a specific test class
pytest tests/test_config.py::TestDefaultValues

# Run a specific test method
pytest tests/test_config.py::TestDefaultValues::test_paperless_defaults
```

### Run with Coverage Report

```bash
# Generate coverage report in terminal
pytest tests/ --cov=scripts/lib --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=scripts/lib --cov-report=html
# Open htmlcov/index.html in browser
```

### Run Only Unit Tests

```bash
pytest tests/ -m unit
```

### Run Verbose Output

```bash
pytest tests/ -v
```

### Run with Detailed Output

```bash
pytest tests/ -vv
```

## Test Coverage

### test_config.py - Configuration Tests

Tests for `scripts/lib/config.py`:

- **Default Values**: Verify all configuration defaults load correctly
- **Environment Overrides**: Test environment variable overrides
- **Path Properties**: Ensure path properties return Path objects
- **Directory Creation**: Test `ensure_directories()` creates all required dirs
- **Validation**: Test Pydantic validators and warnings
- **Representation**: Ensure `__repr__()` doesn't expose secrets

**Key Test Classes:**
- `TestDefaultValues` - Default configuration values
- `TestEnvironmentOverrides` - Environment variable handling
- `TestPathProperties` - Path property methods
- `TestEnsureDirectories` - Directory creation logic
- `TestValidation` - Configuration validation
- `TestEdgeCases` - Edge cases and error handling

### test_paperless_client.py - Paperless Client Tests

Tests for `scripts/lib/paperless_client.py`:

- **Client Initialization**: Test client setup with various configurations
- **Health Check**: Verify health check functionality
- **Error Handling**: Test all HTTP error codes (401, 403, 404, 500)
- **Document Retrieval**: Test fetching documents and content
- **Pagination**: Test multi-page document retrieval with `get_all_documents()`
- **Search**: Test document search functionality
- **Tags & Types**: Test tag and document type retrieval with caching
- **Dossier Detection**: Test dossier identification logic

**Key Test Classes:**
- `TestClientInitialization` - Client setup
- `TestHealthCheck` - Health check functionality
- `TestErrorHandling` - HTTP error handling (401, 403, 404, 500)
- `TestDocumentRetrieval` - Document fetching
- `TestPagination` - Multi-page retrieval
- `TestSearch` - Search functionality
- `TestTagsAndDocumentTypes` - Metadata retrieval
- `TestContextManager` - Context manager behavior

### test_ollama_client.py - Ollama Client Tests

Tests for `scripts/lib/ollama_client.py`:

- **Client Initialization**: Test client setup and configuration
- **Health Check**: Verify Ollama server connectivity
- **Generate**: Test basic text generation with various parameters
- **Streaming**: Test streaming response handling
- **Entity Extraction**: Test entity extraction with JSON parsing
- **Summarization**: Test document summarization
- **Connection Analysis**: Test entity relationship analysis
- **Model Management**: Test model listing and existence checking
- **Memory Management**: Test model unloading and auto-unload
- **Error Handling**: Test timeout, connection errors, model not found

**Key Test Classes:**
- `TestClientInitialization` - Client setup
- `TestHealthCheck` - Server connectivity
- `TestGenerate` - Text generation
- `TestGenerateErrorHandling` - Error handling (404, 500, timeout)
- `TestGenerateStream` - Streaming responses
- `TestEntityExtraction` - Entity extraction
- `TestSummarization` - Text summarization
- `TestConnectionAnalysis` - Relationship analysis
- `TestModelManagement` - Model listing
- `TestMemoryManagement` - Model unloading

## Test Fixtures (conftest.py)

### Environment Fixtures

- `mock_env_vars` - Mock environment variables for all configuration
- `temp_continuum_dir` - Temporary directory structure for file tests
- `reset_environment` - Auto-reset environment between tests

### Paperless API Fixtures

- `mock_paperless_document` - Sample document metadata
- `mock_paperless_documents_page` - Paginated documents response
- `mock_paperless_tags` - Sample tags response
- `mock_paperless_document_types` - Sample document types
- `mock_paperless_api` - responses.RequestsMock for API mocking

### Ollama API Fixtures

- `mock_ollama_generate_response` - Sample generation response
- `mock_ollama_models` - Sample models list
- `mock_ollama_stream_response` - Sample streaming chunks
- `mock_ollama_api` - responses.RequestsMock for API mocking
- `mock_entity_extraction_response` - Sample entity extraction JSON
- `mock_connection_analysis_response` - Sample connection analysis

### Utility Fixtures

- `sample_document_text` - Sample document text for LLM tests
- `pagination_params` - Parametrized pagination configurations
- `error_responses` - Parametrized error responses

## Writing New Tests

### Test Naming Convention

```python
class TestFeatureName:
    """Test suite for specific feature."""

    def test_specific_behavior(self):
        """Test that specific behavior works correctly."""
        # Arrange
        # Act
        # Assert
```

### Using Mocked API Responses

```python
import responses

@responses.activate
def test_api_call(self, mock_env_vars):
    """Test API call with mocked response."""
    responses.add(
        responses.GET,
        "http://test-paperless:8040/api/documents/123/",
        json={"id": 123, "title": "Test"},
        status=200
    )

    client = PaperlessClient()
    doc = client.get_document(123)

    assert doc["id"] == 123
```

### Using Fixtures

```python
def test_with_fixture(self, mock_env_vars, mock_paperless_document):
    """Test using pre-configured fixtures."""
    assert mock_paperless_document["id"] == 123
```

## Test-Driven Development (TDD)

This test suite is designed to support TDD workflows:

1. **Write failing test first** - Define expected behavior
2. **Run test and verify failure** - Ensure test fails for right reason
3. **Implement minimal code** - Make test pass
4. **Run test and verify pass** - Confirm implementation works
5. **Refactor** - Improve code while tests provide safety net

### TDD Example

```python
# 1. Write failing test
def test_new_feature_works(self):
    """Test that new feature returns expected result."""
    client = PaperlessClient()
    result = client.new_feature()  # Doesn't exist yet
    assert result == "expected_value"

# 2. Run test (fails with AttributeError)
# 3. Implement new_feature() in paperless_client.py
# 4. Run test (passes)
# 5. Refactor if needed
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov=scripts/lib --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

## Performance

All tests are designed to be fast:

- **No external API calls** - All HTTP requests are mocked
- **No filesystem I/O** (except temp directories)
- **Parallel execution** - Can run with pytest-xdist

```bash
# Run tests in parallel (if pytest-xdist installed)
pytest tests/ -n auto
```

## Debugging Tests

### Run Single Test with Detailed Output

```bash
pytest tests/test_config.py::TestDefaultValues::test_paperless_defaults -vv
```

### Drop into Debugger on Failure

```bash
pytest tests/ --pdb
```

### Show Print Statements

```bash
pytest tests/ -s
```

### Show Local Variables in Failures

```bash
pytest tests/ -l
```

## Coverage Goals

Target coverage metrics:

- **Overall coverage**: > 90%
- **Critical paths**: 100% (authentication, API calls, error handling)
- **Utility functions**: > 80%

View current coverage:

```bash
pytest tests/ --cov=scripts/lib --cov-report=term-missing
```

## Best Practices

1. **Always mock external dependencies** - No live API calls in unit tests
2. **Test one thing per test** - Keep tests focused and simple
3. **Use descriptive test names** - Clearly state what is being tested
4. **Test edge cases** - Empty inputs, None values, errors
5. **Test error paths** - Ensure errors are handled correctly
6. **Keep tests fast** - All unit tests should complete in < 1 second each
7. **Use fixtures for setup** - Reduce duplication with shared fixtures
8. **Test both success and failure** - Cover happy path and error conditions

## Troubleshooting

### Import Errors

If you get import errors, ensure you're running from the project root:

```bash
# From project root (continuum/)
pytest tests/
```

### Missing Dependencies

Install test dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variable Issues

Tests use `mock_env_vars` fixture which sets all required variables. If tests fail due to missing environment variables, ensure you're using the fixture:

```python
def test_something(self, mock_env_vars):  # Add fixture parameter
    # Test code here
```

## Contributing

When adding new functionality:

1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain > 90% coverage
4. Add new fixtures to conftest.py if needed
5. Update this README with new test information

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [responses library](https://github.com/getsentry/responses)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Pydantic testing](https://docs.pydantic.dev/latest/concepts/testing/)
