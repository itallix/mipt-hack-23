FROM python:3.11-slim-buster

ENV PYTHONDONOTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.5.1
ENV APP_HOME /bot

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install poetry==${POETRY_VERSION} && \
    poetry config virtualenvs.create false

WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock $APP_HOME
COPY bot_service ./bot_service

RUN poetry install \
      --no-cache \
      --only main \
      --no-interaction \
      --no-root \
    && rm -rf /root/.cache/pypoetry

CMD gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 bot_service.app:app
