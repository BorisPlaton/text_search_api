FROM python:3.10.4 AS builder

WORKDIR /text_searcher
COPY poetry.lock pyproject.toml ./
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    python -m venv .venv && \
    export PATH="/text_searcher/.venv/bin:/root/.local/bin:${PATH}" && \
    poetry install --only main
COPY . .

FROM python:3.10.4-slim AS final

WORKDIR /text_searcher
COPY --from=builder /text_searcher .
ENV PATH="/text_searcher/.venv/bin:${PATH}"
RUN apt update && \
    apt install -y libpq5 && \
    rm poetry.lock pyproject.toml

ENTRYPOINT ["sh", "./scripts/entrypoint.sh"]
