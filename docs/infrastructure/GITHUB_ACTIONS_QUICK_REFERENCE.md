# GitHub Actions CI/CD - Quick Reference Guide

**Project:** Continuum Report
**Date:** 2025-12-24
**Status:** Production Ready

---

## Pipeline Overview

### Six Core Workflows

```
┌─────────────────────────────────────────────────────────────┐
│                   Continuum Report CI/CD                     │
└─────────────────────────────────────────────────────────────┘

push/PR to main/develop
    │
    ├─→ [ci.yml] Lint, Test, Security
    │   ├─ Ruff linting + formatting
    │   ├─ Mypy type checking
    │   ├─ Pytest (Python 3.10-3.13)
    │   ├─ Bandit security scan
    │   └─ Safety vulnerability check
    │
    ├─→ [code-quality.yml] Quality Gates
    │   ├─ Code quality checks
    │   ├─ Coverage threshold (80%)
    │   ├─ SonarQube analysis
    │   └─ Pre-commit hooks
    │
    └─→ [security.yml] Comprehensive Security
        ├─ CodeQL analysis
        ├─ Bandit + Semgrep SAST
        ├─ Dependency scanning
        ├─ Container scanning
        └─ License compliance

push to main branch
    │
    └─→ [docker.yml] Container Build
        ├─ Multi-platform build (amd64, arm64)
        ├─ Trivy vulnerability scan
        └─ Push to ghcr.io

git tag v*
    │
    └─→ [release.yml] Release Automation
        ├─ Run full test suite
        ├─ Build Python packages
        ├─ Build and push Docker image
        └─ Create GitHub release

push/PR to main
    │
    └─→ [performance.yml] Performance Tracking
        ├─ Benchmarks
        ├─ Memory profiling
        └─ Code complexity analysis
```

---

## Workflow Triggers

| Workflow | Triggers | Frequency |
|----------|----------|-----------|
| **ci.yml** | Push/PR on main, develop | Every push/PR |
| **code-quality.yml** | Push/PR on main, develop | Every push/PR |
| **docker.yml** | Push to main (path filter) | On Docker-related changes |
| **security.yml** | Push/PR, Weekly schedule | Every push/PR + Sunday 2 AM UTC |
| **release.yml** | Git tags (v*), Manual | On version tags |
| **performance.yml** | Push/PR, Manual | Every push/PR + manual dispatch |

---

## Key Configurations

### Python Environment
```yaml
Primary Version:   3.11
Test Matrix:       3.10, 3.11, 3.12, 3.13
Min Requirement:   >= 3.10 (pyproject.toml)
Dockerfile:        python:3.11-slim
```

### Dependency Management
```yaml
Main Deps:         requests, pydantic, structlog, tenacity
Dev Deps:          pytest, ruff, mypy, pre-commit
Test Extras:       pytest, pytest-cov, responses, hypothesis
Optional Extras:   async, database, queue, observability
```

### Cache Strategy
```yaml
Pip Cache:         ~/.cache/pip
  Key:             ${{ runner.os }}-pip-[job]-v1-${{ hashFiles(...) }}
  Fallback:        Version match → Broad match

Pytest Cache:      .pytest_cache
  Key:             ${{ runner.os }}-pytest-v1-py[version]-${{ hashFiles(...) }}

Docker Cache:      GitHub Actions (type=gha)
```

### Coverage Requirements
```yaml
Threshold:         80% minimum
Report Formats:    xml (Codecov), html (artifact), term-missing (console)
Enforcement:       --cov-fail-under=80 in code-quality.yml
```

### Security Scanning
```yaml
SAST:
  - Bandit:      Python security issues
  - Semgrep:     Security audit + Python + OWASP Top 10

DAST:
  - Trivy:       Container vulnerabilities (HIGH, CRITICAL)

Dependency:
  - Safety:      Known vulnerabilities
  - pip-audit:   Comprehensive dependency analysis

License:
  - licensecheck: Copyleft + unknown license detection

Integration:
  - CodeQL:      GitHub native code analysis
  - SARIF:       GitHub Security tab reporting
```

