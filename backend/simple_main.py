"""
Super simple FastAPI app with no complex dependencies
"""
import os

# Use simple imports only
from fastapi import FastAPI

print("🚀 Starting super simple backend...")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Super Simple Backend Working", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/test")  
def test():
    return {"test": "working", "port": os.getenv("PORT", "8000")}

print("✅ Super simple app ready")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)