# Multi-stage Dockerfile for The Continuum Report
# Production-ready with security best practices

# =============================================================================
# STAGE 1: BUILDER
# =============================================================================
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 2: RUNTIME
# =============================================================================
FROM python:3.11-slim

# Set metadata
LABEL maintainer="The Continuum Report"
LABEL description="AI-powered document processing pipeline with Paperless-ngx and Ollama integration"
LABEL version="1.0.0"

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r continuum && useradd -r -g continuum continuum

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /continuum

# Copy application code
COPY --chown=continuum:continuum scripts/ /continuum/scripts/

# Create required directories
RUN mkdir -p /continuum/{entity_data,reports,checkpoints,documents/inbox} && \
    chown -R continuum:continuum /continuum

# Switch to non-root user
USER continuum

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1 || true

# Default command - run the main pipeline
CMD ["python", "-m", "scripts.continuum_pipeline"]
