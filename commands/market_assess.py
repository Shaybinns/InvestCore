import requests
import os
import json
from datetime import datetime, timezone
from llm_model import call_gpt
from prompt import get_plugin_system_prompt
from memory.short_term_cache import get_current_market_data
from command_engine import run_command

def get_required_fields():
    return {}  # No required fields - runs automatically

# Data collection functions moved to get_market_data.py

def analyze_market_sentiment(market_data):
    """Analyze market sentiment using GPT"""
    plugin_system_prompt = get_plugin_system_prompt()
    system_prompt = f"{plugin_system_prompt}\n\nYou are a market sentiment analyst within Portfolio AI. Your role is to analyze market conditions and provide strategic investment insights."
    
    # Get current datetime for context
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    current_date = current_time.strftime("%Y-%m-%d")
    
    user_prompt = f"""
Analyze the current market conditions as of {current_time_str} (today is {current_date}) based on the following market data:

{market_data}

Provide a concise 5-7 sentence analysis covering:
1. What's driving market sentiment right now (as of {current_time_str})
2. How investors are reacting (risk-on vs risk-off) based on today's data
3. Any arbitrage opportunities or misalignments visible in current prices
4. What this suggests about near-term market direction
5. Key risks or opportunities to watch for the rest of today and tomorrow

Be strategic and actionable. Focus on the most important insights from today's data. But read between the lines and try and decipher what's really going on.
"""

    return call_gpt(system_prompt, user_prompt)

def run(args: dict):
    """Main market assessment function"""
    user_id = args.get("user_id")
    
    # Get current datetime for logging
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    current_date = current_time.strftime("%Y-%m-%d")
    
    # Step 1: Check if we have market data from today
    market_data = get_current_market_data(user_id) if user_id else {}
    
    # Step 2: If no market data from today, collect it
    if not market_data or market_data.get("date") != current_date:
        # Run get_market_data to collect fresh data
        market_data = run_command("get_market_data", {"user_id": user_id})
    
    # Step 3: Analyze and synthesize using the complete market_data object
    market_analysis = analyze_market_sentiment(market_data)
    
    # Add timestamp to the analysis
    timestamped_analysis = f"[Market Assessment as of {current_time_str}]\n\n{market_analysis}"
    
    return timestamped_analysis
