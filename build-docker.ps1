# PowerShell script to build Docker containers correctly
Write-Host "🐳 Building Docker containers with correct context..."

# Stop any running containers
Write-Host "Stopping existing containers..."
docker-compose down

# Build backend with correct context
Write-Host "Building backend..."
docker build -t wotnot-backend ./backend

# Build frontend with correct context  
Write-Host "Building frontend..."
docker build -t wotnot-frontend ./frontend/app

# Run with docker-compose
Write-Host "Starting services..."
docker-compose up --build

Write-Host "✅ Docker containers built and started successfully!"
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:3000"
Write-Host "API Docs: http://localhost:8000/docs"