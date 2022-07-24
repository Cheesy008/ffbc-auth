FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="${PATH}:/root/.poetry/bin"
EXPOSE 4000/tcp
RUN mkdir /app
WORKDIR /app/
# Установка пакетов python и зависимостей необходимых для их сборки
RUN apk add --no-cache --virtual build-deps \
    curl `# для установки poetry` \
    make gcc g++ `# для сборки пакетов` \
    postgresql-dev `# для psycopg2` \
    libjpeg-turbo-dev zlib-dev libffi-dev cairo-dev libwebp-dev `# для pillow` \
    musl-dev python3-dev openssl-dev # для cryptography
# Зависимости необходимые для работы
RUN apk add --no-cache \
    git `# для установки зависимостей из git` \
    libpq `# для psycopg2` \
    libjpeg-turbo zlib libffi cairo libwebp `# для pillow` \
    libxml2 libxslt-dev \
    cargo\
    rust
RUN pip3 install --no-cache-dir cryptography
RUN pip3 install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction --no-ansi
RUN apk del --no-cache build-deps
COPY / /app/
