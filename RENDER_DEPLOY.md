# 🚀 Render Deployment (Alternative to Railway)

## Quick Deploy to Render.com

### Step 1: Connect to Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository

### Step 2: Configure Service
- **Name**: wotnot-backend
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m uvicorn direct_main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: `backend`

### Step 3: Environment Variables
Add these in Render dashboard:
```
OPENAI_API_KEY=your-openai-key
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./wati.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30000
```

### Step 4: Deploy
Render will build and deploy automatically.

## Why Render Might Work Better
- ✅ Simpler Python deployment
- ✅ Better error reporting
- ✅ More stable for FastAPI apps
- ✅ Free tier available

## Render vs Railway
Both are good, but Render sometimes handles Python apps better than Railway's Nixpacks.