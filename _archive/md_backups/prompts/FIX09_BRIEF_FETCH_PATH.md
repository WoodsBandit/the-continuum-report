# FIX09: Connection Briefs Fetch Path

## ISSUE
Clicking "View Brief" on the connections panel shows "Connections Brief Not Available" even though Phase 5 has been run and connection briefs exist.

## ROOT CAUSE
In `ConnectionsPanel.openConnectionsBrief()` (line ~5079), the path is:

```javascript
const briefPath = `/continuum/briefs/connections/${entityId}_connections.md`;
```

This path may not match the actual location of the briefs on the server.

## POTENTIAL PATH ISSUES

### Issue 1: Wrong Base Path
The website is served at `thecontinuumreport.com/continuum.html`
- If briefs are at `/continuum/briefs/...`, path would be `thecontinuumreport.com/continuum/briefs/...`
- If briefs are at root `/briefs/...`, path would be `thecontinuumreport.com/briefs/...`

### Issue 2: File Naming Convention
Phase 5 may have created files with different names:
- Expected: `prince-andrew_connections.md`
- Actual: `prince_andrew_connections.md` (underscores)
- Or: `Prince Andrew_connections.md` (spaces/caps)

### Issue 3: Directory Structure
Briefs might be in a different location:
- `/briefs/connections/`
- `/data/briefs/`
- `/continuum/data/briefs/`

## FILE
`/continuum/website/continuum.html`

## LOCATION
`ConnectionsPanel.openConnectionsBrief()` function, around line 5079-5115

## DIAGNOSIS
First, determine where briefs actually are:

```bash
# On server, find brief files
find /mnt/user/continuum -name "*_connections.md" 2>/dev/null
ls -la /mnt/user/continuum/briefs/
ls -la /mnt/user/continuum/briefs/connections/
```

Also check from browser console:
```javascript
// Try to fetch a known entity's brief
fetch('/briefs/connections/prince-andrew_connections.md')
    .then(r => console.log('Found at /briefs/', r.ok))
    .catch(e => console.log('Not at /briefs/'));

fetch('/continuum/briefs/connections/prince-andrew_connections.md')
    .then(r => console.log('Found at /continuum/briefs/', r.ok))
    .catch(e => console.log('Not at /continuum/briefs/'));

fetch('/data/briefs/connections/prince-andrew_connections.md')
    .then(r => console.log('Found at /data/briefs/', r.ok))
    .catch(e => console.log('Not at /data/briefs/'));
```

## FIX

### Step 1: Verify Actual Path
Check where Cloudflare/Nginx is serving files from and where Phase 5 output went.

### Step 2: Update Path in Code
Once you know the correct path:

```javascript
openConnectionsBrief(entityId) {
    if (!entityId) {
        console.warn('No entity ID provided');
        return;
    }

    const entity = Graph.nodes?.find(n => n.id === entityId);
    const entityName = entity?.name || entityId;

    // UPDATE THIS PATH based on actual server structure
    // Option 1: Relative to site root
    const briefPath = `/briefs/connections/${entityId}_connections.md`;
    
    // Option 2: Under /continuum/
    // const briefPath = `/continuum/briefs/connections/${entityId}_connections.md`;
    
    // Option 3: Under /data/
    // const briefPath = `/data/briefs/connections/${entityId}_connections.md`;

    console.log('Fetching brief from:', briefPath);  // Debug

    fetch(briefPath)
        .then(response => {
            if (!response.ok) throw new Error('Brief not found');
            return response.text();
        })
        .then(markdown => {
            const html = typeof marked !== 'undefined' ? marked.parse(markdown) : `<pre>${markdown}</pre>`;
            this.showBriefModal(entityName, html);
        })
        .catch(error => {
            console.error('Brief fetch error:', error);
            this.showBriefModal(entityName, `
                <div style="text-align: center; padding: 2rem;">
                    <h3 style="color: var(--gold); margin-bottom: 1rem;">Connections Brief Not Available</h3>
                    <p style="color: var(--mist); line-height: 1.6;">
                        The connections brief for <strong>${entityName}</strong> could not be loaded.
                    </p>
                    <p style="color: var(--smoke); font-size: 0.85rem; margin-top: 1rem;">
                        Path attempted: ${briefPath}
                    </p>
                </div>
            `);
        });
}
```

### Step 3: Handle ID Format Variations
Entity IDs might have different formats. Normalize:

```javascript
openConnectionsBrief(entityId) {
    // Normalize entity ID for file lookup
    const normalizedId = entityId
        .toLowerCase()
        .replace(/\s+/g, '-')      // spaces to hyphens
        .replace(/[^a-z0-9-]/g, ''); // remove special chars
    
    const briefPath = `/briefs/connections/${normalizedId}_connections.md`;
    // ...
}
```

## SERVER CONFIGURATION CHECK
If briefs exist but aren't being served, check Nginx/Cloudflare configuration:

```nginx
# In nginx.conf or cloudflare tunnel config
location /briefs/ {
    root /mnt/user/continuum;
    autoindex off;
}
```

## VERIFICATION
1. Confirm brief files exist on server
2. Confirm the web server path to access them
3. Update code with correct path
4. Test by clicking "View Brief" on a connection
5. Verify brief content displays in modal

## BACKUP BEFORE CHANGES
```bash
cp /continuum/website/continuum.html /continuum/website/backups/continuum_pre-fix09.html
```
