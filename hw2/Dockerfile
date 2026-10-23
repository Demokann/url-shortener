# Pinned base image, never latest
FROM python:3.14.6-slim-bookworm

# No .pyc files, and print logs immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies first, so this layer is cached when only code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Non-root user (no local data folder anymore, the app is stateless)
RUN useradd --create-home --uid 10001 appuser

# Copy app code last, since it changes most often
COPY --chown=appuser:appuser . .

USER appuser

# Non-secret settings only. DB connection settings and the password come from Compose.
ENV PORT=8000 \
    BASE_URL=http://localhost:8000

EXPOSE 8000
CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT}"]