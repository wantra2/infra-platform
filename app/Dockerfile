FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app/src


# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /uvx /bin/

# Copy dependency definitions first for Docker layer caching
COPY pyproject.toml uv.lock /app/



FROM base AS runtime
RUN useradd \
    --create-home \
    --uid 10001 \
    appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

RUN uv sync --directory /app/ --locked --no-dev
COPY src /app/src
CMD ["uvicorn", "infra_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS test

RUN uv sync --directory /app/ --locked 
COPY src /app/src
CMD ["sh", "-c", "uv run alembic upgrade head && uv run pytest -v"]