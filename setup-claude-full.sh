#!/bin/bash
# Full Claude Code Plugin Setup - Auto-installs everything
# No manual intervention needed

CLAUDE_DIR="/.claude"
PLUGIN_DIR="$CLAUDE_DIR/plugins"
CACHE_DIR="$PLUGIN_DIR/cache"

echo "=========================================="
echo "Claude Code Full Plugin Setup"
echo "=========================================="
echo ""

# Create directories
mkdir -p "$CACHE_DIR/claude-code-workflows"
mkdir -p "$CACHE_DIR/superpowers-marketplace"
mkdir -p "$CACHE_DIR/claude-plugins-official"

# Write settings.json with enabled plugins
cat > "$CLAUDE_DIR/settings.json" << 'EOF'
{
  "enabledPlugins": {
    "python-development@claude-code-workflows": true,
    "javascript-typescript@claude-code-workflows": true,
    "backend-development@claude-code-workflows": true,
    "kubernetes-operations@claude-code-workflows": true,
    "cloud-infrastructure@claude-code-workflows": true,
    "security-scanning@claude-code-workflows": true,
    "code-review-ai@claude-code-workflows": true,
    "full-stack-orchestration@claude-code-workflows": true,
    "code-documentation@claude-code-workflows": true,
    "debugging-toolkit@claude-code-workflows": true,
    "git-pr-workflows@claude-code-workflows": true,
    "frontend-mobile-development@claude-code-workflows": true,
    "unit-testing@claude-code-workflows": true,
    "incident-response@claude-code-workflows": true,
    "accessibility-compliance@claude-code-workflows": true
  }
}
EOF
echo "✓ Created settings.json"

# Write known_marketplaces.json
cat > "$PLUGIN_DIR/known_marketplaces.json" << 'EOF'
{
  "marketplaces": [
    {
      "name": "claude-plugins-official",
      "url": "https://github.com/anthropics/claude-code-plugins-official",
      "autoUpdate": true
    },
    {
      "name": "claude-code-workflows",
      "url": "https://github.com/anthropics/claude-code-workflows",
      "autoUpdate": true
    },
    {
      "name": "superpowers-marketplace",
      "url": "https://github.com/alioshr/superpowers-marketplace",
      "autoUpdate": true
    }
  ]
}
EOF
echo "✓ Created known_marketplaces.json"

# Write installed_plugins.json with all plugins
cat > "$PLUGIN_DIR/installed_plugins.json" << 'EOF'
{
  "version": 2,
  "plugins": {
    "python-development@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/python-development/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "javascript-typescript@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/javascript-typescript/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "backend-development@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/backend-development/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "kubernetes-operations@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/kubernetes-operations/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "cloud-infrastructure@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/cloud-infrastructure/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "security-scanning@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/security-scanning/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "code-review-ai@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/code-review-ai/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "full-stack-orchestration@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/full-stack-orchestration/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "code-documentation@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/code-documentation/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "debugging-toolkit@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/debugging-toolkit/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "git-pr-workflows@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/git-pr-workflows/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "frontend-mobile-development@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/frontend-mobile-development/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "unit-testing@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/unit-testing/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "incident-response@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/incident-response/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ],
    "accessibility-compliance@claude-code-workflows": [
      {
        "scope": "user",
        "installPath": "/.claude/plugins/cache/claude-code-workflows/accessibility-compliance/latest",
        "version": "latest",
        "installedAt": "2025-12-24T20:00:00.000Z",
        "lastUpdated": "2025-12-24T20:00:00.000Z",
        "isLocal": false
      }
    ]
  }
}
EOF
echo "✓ Created installed_plugins.json with 15 plugins"

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Restart the container, then Claude Code should"
echo "auto-download the plugins on first launch."
echo ""
echo "Run: docker restart claude-code"
echo ""
