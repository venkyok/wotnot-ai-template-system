# 🚂 Railway Deployment Guide

## Quick Deploy to Railway (Recommended)

Since Docker is having context issues, Railway is your fastest deployment option:

### Step 1: Connect to Railway
1. Go to https://railway.app
2. Connect your GitHub account
3. Import your repository: `venkyok/wotnot-ai-template-system`

### Step 2: Set Environment Variables
In Railway dashboard, add these variables:
```
DATABASE_URL=sqlite:///./wati.db
SECRET_KEY=your-super-secret-jwt-key-here-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30000
OPENAI_API_KEY=your-openai-api-key-here
```

### Step 3: Deploy
Railway will automatically:
- Use the `railway.json` configuration I created
- Build with `nixpacks.toml` (Python 3.9)
- Use the minimal `requirements-railway.txt`
- Run with the `start.sh` script

### Step 4: Get Your Backend URL
After deployment, copy your Railway URL (e.g., `https://your-app.up.railway.app`)

### Step 5: Deploy Frontend to Vercel
1. Go to https://vercel.com
2. Import your GitHub repository
3. Set root directory to `frontend/app`
4. Add environment variable:
   ```
   VUE_APP_API_URL=https://your-railway-app.up.railway.app
   ```

## ✅ Your app will be live in minutes!

Backend: Railway (FastAPI + AI)
Frontend: Vercel (Vue.js)
Database: SQLite (included in Railway)