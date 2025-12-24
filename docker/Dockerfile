# CodeFlow Engine Docker Image
# Multi-stage build for optimized production image

# Stage 1: Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual environment (we're in a container)
RUN poetry config virtualenvs.create false

# Install dependencies (without dev dependencies by default)
ARG RUN_TESTS=false
RUN if [ "$RUN_TESTS" = "true" ]; then \
        poetry install --no-interaction --no-ansi; \
    else \
        poetry install --no-interaction --no-ansi --only main,server,database,resilience; \
    fi

# Stage 2: Production stage
FROM python:3.12-slim as production

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash codeflow

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY codeflow_engine/ ./codeflow_engine/
COPY pyproject.toml ./
COPY alembic/ ./alembic/

# Set ownership to non-root user
RUN chown -R codeflow:codeflow /app

# Switch to non-root user
USER codeflow

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8080

# Expose the application port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command: run the server
CMD ["python", "-m", "codeflow_engine.server"]
