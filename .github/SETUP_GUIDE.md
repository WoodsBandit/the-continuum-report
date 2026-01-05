# GitHub Actions CI/CD Setup Guide

## Overview

This guide walks through setting up the complete GitHub Actions CI/CD pipeline for The Continuum Report on your GitHub repository.

## Prerequisites

- GitHub repository with write access
- Python 3.10+ (for local testing)
- Git installed locally
- Docker installed (for building and testing Docker images)

## Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository (if not already done)

```bash
cd /path/to/continuum
git init
git add .
git commit -m "Initial commit"
```

### 1.2 Add GitHub Remote

```bash
# Using HTTPS
git remote add origin https://github.com/your-username/continuum.git

# Or using SSH
git remote add origin git@github.com:your-username/continuum.git

# Verify
git remote -v
```

### 1.3 Verify Project Structure

The pipeline expects:

```
continuum/
├── .github/              # CI/CD configuration (already set up)
├── scripts/              # Python scripts
├── tests/                # Test files
├── pyproject.toml        # Project metadata
├── requirements.txt      # Dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
└── README.md             # Project documentation
```

## Step 2: Configure GitHub Repository Settings

### 2.1 Enable Actions

1. Go to repository **Settings**
2. Click **Actions** in sidebar
3. Select **Allow all actions and reusable workflows**
4. Click **Save**

### 2.2 Configure Branch Protection Rules

1. Go to **Settings** → **Branches**
2. Click **Add rule** under Branch protection rules
3. Set Branch name pattern: `main`
4. Enable these protections:
   - Require a pull request before merging
   - Require status checks to pass before merging:
     - CI / Lint and Type Check
     - CI / Test (Python 3.11) [or all versions]
     - CI / Security Scan
   - Require branches to be up to date before merging
   - Include administrators in restrictions

### 2.3 Enable Security Features

1. Go to **Settings** → **Security & analysis**
2. Enable:
   - **Dependabot alerts** (automatically enabled)
   - **Dependabot security updates** (turn ON)
   - **Dependency graph** (automatically enabled)
   - **Secret scanning**
3. Click **Save**

## Step 3: Configure Repository Secrets

Required secrets for optional features:

### 3.1 Codecov Token (Optional - for coverage reports)

