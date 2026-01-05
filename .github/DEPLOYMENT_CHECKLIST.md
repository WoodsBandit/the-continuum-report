# GitHub Actions CI/CD Deployment Checklist

Use this checklist to verify the CI/CD pipeline is correctly deployed to GitHub.

## Pre-Deployment (Local Machine)

### Code Preparation
- [x] `.github/` directory created with all configuration files
- [x] All workflow files are valid YAML
- [x] All documentation files are complete
- [x] Project structure includes `scripts/`, `tests/`, `pyproject.toml`, `requirements.txt`
- [x] Docker support verified (Dockerfile, docker-compose.yml exist)
- [x] Python dependencies defined in `pyproject.toml` and `requirements.txt`

### File Verification
- [x] 6 workflow files in `.github/workflows/`
- [x] 2 issue templates in `.github/ISSUE_TEMPLATE/`
- [x] Configuration files: `dependabot.yml`, `CODEOWNERS`
- [x] Template files: `pull_request_template.md`
- [x] Documentation files: `README.md`, `CICD_GUIDE.md`, `SETUP_GUIDE.md`

## GitHub Repository Setup

### Repository Creation
- [ ] Create GitHub repository (empty, no README/LICENSE/gitignore initially)
- [ ] Repository name: `continuum` (or your preferred name)
- [ ] Repository visibility: Public (recommended for open source)
- [ ] Initialize with: Nothing (will push our own files)

### Initial Push
- [ ] Navigate to local project directory
- [ ] Initialize git if needed: `git init`
- [ ] Add GitHub remote: `git remote add origin https://github.com/YOUR_USERNAME/continuum.git`
- [ ] Add all files: `git add .`
- [ ] Create initial commit: `git commit -m "Initial commit: Add GitHub Actions CI/CD pipeline"`
- [ ] Push to main branch: `git push -u origin main`
- [ ] Verify files appear on GitHub

## GitHub Settings Configuration

### Settings → General
- [ ] Default branch: Set to `main`
- [ ] Repository description: "AI-powered document analysis pipeline"
- [ ] Topics: Add relevant tags (python, ci-cd, automation, etc.)
- [ ] Include in GitHub profile: Check if desired

### Settings → Actions
- [ ] Actions disabled: **OFF** (must be enabled)
- [ ] Allow all actions: Selected
- [ ] Fork pull request workflows: Allow read repository contents permission (optional)
- [ ] Required approval: Adjust as needed for security

### Settings → Code Security & Analysis
- [ ] Dependabot alerts: **ON** (automatic)
- [ ] Dependabot security updates: **ON**
- [ ] Dependency graph: **ON** (automatic)
- [ ] Secret scanning: **ON** (if available in your plan)
- [ ] Push protection: **ON** (if available)

### Settings → Branches
- [ ] Add branch protection rule for `main`:
  - [ ] Require a pull request before merging: **ON**
  - [ ] Require status checks to pass:
    - [ ] CI / Lint and Type Check
    - [ ] CI / Test (Python 3.11) [can add all versions]
    - [ ] CI / Security Scan
  - [ ] Require branches to be up to date: **ON**
  - [ ] Include administrators: **ON** (recommended)
  - [ ] Allow force pushes: **OFF**
  - [ ] Allow deletions: **OFF**

### Settings → Secrets and Variables
Configure these secrets if using optional features:

