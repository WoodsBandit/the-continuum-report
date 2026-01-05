# The Continuum Report - CI/CD Pipeline Guide

This document describes the GitHub Actions CI/CD pipeline for The Continuum Report project.

## Overview

The pipeline implements a comprehensive, secure, and efficient continuous integration and deployment strategy with:

- Automated linting and type checking
- Multi-version Python testing with coverage reporting
- Security scanning and dependency checking
- Docker image building and pushing
- Release automation with versioning
- Performance benchmarking
- Code quality analysis

## Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

**Trigger Events:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**

#### Lint and Type Check
- Runs on: `ubuntu-latest` (15 min timeout)
- Steps:
  - Install dependencies
  - Run Ruff linter with GitHub output format
  - Run Ruff formatter check
  - Run mypy type checker with automatic type stubs installation
- **Caching:** Pip packages cached with hash of requirements.txt and pyproject.toml
- **Parallelization:** Not parallelized (runs first to fail fast)

#### Test (Matrix Strategy)
- Runs on: `ubuntu-latest` (30 min timeout)
- Matrix: Python 3.10, 3.11, 3.12, 3.13
- Steps:
  - Install test dependencies
  - Run pytest with coverage (80% threshold)
  - Upload coverage to Codecov
  - Upload test results as artifacts
  - Upload HTML coverage reports as artifacts
- **Caching:**
  - Pip packages cached per Python version
  - Pytest cache for faster test discovery
- **Artifacts:** Test results and coverage reports retained 30 days

#### Security Scan
- Runs on: `ubuntu-latest` (15 min timeout)
- Steps:
  - Install dependencies and security tools
  - Run Bandit (SAST tool) for security vulnerabilities
  - Check dependencies with Safety and pip-audit
  - Upload Bandit report as artifact
- **Permissions:** security-events write for uploading results

#### Integration Tests
- Runs on: `ubuntu-latest` (30 min timeout)
- Depends on: lint, test jobs
- Steps:
  - Run tests marked with `@pytest.mark.integration`
  - Report coverage metrics

#### Summary
- Runs on: `ubuntu-latest`
- Depends on: All previous jobs
- Creates final status check

### 2. Docker Workflow (`.github/workflows/docker.yml`)

**Trigger Events:**
- Push to `main` branch
- Manual workflow dispatch with optional image push

**Jobs:**

#### Build Docker Image
- Runs on: `ubuntu-latest` (45 min timeout)
- Platforms: linux/amd64, linux/arm64
- Steps:
  - Set up Docker Buildx for multi-platform builds
  - Log in to GitHub Container Registry (GHCR)
  - Extract metadata and version information
  - Build Docker image (multi-platform, no push)
  - Load image for security scanning
  - Run Trivy container vulnerability scanner
  - Push to GHCR (conditional on main branch)
- **Caching:** GitHub Actions build cache for layers
- **Tags:**
  - Semantic versioning (v1.0.0)
  - Branch name
  - Commit SHA
  - "latest" tag on main branch

#### Test Docker Image
- Runs on: `ubuntu-latest` (20 min timeout)
- Depends on: build job
- Steps:
  - Build test image
  - Run basic container tests
  - Check image metadata and layer information

#### Publish Summary
- Creates job summary with build status and image references

### 3. Release Workflow (`.github/workflows/release.yml`)

**Trigger Events:**
- Push to semantic version tags (v1.0.0, v1.2.3-rc1, etc.)
- Manual workflow dispatch with version input

**Jobs:**

#### Validate Release
- Validates version format (semantic versioning)
- Outputs: version, tag for downstream jobs

#### Test
- Runs full test suite before release
- Enforces 80% coverage threshold

#### Build Artifacts
- Runs on: `ubuntu-latest` (30 min timeout)
- Steps:
  - Build Python distribution packages (wheel + sdist)
  - Build multi-platform Docker image
  - Push Docker image with version and latest tags
- **Outputs:** Python packages and Docker image

#### Create GitHub Release
- Creates GitHub release with:
  - Version-specific Docker image tag
  - Latest tag
  - Release notes
  - Artifact attachments
  - Download instructions

#### Publish Summary
- Creates release summary with artifact links

### 4. Security Workflow (`.github/workflows/security.yml`)

**Trigger Events:**
- Push to `main` or `develop` branches
- Pull requests
- Weekly schedule (Sunday 2 AM UTC)

**Jobs:**

#### CodeQL Analysis
- GitHub's native code scanning tool
- Analyzes Python code for vulnerabilities
- Results uploaded to GitHub Security tab

#### Dependency Check
- Runs Safety for known CVEs in dependencies
- Runs pip-audit for Python package audits
- Continues on error for visibility

#### SAST (Static Application Security Testing)
- Bandit: Python-specific security checker
- Semgrep: Multi-language pattern matching tool
- Coverage: OWASP Top 10, general security patterns

#### Container Scan
- Trivy: Container vulnerability scanner
- Scans final Docker image for CVEs
- Reports uploaded as SARIF for GitHub Security

#### License Check
- Validates license compliance
- Fails on copyleft or unknown licenses
- Helps prevent licensing issues

### 5. Code Quality Workflow (`.github/workflows/code-quality.yml`)

**Trigger Events:**
- Push to `main` or `develop`
- Pull requests

**Jobs:**

#### Quality Gates
- Ruff linting and formatting
- Mypy type checking
- Pytest with 80% coverage requirement

