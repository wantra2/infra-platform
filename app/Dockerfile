FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app/src

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir \
    "fastapi" \
    "uvicorn[standard]" \
    "sqlalchemy>=2.0" \
    "psycopg[binary]" \
    "alembic>=1.16" \
    "pydantic-settings" \
    "prometheus-fastapi-instrumentator"

COPY src .

RUN useradd \
    --create-home \
    --uid 10001 \
    appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "infra_api.main:app", "--host", "0.0.0.0", "--port", "8000"]