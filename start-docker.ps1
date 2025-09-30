#!/usr/bin/env powershell
# Wotnot Docker Startup Script

Write-Host "🐳 Starting Wotnot with Docker" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if Docker is running
try {
    docker version | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (!(Test-Path "backend/.env")) {
    Write-Host "⚠️  Backend .env file not found. Creating from example..." -ForegroundColor Yellow
    Copy-Item "backend/.env.example" "backend/.env"
    Write-Host "📝 Please edit backend/.env with your actual values before continuing." -ForegroundColor Yellow
    Read-Host "Press Enter when ready to continue"
}

# Check if frontend .env exists
if (!(Test-Path "frontend/app/.env")) {
    Write-Host "⚠️  Frontend .env file not found. Creating from example..." -ForegroundColor Yellow
    Copy-Item "frontend/app/.env.example" "frontend/app/.env"
}

# Ask for deployment type
Write-Host "\nSelect deployment mode:" -ForegroundColor Cyan
Write-Host "1. 🚀 Production (optimized builds)"
Write-Host "2. 🛠️  Development (with hot reload)"
Write-Host "3. 🧹 Clean up and rebuild"
Write-Host "4. 📊 View logs"
Write-Host "5. 🛑 Stop services"

$choice = Read-Host "\nEnter your choice (1-5)"

switch ($choice) {
    1 {
        Write-Host "\n🚀 Starting in production mode..." -ForegroundColor Green
        docker-compose down
        docker-compose up -d --build
        Write-Host "\n✅ Services started!" -ForegroundColor Green
        Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
        Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    }
    2 {
        Write-Host "\n🛠️  Starting in development mode..." -ForegroundColor Yellow
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
        docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
        Write-Host "\n✅ Development services started!" -ForegroundColor Green
        Write-Host "📱 Frontend: http://localhost:8080" -ForegroundColor Cyan
        Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor Cyan
    }
    3 {
        Write-Host "\n🧹 Cleaning up..." -ForegroundColor Yellow
        docker-compose down -v
        docker system prune -f
        docker-compose up -d --build --force-recreate
        Write-Host "\n✅ Clean rebuild completed!" -ForegroundColor Green
    }
    4 {
        Write-Host "\n📊 Viewing logs..." -ForegroundColor Cyan
        docker-compose logs -f
    }
    5 {
        Write-Host "\n🛑 Stopping services..." -ForegroundColor Red
        docker-compose down
        Write-Host "✅ All services stopped." -ForegroundColor Green
    }
    default {
        Write-Host "\n❌ Invalid choice. Exiting." -ForegroundColor Red
        exit 1
    }
}

if ($choice -eq 1 -or $choice -eq 2) {
    Write-Host "\n🔍 Service Status:" -ForegroundColor Cyan
    docker-compose ps
    Write-Host "\n💡 Tips:" -ForegroundColor Yellow
    Write-Host "   - View logs: docker-compose logs -f [service_name]"
    Write-Host "   - Stop services: docker-compose down"
    Write-Host "   - Restart: docker-compose restart [service_name]"
}