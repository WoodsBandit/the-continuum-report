"""
The Continuum Report - CLI Scripts

This package contains command-line tools for The Continuum Report pipeline:
- continuum_pipeline: Main document analysis and dossier generation
- build_graph: Knowledge graph construction from briefs
- brief_watcher: File watcher for automatic processing
- entity_discovery: Entity extraction from documents
- export_sources: Export document sources

All scripts can be run as modules or via their CLI entry points
after installing the package.
"""

__all__ = [
    "continuum_pipeline",
    "build_graph",
    "brief_watcher",
    "entity_discovery",
    "export_sources",
]