---

## Common Commands

### Running Workflows Locally

```bash
# Install act (GitHub Actions locally)
brew install act  # or download from https://github.com/nektos/act

# Run all workflows
act

# Run specific workflow
act --job lint
act --job test
act --job build

# Run with specific Python version
act --env PYTHON_VERSION=3.12
```

### Git Triggers

```bash
# Trigger CI/CD (push to main)
git push origin main

# Trigger code-quality (push to develop)
git push origin develop

# Trigger release workflow (push tag)
git tag v1.0.0
git push origin v1.0.0

# Trigger release manually (via GitHub UI)
# Go to Actions → Release → Run workflow
```

### Manual Workflow Dispatch

```bash
# Using GitHub CLI
gh workflow run release.yml -f version=v1.0.0
gh workflow run docker.yml -f push_image=true
gh workflow run performance.yml
```

---

## Environment Variables & Secrets

### Environment Variables
```yaml
PYTHON_VERSION:    3.11 (default for most workflows)
CACHE_VERSION:     v1 (increment to invalidate caches)
REGISTRY:          ghcr.io
IMAGE_NAME:        ${{ github.repository }}
```

### Required Secrets (GitHub Settings)

```yaml
CODECOV_TOKEN:     Upload coverage to codecov.io
SONAR_HOST_URL:    SonarQube instance URL
SONAR_TOKEN:       SonarQube authentication
GITHUB_TOKEN:      Implicitly available (scoped per job)
```

**Setting Secrets:**
1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add secret name and value

---

## Artifact Outputs

### CI Artifacts (30-day retention)
```
test-results-py3.10.xml         JUnit test results
test-results-py3.11.xml
test-results-py3.12.xml
test-results-py3.13.xml

coverage-report-py3.10/         HTML coverage reports
coverage-report-py3.11/
coverage-report-py3.12/
coverage-report-py3.13/

bandit-security-report.json     Security scan results
safety-report.json              Dependency vulnerabilities
```

### Release Artifacts
```
continuum-report-*.whl          Python wheel package
continuum-report-*.tar.gz       Source distribution

ghcr.io/org/continuum:v1.0.0   Docker image (tagged)
ghcr.io/org/continuum:latest   Docker image (latest)
```

---

## Debugging Failed Workflows

### Check Workflow Status
```bash
# View workflow runs
gh run list --workflow=ci.yml --limit=10

# View specific run
gh run view <run-id> --log

# Download logs
gh run download <run-id>
```

### Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Coverage upload fails | `coverage.xml` not found | Check cov-report path in pytest |
| Tests fail | Missing dependencies | Add to pyproject.toml [test] extras |
| Linting fails | Code style issues | Run `ruff format scripts/` locally |
| Type check fails | Type hints missing | Run `mypy scripts/` locally |
| Docker build fails | Invalid Dockerfile | Test: `docker build -t test .` |
| Security scan timeout | Image too large | Reduce image size, check BuildKit |

---

## Performance Optimization Tips

### Reduce Workflow Time
```yaml
# 1. Use matrix efficiently (parallel)
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12', '3.13']

# 2. Implement proper caching
cache:
  path: ~/.cache/pip
  key: ${{ runner.os }}-pip-${{ hashFiles(...) }}

# 3. Use fail-fast strategically
fail-fast: false  # Don't stop other matrix jobs

# 4. Limit scope of code analysis
ruff check scripts/ tests/  # Don't check everything

# 5. Run heavy jobs conditionally
if: github.event_name == 'push'  # Skip on draft PRs
```

### Estimated Workflow Times
```
ci.yml:                15-20 min (4 Python versions in parallel)
code-quality.yml:      10-15 min
docker.yml:            20-30 min (multi-platform)
security.yml:          15-25 min
release.yml:           25-40 min
performance.yml:       10-15 min
```

