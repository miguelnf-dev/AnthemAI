# 1. Start with the official Python base image.
FROM python:3.11-slim

# 2. Use your clever multi-stage copy to get the uv binary.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

# 3. Set the working directory.
WORKDIR /app

# 4. Copy ONLY the dependency files first to enable Docker layer caching.
COPY pyproject.toml uv.lock ./

# 5. Install dependencies from the lock file.
RUN uv sync --locked --no-cache

# 6. Now copy the rest of your application code.
COPY agents.py crew.py app.py tasks.py .env ./
COPY tools ./tools

# 7. Expose the port that Streamlit will run on.
EXPOSE 8501

# 8. Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 9. Use 'uv run' to execute streamlit with the virtual environment
ENTRYPOINT ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]