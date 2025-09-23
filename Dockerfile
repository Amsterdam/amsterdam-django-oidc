FROM python:3.10

WORKDIR /opt/amsterdam-django-oidc

RUN set -eux; \
    apt-get update -yqq; \
    apt-get install -y \
      spatialite-bin \
      libsqlite3-mod-spatialite \
      gdal-bin; \
    apt-get clean

# Install Poetry
RUN set eux; \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python; \
    cd /usr/local/bin; \
    ln -s /opt/poetry/bin/poetry; \
    poetry config virtualenvs.create false; \
    poetry self add poetry-plugin-sort

COPY ./pyproject.toml ./poetry.lock /opt/amsterdam-django-oidc/

RUN poetry install --no-root

COPY . /opt/amsterdam-django-oidc
ENV PYTHON_PATH=/opt/amsterdam-django-oidc
