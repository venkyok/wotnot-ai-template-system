#!/bin/bash
# Railway startup script - redirect to backend
cd backend
python -m uvicorn direct_main:app --host 0.0.0.0 --port $PORT