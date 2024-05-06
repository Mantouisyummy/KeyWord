FROM python:3.11.5-slim as build

ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN mkdir -p /keyword
COPY . /keyword

WORKDIR /keyword

RUN set -ex \
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    && apt-get update \
    && apt-get install -y --no-install-recommends git \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache/pip/*

FROM gcr.io/distroless/python3

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY --from=build /keyword /keyword

ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

WORKDIR /keyword

CMD [ "main.py" ]