---

## Best Practices

### Do's ✅
- Always include `fetch-depth: 0` for version detection
- Use `continue-on-error: true` for non-blocking checks
- Store artifacts for 30 days minimum
- Tag all security-related jobs with permissions
- Use environment variables for configuration
- Test locally before pushing

### Don'ts ❌
- Never hardcode secrets (use GitHub Secrets)
- Don't skip security scans
- Don't commit `.coverage` files
- Don't store sensitive data in artifacts
- Don't rely on default timeouts (set explicit values)
- Don't use `always()` without good reason

---

## Workflow Files

### Location
```
.github/workflows/
├── ci.yml                 # Main CI pipeline
├── code-quality.yml      # Code quality gates
├── docker.yml            # Container build
├── security.yml          # Security scanning
├── release.yml           # Release automation
└── performance.yml       # Performance tests
```

### File Sizes
```
ci.yml:              ~6.3 KB (233 lines)
code-quality.yml:    ~5.2 KB (168 lines)
docker.yml:          ~5.8 KB (171 lines)
security.yml:        ~6.1 KB (201 lines)
release.yml:         ~7.2 KB (249 lines)
performance.yml:     ~4.6 KB (146 lines)
```

---

## Integration Points

### External Services
```yaml
Codecov:           https://codecov.io/gh/org/repo
SonarQube:         https://sonarqube.example.com
GitHub Container: ghcr.io/org/continuum
GitHub Security:   Repo → Security → Code scanning alerts
```

### Notification Channels
```yaml
GitHub:            Actions tab, branch protection status
Email:             GitHub notifications (configure in settings)
Slack:             Configure via GitHub app integration
Custom Webhooks:   Configure via GitHub Actions secrets
```

---

## Version Management

### Semantic Versioning
```yaml
Format:            v<major>.<minor>.<patch>[-prerelease]
Examples:
  v1.0.0           Production release
  v2.1.0           Minor feature
  v2.1.1           Patch fix
  v2.0.0-beta.1    Pre-release
```

### Release Process
```bash
# 1. Update version in pyproject.toml
# 2. Update CHANGELOG.md
# 3. Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "chore: release v1.0.0"

# 4. Create tag
git tag v1.0.0

# 5. Push tag to trigger release workflow
git push origin v1.0.0

# 6. GitHub Actions automatically:
#    - Runs tests
#    - Builds packages
#    - Builds Docker images
#    - Creates GitHub release
```

---

## Monitoring & Alerts

### Key Metrics to Monitor
```yaml
Build Success Rate:        Should be > 95%
Test Coverage:             Should be > 80%
Security Vulnerabilities:  Should be 0 (HIGH/CRITICAL)
Average Build Time:        < 30 minutes
Deployment Frequency:      Track and trend
Lead Time for Changes:     Minimize
Change Failure Rate:       Should be < 15%
MTTR (Mean Time to Recover): Should be < 1 hour
```

### Setting Up Alerts
1. Go to repo → Settings → Branch protection rules
2. Require status checks before merging
3. Mark workflows as required
4. Configure Slack notifications (optional)

---

## Additional Resources

### Documentation
- GitHub Actions: https://docs.github.com/en/actions
- Pytest: https://docs.pytest.org/
- Ruff: https://docs.astral.sh/ruff/
- Docker: https://docs.docker.com/

### Tools
- act (local runner): https://github.com/nektos/act
- GitHub CLI: https://cli.github.com/
- codecov: https://codecov.io/
- semgrep: https://semgrep.dev/

### Best Practices
- GitHub Actions Security: https://docs.github.com/en/actions/security-guides
- SLSA Framework: https://slsa.dev/
- Secure Supply Chain: https://www.cisa.gov/
- Open Source Security: https://openssf.org/

---

**Last Updated:** 2025-12-24
**Maintained By:** Continuum Report Team
**Status:** Active and Production-Ready
