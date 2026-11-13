FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /bin/uv

WORKDIR /app

RUN adduser --system appuser

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY README.md LICENSE ./
COPY src ./src
RUN uv sync --locked --no-dev

RUN chown -R appuser /app

USER appuser

ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["fortune-cookie"]
CMD ["--help"]
