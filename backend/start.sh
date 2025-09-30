#!/bin/bash
# Railway startup script for Wotnot backend

echo "Starting Wotnot AI Template System..."

# Set Python path
export PYTHONPATH=/app:$PYTHONPATH

# Start the FastAPI application
exec uvicorn wati.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1