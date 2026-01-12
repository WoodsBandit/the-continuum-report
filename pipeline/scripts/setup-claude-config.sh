#!/bin/bash
# Direct Claude Code Config Setup for Docker Container
# Copies settings and marketplace config directly

CLAUDE_DIR="/.claude"
PLUGIN_DIR="$CLAUDE_DIR/plugins"

echo "=========================================="
echo "Claude Code Config Setup (Direct Copy)"
echo "=========================================="
echo ""

# Create plugins directory if needed
mkdir -p "$PLUGIN_DIR"

# Write the settings.json with enabled plugins
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

echo "Created settings.json with enabled plugins"

# Write the known_marketplaces.json
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

echo "Created known_marketplaces.json with 3 marketplaces"

echo ""
echo "=========================================="
echo "Config files created!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Restart Claude Code (or the container)"
echo "2. Run: claude /plugin"
echo "3. Go to 'Discover' tab - plugins should now be available"
echo "4. Install the plugins you want"
echo ""
