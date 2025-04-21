#!/bin/bash

# Wait for Postgres to be ready (docker-compose might be fast, Postgres is not)
echo "⏳ Waiting for Postgres to be ready..."
sleep 10

# Run Alembic migrations
echo "📦 Running Alembic migrations..."
alembic upgrade head

# Start the FastAPI app
echo "🚀 Starting the FastAPI server..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
