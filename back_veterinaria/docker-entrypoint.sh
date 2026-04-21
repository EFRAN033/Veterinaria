#!/bin/sh
set -e
cd /app
echo "[docker] Aplicando migraciones Alembic..."
alembic upgrade head
echo "[docker] Usuarios demo por rol (seed_users)..."
python seed_users.py
echo "[docker] Iniciando API en 0.0.0.0:${PORT:-8000}"
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
