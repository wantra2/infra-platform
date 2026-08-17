FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app/src

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*


# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency definitions first for Docker layer caching
COPY pyproject.toml uv.lock /app/

COPY src /app/src

FROM base AS runtime
RUN useradd \
    --create-home \
    --uid 10001 \
    appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000
# Install exactly what's in uv.lock
RUN uv sync --directory /app/ --locked --no-dev
CMD ["uvicorn", "infra_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS test
# Install exactly what's in uv.lock
RUN uv sync --directory /app/ --locked 
CMD ["sh", "-c", "uv run alembic upgrade head && uv run pytest -v"]