1. Go to [codecov.io](https://codecov.io)
2. Sign in with GitHub
3. Authorize and grant access
4. Find your repository
5. Copy the **Repository Upload Token**
6. In GitHub repo → **Settings** → **Secrets and variables** → **Actions**
7. Click **New repository secret**
8. Name: `CODECOV_TOKEN`
9. Value: (paste token)
10. Click **Add secret**

### 3.2 SonarQube Token (Optional - for code quality)

If using SonarQube:

1. Get SonarQube token from your SonarQube instance
2. In GitHub repo → **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `SONAR_HOST_URL`
5. Value: (e.g., https://sonarqube.example.com)
6. Click **Add secret**
7. Create another secret:
   - Name: `SONAR_TOKEN`
   - Value: (paste token)

### 3.3 Container Registry (for Docker images)

GitHub Container Registry (GHCR) uses GITHUB_TOKEN automatically, no action needed.

For Docker Hub:

1. Create access token at hub.docker.com
2. Create secrets:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`

## Step 4: Verify Workflows

### 4.1 Check Workflow Files

```bash
# Validate workflow syntax
find .github/workflows -name "*.yml" | xargs yamllint
```

### 4.2 Test Locally (Optional)

```bash
# Install act to run workflows locally
brew install act  # macOS
# or download from https://github.com/nektos/act

# Run a specific workflow
act -j lint -W .github/workflows/ci.yml
```

## Step 5: Push Configuration to GitHub

```bash
git add .github/
git commit -m "chore: add GitHub Actions CI/CD pipeline"
git push -u origin main
```

## Step 6: Verify Workflows are Running

1. Go to your repository on GitHub
2. Click **Actions** tab
3. You should see workflow runs appearing
4. Wait for initial runs to complete (5-10 minutes)

## Step 7: Configure Default Branch

1. Go to **Settings** → **General**
2. Under "Default branch", select `main` or your primary branch
3. Click **Update**

## Step 8: Setup Local Pre-commit Hooks

To match CI standards locally:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml (if not exists)
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
EOF

# Install pre-commit hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

## Step 9: Configure Protected Environment (Optional)

For enhanced deployment security:

1. Go to **Settings** → **Environments**
2. Click **New environment**
3. Name: `production`
4. Configure:
   - Required reviewers
   - Deployment branches
   - Environment secrets
5. Update `release.yml` to use this environment

## Step 10: Test Your Pipeline

### Test 1: Create a Feature Branch

```bash
git checkout -b test/pipeline-setup
echo "# Test" >> README.md
git add README.md
git commit -m "test: verify pipeline"
git push -u origin test/pipeline-setup
```

### Test 2: Create a Pull Request

1. Go to repository
2. Click **Pull requests**
3. Click **New pull request**
4. Select `test/pipeline-setup` as compare branch
5. Create pull request
6. Wait for checks to complete (5-10 minutes)
7. Verify all checks pass

### Test 3: Merge to Main

1. After PR checks pass, click **Merge pull request**
2. Go to **Actions** tab
3. Verify Docker build and other main-branch workflows run

## Step 11: Enable Status Badges (Optional)

Add to your README.md:

```markdown
# The Continuum Report

[![CI Status](https://github.com/YOUR_USERNAME/continuum/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/continuum/actions/workflows/ci.yml)
[![Docker Build](https://github.com/YOUR_USERNAME/continuum/actions/workflows/docker.yml/badge.svg)](https://github.com/YOUR_USERNAME/continuum/actions/workflows/docker.yml)
[![Security](https://github.com/YOUR_USERNAME/continuum/actions/workflows/security.yml/badge.svg)](https://github.com/YOUR_USERNAME/continuum/actions/workflows/security.yml)
[![Code Coverage](https://codecov.io/gh/YOUR_USERNAME/continuum/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/continuum)

```

## Troubleshooting

### Workflows Not Running

**Problem**: No workflows visible in Actions tab

**Solutions**:
1. Check branch protection doesn't require manually enabling
2. Verify workflow files are in `.github/workflows/` directory
3. Check workflow file syntax (use `yamllint`)
4. Ensure branch is `main` or configured in workflow
5. Wait a few minutes, GitHub may have delays

### Failed Linting

**Problem**: Ruff or mypy checks failing

**Solutions**:
1. Run locally: `ruff check scripts/` and `mypy scripts/`
2. Fix issues: `ruff check --fix scripts/`
3. Format code: `ruff format scripts/`
4. Commit fixes and push

### Failed Tests

**Problem**: Pytest failing in CI

**Solutions**:
1. Run locally: `pytest tests/ -v`
2. Check Python version matches workflow
3. Install all dependencies: `pip install -e ".[test]"`
4. Check for environment variable requirements

### Docker Build Fails

**Problem**: Docker build step fails

**Solutions**:
1. Test locally: `docker build -t continuum-report:test .`
2. Check available space: `docker system df`
3. Verify Dockerfile syntax
4. Check base image availability

### Container Registry Auth Fails

**Problem**: Can't push to GitHub Container Registry

**Solutions**:
1. Check GITHUB_TOKEN is available (automatic)
2. Verify repository is public or token has access
3. Check workflow permissions in job definition
4. Ensure secrets aren't being exposed in logs

### Codecov Token Invalid

**Problem**: Coverage reports not uploading

**Solutions**:
1. Verify token is set correctly in secrets
2. Check token hasn't expired
3. Ensure repository is authorized on codecov.io
4. Try regenerating token

## Next Steps

1. **Customize Workflows**: Adjust Python versions, coverage thresholds, etc.
2. **Setup Monitoring**: Configure notifications and alerts
3. **Documentation**: Update project README with badge and setup info
4. **Team Setup**: Invite team members and configure CODEOWNERS
5. **Release Workflow**: Create first release with version tag

## Maintenance

### Regular Tasks

- Monitor workflow run times and optimize if needed
- Review security alerts weekly
- Update dependencies via Dependabot
- Review test coverage trends
- Update documentation as workflows change

### Updating Workflows

When modifying workflows:

1. Test changes in branch
2. Update CICD_GUIDE.md documentation
3. Merge via pull request
4. Monitor first few runs on main branch

## Support and Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Security Best Practices](https://docs.github.com/en/actions/security-guides)
- [CICD_GUIDE.md](./CICD_GUIDE.md) - Detailed workflow documentation
- [Project README](../README.md) - Project information

## Common Workflows

### How to Release a New Version

1. Update version in `pyproject.toml` and `Dockerfile`
2. Add entry to `CHANGELOG.md`
3. Commit and push to main
4. Tag commit: `git tag v1.0.0`
5. Push tag: `git push origin v1.0.0`
6. GitHub creates release automatically
7. Docker image automatically pushed with tag

### How to Manually Trigger Docker Build

1. Go to **Actions**
2. Click **Docker Build and Push**
3. Click **Run workflow**
4. Check "Push image to registry" input
5. Click **Run workflow**
6. Monitor build progress

### How to Update Dependencies

1. Dependencies auto-updated via Dependabot
2. Review PR, run tests
3. Approve and merge
4. CI runs automatically on main

## Final Checklist

- [ ] Repository created on GitHub
- [ ] .github directory with all files committed
- [ ] Branch protection rules configured
- [ ] Repository secrets configured (if needed)
- [ ] First workflow runs successful
- [ ] Status badges added to README
- [ ] Team members invited
- [ ] Documentation updated
- [ ] Release workflow tested
