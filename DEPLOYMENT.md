# Wotnot Deployment Guide

## Quick Deployment Options

### Option 1: Vercel (Frontend) + Railway/Render (Backend)
**Recommended for beginners**

#### Frontend (Vercel):
1. Push code to GitHub
2. Connect Vercel to your GitHub repo
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Add environment variable: `VUE_APP_API_URL=https://your-backend-url.com`

#### Backend (Railway):
1. Connect Railway to your GitHub repo
2. Select the `backend` folder as root
3. Add environment variables (see .env.example)
4. Deploy automatically

### Option 2: Docker + DigitalOcean/AWS

#### Build and Deploy:
```bash
# Build images
docker-compose build

# Deploy to cloud
docker-compose up -d
```

### Option 3: Heroku

#### Backend:
```bash
# Install Heroku CLI
heroku create your-app-backend
heroku config:set OPENAI_API_KEY=your-key
heroku config:set DATABASE_URL=your-db-url
git subtree push --prefix=backend heroku main
```

#### Frontend:
```bash
heroku create your-app-frontend
heroku buildpacks:set heroku/nodejs
heroku config:set VUE_APP_API_URL=https://your-backend.herokuapp.com
git subtree push --prefix=frontend/app heroku main
```

## Environment Variables

### Backend Required:
- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT tokens

### Frontend Required:
- `VUE_APP_API_URL`: Backend API URL

## Database Setup

### PostgreSQL (Recommended):
```sql
CREATE DATABASE wotnot;
CREATE USER wotnot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE wotnot TO wotnot_user;
```

### Or use managed database:
- Railway PostgreSQL
- Heroku PostgreSQL
- AWS RDS
- DigitalOcean Managed Database

## Security Checklist

- [ ] Set strong JWT_SECRET_KEY
- [ ] Configure CORS_ORIGINS properly
- [ ] Use HTTPS in production
- [ ] Set up database backups
- [ ] Monitor API usage and costs
- [ ] Set up logging and monitoring

## Performance Optimization

### Frontend:
- Nginx gzip compression enabled
- Static asset caching
- CDN for images (optional)

### Backend:
- Database connection pooling
- Redis caching (optional)
- Rate limiting for AI endpoints

## Monitoring

- Set up health checks
- Monitor OpenAI API usage
- Database performance monitoring
- Error tracking (Sentry recommended)

## Support

For deployment issues, check:
1. Environment variables are set correctly
2. Database connection is working
3. API keys are valid
4. CORS settings allow your domain
