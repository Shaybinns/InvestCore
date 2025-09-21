import requests
import os
import json
from datetime import datetime, timezone
from llm_model import call_gpt
from memory.long_term_db import get_latest_result
from memory.short_term_cache import get_recent_conversation, get_current_market_data, get_current_cache
from command_engine import run_command
from prompt import get_plugin_system_prompt

def get_required_fields():
    return {
        "symbol": {"prompt": "Which asset (ticker) would you like to assess?"}
    }


def run(args: dict):
    symbol = args["symbol"]
    user_id = args.get("user_id")  # Fallback to default if not provided
    
    current_time = datetime.now(timezone.utc)
    current_date = current_time.strftime("%Y-%m-%d")
    
    # Get asset_info from current command stack execution results
    current_cache = get_current_cache(user_id)
    execution_results = current_cache.get("execution_results", [])
    
    # Find asset_info from the current stack execution
    asset_info = None
    for result in execution_results:
        if result["command"] == "get_asset_info" and result["is_required"]:
            asset_info = result["result"]
    
    # Fallback to long-term database if not found in current execution
    if not asset_info:
        asset_info = get_latest_result("get_asset_info", symbol)
        if not asset_info:
            asset_info = f"Asset info for {symbol} not available from previous commands. Please run get_asset_info first."
    
    # Get market data from database market_data field (like market_assess does)
    market_data = get_current_market_data(user_id) if user_id else {}
    
    # If no market data from today, collect it
    if not market_data or market_data.get("date") != current_date:
        # Run get_market_data to collect fresh data
        market_data = run_command("get_market_data", {"user_id": user_id})

    # Analyze the asset using GPT
    plugin_system_prompt = get_plugin_system_prompt()
    system_prompt = f"{plugin_system_prompt}\n\nYou are an asset assessment specialist within Portfolio AI. Your role is to evaluate assets and provide buy/sell/hold recommendations based on comprehensive analysis."
    
    prompt = f"""
You have the ananlytical skills of a world class investment analyst, you do not hesitate to let the user know what you think, you give financial suggests aren't afraid to give tell them when is a good time to buy or sell an asset.
You will now evaluate whether a specific asset is a good buy or sell based on the following information and relay your opnion to the user.
Based on the following data, provide a comprehensive assessment of {symbol}:

ASSET INFORMATION:
{asset_info}

MARKET CONDITIONS:
{market_data}

Please provide:
1. A clear buy/sell/hold recommendation with confidence level
2. Price targets or entry/exit points
3. Time horizon for your recommendation
4. Key factors supporting your recommendation, understanding the type of macroeconomic environment the market is in (e.g., risk-on/risk-off, inflationary, recessionary, etc).
5. Determine what kind of moves this asset would benefit from in such a climate.
6. Evaluate the asset's valuation, financial health, and growth potential.
7. Decide whether it's currently undervalued or overvalued.

Be specific, actionable, and data-driven in your analysis.
"""

    return call_gpt(system_prompt, prompt)
