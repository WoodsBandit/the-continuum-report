# Claude Code Session Start Prompt — The Continuum Report

Copy everything below the line and paste it to start a new session:

---

## Session Initialization

You are starting a session for **The Continuum Report** project.

### Step 1: Access the Network Share

The project lives on a network share. Access it via PowerShell (bash shell mangles UNC paths):

```powershell
# To list files, use this pattern:
powershell -Command "Get-ChildItem -LiteralPath ([char]92 + [char]92 + '192.168.1.139' + [char]92 + 'continuum') | Select-Object Name, Mode"

# To read files, use the Read tool with path: \\192.168.1.139\continuum\<filename>
```

### Step 2: Read the Master Context

Read the main project briefing:
```
\\192.168.1.139\continuum\CLAUDE.md
```

This contains:
- Project vision and mission
- Legal framework (CRITICAL — opinion-protection requirements)
- Document corpus locations
- Entity & connection system (15 briefs, 78 connections)
- Key discoveries (Wexner co-conspirator, leaked emails)
- Technical infrastructure (Paperless-ngx, website, server)
- Current priorities
- Commands reference

### Step 3: Key Quick Reference

| Resource | Location |
|----------|----------|
| **Network Share** | `\\192.168.1.139\continuum\` |
| **Paperless-ngx** | http://192.168.1.139:8040 |
| **API Token** | `da99fe6aa0b8d021689126cf72b91986abbbd283` |
| **Website** | https://thecontinuumreport.com |
| **Briefs** | `\\192.168.1.139\continuum\briefs\` (entity/, connections/) |
| **Website files** | `\\192.168.1.139\continuum\website\` |
| **Source PDFs** | `\\192.168.1.139\continuum\website\sources\` |
| **Agent definitions** | `\\192.168.1.139\continuum\agents\` |

### Step 4: Understand the Legal Framework

**CRITICAL:** All content uses opinion-protection framework per *Milkovich v. Lorain Journal* (1990).

Every analytical brief MUST have:
- "ANALYTICAL BRIEF — EDITORIAL COMMENTARY" header
- "The Public Record" section (ONLY quotes + citations, NO interpretation)
- "Editorial Analysis" section (clearly labeled opinion)
- "Alternative Interpretations" section (5-7 minimum — strongest liability shield)
- Opinion-signaling language ("In our assessment...", "We interpret this as...")

**Never use:** "dossier", assertive language implying guilt, rhetorical questions

### Step 5: Current Priorities

1. **Fix Maxwell Sentencing Memos** — Current files are wrong (Nov 2021 pretrial motions, need June 2022 sentencing)
2. **OCR the DOJ 33k Files** — 33,564 image-based PDFs need text extraction
3. **Source Document Hosting** — Continue populating `/website/sources/`
4. **Citation Table Rebuild** — Update briefs with direct download links

### Step 6: Working with Files

**Reading files:**
```
Read tool with path: \\192.168.1.139\continuum\path\to\file.md
```

**Listing directories:**
```powershell
powershell -Command "Get-ChildItem -LiteralPath ([char]92 + [char]92 + '192.168.1.139' + [char]92 + 'continuum' + [char]92 + 'briefs') | Select-Object Name"
```

**Searching files:**
```powershell
powershell -Command "Get-ChildItem -LiteralPath ([char]92 + [char]92 + '192.168.1.139' + [char]92 + 'continuum') -Recurse -Filter '*.md' | Select-Object FullName"
```

**Paperless API:**
```bash
curl -H "Authorization: Token da99fe6aa0b8d021689126cf72b91986abbbd283" "http://192.168.1.139:8040/api/documents/?query=SEARCH_TERM"
```

---

## Ready to Work

After reading CLAUDE.md, you'll have full context on:
- The mission (documenting power networks with rigorous sourcing)
- The operator (WoodsBandit — Christian worldview, forensic approach)
- The legal requirements (opinion protection, alternative interpretations)
- The technical stack (Paperless, Unraid server, Cloudflare tunnel)
- The document corpus (DOJ 33k, court filings, depositions, books)
- The 13-agent architecture for parallel specialized work

**Ask the user what they'd like to work on, or review current priorities.**
