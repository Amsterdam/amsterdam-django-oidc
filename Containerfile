ARG PYTHON_VERSION
FROM ghcr.io/astral-sh/uv:0.9-python${PYTHON_VERSION:-3.10}-trixie-slim

RUN set -eux; \
    apt-get update -yqq; \
    apt-get install -y \
      spatialite-bin \
      libsqlite3-mod-spatialite \
      gdal-bin; \
    apt-get clean

WORKDIR /app

ADD . /app

RUN uv sync --locked
