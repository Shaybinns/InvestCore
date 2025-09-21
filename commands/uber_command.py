import json
from datetime import datetime, timezone
from llm_model import call_gpt
from memory.long_term_db import get_latest_result
from memory.short_term_cache import get_recent_conversation
from memory.knowledge_memory import get_vector_matches
from prompt import get_plugin_system_prompt

def get_required_fields():
    return {
        "question": {"prompt": "What complex question are you synthesizing data for?"},
        "collected_data": {"prompt": "What data has been collected from previous commands in the stack?"}
    }

def get_user_context(user_id=None):
    """Gather user context from various sources"""
    context_parts = []
    
    try:
        # Get recent conversation context
        recent_chat = get_recent_conversation(user_id)
        if recent_chat and len(recent_chat.strip()) > 50:
            context_parts.append(f"Recent conversation context: {recent_chat[:500]}...")
    except:
        pass
    
    try:
        # Get user knowledge from vector search
        user_knowledge = get_vector_matches("investment preferences portfolio holdings risk tolerance goals")
        if user_knowledge:
            context_parts.append(f"User knowledge base: {user_knowledge}")
    except:
        pass
    
    try:
        # Get latest portfolio data
        portfolio_data = get_latest_result("get_user_portfolio")
        if portfolio_data:
            context_parts.append(f"Portfolio holdings: {portfolio_data}")
    except:
        pass
    
    return "\n".join(context_parts) if context_parts else None

def synthesize_comprehensive_answer(question, collected_data, user_context=None):
    """Synthesize collected data into a comprehensive answer"""
    plugin_system_prompt = get_plugin_system_prompt()
    system_prompt = f"{plugin_system_prompt}\n\nYou are Portfolio AI's master synthesis specialist. Your role is to combine data from multiple sources to provide comprehensive, actionable insights on complex financial questions."
    
    # Get current timestamp
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Format user context if available
    user_context_text = ""
    if user_context:
        user_context_text = f"\n=== USER CONTEXT ===\n{user_context}\n"
    
    user_prompt = f"""
    You are a world-class financial analyst with the expertise of top-tier hedge fund managers, central bank economists, and market strategists. Your task is to synthesize comprehensive data to answer a complex question.
    
    CURRENT TIME: {current_time_str}
    
    ORIGINAL QUESTION: {question}
    
    {user_context_text}
    
    COLLECTED DATA FROM COMMAND STACK:
    {collected_data}
    
    Provide a comprehensive analysis that:
    
    1. **DIRECT ANSWER**: Directly address the original question with clear, actionable insights
    
    2. **DATA SYNTHESIS**: Weave together insights from all data sources to tell a coherent story
    
    3. **MARKET IMPLICATIONS**: Explain what this means for:
       - Different asset classes and sectors
       - Risk-on vs risk-off environments
       - Portfolio positioning opportunities
       - Time horizons for these effects
    
    4. **STRATEGIC RECOMMENDATIONS**: Provide specific, actionable recommendations:
       - Which sectors/assets to overweight/underweight
       - Entry/exit strategies
       - Risk management considerations
       - Alternative scenarios to monitor
    
    5. **CONFIDENCE & RISKS**: Assess:
       - Confidence levels in your analysis
       - Key risks that could change the outlook
       - What to monitor for early warning signals
    
    6. **CONTEXT & TIMING**: Consider:
       - How current market conditions amplify or dampen these effects
       - Seasonal or cyclical factors
       - Geopolitical or policy uncertainties
    
    Be specific, data-driven, and actionable. Use the synthesized data to provide insights that go beyond what any single data source could provide. Think like a portfolio manager making real investment decisions.
    
    Format your response with clear sections and bullet points for easy reading.
    """
    
    return call_gpt(system_prompt, user_prompt)

def run(args: dict):
    """Main uber command function - the synthesis engine"""
    question = args["question"]
    collected_data = args["collected_data"]
    user_id = args.get("user_id")
    
    # Get current timestamp for logging
    current_time = datetime.now(timezone.utc)
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Gather user context
    user_context = get_user_context(user_id)
    
    # Synthesize comprehensive answer
    comprehensive_answer = synthesize_comprehensive_answer(
        question, 
        collected_data,
        user_context
    )
    
    return comprehensive_answer