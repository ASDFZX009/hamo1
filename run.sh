#!/usr/bin/env bash
# ── run.sh ─────────────────────────────────────────────────────────
# Quick launcher for the Hamo docker-compose stack
set -e

# 1. Make sure .env exists for backend
if [ ! -f backend/.env ]; then
  echo "[INFO] backend/.env not found – copying from .env.example"
  cp backend/.env.example backend/.env
  echo "[WARN] Please fill in SUPABASE_URL and SUPABASE_KEY in backend/.env before re-running."
  exit 1
fi

# 2. Build and start services
echo "[INFO] Building and starting containers..."
docker compose up --build -d

echo ""
echo "✅  Stack is running!"
echo "   Frontend  →  http://localhost"
echo "   Backend   →  http://localhost:5000"
echo ""
echo "To stop:  docker compose down"
echo "To logs:  docker compose logs -f"
