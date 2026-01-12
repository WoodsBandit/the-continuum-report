#!/bin/bash
# Claude Code Plugin Setup Script for Unraid
# Generated from Windows configuration on 2025-12-24

set -e

echo "=========================================="
echo "Claude Code Plugin Setup for Unraid"
echo "=========================================="
echo ""

# Check if claude is available
if ! command -v claude &> /dev/null; then
    echo "Error: 'claude' command not found."
    echo "Please install Claude Code first: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

echo "Step 1: Adding plugin marketplaces..."
echo ""

claude /plugin marketplace add https://github.com/anthropics/claude-code-plugins-official 2>/dev/null || echo "  - Official marketplace already added or failed"
claude /plugin marketplace add https://github.com/anthropics/claude-code-workflows 2>/dev/null || echo "  - Workflows marketplace already added or failed"
claude /plugin marketplace add https://github.com/alioshr/superpowers-marketplace 2>/dev/null || echo "  - Superpowers marketplace already added or failed"

echo ""
echo "Step 2: Installing user-scoped plugins (claude-code-workflows)..."
echo "These will be available across all projects."
echo ""

WORKFLOW_PLUGINS=(
    "python-development"
    "javascript-typescript"
    "backend-development"
    "kubernetes-operations"
    "cloud-infrastructure"
    "security-scanning"
    "code-review-ai"
    "full-stack-orchestration"
    "code-documentation"
    "debugging-toolkit"
    "git-pr-workflows"
    "frontend-mobile-development"
    "unit-testing"
    "incident-response"
    "accessibility-compliance"
)

for plugin in "${WORKFLOW_PLUGINS[@]}"; do
    echo "  Installing: $plugin"
    claude /plugin install "${plugin}@claude-code-workflows" --user 2>/dev/null || echo "    Warning: Failed to install $plugin"
done

echo ""
echo "Step 3: Installing project-scoped plugins (superpowers-marketplace)..."
echo "These will need to be enabled per-project."
echo ""

SUPERPOWERS_PLUGINS=(
    "double-shot-latte"
    "elements-of-style"
    "episodic-memory"
    "superpowers"
    "superpowers-chrome"
    "superpowers-developing-for-claude-code"
    "superpowers-lab"
)

for plugin in "${SUPERPOWERS_PLUGINS[@]}"; do
    echo "  Installing: $plugin"
    claude /plugin install "${plugin}@superpowers-marketplace" 2>/dev/null || echo "    Warning: Failed to install $plugin"
done

echo ""
echo "Step 4: Installing frontend-design (official)..."
claude /plugin install frontend-design@claude-plugins-official 2>/dev/null || echo "  Warning: Failed to install frontend-design"

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Installed plugins:"
echo "  - 15 user-scoped plugins (claude-code-workflows)"
echo "  - 7 project-scoped plugins (superpowers-marketplace)"
echo "  - 1 project-scoped plugin (official)"
echo ""
echo "Run 'claude /plugin list' to verify installation."
echo ""
