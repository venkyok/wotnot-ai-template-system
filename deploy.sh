#!/bin/bash

# Wotnot Deployment Script
# This script helps deploy your application to various cloud platforms

set -e  # Exit on any error

echo "🚀 Wotnot Deployment Helper"
echo "=========================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        print_error "Git is required but not installed"
        exit 1
    fi
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir &> /dev/null; then
        print_warning "Not in a git repository. Initializing..."
        git init
        git add .
        git commit -m "Initial commit"
    fi
    
    print_status "Prerequisites checked"
}

# Setup environment files
setup_environment() {
    print_info "Setting up environment files..."
    
    # Backend environment
    if [ ! -f "backend/.env" ]; then
        print_warning "Backend .env file not found. Creating from template..."
        cp backend/.env.example backend/.env
        print_warning "Please edit backend/.env with your actual values"
    fi
    
    # Frontend environment
    if [ ! -f "frontend/app/.env" ]; then
        print_warning "Frontend .env file not found. Creating from template..."
        cp frontend/app/.env.example frontend/app/.env
        print_warning "Please edit frontend/app/.env with your actual values"
    fi
    
    print_status "Environment files ready"
}

# Deploy to Vercel (Frontend)
deploy_vercel() {
    print_info "Deploying frontend to Vercel..."
    
    if ! command -v vercel &> /dev/null; then
        print_error "Vercel CLI not found. Install it with: npm i -g vercel"
        return 1
    fi
    
    cd frontend/app
    
    # Build the project
    print_info "Building frontend..."
    npm run build
    
    # Deploy to Vercel
    print_info "Deploying to Vercel..."
    vercel --prod
    
    cd ../..
    print_status "Frontend deployed to Vercel"
}

# Deploy to Railway (Backend)
deploy_railway() {
    print_info "Deploying backend to Railway..."
    
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI not found. Install it from: https://railway.app/cli"
        return 1
    fi
    
    # Login to Railway (if not already)
    railway login
    
    # Deploy
    railway up
    
    print_status "Backend deployed to Railway"
}

# Deploy with Docker
deploy_docker() {
    print_info "Building and deploying with Docker..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker not found. Please install Docker first"
        return 1
    fi
    
    # Build images
    print_info "Building Docker images..."
    docker-compose build
    
    # Start services
    print_info "Starting services..."
    docker-compose up -d
    
    print_status "Application deployed with Docker"
    print_info "Frontend: http://localhost:3000"
    print_info "Backend: http://localhost:8000"
}

# Deploy to Heroku
deploy_heroku() {
    print_info "Deploying to Heroku..."
    
    if ! command -v heroku &> /dev/null; then
        print_error "Heroku CLI not found. Install it from: https://devcenter.heroku.com/articles/heroku-cli"
        return 1
    fi
    
    # Login to Heroku
    heroku login
    
    # Create apps if they don't exist
    read -p "Enter your backend app name (or press enter to create new): " backend_app
    read -p "Enter your frontend app name (or press enter to create new): " frontend_app
    
    if [ -z "$backend_app" ]; then
        backend_app="wotnot-backend-$(date +%s)"
        heroku create $backend_app
    fi
    
    if [ -z "$frontend_app" ]; then
        frontend_app="wotnot-frontend-$(date +%s)"
        heroku create $frontend_app
    fi
    
    # Deploy backend
    print_info "Deploying backend..."
    git subtree push --prefix=backend heroku main || git subtree push --prefix=backend heroku master
    
    # Set environment variables (you'll need to do this manually or script it)
    print_warning "Don't forget to set environment variables on Heroku:"
    print_warning "heroku config:set OPENAI_API_KEY=your-key -a $backend_app"
    print_warning "heroku config:set DATABASE_URL=your-db-url -a $backend_app"
    
    print_status "Heroku deployment initiated"
}

# Main menu
show_menu() {
    echo ""
    echo "Choose deployment option:"
    echo "1) Quick Deploy (Vercel + Railway) - Recommended"
    echo "2) Docker (Local/VPS)"
    echo "3) Heroku"
    echo "4) Setup environment files only"
    echo "5) Exit"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    
    while true; do
        show_menu
        read -p "Enter your choice (1-5): " choice
        
        case $choice in
            1)
                setup_environment
                print_info "Starting quick deployment..."
                deploy_vercel
                deploy_railway
                print_status "Quick deployment completed!"
                break
                ;;
            2)
                setup_environment
                deploy_docker
                break
                ;;
            3)
                setup_environment
                deploy_heroku
                break
                ;;
            4)
                setup_environment
                print_status "Environment files set up. Please edit them with your actual values."
                break
                ;;
            5)
                print_info "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please choose 1-5."
                ;;
        esac
    done
    
    echo ""
    print_status "Deployment process completed!"
    echo ""
    print_info "Next steps:"
    echo "1. Set up your database (PostgreSQL recommended)"
    echo "2. Configure environment variables with real values"
    echo "3. Set up domain names (optional)"
    echo "4. Configure monitoring and backups"
    echo ""
    print_info "For detailed instructions, see DEPLOYMENT.md"
}

# Run main function
main "$@"