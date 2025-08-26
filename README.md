# 🚀 InvestCore AI

**Intelligent Investment Analysis & Portfolio Management Powered by AI**

InvestCore AI is a sophisticated financial analysis platform that combines natural language processing with real-time market data to provide comprehensive investment insights, portfolio analysis, and market assessments.

## ✨ Features

### 🤖 **AI-Powered Analysis**
- **Natural Language Queries** - Ask investment questions in plain English
- **Intelligent Command Execution** - Automatically identifies and runs relevant financial analysis commands
- **Context-Aware Responses** - Maintains conversation context for multi-step analysis

### 📊 **Comprehensive Financial Data**
- **Real-time Asset Information** - Current prices, market metrics, and performance data
- **Financial Statements** - Balance sheets, income statements, cash flow analysis
- **Earnings Data** - Quarterly and annual earnings reports with analysis
- **Macroeconomic Indicators** - Economic trends and market conditions

### 🎯 **Advanced Portfolio Tools**
- **Asset Screening** - Filter stocks based on custom criteria
- **Sector Analysis** - Industry-specific performance insights
- **Market Assessment** - Overall market conditions and sentiment
- **Portfolio Optimization** - Data-driven investment recommendations

### 🌐 **Web Integration**
- **RESTful API** - Full-featured API for app integration
- **Web Dashboard** - Interactive chatbot interface for testing
- **Streaming Responses** - Real-time data delivery via NDJSON

## 🏗️ Architecture

```
InvestCore/
├── 🧠 brain.py              # Core AI logic and command orchestration
├── 🌐 api_server.py         # Flask API server with all endpoints
├── 🎮 command_engine.py    # Command execution and management
├── 🔍 command_checker.py   # Command validation and parsing
├── 📱 test_dashboard.py    # Web-based chatbot interface
├── 📦 commands/            # Individual command modules
│   ├── asset_assess.py     # Asset performance analysis
│   ├── create_portfolio.py # Portfolio creation tools
│   ├── get_asset_info.py  # Real-time asset data
│   ├── get_earnings.py    # Earnings analysis
│   ├── get_financials.py  # Financial statement data
│   ├── get_macros.py      # Macroeconomic indicators
│   ├── market_assess.py   # Market condition analysis
│   ├── screen_assets.py   # Asset screening tools
│   ├── sector_assess.py   # Sector performance analysis
│   └── search_web.py      # Web search for financial news
├── 🧠 memory/              # AI memory and state management
├── 🛠️ utils/               # Utility functions and helpers
└── 📋 requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- RapidAPI account (for market data)
- OpenAI API key (for AI responses)

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/investcore.git
cd investcore
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Set Up Environment Variables**
Create a `.env` file in the root directory:
```env
RAPIDAPI_KEY=your_rapidapi_key_here
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your-secret-key-here
```

### **4. Start the API Server**
```bash
python api_server.py
```

The API will be available at `http://localhost:5000`

### **5. Test the Dashboard**
In another terminal:
```bash
python test_dashboard.py
```

Access the chatbot interface at `http://localhost:5001`

## 🌐 API Endpoints

### **Core Endpoints**
- `GET /` - API information and available endpoints
- `GET /api/health` - Health check and system status
- `POST /api/chat` - Main chat endpoint for AI interactions

### **Data Endpoints**
- `GET /api/asset/<symbol>` - Asset information and metrics
- `GET /api/financials/<symbol>` - Financial statement data
- `GET /api/earnings/<symbol>` - Earnings reports and analysis
- `GET /api/macros` - Macroeconomic indicators

### **Analysis Endpoints**
- `POST /api/screen` - Asset screening and filtering
- `POST /api/market/assess` - Market condition analysis
- `POST /api/sector/assess` - Sector performance analysis
- `POST /api/asset/assess` - Individual asset assessment

### **Advanced Endpoints**
- `POST /api/chat/stream` - Streaming chat responses (NDJSON)
- `POST /api/search/web` - Web search for financial information

## 💬 Usage Examples

### **Basic Asset Analysis**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "message": "Analyze AAPL stock for me"
  }'
```

### **Portfolio Screening**
```bash
curl -X POST http://localhost:5000/api/screen \
  -H "Content-Type: application/json" \
  -d '{
    "filters": ["market_cap > 1000000000", "pe_ratio < 20"],
    "description": "Large-cap value stocks"
  }'
```

### **Market Assessment**
```bash
curl -X POST http://localhost:5000/api/market/assess \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 🚀 Railway Deployment

### **1. Set Environment Variables in Railway**
- `RAPIDAPI_KEY` - Your RapidAPI key
- `OPENAI_API_KEY` - Your OpenAI API key
- `SECRET_KEY` - Flask secret key
- `PORT` - Railway sets this automatically

### **2. Deploy**
```bash
railway up
```

### **3. Monitor Health**
The health check endpoint `/api/health` will verify all dependencies are working.

## 🔧 Configuration

### **Environment Variables**
| Variable | Description | Required |
|----------|-------------|----------|
| `RAPIDAPI_KEY` | RapidAPI key for market data | Yes |
| `OPENAI_API_KEY` | OpenAI API key for AI responses | Yes |
| `SECRET_KEY` | Flask secret key for security | Yes |
| `PORT` | Server port (set by Railway) | No |
| `HOST` | Server host (default: 0.0.0.0) | No |

### **Railway Configuration**
```json
{
  "startCommand": "python api_server.py",
  "healthcheckPath": "/api/health",
  "healthcheckTimeout": 300,
  "restartPolicyType": "ON_FAILURE"
}
```

## 🧪 Testing

### **Local Testing**
```bash
# Test API endpoints
python -m pytest

# Test dashboard
python test_dashboard.py

# Test individual commands
python -c "from commands.get_asset_info import run; print(run({'symbol': 'AAPL'}))"
```

### **API Testing**
```bash
# Health check
curl http://localhost:5000/api/health

# Root endpoint
curl http://localhost:5000/

# Chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "Hello"}'
```

## 🏗️ Development

### **Adding New Commands**
1. Create a new file in `commands/` directory
2. Implement a `run(params)` function
3. Add command metadata and validation
4. Update command registry in `command_engine.py`

### **Extending the API**
1. Add new routes in `api_server.py`
2. Implement proper error handling
3. Add input validation
4. Update documentation

### **AI Model Customization**
- Modify prompts in `prompt.py`
- Adjust AI parameters in `llm_model.py`
- Customize command selection logic in `brain.py`

## 📊 Performance

### **Response Times**
- **Simple queries**: < 2 seconds
- **Data analysis**: 3-5 seconds
- **Complex portfolio analysis**: 5-10 seconds

### **Scalability**
- **Concurrent users**: 100+ simultaneous connections
- **API rate limits**: Respects external API limits
- **Memory usage**: Optimized for Railway's container limits

## 🔒 Security

### **API Security**
- CORS enabled for web integration
- Input validation on all endpoints
- Rate limiting (configurable)
- Secure environment variable handling

### **Data Privacy**
- No user data stored permanently
- API keys encrypted in environment
- Secure communication protocols

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Development Guidelines**
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure all tests pass

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT models and API
- **RapidAPI** for financial data services
- **Flask** for the web framework
- **Community contributors** for feedback and improvements

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/investcore/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/investcore/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/investcore/wiki)

---

**Built with ❤️ for the investment community**

*InvestCore AI - Making investment analysis accessible to everyone*
