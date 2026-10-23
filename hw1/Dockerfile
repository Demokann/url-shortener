# Pinned base image, never latest
FROM python:3.14.6-slim-bookworm

# No .pyc files, and print logs immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies first, so this layer is cached when only code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Non-root user, and a folder for the database
RUN useradd --create-home --uid 10001 appuser \
    && mkdir /data && chown appuser:appuser /data

# Copy app code last, since it changes most often
COPY --chown=appuser:appuser . .

USER appuser

# Settings come from environment variables
ENV PORT=8000 \
    BASE_URL=http://localhost:8000 \
    DB_PATH=/data/urls.db

EXPOSE 8000
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT}"]