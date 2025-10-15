FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-cache
COPY agents.py crew.py app.py tasks.py .env ./
COPY tools ./tools
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]