# Contributing to The Continuum Report

Thank you for your interest in contributing to The Continuum Report! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Testing](#testing)
- [Pull Request Checklist](#pull-request-checklist)
- [Commit Message Guidelines](#commit-message-guidelines)

---

## Development Setup

### Prerequisites

- Python 3.10 or higher (3.11+ recommended)
- Git
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/continuum-report/continuum.git
cd continuum

# Create virtual environment and install dependencies
# Option 1: Using uv (recommended - much faster)
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv pip install -e ".[dev]"

# Option 2: Using pip
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -e ".[dev]"

# Install pre-commit hooks (REQUIRED)
pre-commit install
pre-commit install --hook-type commit-msg

# Verify setup
make version
make check
```

### Using the Makefile

The project includes a comprehensive Makefile for common tasks:

```bash
make help          # Show all available commands
make setup         # Full development setup
make lint          # Run linter
make format        # Auto-format code
make typecheck     # Run type checker
make test          # Run tests
make all           # Run all checks
```

---

## Code Style Guidelines

We follow modern Python best practices (2024/2025 standards) using automated tooling.

### Tooling

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **Ruff** | Linting + formatting (replaces black, isort, flake8) | `pyproject.toml` |
| **MyPy** | Static type checking | `pyproject.toml` |
| **Pytest** | Testing framework | `pyproject.toml` |
| **Pre-commit** | Git hooks automation | `.pre-commit-config.yaml` |
| **detect-secrets** | Secret detection | `.pre-commit-config.yaml` |

### Python Style

1. **Line Length**: 100 characters maximum
2. **Quotes**: Double quotes for strings (`"hello"`)
3. **Imports**: Sorted by ruff (isort-compatible)
4. **Type Hints**: Required for all new code

### Type Hints

All new code must include type hints:

```python
# Good
def process_document(doc_id: int, content: str) -> dict[str, Any]:
    """Process a document and return results."""
    ...

# Bad - missing type hints
def process_document(doc_id, content):
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def fetch_entity(entity_id: int, include_relations: bool = False) -> Entity:
    """Fetch an entity from the database.

    Args:
        entity_id: The unique identifier of the entity.
        include_relations: Whether to include related entities.

    Returns:
        The requested Entity object.

    Raises:
        EntityNotFoundError: If the entity doesn't exist.
    """
    ...
```

### Import Organization

Imports are automatically sorted by ruff:

```python
# Standard library
import json
import os
from datetime import datetime
from typing import Any, Optional

# Third-party
import requests
from pydantic import BaseModel

# First-party (this project)
from lib.config import settings
from lib.logging_config import get_logger
```

---

## Pre-commit Hooks

Pre-commit hooks run automatically on every commit to ensure code quality.

### Setup

```bash
# Install hooks (run once after cloning)
pre-commit install
pre-commit install --hook-type commit-msg
```

### Hooks Included

1. **Whitespace/formatting**: Trailing whitespace, end-of-file, line endings
2. **File validation**: YAML, TOML, JSON syntax
3. **Git hygiene**: Merge conflicts, large files, protected branches
4. **Ruff linting**: Python linting with auto-fix
5. **Ruff formatting**: Code formatting
6. **MyPy**: Static type checking
7. **detect-secrets**: Scan for accidentally committed secrets
8. **Bandit**: Security-focused static analysis
9. **Codespell**: Spell checking

### Running Manually

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run mypy --all-files

# Skip hooks temporarily (use sparingly!)
git commit --no-verify -m "WIP: temporary commit"
```

### Updating Hooks

```bash
# Update to latest versions
pre-commit autoupdate

# Or use make
make update-hooks
```

---

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run fast tests only (skip slow/integration)
make test-fast

# Run specific test file
pytest tests/test_config.py -v

# Run specific test
pytest tests/test_config.py::test_settings_load -v
```

### Test Markers

```python
import pytest

@pytest.mark.unit
def test_parse_entity():
    """Unit test - fast, no external dependencies."""
    ...

@pytest.mark.integration
def test_paperless_connection():
    """Integration test - requires external services."""
    ...

@pytest.mark.slow
def test_full_pipeline():
    """Slow test - takes significant time."""
    ...
```

### Writing Tests

```python
"""Tests for entity discovery module."""
import pytest
from unittest.mock import Mock, patch

from scripts.entity_discovery import extract_entities


class TestExtractEntities:
    """Tests for the extract_entities function."""

    def test_extracts_person_names(self):
        """Should extract person names from text."""
        text = "John Smith met with Jane Doe yesterday."
        result = extract_entities(text)

        assert "John Smith" in result["people"]
        assert "Jane Doe" in result["people"]

    def test_handles_empty_text(self):
        """Should return empty results for empty text."""
        result = extract_entities("")

        assert result["people"] == []
        assert result["organizations"] == []

    @pytest.mark.integration
    def test_with_real_api(self, api_client):
        """Integration test with real API."""
        ...
```

---

## Pull Request Checklist

Before submitting a PR, ensure:

### Code Quality

- [ ] All pre-commit hooks pass (`pre-commit run --all-files`)
- [ ] Ruff linting passes (`make lint`)
- [ ] Code is properly formatted (`make format-check`)
- [ ] Type checking passes (`make typecheck`)
- [ ] No secrets in code (`detect-secrets scan`)

### Testing

- [ ] All existing tests pass (`make test`)
- [ ] New tests added for new functionality
- [ ] Test coverage maintained or improved

### Documentation

- [ ] Code includes appropriate docstrings
- [ ] Complex logic has inline comments
- [ ] README updated if needed
- [ ] CHANGELOG updated for significant changes

### Git

- [ ] Branch is up to date with main
- [ ] Commits are atomic and well-described
- [ ] No merge commits (rebase preferred)
- [ ] PR title follows conventional commits format

---

## Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |
| `ci` | CI/CD changes |

### Examples

```bash
# Feature
feat(entity): add support for organization extraction

# Bug fix
fix(api): handle timeout errors in Paperless client

# Documentation
docs: update installation instructions

# Refactoring
refactor(config): use Pydantic settings for validation

# Tests
test(pipeline): add integration tests for batch processing
```

---

## Additional Resources

- [Python Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pre-commit Documentation](https://pre-commit.com/)

---

## Questions?

If you have questions about contributing, feel free to:

1. Open an issue for discussion
2. Check existing issues for similar questions
3. Review the project documentation

Thank you for contributing!
