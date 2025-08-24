# 🚀 Railway Deployment Guide for InvestCore API

Deploy your InvestCore API to Railway in minutes!

## 📋 Prerequisites

- [Railway Account](https://railway.app/) (free tier available)
- [GitHub Account](https://github.com/) (to host your code)
- Your InvestCore project ready

## 🚀 Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure these files are in your project:
```
✅ api_server.py          # Main API server
✅ simple_requirements.txt # Dependencies
✅ railway.json           # Railway configuration
✅ .env                   # Your API keys (don't commit this!)
✅ commands/              # Command modules
✅ brain.py              # AI brain
✅ llm_model.py          # OpenAI integration
✅ All other core files
```

### 2. Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial InvestCore API commit"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/investcore-api.git
git push -u origin main
```

### 3. Deploy to Railway

1. **Go to [Railway.app](https://railway.app/)**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your InvestCore repository**
6. **Click "Deploy"**

### 4. Set Environment Variables

In Railway dashboard:
1. **Go to your project**
2. **Click "Variables" tab**
3. **Add these variables:**

```env
RAPIDAPI_KEY=your_rapidapi_key_here
OPENAI_API_KEY=your_openai_api_key_here
PORT=5000
HOST=0.0.0.0
```

### 5. Get Your API URL

1. **Click on your deployed service**
2. **Copy the generated URL** (e.g., `https://investcore-api-production.up.railway.app`)
3. **Your API endpoints are now at:**
   - `https://your-url.railway.app/api/health`
   - `https://your-url.railway.app/api/chat`
   - `https://your-url.railway.app/api/asset/AAPL`

## 🔄 Updating Your API

### Automatic Updates (Recommended)
- **Push to GitHub** → Railway automatically redeploys
- **No manual intervention needed**
- **Zero downtime deployments**

### Manual Updates
- **Go to Railway dashboard**
- **Click "Deploy"** to trigger rebuild

## 🧪 Test Your Deployed API

```bash
# Health check
curl https://your-url.railway.app/api/health

# Test chat
curl -X POST https://your-url.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "What is AAPL stock price?"}'
```

## 📱 Update Your App

Change your app's API base URL from:
```javascript
const API_BASE = 'http://localhost:5000';
```

To:
```javascript
const API_BASE = 'https://your-url.railway.app';
```

## 🎉 You're Live!

Your InvestCore API is now:
- ✅ **Publicly accessible** from anywhere
- ✅ **Auto-scaling** with Railway
- ✅ **Professional hosting** with SSL
- ✅ **Easy to update** with Git integration

## 🚨 Important Notes

- **Never commit your `.env` file** to GitHub
- **Railway automatically handles SSL certificates**
- **Free tier has usage limits** - check Railway pricing
- **Your API keys are secure** in Railway's environment variables

## 🆘 Troubleshooting

### Common Issues:
1. **Build fails**: Check `simple_requirements.txt` for typos
2. **API keys not working**: Verify environment variables in Railway
3. **Port issues**: Railway sets `PORT` automatically, don't override

### Get Help:
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Railway Docs: [docs.railway.app](https://docs.railway.app)

---

**Ready to deploy? Let's get your InvestCore API live! 🚀**
