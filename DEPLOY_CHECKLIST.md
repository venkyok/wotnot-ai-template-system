# 🚀 Wotnot Deployment Checklist

## Pre-Deployment Setup

### 1. 🔑 Get Required Keys
- [ ] **OpenAI API Key** - Get from [OpenAI Dashboard](https://platform.openai.com/api-keys)
- [ ] **Database URL** - Will be provided by Railway automatically
- [ ] **JWT Secret** - Generate a random 32+ character string

### 2. 📱 Account Setup
- [ ] **GitHub Account** - Repository is ready ✅
- [ ] **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
- [ ] **Railway Account** - Sign up at [railway.app](https://railway.app)

## Deployment Steps

### Phase 1: Backend Deployment (Railway)

1. **Deploy to Railway**
   - [ ] Go to [railway.app](https://railway.app)
   - [ ] Click "New Project" → "Deploy from GitHub repo"
   - [ ] Select `wotnot-ai-template-system` repository
   - [ ] Set **Root Directory**: `backend`
   - [ ] Railway will auto-detect Python and deploy

2. **Add Environment Variables**
   - [ ] In Railway dashboard, go to Variables tab
   - [ ] Add: `OPENAI_API_KEY=sk-your-key-here`
   - [ ] Add: `JWT_SECRET_KEY=your-32-char-secret`
   - [ ] Add: `CORS_ORIGINS=https://your-app.vercel.app`
   - [ ] Railway auto-provides `DATABASE_URL`

3. **Test Backend**
   - [ ] Visit: `https://your-backend.up.railway.app/docs`
   - [ ] Should see FastAPI documentation

### Phase 2: Frontend Deployment (Vercel)

1. **Deploy to Vercel**
   - [ ] Go to [vercel.com](https://vercel.com)
   - [ ] Click "New Project" → Import Git Repository
   - [ ] Select `wotnot-ai-template-system`
   - [ ] Set **Root Directory**: `frontend/app`
   - [ ] Set **Build Command**: `npm run build`
   - [ ] Set **Output Directory**: `dist`

2. **Add Environment Variables**
   - [ ] In Vercel dashboard, go to Settings → Environment Variables
   - [ ] Add: `VUE_APP_API_URL=https://your-backend.up.railway.app`
   - [ ] Redeploy to apply changes

3. **Test Frontend**
   - [ ] Visit your Vercel app URL
   - [ ] Test login/signup functionality
   - [ ] Test AI template generation

## Post-Deployment

### 1. 🔒 Security Updates
- [ ] Update CORS_ORIGINS with actual frontend URL
- [ ] Set strong JWT_SECRET_KEY in production
- [ ] Enable HTTPS enforcement

### 2. 🎯 Domain Setup (Optional)
- [ ] Add custom domain in Vercel
- [ ] Update CORS_ORIGINS with new domain

### 3. 📊 Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Monitor API usage costs
- [ ] Set up database backups

## 🎉 Success Criteria

- [ ] ✅ Backend API accessible and docs loading
- [ ] ✅ Frontend loading and connecting to backend
- [ ] ✅ User registration/login working
- [ ] ✅ AI template generation functional
- [ ] ✅ WhatsApp template preview displaying

## 📞 Support

**Estimated Total Time**: 15-30 minutes
**Monthly Cost**: ~$5-10 (Railway) + $0 (Vercel free tier)

**Stuck?** Check:
1. Environment variables are set correctly
2. API keys are valid and have credits
3. CORS origins include your frontend URL
4. Database connection is working

---

**🚀 Ready to deploy?** Start with Railway backend, then Vercel frontend!