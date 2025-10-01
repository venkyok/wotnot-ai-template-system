"""
Direct entry point for Railway - bypasses potential module import issues
"""
import os
import sys
from fastapi import FastAPI

print("🚀 Starting Wotnot Backend...")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"PORT environment variable: {os.getenv('PORT', 'not set')}")

app = FastAPI(title="Wotnot Backend", version="1.0.1")

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

print("✅ Direct entry FastAPI app created successfully")
print("🌐 CORS middleware added")
print("📡 Ready to accept connections...")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting uvicorn on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)