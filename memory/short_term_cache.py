import psycopg2
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Get connection to database using Railway's injected DATABASE_URL"""
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def create_session_id(user_id: str) -> str:
    """Create a unique session ID for the user"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{user_id}_{timestamp}"

def add_to_recent_conversation(user_id: str, message: str, role: str = "user"):
    """
    Add message to recent conversation in database
    Maintains only the last 20 messages per user session
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get or create session
        session_id = get_or_create_session(cursor, user_id)
        
        # Get current messages
        cursor.execute("""
            SELECT recent_messages FROM short_term_memory 
            WHERE user_id = %s AND session_id = %s
        """, (user_id, session_id))
        
        result = cursor.fetchone()
        if result and result[0]:
            messages = result[0]
        else:
            messages = []
        
        # Add new message
        new_message = {
            "role": role,
            "content": message,
            "timestamp": datetime.now().isoformat()
        }
        
        messages.append(new_message)
        
        # Keep only last 20 messages (Google-style conversation limit)
        if len(messages) > 20:
            messages = messages[-20:]
        
        # Update the database
        cursor.execute("""
            INSERT INTO short_term_memory (user_id, session_id, recent_messages, updated_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, session_id) 
            DO UPDATE SET 
                recent_messages = %s,
                updated_at = %s
        """, (user_id, session_id, json.dumps(messages), datetime.now(),
               json.dumps(messages), datetime.now()))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error adding to conversation: {e}")
        return False

def get_recent_conversation(user_id: str, limit: int = 20) -> str:
    """
    Get recent conversation from database
    Returns formatted conversation string
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get current session
        session_id = get_or_create_session(cursor, user_id)
        
        cursor.execute("""
            SELECT recent_messages FROM short_term_memory 
            WHERE user_id = %s AND session_id = %s
        """, (user_id, session_id))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not result or not result[0]:
            return ""
        
        messages = result[0]
        
        # Format conversation for display
        formatted_conversation = []
        for msg in messages:
            role_display = "User" if msg["role"] == "user" else "Assistant"
            formatted_conversation.append(f"{role_display}: {msg['content']}")
        
        return "\n".join(formatted_conversation)
        
    except Exception as e:
        print(f"Error retrieving conversation: {e}")
        return ""

def update_current_cache(user_id: str, cache_data: Dict[str, Any]):
    """
    Update current cache with new data
    Cache can store command stack, user inputs, temporary calculations, etc.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        session_id = get_or_create_session(cursor, user_id)
        
        # Get existing cache
        cursor.execute("""
            SELECT current_cache FROM short_term_memory 
            WHERE user_id = %s AND session_id = %s
        """, (user_id, session_id))
        
        result = cursor.fetchone()
        existing_cache = result[0] if result and result[0] else {}
        
        # Merge new cache data
        updated_cache = {**existing_cache, **cache_data}
        
        # Update database
        cursor.execute("""
            INSERT INTO short_term_memory (user_id, session_id, current_cache, updated_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, session_id) 
            DO UPDATE SET 
                current_cache = %s,
                updated_at = %s
        """, (user_id, session_id, json.dumps(updated_cache), datetime.now(),
               json.dumps(updated_cache), datetime.now()))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error updating cache: {e}")
        return False

def get_current_cache(user_id: str) -> Dict[str, Any]:
    """Get current cache data for user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        session_id = get_or_create_session(cursor, user_id)
        
        cursor.execute("""
            SELECT current_cache FROM short_term_memory 
            WHERE user_id = %s AND session_id = %s
        """, (user_id, session_id))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return result[0] if result and result[0] else {}
        
    except Exception as e:
        print(f"Error retrieving cache: {e}")
        return {}

def update_market_data(user_id: str, market_data: Dict[str, Any]):
    """
    Update current market data context
    Stores market assessments, macro data, risk metrics, etc.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        session_id = get_or_create_session(cursor, user_id)
        
        # Add timestamp to market data
        market_data["last_updated"] = datetime.now().isoformat()
        
        # Update database
        cursor.execute("""
            INSERT INTO short_term_memory (user_id, session_id, current_market_data, updated_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, session_id) 
            DO UPDATE SET 
                current_market_data = %s,
                updated_at = %s
        """, (user_id, session_id, json.dumps(market_data), datetime.now(),
               json.dumps(market_data), datetime.now()))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error updating market data: {e}")
        return False

