# Wotnot Quick Deploy Script for Windows
# Run this in PowerShell as Administrator

Write-Host "🚀 Wotnot AI Template System - Quick Deploy" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Check if required tools are installed
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

# Check Git
if (Test-Command "git") {
    Write-Host "✅ Git is installed" -ForegroundColor Green
} else {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Check Node.js
if (Test-Command "node") {
    $nodeVersion = node --version
    Write-Host "✅ Node.js is installed: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js is not installed. Please install Node.js first." -ForegroundColor Red
    exit 1
}

# Check Python
if (Test-Command "python") {
    $pythonVersion = python --version
    Write-Host "✅ Python is installed: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python is not installed. Please install Python first." -ForegroundColor Red
    exit 1
}

Write-Host "
📋 Deployment Options:" -ForegroundColor Cyan
Write-Host "1. 🌐 Deploy to Cloud (Vercel + Railway) - Recommended"
Write-Host "2. 🐳 Deploy with Docker (Local/VPS)"
Write-Host "3. ⚙️ Setup environment files only"
Write-Host "4. 📚 Open deployment guide"
Write-Host "5. 🚪 Exit"

$choice = Read-Host "
Enter your choice (1-5)"

switch ($choice) {
    1 {
        Write-Host "
🌐 Cloud Deployment Selected" -ForegroundColor Green
        Write-Host "Please follow these steps:"
        Write-Host "1. 🔧 Backend: Deploy to Railway.app"
        Write-Host "   - Visit: https://railway.app"
        Write-Host "   - New Project → Deploy from GitHub"
        Write-Host "   - Root Directory: backend"
        Write-Host "   - Add environment variables from backend/.env.example"
        Write-Host "
2. 🎨 Frontend: Deploy to Vercel.com"
        Write-Host "   - Visit: https://vercel.com"
        Write-Host "   - Import Git Repository"
        Write-Host "   - Root Directory: frontend/app"
        Write-Host "   - Add VUE_APP_API_URL with your Railway URL"
        Write-Host "
📚 See DEPLOY_CHECKLIST.md for detailed steps"
    }
    2 {
        Write-Host "
🐳 Docker Deployment" -ForegroundColor Green
        if (Test-Command "docker") {
            Write-Host "Starting Docker deployment..."
            docker-compose --version
            Write-Host "Building and starting services..."
            docker-compose up -d --build
            Write-Host "✅ Services started!"
            Write-Host "Frontend: http://localhost:3000"
            Write-Host "Backend: http://localhost:8000"
        } else {
            Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
        }
    }
    3 {
        Write-Host "
⚙️ Setting up environment files..." -ForegroundColor Yellow
        if (!(Test-Path "backend/.env")) {
            Copy-Item "backend/.env.example" "backend/.env"
            Write-Host "✅ Created backend/.env"
        }
        if (!(Test-Path "frontend/app/.env")) {
            Copy-Item "frontend/app/.env.example" "frontend/app/.env"
            Write-Host "✅ Created frontend/app/.env"
        }
        Write-Host "📝 Please edit the .env files with your actual values"
        Write-Host "🔑 You'll need: OpenAI API key, Database URL, JWT secret"
    }
    4 {
        Write-Host "
📚 Opening deployment guide..." -ForegroundColor Cyan
        if (Test-Path "DEPLOY_CHECKLIST.md") {
            Start-Process "DEPLOY_CHECKLIST.md"
        }
        if (Test-Path "DEPLOYMENT.md") {
            Start-Process "DEPLOYMENT.md"
        }
    }
    5 {
        Write-Host "
👋 Goodbye!" -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host "❌ Invalid choice. Please run the script again." -ForegroundColor Red
    }
}

Write-Host "
🎉 Deployment helper completed!" -ForegroundColor Green
Write-Host "📚 For detailed instructions, see DEPLOY_CHECKLIST.md" -ForegroundColor Cyan