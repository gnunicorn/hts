# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Install packages needed to run your application (not build deps):
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
        libexpat1 \
        libjpeg62-turbo \
        libpcre3 \
        libpq5 \
        mime-support \
        postgresql-client \
        procps \
        zlib1g \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=hts.settings.production DJANGO_DEBUG=off

RUN mkdir /code
COPY ./requirements.txt /code/requirements.txt

RUN set -ex \
    && BUILD_DEPS=" \
        build-essential \
        git \
        libexpat1-dev \
        libjpeg62-turbo-dev \
        libpcre3-dev \
        libpq-dev \
        zlib1g-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install -U pip \
    && pip install --no-cache-dir -r /code/requirements.txt \
    && pip install gunicorn \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /code/
COPY .maintain/docker-entrypoint.sh /code/
COPY manage.py /code/
COPY hts /code/hts
# Set the working directory to /code/
WORKDIR /code/

RUN chown -R root /code
USER root

EXPOSE 8000

VOLUME ["/code/media/", "/code/static/"]

ENTRYPOINT ["/code/docker-entrypoint.sh"]

CMD start
