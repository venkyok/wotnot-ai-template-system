"""
Ultra-minimal FastAPI app for Render deployment
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("🚀 Starting ultra-minimal Wotnot Backend...")

app = FastAPI(title="Wotnot Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Wotnot AI Template System API - Ultra Minimal", 
        "status": "running", 
        "docs": "/docs",
        "environment": "render"
    }

@app.get("/health")
def health_check():
    import datetime
    return {
        "status": "healthy", 
        "service": "wotnot-backend-minimal", 
        "timestamp": datetime.datetime.now().isoformat()
    }

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint working", "success": True}

print("✅ Ultra-minimal FastAPI app created successfully")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting uvicorn on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)