import requests
import os
from llm_model import call_gpt
import json
from datetime import datetime, timezone
from prompt import get_plugin_system_prompt
from memory.short_term_cache import get_current_market_data
from command_engine import run_command
from commands.get_user_info import run_command as get_user_info

def create_perplexity_search_query(user_request, user_info, market_data):
    """Create an optimized Perplexity search query using AI, incorporating user context and market data"""
    plugin_system_prompt = get_plugin_system_prompt()
    system_prompt = f"{plugin_system_prompt}\n\nYou are Portfolio AI's search query optimizer. Your role is to create highly targeted Perplexity search queries for asset screening."
    
    # Get current datetime for context
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    current_date = current_time.strftime("%Y-%m-%d")
    
    prompt = f"""You are an expert investment research assistant. Create a precise Perplexity search query to find the best investment opportunities based on the user's request, their investment profile, and current market conditions.

Current Date/Time: {current_time_str} (today is {current_date})

User's Request: "{user_request}"

User's Investment Profile:
{json.dumps(user_info, indent=2)}

Current Market Context:
{json.dumps(market_data, indent=2)}

Your task: Create a single, focused Perplexity search query that:
1. Directly addresses the user's investment request
2. Incorporates relevant aspects of their investment goals and risk profile
3. Considers current market conditions and opportunities
4. Searches for specific stocks, sectors, or asset types that would be most suitable

The query should be:
- Specific and actionable (include specific company names, sectors, or investment themes when relevant)
- Current (emphasize recent developments, earnings, or market conditions)
- Personalized (consider the user's investment style and objectives)
- Comprehensive (cover multiple angles of the investment opportunity)

Return ONLY the search query text, no explanations or additional text.

Example format: "Best technology stocks to buy December 2024 with strong earnings growth and low volatility for conservative investors"
"""
    
    result = call_gpt(system_prompt, prompt)
    return result.strip()

def search_assets_with_perplexity(search_query):
    """Search for assets using Perplexity API"""
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }

    # Get current datetime for context
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    current_date = current_time.strftime("%Y-%m-%d")

    prompt = f"""You are an expert financial analyst. The current date and time is {current_time_str} (today is {current_date}).

Find at least 10 investment assets based on the user's search request:

{search_query}

For each opportunity, evaluate using these criteria:
1. Does this asset satisfy what the user is asking for?
2. Will this asset perform well in the next 6-12 months based on current market conditions?
3. Does this asset align with the user's preferences and investment profile?
4. Does this asset have solid financials?

Please provide at least 10 specific investment recommendations with:
   - Company name and ticker symbol
   - Current stock price (as of {current_date})
   - Recent performance and key metrics
   - Brief investment thesis (why this is a good opportunity)
   - Key risks or considerations
   - How it meets the 4 evaluation criteria above

For each recommendation, include recent news or developments that support the investment case.

Focus on actionable, current opportunities with concrete reasoning. Provide diverse options across different sectors and market caps when relevant.

Format your response clearly with specific company names, ticker symbols, and current data.
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={
            "model": "perplexity/sonar-pro",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 3000
        }
    )

    if response.status_code != 200:
        raise Exception(f"Perplexity API Error: {response.status_code} — {response.text}")

    data = response.json()
    return data['choices'][0]['message']['content']

def organize_screening_results(perplexity_results, user_request):
    """Organize Perplexity results into structured screening results format"""
    plugin_system_prompt = get_plugin_system_prompt()
    system_prompt = f"{plugin_system_prompt}\n\nYou are Portfolio AI's result organizer. Your role is to structure and analyze search results into actionable investment insights."
    
    prompt = f"""Analyze and organize the following asset search results based on the user's original request: "{user_request}"

Search Results:
{perplexity_results}

The search found multiple investment opportunities. Please provide a structured analysis with:

1. **EXECUTIVE SUMMARY** - 2-3 sentence overview of the investment landscape and best opportunities found

2. **TOP TIER RECOMMENDATIONS** - List the 3-5 highest-quality investments that best meet all criteria:
   - Company name and ticker
   - Current price and recent performance
   - Key investment thesis
   - Risk level and considerations
   - How it scores on the 4 evaluation criteria
   - Does this asset align with Portfolio AI's investment criteria?

3. **SECONDARY OPTIONS** - List 2-3 additional solid opportunities that are worth considering:
   - Company name and ticker
   - Brief reasoning for inclusion
   - Any notable strengths or concerns

4. **MARKET INSIGHTS** - What these results reveal about current market conditions and investment themes

5. **PORTFOLIO CONSIDERATIONS** - How these opportunities could work together in a diversified portfolio and fit into the user's current portfolio if applicable

6. **NEXT STEPS** - Specific actions the user should consider (research priorities, buy/sell recommendations, etc.)

7. **ALTERNATIVE APPROACHES** - If the search didn't yield ideal results, suggest other screening criteria or investment themes to explore

Focus on actionable insights and provide clear reasoning for why certain assets are prioritized over others.
"""
    
    analysis = call_gpt(system_prompt, prompt)
    
    # Format the final result
    screening_results = f"ASSET SCREENING RESULTS\n{'='*50}\n\n{analysis}"
    
    return screening_results

def get_required_fields():
    return {
        "filters": {
            "prompt": "What kind of stocks or investments are you looking for? (e.g., tech stocks with strong growth, dividend-paying utilities, AI companies)"
        }
    }

def run(args: dict):
    """Main asset screening function using Perplexity search"""
    user_query = args["filters"]
    user_id = args.get("user_id")
    
    # Get current datetime for logging
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    current_date = current_time.strftime("%Y-%m-%d")
    
    try:
        # Step 1: Get or collect market data (similar to market_assess)
        if user_id:
            market_data = get_current_market_data(user_id)
            # If no market data from today, collect it
            if not market_data or market_data.get("date") != current_date:
                market_data = run_command("get_market_data", {"user_id": user_id})
        else:
            # For users without ID, collect fresh market data
            market_data = run_command("get_market_data", {"user_id": None})
        
        # Step 2: Get user information
        user_info = get_user_info({"user_id": user_id}) if user_id else {}
        
        # Step 3: Create optimized Perplexity search query
        search_query = create_perplexity_search_query(user_query, user_info, market_data)
        
        # Step 4: Search for assets using Perplexity
        perplexity_results = search_assets_with_perplexity(search_query)
        
        # Step 5: Organize results into screening format
        screening_results = organize_screening_results(perplexity_results, user_query)
        
        # Add timestamp to the results
        timestamped_results = f"[Asset Screening as of {current_time_str}]\n\n{screening_results}"
        
        return timestamped_results
        
    except Exception as e:
        error_message = f"Error during asset screening: {str(e)}"
        return f"[Asset Screening as of {current_time_str}]\n\n{error_message}"
