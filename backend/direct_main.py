"""
Direct entry point for Railway - bypasses potential module import issues
"""
from fastapi import FastAPI
import os

app = FastAPI(title="Wotnot Backend", version="1.0.0")

@app.get("/")
def read_root():
    return {
        "message": "Wotnot AI Template System API - Direct Entry Point", 
        "status": "running", 
        "docs": "/docs",
        "environment": "railway",
        "version": "1.0.1"
    }

@app.get("/health")
def health_check():
    from datetime import datetime
    return {
        "status": "healthy", 
        "service": "wotnot-backend", 
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv("RAILWAY_ENVIRONMENT_NAME", "railway")
    }

# CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Direct entry FastAPI app created successfully")