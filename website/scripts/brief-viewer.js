/**
 * Brief Viewer Module
 * Handles rendering and navigation of entity analytical briefs
 *
 * @module brief-viewer
 * @requires marked.js
 * @requires PDFViewer (Continuum.PDFViewer)
 */

window.Continuum = window.Continuum || {};

Continuum.BriefViewer = {
    currentEntity: null,
    entityList: [],
    currentIndex: -1,

    async open(entity) {
        this.currentEntity = entity;
        this.currentIndex = this.entityList.findIndex(e => e.id === entity.id);
        this.updateNavButtons();

        const viewer = document.getElementById('briefViewer');
        const content = document.getElementById('briefContent');
        const titleBar = document.getElementById('briefTitleBar');

        titleBar.textContent = entity.name;
        content.innerHTML = `
            <div class="brief-loading">
                <div class="loading-spinner"></div>
                <p>Loading analytical brief...</p>
            </div>
        `;
        viewer.classList.add('active');

        try {
            const briefPath = `/briefs/${entity.brief_file}`;
            const response = await fetch(briefPath);

            if (!response.ok) {
                throw new Error(`Brief not found: ${briefPath}`);
            }

            const markdown = await response.text();
            const html = this.renderMarkdown(markdown);
            content.innerHTML = html;

            // Add click handlers for entity mentions
            this.linkifyEntityMentions(content);

        } catch (error) {
            console.error('Error loading brief:', error);
            content.innerHTML = `
                <div style="text-align: center; padding: 3rem;">
                    <h2 style="color: var(--gold); margin-bottom: 1rem;">Brief Not Available</h2>
                    <p style="color: var(--smoke); margin-bottom: 1.5rem;">
                        The analytical brief for ${entity.name} could not be loaded.
                    </p>
                    <p style="color: var(--smoke); font-size: 0.9rem;">
                        Expected location: /briefs/${entity.brief_file}
                    </p>
                </div>
            `;
        }
    },

    renderMarkdown(markdown) {
        return marked.parse(markdown);
    },

    linkifyEntityMentions(container) {
        // Get all known entity names
        const entityNames = {};
        this.entityList.forEach(e => {
            entityNames[e.name.toLowerCase()] = e;
            // Also add common variations
            const nameParts = e.name.split(' ');
            if (nameParts.length > 1) {
                entityNames[nameParts[nameParts.length - 1].toLowerCase()] = e;
            }
        });

        // Linkify ECF references throughout the brief
        this.linkifyECFReferences(container);
    },

    // Convert ECF references into clickable links
    linkifyECFReferences(container) {
        // Combined pattern for all ECF formats
        const combinedPattern = /(?:ECF\s+(?:Doc(?:ument)?\.?\s*)?#?\s*|Document\s+|Doc\.\s*)(\d{3,4}(?:-\d{1,3})?)/gi;

        // Process all text nodes in the container
        const walker = document.createTreeWalker(
            container,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const nodesToProcess = [];
        let node;
        while (node = walker.nextNode()) {
            if (combinedPattern.test(node.textContent)) {
                nodesToProcess.push(node);
            }
            combinedPattern.lastIndex = 0; // Reset regex
        }

        // Process each text node
        nodesToProcess.forEach(textNode => {
            const text = textNode.textContent;
            const parent = textNode.parentNode;

            // Skip if already inside a link or ECF link
            if (parent.tagName === 'A' || parent.classList?.contains('ecf-link')) {
                return;
            }

            // Create a temporary container
            const span = document.createElement('span');
            let lastIndex = 0;
            let hasMatches = false;

            // Reset and find all matches
            combinedPattern.lastIndex = 0;
            const matches = [];
            let match;
            while ((match = combinedPattern.exec(text)) !== null) {
                matches.push({
                    fullMatch: match[0],
                    ecf: match[1],
                    index: match.index
                });
            }

            if (matches.length === 0) return;

            const self = this;
            matches.forEach(m => {
                hasMatches = true;
                // Add text before the match
                if (m.index > lastIndex) {
                    span.appendChild(document.createTextNode(text.slice(lastIndex, m.index)));
                }

                // Create clickable ECF link
                const ecfLink = document.createElement('span');
                ecfLink.className = 'ecf-link';
                ecfLink.textContent = m.fullMatch;
                ecfLink.dataset.ecf = m.ecf;
                ecfLink.title = `View ECF ${m.ecf}`;
                ecfLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    self.openECFDocument(m.ecf);
                });

                span.appendChild(ecfLink);
                lastIndex = m.index + m.fullMatch.length;
            });

            // Add remaining text
            if (lastIndex < text.length) {
                span.appendChild(document.createTextNode(text.slice(lastIndex)));
            }

            if (hasMatches) {
                parent.replaceChild(span, textNode);
            }
        });

        // Also make table cells with ECF numbers clickable
        this.linkifySourceTables(container);
    },

    // Make source document tables clickable
    linkifySourceTables(container) {
        const tables = container.querySelectorAll('table');
        const self = this;

        tables.forEach(table => {
            const rows = table.querySelectorAll('tbody tr, tr');
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length >= 2) {
                    const firstCell = cells[0];
                    const text = firstCell.textContent.trim();

                    // Check if first cell contains an ECF reference
                    const ecfMatch = text.match(/^(\d{3,4}(?:-\d{1,3})?(?:_\d+)?)$/);
                    if (ecfMatch) {
                        // Normalize ECF: remove underscore suffix for lookup
                        const ecfRaw = ecfMatch[1];
                        const ecf = ecfRaw.replace(/_\d+$/, '');

                        // Make the entire row clickable
                        row.classList.add('ecf-table-row');
                        row.style.cursor = 'pointer';
                        row.title = `View ECF ${ecf}`;
                        row.addEventListener('click', (e) => {
                            if (e.target.tagName !== 'A') {
                                e.preventDefault();
                                self.openECFDocument(ecf);
                            }
                        });

                        // Also wrap the ECF number in the cell
                        if (!firstCell.querySelector('.ecf-link')) {
                            firstCell.innerHTML = `<span class="ecf-link" data-ecf="${ecf}">${text}</span>`;
                        }
                    }
                }
            });
        });
    },

    // Open ECF document in PDF viewer
    openECFDocument(ecf) {
        // Get description from current entity's sources if available
        let description = 'Court Document';
        if (this.currentEntity && this.currentEntity.sources) {
            const sourceDoc = this.currentEntity.sources.find(s => s.ecf === ecf);
            if (sourceDoc) {
                description = sourceDoc.description || 'Court Document';
            }
        }

        // Open the PDF viewer with this ECF
        if (Continuum.PDFViewer) {
            Continuum.PDFViewer.open({
                ecf: ecf,
                description: description
            });
        }
    },

    close() {
        document.getElementById('briefViewer').classList.remove('active');
        this.currentEntity = null;
    },

    updateNavButtons() {
        const prevBtn = document.getElementById('briefPrev');
        const nextBtn = document.getElementById('briefNext');

        prevBtn.disabled = this.currentIndex <= 0;
        nextBtn.disabled = this.currentIndex >= this.entityList.length - 1;
    },

    prev() {
        if (this.currentIndex > 0) {
            const prevEntity = this.entityList[this.currentIndex - 1];
            if (prevEntity.brief_file) {
                this.open(prevEntity);
            }
        }
    },

    next() {
        if (this.currentIndex < this.entityList.length - 1) {
            const nextEntity = this.entityList[this.currentIndex + 1];
            if (nextEntity.brief_file) {
                this.open(nextEntity);
            }
        }
    }
};

// Alias for backward compatibility
const BriefViewer = Continuum.BriefViewer;
