#!/bin/bash
# scripts/run_dev.sh
# Starts both backend and frontend in development mode.

set -e

echo "🚀 Starting Insurance Support AI dev environment..."

# ── Backend ──────────────────────────────────────────
echo "▶  Starting FastAPI backend on http://localhost:8000"
uvicorn backend.main:app --reload --port 8000 &
BACKEND_PID=$!

# ── Frontend ─────────────────────────────────────────
echo "▶  Starting React frontend on http://localhost:5173"
cd frontend
npm run dev &
FRONTEND_PID=$!

# Cleanup on exit
trap "echo '🛑 Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

echo ""
echo "✅ Services running:"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo "   API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop."
wait
