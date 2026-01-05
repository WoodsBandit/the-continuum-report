/**
 * Data Loader Module
 * Handles fetching and parsing of entity/connection data
 *
 * @module data-loader
 */

// Global namespace for the Continuum application
window.Continuum = window.Continuum || {};

// Sources index for PDF availability checking
Continuum.sourcesIndex = null;

/**
 * Load all data required for the application
 * @returns {Promise<{entities: Array, connections: Array}>}
 */
Continuum.loadData = async function() {
    const statusEl = document.getElementById('loadingStatus');
    try {
        statusEl.textContent = 'Fetching entities...';
        const entitiesRes = await fetch('/data/entities.json');
        if (!entitiesRes.ok) throw new Error('Failed to load entities.json');
        const entitiesData = await entitiesRes.json();

        statusEl.textContent = 'Fetching connections...';
        const connectionsRes = await fetch('/data/connections.json');
        if (!connectionsRes.ok) throw new Error('Failed to load connections.json');
        const connectionsData = await connectionsRes.json();

        // Load sources index for PDF availability
        statusEl.textContent = 'Fetching sources index...';
        try {
            const sourcesRes = await fetch('/sources/index.json');
            if (sourcesRes.ok) {
                Continuum.sourcesIndex = await sourcesRes.json();
            }
        } catch (e) {
            console.warn('Sources index not available:', e);
        }

        statusEl.textContent = 'Building graph...';
        return {
            entities: entitiesData.entities,
            connections: connectionsData.connections
        };
    } catch (error) {
        console.error('Error loading data:', error);
        throw error;
    }
};

// Export for ES6 module usage (if loaded as module)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { loadData: Continuum.loadData };
}
