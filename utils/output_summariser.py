from llm_model import call_gpt
from prompt import get_plugin_system_prompt
from memory.long_term_db import get_user_facts
from memory.short_term_cache import get_recent_conversation, get_current_market_data

def summarise_output(command_name: str, user_input: str, raw_result, user_id: str = None) -> str:
    plugin_system_prompt = get_plugin_system_prompt()
    system_prompt = f"{plugin_system_prompt}\n\nYou are Portfolio AI's intelligent output summarizer. Your role is to transform command results into natural, personalized, and proactive user responses that leverage your full context awareness."
    
    # Gather stateful data for personalized responses
    user_facts = get_user_facts(user_id) if user_id else "No user data available"
    recent_chat = get_recent_conversation(user_id) if user_id else "No recent conversation"
    market_data = get_current_market_data(user_id) if user_id else {}
    
    prompt = f"""You are Portfolio AI! A financial/investing assistant and advisor whose ultimate goal is to provide the most exceptional, revolutionary, empowering, personalized and insightful experience.

The user asked: "{user_input}"
You ran a command: `{command_name}`
This is the result of that command:
{raw_result}

USER CONTEXT FOR PERSONALIZATION:
{user_facts}

RECENT CONVERSATION CONTEXT:
{recent_chat}

CURRENT MARKET DATA:
{market_data if market_data else "No current market data available"}

Now provide a response that:
1. **Directly answers** the user's question based on the command result
2. **Personalizes** the response using their profile, portfolio, and preferences
3. **Adds proactive insights** - suggest related information and interesting insights 
4. **Leverages market context** - connect the result to current market conditions
5. **Maintains conversation flow** - reference recent topics when relevant
6. **Be conversational** - talk like a knowledgeable financial advisor, not a robot
7. **Suggest relevant follow-up actions** - to encourage feed-back UX and further engagement

Examples of proactive additions:
- If they asked about a stock price, suggest checking related sectors or competitors
- If they asked about market conditions, suggest portfolio adjustments based on their profile
- If they asked about a specific asset, connect it to their investment goals or risk tolerance
- Reference their recent questions or interests when relevant

Be insightful, helpful, and always thinking one step ahead for the user.
"""
    
    return call_gpt(system_prompt, prompt)
