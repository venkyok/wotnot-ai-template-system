# 🐳 Docker Build Fix Guide

## Problem
The Docker build fails because it can't find `requirements.txt` due to incorrect build context.

## Solution 1: Install Docker Desktop (If not installed)
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Install and restart your computer
3. Make sure Docker is running

## Solution 2: Run Docker with Correct Commands

### From PowerShell (in the wotnot root directory):

```powershell
# Build backend only
docker build -f backend/Dockerfile -t wotnot-backend ./backend

# Build with docker-compose (recommended)
docker-compose up --build
```

### From Command Prompt:
```cmd
cd C:\Users\vy916\Desktop\ppro\wotnot
docker-compose up --build
```

## Solution 3: Use the Build Scripts I Created

```powershell
# Make script executable and run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\build-docker.ps1
```

## Troubleshooting Docker Issues

### Issue: "docker: command not found"
- Install Docker Desktop
- Restart PowerShell/CMD after installation
- Make sure Docker Desktop is running

### Issue: "requirements.txt not found"
- Make sure you're in the wotnot root directory
- Use the correct build context: `./backend`
- The requirements.txt exists in `backend/requirements.txt`

### Issue: Build context problems
- Always run from the wotnot root directory
- Use `docker-compose up --build` instead of individual builds

## Quick Test
```powershell
# Test if Docker is installed
docker --version

# Test if build context is correct
dir backend\requirements.txt

# Build and run
docker-compose up --build
```

## 🎯 Recommended: Use Railway instead
Railway deployment is much easier and already configured with all the fixes!