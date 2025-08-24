user_logs = {}

def save_result(user_id, result):
    user_logs.setdefault(user_id, []).append({
        "result": result
    })

def get_user_facts(user_id):
    # You could also summarize logs here
    logs = user_logs.get(user_id, [])
    return "\n".join([f"Task Result: {log['result']}" for log in logs])

def get_latest_result(command_name, symbol=None):
    """Get the latest result for a specific command"""
    # For now, return None to indicate no previous result
    # This can be enhanced later to actually store and retrieve command results
    return None