def get_current_market_data(user_id: str) -> Dict[str, Any]:
    """Get current market data for user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        session_id = get_or_create_session(cursor, user_id)
        
        cursor.execute("""
            SELECT current_market_data FROM short_term_memory 
            WHERE user_id = %s AND session_id = %s
        """, (user_id, session_id))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return result[0] if result and result[0] else {}
        
    except Exception as e:
        print(f"Error retrieving market data: {e}")
        return {}

def get_or_create_session(cursor, user_id: str) -> str:
    """Get existing session or create new one"""
    # Try to get existing active session (within last 2 hours)
    cursor.execute("""
        SELECT session_id FROM short_term_memory 
        WHERE user_id = %s 
        AND updated_at > %s
        ORDER BY updated_at DESC 
        LIMIT 1
    """, (user_id, datetime.now() - timedelta(hours=2)))
    
    result = cursor.fetchone()
    if result:
        return result[0]
    
    # Create new session
    return create_session_id(user_id)

def clear_expired_sessions():
    """Clean up expired sessions (older than 24 hours)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM short_term_memory 
            WHERE updated_at < %s
        """, (datetime.now() - timedelta(hours=24),))
        
        deleted_count = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Cleared {deleted_count} expired sessions")
        return deleted_count
        
    except Exception as e:
        print(f"Error clearing expired sessions: {e}")
        return 0

def get_session_summary(user_id: str) -> Dict[str, Any]:
    """Get comprehensive session summary for user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        session_id = get_or_create_session(cursor, user_id)
        
        cursor.execute("""
            SELECT recent_messages, current_cache, current_market_data, 
                   created_at, updated_at
            FROM short_term_memory 
            WHERE user_id = %s AND session_id = %s
        """, (user_id, session_id))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not result:
            return {
                "session_id": session_id,
                "message_count": 0,
                "cache_keys": [],
                "market_data_keys": [],
                "session_age": "new"
            }
        
        messages, cache, market_data, created_at, updated_at = result
        
        return {
            "session_id": session_id,
            "message_count": len(messages) if messages else 0,
            "cache_keys": list(cache.keys()) if cache else [],
            "market_data_keys": list(market_data.keys()) if market_data else [],
            "session_age": str(datetime.now() - created_at) if created_at else "unknown",
            "last_activity": str(updated_at) if updated_at else "unknown"
        }
        
    except Exception as e:
        print(f"Error getting session summary: {e}")
        return {}

# Convenience functions for common operations
def add_user_message(user_id: str, message: str):
    """Add user message to conversation"""
    return add_to_recent_conversation(user_id, message, "user")

def add_assistant_message(user_id: str, message: str):
    """Add assistant message to conversation"""
    return add_to_recent_conversation(user_id, message, "assistant")

def update_command_stack(user_id: str, command_stack: List[Dict]):
    """Update command stack in cache"""
    return update_current_cache(user_id, {"command_stack": command_stack})

def get_command_stack(user_id: str) -> List[Dict]:
    """Get current command stack from cache"""
    cache = get_current_cache(user_id)
    return cache.get("command_stack", [])

def update_user_preferences(user_id: str, preferences: Dict[str, Any]):
    """Update user preferences in cache"""
    return update_current_cache(user_id, {"user_preferences": preferences})

def get_user_preferences(user_id: str) -> Dict[str, Any]:
    """Get user preferences from cache"""
    cache = get_current_cache(user_id)
    return cache.get("user_preferences", {})
