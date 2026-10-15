FROM python:3.12-slim
WORKDIR /workspace
COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install --no-cache-dir ".[postgres]"
COPY sql/ ./sql/
COPY dashboard/ ./dashboard/
COPY docs/ ./docs/
COPY scripts/ ./scripts/
ENTRYPOINT ["python", "-m", "experimentiq.cli"]
