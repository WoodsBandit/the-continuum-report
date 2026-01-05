# Continuum Frontend Scripts

## Module Architecture

The Continuum application JavaScript is being modularized from a monolithic `continuum.html` into separate ES modules. This is an incremental migration - modules can be adopted one at a time.

### Current Status

| Module | Lines | Status | Dependencies |
|--------|-------|--------|--------------|
| `data-loader.js` | ~50 | Extracted | None |
| `brief-viewer.js` | ~260 | Extracted | PDFViewer |
| `pdf-viewer.js` | ~340 | Extracted | sourcesIndex |
| `hierarchy-manager.js` | ~875 | Pending | Graph, EntitiesLayer |
| `entities-layer.js` | ~480 | Pending | Graph, BriefViewer |
| `graph.js` | ~1040 | Pending | HierarchyManager, BriefViewer |
| `connections-panel.js` | ~130 | Pending | None |
| `main.js` | ~210 | Pending | All modules |

### Global Namespace Pattern

Due to circular dependencies between modules (Graph ↔ HierarchyManager ↔ EntitiesLayer), we use a global namespace pattern rather than ES6 module imports:

```javascript
// Each module registers itself on window.Continuum
window.Continuum = window.Continuum || {};

Continuum.ModuleName = {
    // module methods
};

// Local alias for backward compatibility
const ModuleName = Continuum.ModuleName;
```

### Load Order (when using separate scripts)

If loading as separate `<script>` tags (not ES modules):

```html
<!-- CDN Dependencies -->
<script src="d3.min.js"></script>
<script src="marked.min.js"></script>
<script src="pdf.min.js"></script>

<!-- Application Modules (order matters) -->
<script src="/scripts/data-loader.js"></script>
<script src="/scripts/pdf-viewer.js"></script>
<script src="/scripts/brief-viewer.js"></script>
<script src="/scripts/hierarchy-manager.js"></script>
<script src="/scripts/entities-layer.js"></script>
<script src="/scripts/graph.js"></script>
<script src="/scripts/connections-panel.js"></script>
<script src="/scripts/main.js"></script>
```

### Module Dependencies

```
                    ┌─────────────────┐
                    │   data-loader   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────────┐
        │ PDFViewer│  │BriefViewer│  │HierarchyMgr │
        └────┬─────┘  └─────┬────┘  └──────┬───────┘
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │    Graph     │◄────────┐
                    └──────┬───────┘         │
                           │                 │
              ┌────────────┴─────────────┐   │
              │                          │   │
              ▼                          ▼   │
      ┌──────────────┐          ┌────────────┴───┐
      │EntitiesLayer │          │ConnectionsPanel│
      └──────────────┘          └────────────────┘
```

### Using Extracted Modules

For now, the extracted modules (`data-loader.js`, `brief-viewer.js`, `pdf-viewer.js`) can be tested standalone by including them before the inline script in `continuum.html`.

### Future Migration Path

1. **Phase 1** (current): Extract utility modules with minimal dependencies
2. **Phase 2**: Extract UI components (ConnectionsPanel, BriefViewer, PDFViewer)
3. **Phase 3**: Extract core visualization (HierarchyManager, EntitiesLayer, Graph)
4. **Phase 4**: Create `main.js` entry point
5. **Phase 5**: Convert to ES modules with bundler (esbuild/rollup)

### Development Notes

- All modules must register on `window.Continuum` for cross-module access
- Keep backward-compatible aliases (`const ModuleName = Continuum.ModuleName`)
- Test after each module extraction to ensure functionality
- The inline script in `continuum.html` remains the source of truth until full migration

## File Structure

```
website/scripts/
├── README.md              # This file
├── data-loader.js         # Data fetching utilities
├── brief-viewer.js        # Markdown brief rendering
├── pdf-viewer.js          # PDF.js integration
├── hierarchy-manager.js   # (pending) Hierarchical zoom navigation
├── entities-layer.js      # (pending) Entity grid view
├── graph.js               # (pending) D3 force-directed graph
├── connections-panel.js   # (pending) Connection dropdown UI
└── main.js                # (pending) Entry point & event handlers
```