#### Documentation
- Checks for missing docstrings
- Generates API documentation

#### SonarQube Analysis (Optional)
- Requires SONAR_HOST_URL and SONAR_TOKEN secrets
- Analyzes code quality metrics
- Continues on error if secrets not set

#### Pre-commit Hooks
- Runs pre-commit framework hooks
- Ensures consistency with local development

### 6. Performance Workflow (`.github/workflows/performance.yml`)

**Trigger Events:**
- Push to `main` branch
- Pull requests
- Manual workflow dispatch

**Jobs:**

#### Benchmark
- Runs pytest-benchmark on test suite
- Generates benchmark JSON report
- Comments results on PRs

#### Memory Profile
- Runs memory-profiler on main scripts
- Identifies memory-intensive operations

#### Code Complexity
- Radon: Cyclomatic complexity analysis
- Radon: Maintainability index
- Pylint: General Python linting

## Caching Strategy

### Pip Cache
- **Location:** `~/.cache/pip`
- **Key:** `{os}-pip-{job}-{cache_version}-{hash(requirements.txt, pyproject.toml)}`
- **Scope:** Per Python version, per workflow type
- **Restore keys:** Cascade fallback to similar versions

### Pytest Cache
- **Location:** `.pytest_cache`
- **Key:** Per Python version and test configuration
- **Purpose:** Faster test discovery and execution

### Docker BuildKit Cache
- **Location:** GitHub Actions cache
- **Modes:** max compression for optimal layer caching

## Secret Management

Required secrets for full pipeline functionality:

| Secret | Usage | Required |
|--------|-------|----------|
| `GITHUB_TOKEN` | Container registry auth, release creation | Yes (auto) |
| `CODECOV_TOKEN` | Upload coverage reports | No |
| `SONAR_HOST_URL` | SonarQube endpoint | No |
| `SONAR_TOKEN` | SonarQube authentication | No |

## Dependency Updates

Dependabot automatically creates PRs for dependency updates:

- **Python (pip):** Weekly (Mondays, 3 AM UTC)
- **GitHub Actions:** Weekly (Tuesdays, 3 AM UTC)
- **Docker:** Weekly (Wednesdays, 3 AM UTC)

Configuration: `.github/dependabot.yml`

## Code Owners

Default code owners configured in `.github/CODEOWNERS`:

- Entire repository: `@continuum-report-team`
- Documentation and CI/CD: Specific paths
- Python code: Source and test directories

## Monitoring and Notifications

### GitHub Native
- Workflow status in PR checks
- Security scanning results in Security tab
- Coverage status badges (if Codecov connected)

### External Integrations
- Codecov: Coverage trend tracking
- Docker Hub/GHCR: Image availability
- SonarQube: Code quality metrics (optional)

## Local Development

### Pre-commit Setup
```bash
pre-commit install
pre-commit run --all-files
```

### Running Tests Locally
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run linting
ruff check scripts/ tests/
ruff format scripts/ tests/

# Run type checking
mypy scripts/

# Run tests with coverage
pytest tests/ -v --cov=scripts --cov-report=html

# Build Docker image
docker build -t continuum-report:dev .
```

## Troubleshooting

### Workflow Failure Investigation

1. **Check workflow logs:** GitHub Actions tab -> Workflow -> Run
2. **Review artifact uploads:** Check uploaded logs, coverage reports, test results
3. **Common issues:**
   - **Coverage failing:** Update tests or lower threshold in pyproject.toml
   - **Type checking:** Run mypy locally, check stub installation
   - **Docker build:** Check Dockerfile and docker-compose.yml, verify base image availability
   - **Security scan:** Review CVE details, may need dependency pinning

### Cache Issues
- Cache key mismatch: Check hash of requirements.txt
- Stale cache: Manually clear via GitHub Actions settings
- Cache misses: Verify cache-dependency-path in setup-python

## Performance Optimization

### Build Performance
- Multi-platform Docker builds: Enable BuildKit
- Pip cache: Reused across runs within retention period
- Pytest cache: Speeds up test discovery

### Job Dependencies
- Lint runs first (fail fast, fast feedback)
- Test runs in parallel across Python versions
- Security checks run in parallel with tests
- Integration tests depend on main tests
- Release jobs depend on all other jobs

## Best Practices

1. **Always run CI before merging:**
   - All checks must pass
   - Coverage must not decrease
   - Security scans must pass

2. **Meaningful commit messages:**
   - Use conventional commits
   - Helps with changelog generation

3. **Version tags:**
   - Use semantic versioning (MAJOR.MINOR.PATCH)
   - Tag on main branch for releases
   - Signed tags recommended for security

4. **Docker image optimization:**
   - Multi-stage builds minimize layer size
   - Non-root user for security
   - Health checks included

5. **Documentation:**
   - Keep docstrings updated
   - Update CHANGELOG.md
   - Document breaking changes

## Customization

### Modifying Workflow Triggers
Edit trigger conditions in each `.github/workflows/*.yml` file

### Adjusting Coverage Threshold
Update `fail_under` in `pyproject.toml` `[tool.coverage.report]` section

### Adding Python Versions
Update `matrix.python-version` in `.github/workflows/ci.yml`

### Custom Status Checks
Modify job definitions and add additional job-specific steps

## Related Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Mypy Documentation](https://mypy.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
