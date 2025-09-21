import requests
import os
import json
from datetime import datetime, timezone
from memory.short_term_cache import update_market_data

def get_required_fields():
    return {}  # No required fields - runs automatically

def get_market_news():
    """Fetch current market headlines and breaking news using Perplexity"""
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }

    # Get current datetime for context
    current_time = datetime.now(timezone.utc)
    current_date = current_time.strftime("%Y-%m-%d")
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")

    prompt = f"""Find the top 5-7 most important market-moving headlines and breaking news as of {current_time_str} (today is {current_date}). Focus on:
- Major economic data releases from today
- Central bank announcements from today
- Geopolitical events affecting markets from today
- Corporate earnings or major company news from today
- Market sentiment indicators from today
- Any breaking news that happened in the last few hours

IMPORTANT: Only include news from today ({current_date}) or very recent breaking news. Ignore older news.

Return only the headlines and brief context, no analysis yet."""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={
            "model": "perplexity/sonar-pro",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
    )

    if response.status_code != 200:
        raise Exception(f"News API Error: {response.status_code} — {response.text}")

    data = response.json()
    return data['choices'][0]['message']['content']

def get_risk_proxy_data():
    """Fetch current prices for key risk proxy assets"""
    symbols = ["DX-Y.NYB", "^VIX", "^TNX", "^UST2YR", "GC=F", "^GSPC", "CL=F", "HG=F", "BTC-USD"]
    
    url = "https://yahoo-finance166.p.rapidapi.com/api/market/get-quote-v2"
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "yahoo-finance166.p.rapidapi.com"
    }

    all_data = {}
    for symbol in symbols:
        querystring = {"symbols": symbol, "fields": "quoteSummary"}
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            try:
                result = data['quoteResponse']['result'][0]
                all_data[symbol] = {
                    "price": result.get("regularMarketPrice"),
                    "change": result.get("regularMarketChangePercent"),
                    "volume": result.get("regularMarketVolume")
                }
            except (KeyError, IndexError):
                all_data[symbol] = {"error": "Data unavailable"}
        else:
            all_data[symbol] = {"error": f"API Error: {response.status_code}"}

    return all_data

def get_macro_data():
    """Fetch current macroeconomic data using Perplexity"""
    current_time = datetime.now().strftime("%A, %B %d, %Y at %H:%M %p")
    
    # Default macroeconomic indicators to always search for
    default_indicators = [
        "GDP growth rate",
        "Federal Reserve interest rates", 
        "Inflation rate (CPI)",
        "Unemployment rate",
        "Housing prices and trends",
        "Industrial production index",
        "Consumer confidence index"
    ]
    
    # Build the search query
    search_query = f"Latest US macroeconomic data and current values as of {current_time} for: {', '.join(default_indicators)}. Include most recent data, trends, and Federal Reserve updates."

    prompt = f"""You are a macroeconomic data research specialist. The current date and time is {current_time}.

Search the internet for the most recent, accurate macroeconomic data for the United States. Focus on:

{search_query}

Please provide:
1. Current values for each indicator
2. Recent trends and changes
3. Federal Reserve policy updates
4. Data sources and dates
5. Brief analysis of what the data suggests about the economy

Format your response clearly with the most important data points highlighted.
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={
            "model": "perplexity/sonar-pro",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1500
        }
    )

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} — {response.text}")

    data = response.json()
    return data['choices'][0]['message']['content']

def run(args: dict):
    """Main market data collection function"""
    user_id = args.get("user_id")
    
    # Get current datetime for logging
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Step 1: Get current market news
    market_news = get_market_news()
    
    # Step 2: Get risk proxy asset data
    risk_data = get_risk_proxy_data()
    
    # Step 3: Get macroeconomic data
    macro_data = get_macro_data()
    
    # Step 4: Combine all data into comprehensive market data
    market_data = {
        "timestamp": current_time_str,
        "date": current_time.strftime("%Y-%m-%d"),
        "market_news": market_news,
        "risk_proxy_data": risk_data,
        "macro_data": macro_data,
        "data_sources": ["perplexity_news", "yahoo_finance", "perplexity_macro"]
    }
    
    # Step 5: Save to short_term_memory
    if user_id:
        update_market_data(user_id, market_data)
    
    return market_data
