#!/bin/bash
# Render.com build script - ultra minimal to avoid Rust compilation
cd backend
pip install --upgrade pip
pip install -r requirements-ultra-minimal.txt