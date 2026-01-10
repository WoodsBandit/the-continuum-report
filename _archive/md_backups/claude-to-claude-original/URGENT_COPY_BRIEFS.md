# URGENT: Copy Remaining Connection Briefs to Website

## TASK
Bulk copy all connection brief files from `/continuum/briefs/connections/` to `/continuum/website/briefs/connections/`.

## WHAT'S BEEN DONE
The following files have already been copied:
- All 15 `*_connections.md` entity briefs
- `manifest.json`
- 2 pairwise briefs (jeffrey-epstein_virginia-giuffre.md, ghislaine-maxwell_jeffrey-epstein.md)

## WHAT NEEDS TO BE COPIED
All remaining pairwise connection briefs (~68 files) like:
- `prince-andrew_virginia-giuffre.md`
- `alan-dershowitz_jeffrey-epstein.md`
- `deutsche-bank_jeffrey-epstein.md`
- etc.

## COMMAND
```bash
# Copy all files that don't already exist in destination
cd /continuum/briefs/connections/
for file in *.md; do
    if [ ! -f "/continuum/website/briefs/connections/$file" ]; then
        cp "$file" "/continuum/website/briefs/connections/"
        echo "Copied: $file"
    fi
done
```

## VERIFICATION
```bash
# Count files in source
ls -1 /continuum/briefs/connections/*.md | wc -l

# Count files in destination
ls -1 /continuum/website/briefs/connections/*.md | wc -l

# Should match
```

## PRIORITY
HIGH - This is blocking connection brief display on the live site.

---
*Task from Continuum Visualization Expert — 2025-12-23*
