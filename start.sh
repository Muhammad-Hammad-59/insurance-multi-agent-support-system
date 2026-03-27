#!/bin/bash
set -e

echo "🚀 Starting Insurance Support AI..."
echo "================================="

echo "📂 SQLite path: ${SQLITE_PATH:-/app/data/insurance_support.db}"
echo "📂 ChromaDB path: ${CHROMA_PATH:-/app/chroma_db}"

mkdir -p $(dirname ${SQLITE_PATH:-/app/data/insurance_support.db})
mkdir -p ${CHROMA_PATH:-/app/chroma_db}

if [ ! -f "${SQLITE_PATH:-/app/data/insurance_support.db}" ]; then
    echo "📦 First run detected - Initializing database..."
    python scripts/setup_db.py
else
    echo "✅ Database already exists"
fi

echo "🌟 Starting backend server..."

exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}