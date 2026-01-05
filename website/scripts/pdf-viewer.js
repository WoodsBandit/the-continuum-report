/**
 * PDF Viewer Module
 * Handles rendering and navigation of PDF documents using pdf.js
 *
 * @module pdf-viewer
 * @requires pdf.js (pdfjsLib)
 */

window.Continuum = window.Continuum || {};

Continuum.PDFViewer = {
    // State
    pdfDoc: null,
    currentPage: 1,
    totalPages: 0,
    scale: 1.5,
    currentPdfPath: null,
    rendering: false,

    // Case folder mappings - most briefs cite Giuffre v. Maxwell
    caseInfo: {
        'giuffre-v-maxwell': {
            citation: 'Giuffre v. Maxwell, No. 15-cv-07433-LAP (S.D.N.Y.)',
            pacer: 'https://pacer.uscourts.gov'
        },
        'epstein-sdny': {
            citation: 'United States v. Epstein, No. 19-cr-00490 (S.D.N.Y.)',
            pacer: 'https://pacer.uscourts.gov'
        },
        'maxwell-criminal': {
            citation: 'United States v. Maxwell, No. 20-cr-00330 (S.D.N.Y.)',
            pacer: 'https://pacer.uscourts.gov'
        }
    },

    init() {
        // Set up pdf.js worker
        if (typeof pdfjsLib !== 'undefined') {
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        }

        // Bind navigation controls
        document.getElementById('pdfPrevPage')?.addEventListener('click', () => this.prevPage());
        document.getElementById('pdfNextPage')?.addEventListener('click', () => this.nextPage());
        document.getElementById('pdfZoomIn')?.addEventListener('click', () => this.zoomIn());
        document.getElementById('pdfZoomOut')?.addEventListener('click', () => this.zoomOut());
    },

    // Check if PDF is available in sources index
    isPdfAvailable(ecf) {
        const sourcesIndex = Continuum.sourcesIndex;
        if (!sourcesIndex || !sourcesIndex.cases) return { available: false, caseFolder: null };

        // Search all cases for this ECF number
        for (const [folder, caseData] of Object.entries(sourcesIndex.cases)) {
            const doc = caseData.documents.find(d => d.ecf === ecf);
            if (doc && doc.available) {
                return { available: true, caseFolder: folder, filename: doc.filename };
            }
        }
        return { available: false, caseFolder: 'giuffre-v-maxwell' }; // Default case for PACER link
    },

    // Check if on mobile device
    isMobile() {
        return window.innerWidth <= 768 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    },

    async open(source) {
        const viewer = document.getElementById('pdfViewer');
        const container = document.getElementById('pdfContainer');
        const title = document.getElementById('pdfTitle');
        const navControls = document.getElementById('pdfNavControls');
        const downloadLink = document.getElementById('pdfDownloadLink');

        title.textContent = `ECF ${source.ecf} - ${source.description}`;

        // Reset state
        this.pdfDoc = null;
        this.currentPage = 1;
        this.totalPages = 0;
        this.scale = this.isMobile() ? 1.0 : 1.5;

        // Check PDF availability from pre-loaded index
        const pdfStatus = this.isPdfAvailable(source.ecf);
        const caseFolder = pdfStatus.caseFolder || 'giuffre-v-maxwell';
        const caseData = this.caseInfo[caseFolder];

        if (pdfStatus.available) {
            const pdfPath = `/sources/${caseFolder}/${pdfStatus.filename}`;
            this.currentPdfPath = pdfPath;

            // Show download link
            downloadLink.href = pdfPath;
            downloadLink.style.display = 'flex';

            // Show loading state
            container.innerHTML = `
                <div class="pdf-loading">
                    <div class="loading-spinner"></div>
                    <p>Loading document...</p>
                </div>
            `;
            navControls.style.display = 'none';

            viewer.classList.add('active');

            // Try to load with pdf.js
            await this.loadPDF(pdfPath, container, source, caseData);
        } else {
            // PDF not available - show PACER verification link
            downloadLink.style.display = 'none';
            navControls.style.display = 'none';

            container.innerHTML = `
                <div class="pdf-placeholder">
                    <h3>ECF Document ${source.ecf}</h3>
                    <p><strong>${source.description}</strong></p>
                    <p style="margin-top: 1.5rem; font-size: 0.95rem; color: var(--smoke);">
                        This document is not yet available in our archive.
                    </p>
                    <p style="margin-top: 1.5rem;">
                        <span class="pacer-verify">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 0.5rem;">
                                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                            </svg>
                            Verify via PACER: <em>${caseData.citation}</em>
                        </span>
                    </p>
                    <p style="margin-top: 1.5rem; font-size: 0.85rem;">
                        <a href="${caseData.pacer}" target="_blank" rel="noopener" style="color: var(--gold);">
                            Access PACER →
                        </a>
                    </p>
                </div>
            `;

            viewer.classList.add('active');
        }
    },

    async loadPDF(pdfPath, container, source, caseData) {
        // Check if pdf.js is available
        if (typeof pdfjsLib === 'undefined') {
            // Fallback to iframe for desktop, download for mobile
            this.showFallback(pdfPath, container, source, caseData);
            return;
        }

        try {
            // Load the PDF document
            const loadingTask = pdfjsLib.getDocument(pdfPath);
            this.pdfDoc = await loadingTask.promise;
            this.totalPages = this.pdfDoc.numPages;

            // Set up the canvas container
            container.innerHTML = `<div class="pdf-canvas-wrapper" id="pdfCanvasWrapper"><canvas id="pdfCanvas"></canvas></div>`;

            // Show navigation controls
            document.getElementById('pdfNavControls').style.display = 'flex';
            this.updatePageInfo();

            // Render the first page
            await this.renderPage(this.currentPage);

            // Add touch/pinch zoom support for mobile
            this.setupTouchZoom();

        } catch (error) {
            console.error('Error loading PDF with pdf.js:', error);
            // Fallback
            this.showFallback(pdfPath, container, source, caseData);
        }
    },

    showFallback(pdfPath, container, source, caseData) {
        const navControls = document.getElementById('pdfNavControls');
        navControls.style.display = 'none';

        if (this.isMobile()) {
            // On mobile, show download button prominently
            container.innerHTML = `
                <div class="pdf-placeholder">
                    <h3>ECF Document ${source.ecf}</h3>
                    <p><strong>${source.description}</strong></p>
                    <p style="margin-top: 1rem; font-size: 0.9rem;">
                        Source: <em>${caseData.citation}</em>
                    </p>
                    <p style="margin-top: 1.5rem; color: var(--smoke);">
                        For the best viewing experience on mobile, open this document in your device's PDF viewer.
                    </p>
                    <p style="margin-top: 1.5rem;">
                        <a href="${pdfPath}" target="_blank" class="pdf-download-btn">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
                            </svg>
                            Open in PDF Viewer
                        </a>
                    </p>
                </div>
            `;
        } else {
            // On desktop, use iframe
            container.innerHTML = `<iframe src="${pdfPath}" title="ECF ${source.ecf}"></iframe>`;
        }
    },

    async renderPage(pageNum) {
        if (!this.pdfDoc || this.rendering) return;

        this.rendering = true;
        const canvas = document.getElementById('pdfCanvas');
        const ctx = canvas.getContext('2d');

        try {
            const page = await this.pdfDoc.getPage(pageNum);

            // Get device pixel ratio for crisp rendering on retina/high-DPI displays
            const pixelRatio = window.devicePixelRatio || 1;

            // Calculate base scale based on container width for mobile
            let baseScale = this.scale;
            if (this.isMobile()) {
                const wrapper = document.getElementById('pdfCanvasWrapper');
                const wrapperWidth = wrapper.clientWidth - 20; // Account for padding
                const baseViewport = page.getViewport({ scale: 1 });
                baseScale = Math.min(wrapperWidth / baseViewport.width, this.scale);
            }

            // Create viewport at base scale for CSS dimensions
            const cssViewport = page.getViewport({ scale: baseScale });

            // Create viewport at higher resolution for crisp rendering
            const renderScale = baseScale * pixelRatio;
            const renderViewport = page.getViewport({ scale: renderScale });

            // Set canvas dimensions at high resolution
            canvas.width = renderViewport.width;
            canvas.height = renderViewport.height;

            // Set CSS dimensions at logical size (this creates crisp rendering)
            canvas.style.width = cssViewport.width + 'px';
            canvas.style.height = cssViewport.height + 'px';

            const renderContext = {
                canvasContext: ctx,
                viewport: renderViewport
            };

            await page.render(renderContext).promise;
            this.updatePageInfo();

        } catch (error) {
            console.error('Error rendering page:', error);
        }

        this.rendering = false;
    },

    updatePageInfo() {
        const pageInfo = document.getElementById('pdfPageInfo');
        const prevBtn = document.getElementById('pdfPrevPage');
        const nextBtn = document.getElementById('pdfNextPage');

        pageInfo.textContent = `${this.currentPage} / ${this.totalPages}`;
        prevBtn.disabled = this.currentPage <= 1;
        nextBtn.disabled = this.currentPage >= this.totalPages;
    },

    prevPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.renderPage(this.currentPage);
            // Scroll to top of canvas
            document.getElementById('pdfCanvasWrapper')?.scrollTo(0, 0);
        }
    },

    nextPage() {
        if (this.currentPage < this.totalPages) {
            this.currentPage++;
            this.renderPage(this.currentPage);
            // Scroll to top of canvas
            document.getElementById('pdfCanvasWrapper')?.scrollTo(0, 0);
        }
    },

    zoomIn() {
        this.scale = Math.min(this.scale + 0.25, 3);
        this.renderPage(this.currentPage);
    },

    zoomOut() {
        this.scale = Math.max(this.scale - 0.25, 0.5);
        this.renderPage(this.currentPage);
    },

    setupTouchZoom() {
        const wrapper = document.getElementById('pdfCanvasWrapper');
        if (!wrapper) return;

        let initialDistance = 0;
        let initialScale = this.scale;
        const self = this;

        wrapper.addEventListener('touchstart', (e) => {
            if (e.touches.length === 2) {
                initialDistance = Math.hypot(
                    e.touches[0].pageX - e.touches[1].pageX,
                    e.touches[0].pageY - e.touches[1].pageY
                );
                initialScale = self.scale;
            }
        }, { passive: true });

        wrapper.addEventListener('touchmove', (e) => {
            if (e.touches.length === 2 && initialDistance > 0) {
                const currentDistance = Math.hypot(
                    e.touches[0].pageX - e.touches[1].pageX,
                    e.touches[0].pageY - e.touches[1].pageY
                );
                const ratio = currentDistance / initialDistance;
                const newScale = Math.min(Math.max(initialScale * ratio, 0.5), 3);

                if (Math.abs(newScale - self.scale) > 0.1) {
                    self.scale = newScale;
                    self.renderPage(self.currentPage);
                }
            }
        }, { passive: true });

        wrapper.addEventListener('touchend', () => {
            initialDistance = 0;
        }, { passive: true });
    },

    close() {
        const viewer = document.getElementById('pdfViewer');
        const navControls = document.getElementById('pdfNavControls');
        const downloadLink = document.getElementById('pdfDownloadLink');

        viewer.classList.remove('active');
        navControls.style.display = 'none';
        downloadLink.style.display = 'none';

        // Clean up
        this.pdfDoc = null;
        this.currentPage = 1;
        this.totalPages = 0;
        this.currentPdfPath = null;
    }
};

// Alias for backward compatibility
const PDFViewer = Continuum.PDFViewer;