#### For Coverage Reports (Optional)
- [ ] Add secret `CODECOV_TOKEN`
  - [ ] Get token from [codecov.io](https://codecov.io)
  - [ ] Paste in value field
  - [ ] Save

#### For SonarQube (Optional)
- [ ] Add secret `SONAR_HOST_URL` (e.g., https://sonarqube.example.com)
- [ ] Add secret `SONAR_TOKEN` (from SonarQube instance)

#### For Docker Hub (Optional)
- [ ] Add secret `DOCKERHUB_USERNAME`
- [ ] Add secret `DOCKERHUB_TOKEN`

### Settings → Notifications
- [ ] Email notifications: Configure as preferred
- [ ] Slack integration: (optional)
- [ ] Teams integration: (optional)

## Verify Workflows Running

### Initial Workflow Run
- [ ] Navigate to **Actions** tab on GitHub
- [ ] Wait 1-2 minutes for workflows to appear
- [ ] Verify workflows are listed:
  - [ ] CI
  - [ ] Docker Build and Push (may skip if not on main)
  - [ ] Security
  - [ ] Code Quality
  - [ ] Performance
- [ ] Click on a workflow to see job breakdown

### CI Workflow Verification
- [ ] Navigate to latest **CI** workflow run
- [ ] Verify these jobs appear and pass:
  - [ ] Lint and Type Check (5-10 min)
  - [ ] Test - Python 3.10 (10-15 min)
  - [ ] Test - Python 3.11 (10-15 min)
  - [ ] Test - Python 3.12 (10-15 min)
  - [ ] Test - Python 3.13 (10-15 min)
  - [ ] Security Scan (5-10 min)
  - [ ] Integration (5-10 min, may skip)
  - [ ] Summary (1 min)
- [ ] All jobs show green checkmarks
- [ ] No red X's or warnings

### Docker Workflow Verification (Main Branch Only)
- [ ] Push a test commit to `main`
- [ ] Wait for **Docker Build and Push** workflow
- [ ] Verify jobs:
  - [ ] Build Docker Image (15-20 min)
  - [ ] Test Image (5-10 min)
  - [ ] Publish Summary (1 min)
- [ ] Verify image pushed to GitHub Container Registry
  - [ ] Go to **Packages** on repository page
  - [ ] See `continuum-report` package listed

### Security Workflow Verification
- [ ] Navigate to **Security** tab
- [ ] Click **Code scanning** alerts
- [ ] Verify CodeQL scan completed:
  - [ ] Check for reported issues
  - [ ] Review severity levels
- [ ] Verify no critical vulnerabilities (warnings OK)

## Test Pull Request Workflow

### Create Test PR
- [ ] Create feature branch: `git checkout -b test/pipeline`
- [ ] Make a small change (e.g., add comment to README)
- [ ] Commit and push: `git push -u origin test/pipeline`
- [ ] On GitHub, create Pull Request
  - [ ] Base: `main`
  - [ ] Compare: `test/pipeline`
  - [ ] Use PR template
  - [ ] Fill in all sections
  - [ ] Create pull request

### Verify PR Checks
- [ ] Wait 5-10 minutes for checks to run
- [ ] Verify all checks appear in "Checks" section:
  - [ ] CI / Lint and Type Check: PASS (green)
  - [ ] CI / Test (all Python versions): PASS
  - [ ] CI / Security Scan: PASS
  - [ ] Other checks: As configured
- [ ] No required checks failing
- [ ] PR shows "All checks have passed"

### Test Merge and Cleanup
- [ ] If all checks pass, merge PR: "Squash and merge" or "Merge pull request"
- [ ] Confirm merge
- [ ] Delete branch
- [ ] Verify main branch workflows trigger automatically
- [ ] Verify Docker workflow runs (if configured for main)

## Documentation Verification

### README Setup
- [ ] Update project README with badge section:
  ```markdown
  [![CI](https://github.com/YOUR_USERNAME/continuum/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/continuum/actions/workflows/ci.yml)
  [![Docker](https://github.com/YOUR_USERNAME/continuum/actions/workflows/docker.yml/badge.svg)](https://github.com/YOUR_USERNAME/continuum/actions/workflows/docker.yml)
  [![Security](https://github.com/YOUR_USERNAME/continuum/actions/workflows/security.yml/badge.svg)](https://github.com/YOUR_USERNAME/continuum/actions/workflows/security.yml)
  ```
- [ ] Add section on CI/CD in README
- [ ] Link to `.github/CICD_GUIDE.md` for documentation

### Local Development Setup
- [ ] Create `.pre-commit-config.yaml` in project root
- [ ] Install pre-commit: `pip install pre-commit`
- [ ] Install hooks: `pre-commit install`
- [ ] Test hooks: `pre-commit run --all-files`

### Team Communication
- [ ] Inform team about new CI/CD pipeline
- [ ] Share `.github/SETUP_GUIDE.md` with team
- [ ] Review PR template expectations
- [ ] Document any local development requirements

## Test Release Workflow (Optional)

### Create Version Tag
- [ ] Make sure main branch is clean
- [ ] Create annotated tag:
  ```bash
  git tag -a v1.0.0 -m "Release version 1.0.0"
  git push origin v1.0.0
  ```
- [ ] Verify tag on GitHub under **Releases**

### Verify Release Workflow
- [ ] Navigate to **Actions**
- [ ] Look for **Release** workflow
- [ ] Wait for it to complete (10-20 minutes)
- [ ] Verify jobs:
  - [ ] Validate Release
  - [ ] Run Tests
  - [ ] Build Artifacts
  - [ ] Create GitHub Release
  - [ ] Publish Summary
- [ ] Navigate to **Releases** page
- [ ] Verify release created with:
  - [ ] Release title: v1.0.0
  - [ ] Release notes
  - [ ] Attached artifacts (if any)
  - [ ] Python package downloads

## Dependabot Setup Verification

### Enable Dependabot
- [ ] Go to **Settings** → **Code security & analysis**
- [ ] Dependabot alerts: **ON**
- [ ] Dependabot security updates: **ON**

### Configure Pull Request Settings
- [ ] Go to **Settings** → **Actions** → **General**
- [ ] For Dependabot PRs:
  - [ ] Can approve automatically (not recommended for security)
  - [ ] Or require review (recommended)

### Monitor First Updates
- [ ] Check **Pull requests** for Dependabot PRs
- [ ] Verify PR creation schedule matches `.github/dependabot.yml`:
  - [ ] Python: Weekly Monday
  - [ ] Actions: Weekly Tuesday
  - [ ] Docker: Weekly Wednesday
- [ ] Review and merge PRs as appropriate

## Performance Optimization

### Monitor Workflow Times
- [ ] Check recent workflow runs
- [ ] Note average execution times:
  - [ ] CI pipeline: Should be 25-35 minutes
  - [ ] Docker build: Should be 15-20 minutes
  - [ ] Security scan: Should be 20-25 minutes
- [ ] If slow, check for:
  - [ ] Cache hits (should see "Cache hit" in logs)
  - [ ] Network issues
  - [ ] Resource constraints

### Verify Caching
- [ ] Click on a test job
- [ ] Expand "Set up Python" step
- [ ] Verify "Cache hit" message appears
- [ ] Check "Save cache" step
- [ ] Note cache size and keys

## Team Configuration

### Code Owners
- [ ] Update `.github/CODEOWNERS` with team members
- [ ] Test by making a PR
- [ ] Verify code owners are auto-requested as reviewers

### Branch Protections
- [ ] Verify all team members can create PRs
- [ ] Ensure only authorized users can push to main
- [ ] Test with team member creating PR

### Notifications
- [ ] Configure team notification preferences
- [ ] Set up Slack/Teams integration if desired
- [ ] Test notifications with a test PR

## Security Verification

### Secrets Management
- [ ] Verify no secrets in code or git history
- [ ] Check git log for accidentally committed secrets
- [ ] Run `git secrets --scan` if installed
- [ ] Verify `.env` files not committed

### Container Security
- [ ] Review Docker image in GHCR
- [ ] Check image layers and size
- [ ] Verify non-root user is used
- [ ] Confirm Trivy scanning completed

### Dependency Security
- [ ] Review GitHub Security tab for vulnerabilities
- [ ] Check for any open security alerts
- [ ] Verify Dependabot will handle updates
- [ ] Test updating a dependency manually

## Final Checks

### All Workflows Functional
- [ ] CI pipeline: PASS
- [ ] Docker build: PASS (on main branch)
- [ ] Security scan: PASS (no critical issues)
- [ ] Code quality: PASS
- [ ] Performance: PASS (benchmark ran)
- [ ] Release (if tested): PASS

### Documentation Complete
- [ ] `.github/README.md`: Verified
- [ ] `.github/CICD_GUIDE.md`: Verified
- [ ] `.github/SETUP_GUIDE.md`: Verified
- [ ] Project README: Updated with badges
- [ ] Inline code comments: Present in workflows

### Team Ready
- [ ] Team trained on PR workflow
- [ ] Team knows about pre-commit hooks
- [ ] Team knows how to check workflow status
- [ ] Team knows how to troubleshoot failures

## Go-Live Decision

All of the following must be checked before considering the pipeline production-ready:

### Must Have (Critical)
- [x] All 6 workflows created and documented
- [x] All configuration files in place
- [x] All templates created
- [x] Code can be pushed to GitHub
- [ ] At least one complete CI run successful
- [ ] Branch protection rules configured
- [ ] Team members can create PRs and commit

### Should Have (Recommended)
- [ ] Codecov integration (if coverage important)
- [ ] SonarQube integration (if quality metrics needed)
- [ ] Pre-commit hooks installed locally
- [ ] Team trained on new process
- [ ] Badges added to README
- [ ] Release workflow tested

### Nice to Have (Optional)
- [ ] Docker Hub integration
- [ ] Slack notifications
- [ ] Performance benchmarking in use
- [ ] Custom monitoring dashboard

## Post-Deployment Monitoring

### First Month
- [ ] Monitor workflow success rates (target: >95%)
- [ ] Review failed workflow logs
- [ ] Adjust thresholds if needed
- [ ] Train team on any issues
- [ ] Collect feedback from team

### Ongoing Maintenance
- [ ] Review Dependabot PRs weekly
- [ ] Check security alerts twice weekly
- [ ] Monitor workflow performance monthly
- [ ] Update documentation as workflows change
- [ ] Review and update CODEOWNERS quarterly

## Troubleshooting Guide

### Common Issues

#### Workflows Not Running
1. Check Actions are enabled
2. Check workflow file syntax
3. Wait a few minutes
4. Check git push was successful

#### Tests Failing
1. Run tests locally: `pytest tests/ -v`
2. Check Python version matches
3. Check dependencies installed: `pip install -e ".[test]"`
4. Review workflow logs for specific error

#### Docker Build Failing
1. Test locally: `docker build -t continuum:test .`
2. Check Dockerfile syntax
3. Verify base image available
4. Check available disk space

#### Coverage Below Threshold
1. Run coverage locally
2. Check `pyproject.toml` coverage threshold
3. Add tests or update threshold
4. Retest and push

#### Security Scan Alerts
1. Review alert details in Security tab
2. Update dependencies or pin versions
3. Mark as false positive if needed
4. Document workarounds

## Completion

- [ ] All checklist items completed
- [ ] All workflows tested and verified
- [ ] Team trained and ready
- [ ] Documentation reviewed
- [ ] No open issues or warnings

**Deployment Date**: _______________
**Deployed By**: _______________
**Notes**: _______________

---

For detailed guidance, see:
- `.github/SETUP_GUIDE.md` - Initial setup instructions
- `.github/CICD_GUIDE.md` - Detailed workflow documentation
- `.github/README.md` - Quick reference guide
