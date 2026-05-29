# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN addgroup --system app && useradd --system --gid app --create-home --home-dir /app app

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure ownership for non-root user
RUN chown -R app:app /app

USER app

EXPOSE 7331

CMD ["python", "scripts/run_mcp_server.py"] 