FROM public.ecr.aws/docker/library/python:3.11.11-slim

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    gcc g++ libxml2-dev libxslt-dev libssl-dev make curl supervisor nginx dos2unix libcurl4-openssl-dev \
    libpq-dev postgis\
    && rm -rf /var/lib/apt/lists/*
