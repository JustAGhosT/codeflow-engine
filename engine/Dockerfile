FROM python:3.12-slim

ARG RUN_TESTS=false

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && pip install --no-cache-dir poetry \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock README.md setup.py ./
COPY alembic ./alembic
COPY configs ./configs
COPY templates ./templates
COPY codeflow_engine ./codeflow_engine

RUN poetry install --with server,database,resilience --no-interaction

EXPOSE 8000

CMD ["python", "-m", "codeflow_engine.server"]
