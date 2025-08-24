# 🚀 Simple InvestCore API - App Integration

Just the essential endpoints for your app, no extra complexity.

## 📱 Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/chat` | POST | AI chat interface |
| `/api/asset/{symbol}` | GET | Get asset information |
| `/api/screen` | POST | Screen assets with filters |
| `/api/market/assess` | POST | Assess market conditions |
| `/api/sector/assess` | POST | Assess sector performance |
| `/api/asset/assess` | POST | Assess asset performance |
| `/api/financials/{symbol}` | GET | Get financial data |
| `/api/earnings/{symbol}` | GET | Get earnings data |
| `/api/macros` | GET | Get macroeconomic data |
| `/api/search/web` | POST | Search web for financial info |

## ⚡ Quick Setup

### 1. Install Dependencies
```bash
pip install -r simple_requirements.txt
```

### 2. Set Environment Variables
```bash
# Create .env file with:
RAPIDAPI_KEY=your_rapidapi_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Start Server
```bash
python api_server.py
```

Your API is now running at `http://localhost:5000`! 🎉

## 📱 App Integration Examples

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Chat with AI
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "What is the current price of AAPL?"}'
```

### Get Asset Info
```bash
curl http://localhost:5000/api/asset/AAPL
```

### Screen Assets
```bash
curl -X POST http://localhost:5000/api/screen \
  -H "Content-Type: application/json" \
  -d '{"description": "stocks over $50 with volume above 10k"}'
```

## 🚀 Deploy to Production

### Option 1: Simple Hosting (Railway, Render, etc.)
```bash
# Just upload these files:
# - api_server.py
# - simple_requirements.txt
# - .env (with your API keys)
# - commands/ folder
# - brain.py and other core files
```

### Option 2: VPS/Server
```bash
# Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip

# Upload files and run
pip install -r simple_requirements.txt
python3 api_server.py

# Or use systemd service for auto-restart
```

### Option 3: Docker (if you want)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY simple_requirements.txt .
RUN pip install -r simple_requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "api_server.py"]
```

## 🔑 What You Need

- **RapidAPI Key**: For Yahoo Finance data
- **OpenAI API Key**: For AI analysis
- **Python 3.8+**: On your server/hosting platform

That's it! Simple and focused for app integration. 🎯
