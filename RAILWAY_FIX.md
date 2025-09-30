# 🚂 Railway Deployment Fix

## Issue: Nixpacks Build Failed
Railway was trying to build from the root directory, but your Python app is in the `backend` directory.

## ✅ Solution: Set Root Directory in Railway

### Step 1: Deploy to Railway
1. Go to https://railway.app
2. Connect GitHub and import your repository
3. **IMPORTANT**: In Railway dashboard → Settings → **Set Root Directory to: `backend`**

### Step 2: Environment Variables
Add these in Railway dashboard:
```
OPENAI_API_KEY=your-openai-key-here
SECRET_KEY=your-jwt-secret-key-min-32-chars
DATABASE_URL=sqlite:///./wati.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30000
```

### Step 3: Deploy
Railway will now:
- Build from the `backend` directory
- Find `requirements.txt` in the correct location
- Use `nixpacks.toml` for Python 3.9 setup
- Start with `uvicorn wati.main:app`

## 🎯 Alternative: Deploy Backend as Separate Service

If setting root directory doesn't work:
1. In Railway, create a new service
2. Connect to the same GitHub repository  
3. Set root directory to `backend`
4. Deploy

## 📁 File Structure Summary
```
wotnot/
├── backend/          ← Deploy this directory to Railway
│   ├── requirements.txt
│   ├── nixpacks.toml
│   ├── railway.json
│   └── wati/
└── frontend/app/     ← Deploy this to Vercel
```

## ✅ Your deployment should now work!

Railway will detect Python in the backend directory and build successfully.