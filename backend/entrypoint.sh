#!/bin/sh
set -e

echo "[entrypoint] Running database migrations..."
python -m alembic upgrade head

echo "[entrypoint] Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
