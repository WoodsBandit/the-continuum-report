# Claude Desktop SMB Share Write Access - SOLVED

**Date Resolved:** December 23, 2025

---

## The Problem

Claude Desktop's MCP filesystem server was configured with the UNC path to the Continuum share:

```
\\192.168.1.139\continuum\
```

Despite this path being listed as "allowed," all write operations failed with:

```
Access denied - path outside allowed directories
```

Read operations worked fine. The SMB share was configured as public with full permissions. Multiple troubleshooting attempts were made including:
- Symbolic links
- Different MCP filesystem server configurations
- Verifying SMB permissions on Unraid
- Testing various path formats

## The Solution

**Use the mapped drive letter instead of the UNC path.**

The MCP Filesystem Plus server had `T:\` configured as an allowed directory. Writing to `T:\test.md` succeeded immediately.

## Why It Works

The path validation logic in the MCP filesystem servers doesn't properly normalize or compare UNC paths. When you write to `\\192.168.1.139\continuum\file.md`, the server's path matching fails to recognize it as being within the allowed `\\192.168.1.139\continuum\` directory.

The mapped drive letter `T:\` bypasses this issue entirely because:
1. Windows resolves `T:\` to the network location transparently
2. The path validation compares `T:\file.md` against `T:\` - a simple string prefix match that works correctly

## Configuration Fix

In your Claude Desktop MCP config (`claude_desktop_config.json`), ensure the filesystem server uses:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/mcp-filesystem-server",
        "T:\\",
        "C:\\Users\\Xx LilMan xX\\Documents\\Claude Docs"
      ]
    }
  }
}
```

**Not** the UNC path version.

## Key Takeaway

The issue was never SMB permissions or share configuration - it was a path string matching bug in the MCP filesystem server when handling UNC paths. Mapped drive letters work correctly.

---

*This resolves the TODO item: "Fix Claude's write access to \\192.168.1.139\continuum\ share"*
