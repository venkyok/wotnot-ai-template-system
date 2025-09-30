#!/bin/bash
# Shell script to build Docker containers correctly

echo "🐳 Building Docker containers with correct context..."

# Stop any running containers
echo "Stopping existing containers..."
docker-compose down

# Build backend with correct context
echo "Building backend..."
docker build -t wotnot-backend ./backend

# Build frontend with correct context  
echo "Building frontend..."
docker build -t wotnot-frontend ./frontend/app

# Run with docker-compose
echo "Starting services..."
docker-compose up --build

echo "✅ Docker containers built and started successfully!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"