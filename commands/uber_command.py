import json
from datetime import datetime, timezone
from llm_model import call_gpt
from memory.long_term_db import get_user_facts
from memory.short_term_cache import get_recent_conversation, get_current_market_data, get_current_cache
from memory.knowledge_memory import get_vector_matches
from prompt import get_plugin_system_prompt

def get_required_fields():
    return {
        "question": {"prompt": "What complex question are you synthesizing data for?"}
    }

def get_comprehensive_context(user_id=None, question=""):
    """Gather comprehensive context like brain.py does"""
    # Get all the same context as brain.py
    recent_chat = get_recent_conversation(user_id) if user_id else "No recent conversation"
    user_facts = get_user_facts(user_id) if user_id else "No user data available"
    vector_recall = get_vector_matches(question) if question else "No relevant knowledge"
    market_data = get_current_market_data(user_id) if user_id else {}
    
    return {
        "recent_chat": recent_chat,
        "user_facts": user_facts,
        "vector_recall": vector_recall,
        "market_data": market_data
    }

def get_collected_data_from_cache(user_id):
    """Automatically collect all data from the command stack cache"""
    if not user_id:
        return "No command stack data available"
    
    # Get data from current command stack execution results
    current_cache = get_current_cache(user_id)
    execution_results = current_cache.get("execution_results", [])
    
    if not execution_results:
        return "No command stack data available"
    
    # Collect all results from required commands (previous commands in the stack)
    collected_data = []
    for result in execution_results:
        if result.get("is_required", False):  # Only get required commands (previous commands)
            collected_data.append({
                "command": result["command"],
                "result": result["result"]
            })
    
    if not collected_data:
        return "No data collected from previous commands in the stack"
    
    # Format the collected data nicely
    formatted_data = []
    for item in collected_data:
        formatted_data.append(f"=== {item['command'].upper()} ===\n{item['result']}\n")
    
    return "\n".join(formatted_data)

def synthesize_comprehensive_answer(question, collected_data, context):
    """Synthesize collected data into a comprehensive answer using brain.py context"""
    plugin_system_prompt = get_plugin_system_prompt()
    system_prompt = f"{plugin_system_prompt}\n\nYou are Portfolio AI's master synthesis specialist. Your role is to combine data from multiple sources to provide comprehensive, actionable insights on complex financial questions."
    
    # Get current timestamp
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    user_prompt = f"""
You are Portfolio AI! A financial/investing assistant and advisor whose ultimate goal is to provide the most exceptional, revolutionary, empowering, personalized and insightful experience.

ORIGINAL QUESTION: {question}

[User Facts & Profile]
{context['user_facts']}

[Current Market Data]
{context['market_data'] if context['market_data'] else "No current market data available"}

[Relevant Knowledge]
{context['vector_recall']}

[Conversation So Far]
{context['recent_chat']}

[COLLECTED DATA FROM COMMAND STACK]
{collected_data}

Based on this comprehensive context and the collected data, provide a comprehensive analysis that:

1. **DIRECT ANSWER**: Directly address the original question with clear, actionable insights tailored to the user's profile and situation

2. **DATA SYNTHESIS**: Weave together insights from all data sources to tell a coherent story that connects to the user's goals and preferences

3. **PERSONALIZED RECOMMENDATIONS**: Provide specific, actionable recommendations that align with:
   - The user's risk tolerance and investment style
   - Their current portfolio and goals
   - Current market conditions and trends

4. **STRATEGIC INSIGHTS**: Explain what this means for:
   - Different asset classes and sectors relevant to the user
   - Portfolio positioning opportunities
   - Risk management considerations
   - Time horizons for these effects

5. **PROACTIVE GUIDANCE**: Suggest:
   - Next steps the user should consider
   - Related questions they might want to explore
   - Opportunities to optimize their current situation

Be specific, data-driven, and actionable. Use the synthesized data to provide insights that go beyond what any single data source could provide. Think like a portfolio manager making real investment decisions for this specific user.

Format your response with clear sections and bullet points for easy reading. Be conversational and engaging while maintaining your authoritative expertise.
"""
    
    return call_gpt(system_prompt, user_prompt)

def run(args: dict):
    """Main uber command function - the synthesis engine"""
    question = args["question"]
    user_id = args.get("user_id")
    
    # Get current timestamp for logging
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Automatically collect data from command stack cache
    collected_data = get_collected_data_from_cache(user_id)
    
    # Gather comprehensive context like brain.py does
    context = get_comprehensive_context(user_id, question)
    
    # Synthesize comprehensive answer
    comprehensive_answer = synthesize_comprehensive_answer(
        question, 
        collected_data,
        context
    )
    
    return comprehensive_answer