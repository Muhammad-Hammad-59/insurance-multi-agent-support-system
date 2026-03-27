# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY scripts/ ./scripts/

# Create startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Create data directories (will be overridden by volumes)
RUN mkdir -p /app/data /app/chroma_db

EXPOSE 8000

CMD ["/app/start.sh"]