import requests
import os
import json
from datetime import datetime, timezone
from llm_model import call_gpt
from memory.long_term_db import get_user_facts
from memory.short_term_cache import get_recent_conversation, get_current_market_data
from command_engine import run_command
from prompt import get_plugin_system_prompt

def get_required_fields():
    return {}  # No required fields - runs automatically

# Old functions removed - now using market_data system and user_facts

def run(args: dict):
    """Main market recommendation function"""
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
    
    # Step 3: Get user data and recent conversation
    user_facts = get_user_facts(user_id) if user_id else "No user data available"
    recent_chat = get_recent_conversation(user_id) if user_id else "No recent conversation"
    
    # Step 4: Analyze and provide recommendations using GPT
    plugin_system_prompt = get_plugin_system_prompt()
    system_prompt = f"{plugin_system_prompt}\n\nYou are Portfolio AI's market recommendation specialist. Your role is to provide strategic asset and trend recommendations based on market conditions and user profile."
    
    prompt = f"""
You are a world-class investment strategist with the analytical skills of a top-tier hedge fund manager. You combine macro analysis, sector rotation, and individual stock selection to provide actionable investment recommendations.

Based on the following data, provide comprehensive market recommendations:

CURRENT MARKET DATA:
{market_data}

USER PROFILE & FACTS:
{user_facts}

RECENT CONVERSATION CONTEXT:
{recent_chat}

Please provide:

1. **ASSET RECOMMENDATIONS (3-5 specific stocks/ETFs)**:
   - Include ticker symbols and company names
   - Explain why each asset is attractive in current market conditions
   - Provide entry price targets and time horizons
   - Assess risk/reward ratios

2. **TREND RECOMMENDATIONS**:
   - Which sectors/asset classes will see significant movements
   - Macro themes driving these trends
   - Timeframes for these movements
   - Risk factors to monitor

3. **STRATEGIC INSIGHTS**:
   - How current market conditions favor certain investment styles
   - Portfolio positioning recommendations
   - Risk management considerations
   - Opportunities for tactical allocation

4. **CONFIDENCE LEVELS**:
   - Rate your confidence in each recommendation (High/Medium/Low)
   - Explain what could change your view

Be specific, actionable, and data-driven. Consider the user's preferences, risk tolerance, and portfolio from their profile. Focus on opportunities that align with current market dynamics while managing risk appropriately.

Format your response clearly with sections for Asset Recommendations, Trend Recommendations, Strategic Insights, and Confidence Levels.
"""

    return call_gpt(system_prompt, prompt)
