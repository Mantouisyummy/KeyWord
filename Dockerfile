# 首先，使用 multi-stage build 來減少最終映像的大小
FROM python:3.11.5-slim as build

ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.2

RUN mkdir -p /keyword
WORKDIR /keyword

# 安裝 Poetry 並安裝依賴
COPY pyproject.toml poetry.lock ./
RUN pip install "poetry==$POETRY_VERSION" \
    && poetry install --no-root --no-ansi --no-interaction \
    && poetry export -f requirements.txt -o requirements.txt

# 最終階段
FROM python:3.11.5-slim as Final

WORKDIR /keyword

# 複製依賴並安裝
COPY --from=build /keyword/requirements.txt .
RUN set -ex \
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    && apt-get update \
    && apt-get install -y --no-install-recommends git \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm requirements.txt \
    && rm -rf /root/.cache/pip/*

# 複製程式碼並設置運行命令
COPY .env .env
COPY /guild /guild
COPY . .

CMD [ "python3", "main.py" ]