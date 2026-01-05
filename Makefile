# =============================================================================
# The Continuum Report - Makefile
# =============================================================================
# Modern Python development workflow automation (2024/2025 best practices)
#
# Usage:
#   make help      - Show available commands
#   make setup     - Set up development environment
#   make all       - Run all checks (lint, format-check, typecheck, test)
#   make lint      - Run ruff linter
#   make format    - Auto-format code with ruff
#   make typecheck - Run mypy type checker
#   make test      - Run pytest test suite
#
# =============================================================================

# Shell settings
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

# Python settings
PYTHON := python3
PIP := $(PYTHON) -m pip
UV := uv

# Directories
SRC_DIRS := scripts src
TEST_DIR := tests
COVERAGE_DIR := htmlcov

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m  # No Color

# =============================================================================
# HELP
# =============================================================================

.PHONY: help
help:  ## Show this help message
	@echo ""
	@echo "$(BLUE)The Continuum Report - Development Commands$(NC)"
	@echo "=============================================="
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make $(GREEN)<target>$(NC)\n\n"} \
		/^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2 } \
		/^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) }' $(MAKEFILE_LIST)
	@echo ""

##@ Development Setup

.PHONY: setup
setup: install-deps install-hooks  ## Set up development environment (install deps + hooks)
	@echo "$(GREEN)Development environment setup complete!$(NC)"

.PHONY: install-deps
install-deps:  ## Install all dependencies (including dev)
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@if command -v uv &> /dev/null; then \
		echo "Using uv (fast mode)..."; \
		$(UV) pip install -e ".[dev]"; \
	else \
		echo "Using pip..."; \
		$(PIP) install -e ".[dev]"; \
	fi
	@echo "$(GREEN)Dependencies installed!$(NC)"

.PHONY: install-hooks
install-hooks:  ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "$(GREEN)Pre-commit hooks installed!$(NC)"

.PHONY: update-hooks
update-hooks:  ## Update pre-commit hooks to latest versions
	@echo "$(BLUE)Updating pre-commit hooks...$(NC)"
	pre-commit autoupdate
	@echo "$(GREEN)Hooks updated!$(NC)"

##@ Code Quality

.PHONY: lint
lint:  ## Run ruff linter on all Python files
	@echo "$(BLUE)Running ruff linter...$(NC)"
	ruff check $(SRC_DIRS) $(TEST_DIR) --output-format=full
	@echo "$(GREEN)Linting complete!$(NC)"

.PHONY: lint-fix
lint-fix:  ## Run ruff linter with auto-fix
	@echo "$(BLUE)Running ruff linter with auto-fix...$(NC)"
	ruff check $(SRC_DIRS) $(TEST_DIR) --fix
	@echo "$(GREEN)Linting with fixes complete!$(NC)"

.PHONY: format
format:  ## Auto-format code with ruff formatter
	@echo "$(BLUE)Formatting code with ruff...$(NC)"
	ruff format $(SRC_DIRS) $(TEST_DIR)
	@echo "$(GREEN)Formatting complete!$(NC)"

.PHONY: format-check
format-check:  ## Check code formatting (no changes)
	@echo "$(BLUE)Checking code formatting...$(NC)"
	ruff format --check $(SRC_DIRS) $(TEST_DIR)
	@echo "$(GREEN)Format check complete!$(NC)"

.PHONY: typecheck
typecheck:  ## Run mypy type checker
	@echo "$(BLUE)Running mypy type checker...$(NC)"
	mypy $(SRC_DIRS) --config-file pyproject.toml
	@echo "$(GREEN)Type checking complete!$(NC)"

.PHONY: typecheck-strict
typecheck-strict:  ## Run mypy with strict mode on all files
	@echo "$(BLUE)Running mypy in strict mode...$(NC)"
	mypy $(SRC_DIRS) --strict --config-file pyproject.toml
	@echo "$(GREEN)Strict type checking complete!$(NC)"

.PHONY: security
security:  ## Run security checks (bandit)
	@echo "$(BLUE)Running security checks...$(NC)"
	bandit -r $(SRC_DIRS) -c pyproject.toml
	@echo "$(GREEN)Security checks complete!$(NC)"

