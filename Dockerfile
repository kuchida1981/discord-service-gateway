FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Install dependencies first (cached layer)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy source (overridden by volume mount in development)
COPY src/ ./src/

# Cloud Run compatibility: Use PORT environment variable if set, otherwise default to 8000
# In production (Cloud Run), --reload is omitted for performance
ENV PORT=8000
CMD ["/bin/sh", "-c", "exec uv run uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]
