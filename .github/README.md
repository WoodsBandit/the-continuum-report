# GitHub Configuration for The Continuum Report

This directory contains GitHub-specific configurations, workflows, and templates for The Continuum Report project.

## Directory Structure

```
.github/
├── workflows/              # GitHub Actions CI/CD workflows
│   ├── ci.yml             # Main continuous integration pipeline
│   ├── docker.yml         # Docker build and push workflow
│   ├── release.yml        # Release and publishing workflow
│   ├── security.yml       # Security scanning and compliance
│   ├── code-quality.yml   # Code quality analysis
│   └── performance.yml    # Performance benchmarking
├── ISSUE_TEMPLATE/        # Issue templates
│   ├── bug_report.md      # Bug report template
│   └── feature_request.md # Feature request template
├── dependabot.yml         # Automated dependency updates
├── CODEOWNERS             # Code ownership rules
├── pull_request_template.md # PR template
├── CICD_GUIDE.md          # CI/CD pipeline documentation
└── README.md              # This file

```

## Key Files

### Workflows (`workflows/`)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **CI** | Push/PR to main/develop | Lint, test, and validate code |
| **Docker** | Push to main | Build multi-platform images |
| **Release** | Version tags | Create releases and publish |
| **Security** | Push/PR/Weekly | Security scanning and audits |
| **Code Quality** | Push/PR | Code quality metrics |
| **Performance** | Push/PR/Manual | Benchmarking and profiling |

### Configuration Files

| File | Purpose |
|------|---------|
| **dependabot.yml** | Automatic dependency version updates |
| **CODEOWNERS** | Automatic code ownership assignment |
| **CICD_GUIDE.md** | Comprehensive CI/CD documentation |

### Templates

| Template | Usage |
|----------|-------|
| **pull_request_template.md** | Standardized PR description format |
| **ISSUE_TEMPLATE/** | Standard issue types (bug, feature) |

## Quick Start

### Viewing Workflow Status

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select a workflow to see recent runs
4. Click a workflow run to see detailed logs

### Running a Workflow Manually

For workflows with `workflow_dispatch` trigger:

1. Go to **Actions** tab
2. Select the workflow (e.g., "Docker Build and Push")
3. Click **Run workflow** button
4. Fill in any required inputs
5. Click **Run workflow**

### Reviewing Security Scans

1. Go to **Security** tab
2. Click **Code scanning** or **Secret scanning**
3. View alerts and remediation guidance

## Workflow Features

### Performance Optimizations

- **Pip caching**: Speeds up dependency installation
- **Docker layer caching**: Reuses Docker build layers
- **Pytest caching**: Faster test discovery
- **Matrix strategy**: Parallel Python version testing

### Security Features

- **Static analysis**: Ruff, mypy, Bandit, Semgrep
- **Dependency scanning**: Safety, pip-audit, Dependabot
- **Container scanning**: Trivy vulnerability scanner
- **CodeQL**: GitHub's native code scanning
- **License compliance**: Checks for GPL/copyleft issues

### Release Automation

- **Versioning**: Semantic version extraction from tags
- **Building**: Multi-platform Docker images
- **Publishing**: PyPI packages and GitHub releases
- **Distribution**: Automatic artifact management

## Customization

### Adding a New Workflow

1. Create a new file in `workflows/` directory
2. Define triggers and jobs
3. Use existing workflows as templates
4. Test workflow with manual dispatch if possible

### Modifying Python Versions

Edit `ci.yml` and update the test matrix:

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12', '3.13']
```

### Adjusting Coverage Threshold

Modify in `pyproject.toml`:

```toml
[tool.coverage.report]
fail_under = 85  # Change threshold here
```

### Setting Up Secrets

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secrets required by workflows:
   - `CODECOV_TOKEN` (for coverage reports)
   - `SONAR_HOST_URL` and `SONAR_TOKEN` (for SonarQube)

## Troubleshooting

### Workflow Won't Run

- Check branch protection rules require status checks
- Verify workflow file syntax with `yamllint`
- Check if workflow is disabled in Actions settings

### Tests Failing in CI but Passing Locally

- Different Python version (use same version as workflow)
- Missing test dependencies (install `[test]` extras)
- Missing environment variables (check workflow env)
- Platform differences (Linux vs Windows/Mac)

### Docker Build Fails

- Check available disk space in runner
- Verify Dockerfile syntax
- Check base image availability
- Review build logs for specific errors

### Security Scan Alerts

- Review the alert details in Security tab
- Check vulnerability databases for false positives
- Update dependencies or apply workarounds
- Document known issues if necessary

## Environment Variables

### Workflow-wide

Set in workflow file or repository secrets:

```yaml
env:
  PYTHON_VERSION: '3.11'
  CACHE_VERSION: v1
```

### Secrets

Required secrets must be added to GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add repository secrets
3. Reference in workflows as `${{ secrets.SECRET_NAME }}`

## Monitoring

### Status Badges

Add to your README:

```markdown
[![CI](https://github.com/continuum-report/continuum/actions/workflows/ci.yml/badge.svg)](https://github.com/continuum-report/continuum/actions/workflows/ci.yml)
[![Docker](https://github.com/continuum-report/continuum/actions/workflows/docker.yml/badge.svg)](https://github.com/continuum-report/continuum/actions/workflows/docker.yml)
[![Security](https://github.com/continuum-report/continuum/actions/workflows/security.yml/badge.svg)](https://github.com/continuum-report/continuum/actions/workflows/security.yml)
```

### Notifications

- **Email**: Enabled by default for failed workflows
- **Custom**: Set up via GitHub Settings → Notifications
- **Integrations**: Slack, Teams, etc. via third-party actions

## Related Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Security Best Practices](https://docs.github.com/en/actions/security-guides)
- [CICD_GUIDE.md](./CICD_GUIDE.md) - Detailed workflow documentation

## Contributing

When modifying workflows or templates:

1. Test changes locally or in a test workflow
2. Document changes in CICD_GUIDE.md
3. Update this README if adding new workflows
4. Consider impact on build times and resource usage

## Support

For issues with GitHub Actions:

1. Check workflow logs in Actions tab
2. Review GitHub Actions documentation
3. Check existing GitHub issues
4. File a new issue with workflow logs attached