.PHONY: secrets
secrets:  ## Scan for secrets in code
	@echo "$(BLUE)Scanning for secrets...$(NC)"
	detect-secrets scan --baseline .secrets.baseline
	@echo "$(GREEN)Secret scan complete!$(NC)"

.PHONY: secrets-baseline
secrets-baseline:  ## Create/update secrets baseline
	@echo "$(BLUE)Creating secrets baseline...$(NC)"
	detect-secrets scan > .secrets.baseline
	@echo "$(GREEN)Secrets baseline created!$(NC)"

##@ Testing

.PHONY: test
test:  ## Run pytest test suite
	@echo "$(BLUE)Running tests...$(NC)"
	pytest $(TEST_DIR) -v
	@echo "$(GREEN)Tests complete!$(NC)"

.PHONY: test-fast
test-fast:  ## Run tests excluding slow tests
	@echo "$(BLUE)Running fast tests...$(NC)"
	pytest $(TEST_DIR) -v -m "not slow"
	@echo "$(GREEN)Fast tests complete!$(NC)"

.PHONY: test-cov
test-cov:  ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest $(TEST_DIR) -v --cov=src --cov=scripts --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)Coverage report generated in $(COVERAGE_DIR)/$(NC)"

.PHONY: test-unit
test-unit:  ## Run only unit tests
	@echo "$(BLUE)Running unit tests...$(NC)"
	pytest $(TEST_DIR) -v -m "unit"

.PHONY: test-integration
test-integration:  ## Run only integration tests
	@echo "$(BLUE)Running integration tests...$(NC)"
	pytest $(TEST_DIR) -v -m "integration"

##@ Combined Commands

.PHONY: all
all: lint format-check typecheck test  ## Run all checks (lint, format-check, typecheck, test)
	@echo "$(GREEN)All checks passed!$(NC)"

.PHONY: check
check: lint format-check typecheck  ## Run all static checks (no tests)
	@echo "$(GREEN)All static checks passed!$(NC)"

.PHONY: fix
fix: lint-fix format  ## Auto-fix all issues (lint + format)
	@echo "$(GREEN)All auto-fixes applied!$(NC)"

.PHONY: ci
ci: lint format-check typecheck test-cov  ## Run full CI pipeline
	@echo "$(GREEN)CI pipeline complete!$(NC)"

.PHONY: pre-commit
pre-commit:  ## Run pre-commit on all files
	@echo "$(BLUE)Running pre-commit on all files...$(NC)"
	pre-commit run --all-files

##@ Cleanup

.PHONY: clean
clean:  ## Remove build artifacts and caches
	@echo "$(BLUE)Cleaning up...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf $(COVERAGE_DIR)/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

.PHONY: clean-all
clean-all: clean  ## Remove all generated files including venv
	@echo "$(BLUE)Deep cleaning...$(NC)"
	rm -rf .venv/
	rm -rf venv/
	@echo "$(GREEN)Deep cleanup complete!$(NC)"

##@ Documentation

.PHONY: docs
docs:  ## Build documentation (if using mkdocs/sphinx)
	@echo "$(BLUE)Building documentation...$(NC)"
	@echo "$(YELLOW)Note: Documentation build not configured yet$(NC)"

##@ Docker

.PHONY: docker-build
docker-build:  ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	docker build -t continuum-report:latest .

.PHONY: docker-run
docker-run:  ## Run Docker container
	docker run -it --rm continuum-report:latest

##@ Utilities

.PHONY: version
version:  ## Show tool versions
	@echo "$(BLUE)Tool Versions:$(NC)"
	@echo "Python:     $$($(PYTHON) --version)"
	@echo "Ruff:       $$(ruff --version)"
	@echo "Mypy:       $$(mypy --version)"
	@echo "Pytest:     $$(pytest --version | head -1)"
	@echo "Pre-commit: $$(pre-commit --version)"

.PHONY: outdated
outdated:  ## Check for outdated dependencies
	@echo "$(BLUE)Checking for outdated dependencies...$(NC)"
	@if command -v uv &> /dev/null; then \
		$(UV) pip list --outdated; \
	else \
		$(PIP) list --outdated; \
	fi
