#!/usr/bin/env python3
"""
Ultra-minimal FastAPI test - no database, no imports, just FastAPI
"""
from fastapi import FastAPI

app = FastAPI(title="Minimal Test")

@app.get("/")
def root():
    return {"status": "working", "message": "Ultra minimal FastAPI test"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# No database, no scheduler, no imports - just basic FastAPI