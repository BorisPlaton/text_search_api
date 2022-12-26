FROM python:3.10.4 AS builder

WORKDIR /text_searcher
RUN python -m venv venv
ENV PATH="/text_searcher/venv/bin:${PATH}"

COPY . .
RUN pip install -r requirements.prod.txt

FROM python:3.10.4-slim AS final

WORKDIR /text_searcher
COPY --from=builder /text_searcher .
ENV PATH="/text_searcher/venv/bin:${PATH}"
RUN apt update && apt install -y libpq5

ENTRYPOINT ["sh", "./scripts/entrypoint.sh",]
