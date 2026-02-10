# Testing Quick Start Guide

## Installation

```bash
# From project root (WoodsDen local)
cd "C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum"

# Install all dependencies (includes test dependencies)
pip install -r requirements.txt
```

## Running Tests

### Run All Working Tests

```bash
# Run config tests (all passing)
pytest tests/test_config.py -v
```

### Run Specific Tests

```bash
# Run a specific test class
pytest tests/test_config.py::TestDefaultValues -v

# Run a specific test method
pytest tests/test_config.py::TestDefaultValues::test_paperless_defaults -v
```

### With Coverage Report

```bash
# Terminal coverage report
pytest tests/test_config.py --cov=scripts/lib --cov-report=term-missing

# HTML coverage report
pytest tests/test_config.py --cov=scripts/lib --cov-report=html
# Then open: htmlcov/index.html
```

### Verbose Output

```bash
# Very verbose
pytest tests/test_config.py -vv

# Show print statements
pytest tests/test_config.py -s

# Show local variables on failure
pytest tests/test_config.py -l
```

## Test Examples

### Example: Test Default Configuration

```python
def test_paperless_defaults(self, mock_env_vars):
    """Test Paperless default configuration values."""
    settings = ContinuumSettings()

    assert settings.paperless_url == "http://test-paperless:8040"
    assert settings.paperless_token == "test-token-12345"
    assert settings.paperless_timeout == 30
```

### Example: Test Environment Override

```python
def test_ollama_model_override(self, monkeypatch):
    """Test OLLAMA_MODEL environment variable override."""
    monkeypatch.setenv("OLLAMA_MODEL", "llama3")
    monkeypatch.setenv("PAPERLESS_TOKEN", "test-token")

    settings = ContinuumSettings()
    assert settings.ollama_model == "llama3"
```

### Example: Test Directory Creation

```python
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
```

## Writing New Tests

### 1. Add Test to Existing File

```python
# In tests/test_config.py

class TestNewFeature:
    """Test suite for new feature."""

    def test_feature_works(self, mock_env_vars):
        """Test that new feature returns expected value."""
        # Arrange
        settings = ContinuumSettings()

        # Act
        result = settings.new_feature

        # Assert
        assert result == "expected_value"
```

### 2. Use Fixtures

```python
def test_with_temp_directory(self, temp_continuum_dir):
    """Test using temporary directory fixture."""
    # temp_continuum_dir is a Path object with subdirectories created
    assert temp_continuum_dir.exists()
    assert (temp_continuum_dir / "entity_data").exists()
```

### 3. Test Error Handling

```python
def test_missing_token_warning(self, monkeypatch, caplog):
    """Test that missing PAPERLESS_TOKEN raises warning."""
    monkeypatch.delenv("PAPERLESS_TOKEN", raising=False)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        settings = ContinuumSettings()

        assert len(w) == 1
        assert "PAPERLESS_TOKEN is not set" in str(w[0].message)
```

## TDD Workflow

### Red-Green-Refactor Cycle

```bash
# 1. RED: Write failing test
pytest tests/test_config.py::TestNewFeature::test_new_config_value -v
# Expected: FAIL (feature doesn't exist yet)

# 2. GREEN: Implement minimal code to pass
# Edit scripts/lib/config.py to add feature

pytest tests/test_config.py::TestNewFeature::test_new_config_value -v
# Expected: PASS

# 3. REFACTOR: Improve code while keeping test green
# Refactor implementation, run test again to ensure still passing
```

## Common Fixtures

### Environment Variables

```python
def test_with_env_vars(self, mock_env_vars):
    """All environment variables are mocked."""
    # mock_env_vars provides:
    # - PAPERLESS_URL
    # - PAPERLESS_TOKEN
    # - OLLAMA_URL
    # - OLLAMA_MODEL
    # - CONTINUUM_BASE_DIR
    # - etc.
```

### Temporary Directories

```python
def test_with_temp_dir(self, temp_continuum_dir):
    """Use temporary directory for file operations."""
    # temp_continuum_dir is a Path with structure:
    # - entity_data/
    # - reports/
    # - checkpoints/
    # - documents/inbox/
```

### Monkeypatch (Override anything)

```python
def test_custom_override(self, monkeypatch):
    """Override specific environment variables."""
    monkeypatch.setenv("CUSTOM_VAR", "custom_value")
    monkeypatch.delenv("UNWANTED_VAR", raising=False)
```

## Expected Output

### Successful Test Run

```
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.0.2, pluggy-1.6.0
collected 31 items

tests/test_config.py::TestDefaultValues::test_paperless_defaults PASSED [  3%]
tests/test_config.py::TestDefaultValues::test_ollama_defaults PASSED [  6%]
tests/test_config.py::TestDefaultValues::test_directory_defaults PASSED [  9%]
...
======================== 31 passed, 1 skipped in 2.81s ========================
```

### With Coverage

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
scripts/lib/config.py      77     17    78%   228-258
-----------------------------------------------------
TOTAL                      77     17    78%
```

## Troubleshooting

### Import Errors

```bash
# Ensure you're in project root (WoodsDen local)
cd "C:\Users\Xx LilMan xX\Documents\Claude Docs\Continuum"

# Verify Python can find modules
python -c "import scripts.lib.config"
```

### Missing Dependencies

```bash
# Install test dependencies
pip install pytest pytest-cov responses pytest-mock

# Or install everything
pip install -r requirements.txt
```

### Tests Not Found

```bash
# Explicitly specify test directory
pytest tests/ -v

# Or specific file
pytest tests/test_config.py -v
```

## Best Practices

1. **Run tests before committing**: `pytest tests/test_config.py -v`
2. **Write tests first**: TDD approach ensures better design
3. **One assertion per test**: Keep tests focused
4. **Use descriptive names**: `test_paperless_url_override_works`
5. **Test edge cases**: Empty strings, None values, errors
6. **Keep tests fast**: Mock external dependencies
7. **Use fixtures**: Reduce duplication

## Performance

All config tests run in under 3 seconds:

```bash
pytest tests/test_config.py -v
# ======================== 31 passed in 2.81s ========================
```

## Next Steps

1. Read full documentation: `tests/README.md`
2. Read infrastructure summary: `tests/TESTING_INFRASTRUCTURE_SUMMARY.md`
3. Try writing a new test following the examples
4. Run tests before making changes (establish baseline)
5. Use TDD for new features

## Resources

- Full documentation: `tests/README.md`
- Pytest docs: https://docs.pytest.org/
- Fixtures guide: https://docs.pytest.org/en/stable/fixture.html
- Coverage docs: https://pytest-cov.readthedocs.io/

---

**Quick Commands Reference**

```bash
# Run config tests (fast, all pass)
pytest tests/test_config.py -v

# With coverage
pytest tests/test_config.py --cov=scripts/lib --cov-report=term-missing

# Specific test
pytest tests/test_config.py::TestDefaultValues::test_paperless_defaults -v

# Very verbose with locals
pytest tests/test_config.py -vv -l

# Generate HTML coverage
pytest tests/test_config.py --cov=scripts/lib --cov-report=html
```
