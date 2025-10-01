# 🔐 Railway Environment Variables Setup

## Required Environment Variables

Add these in Railway Dashboard → Variables tab:

### 1. OpenAI Configuration
```
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```
⚠️ **CRITICAL**: Replace with your actual OpenAI API key

### 2. JWT Security  
```
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production-minimum-32-characters
```
⚠️ **CRITICAL**: Use a strong, unique secret key (minimum 32 characters)

### 3. Database Configuration
```
DATABASE_URL=sqlite:///./wati.db
```
✅ This creates a SQLite database file in Railway

### 4. Authentication Settings
```
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30000
```

### 5. Optional: CORS Configuration
```
CORS_ORIGINS=https://your-frontend-url.vercel.app
```
(Add this later when you deploy frontend)

## 🚀 How to Add in Railway:

1. **Railway Dashboard** → Your Project
2. **Variables Tab** → **New Variable**
3. **Add each variable** one by one
4. **Deploy** → Railway will restart with new environment variables

## 🧪 Test After Adding Variables:

Visit: `https://your-railway-url.up.railway.app/docs`
- Should show FastAPI documentation
- All endpoints should be accessible
- AI template generation should work

## ⚠️ Security Notes:

- **Never commit API keys** to GitHub
- **Use strong SECRET_KEY** for production
- **Keep OPENAI_API_KEY private**

## 📋 Quick Copy-Paste Format:

```
Name: OPENAI_API_KEY
Value: sk-your-api-key

Name: SECRET_KEY  
Value: your-32-char-secret-key

Name: DATABASE_URL
Value: sqlite:///./wati.db

Name: ALGORITHM
Value: HS256

Name: ACCESS_TOKEN_EXPIRE_MINUTES
Value: 30000
```