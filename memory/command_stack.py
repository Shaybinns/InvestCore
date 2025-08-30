from memory.short_term_cache import update_current_cache, get_current_cache
from datetime import datetime
import json

def push_stack(user_id, command_name, args, goal=None):
    """Push a new command to the stack with timestamp and store in database"""
    # Get current stack from database
    current_cache = get_current_cache(user_id)
    command_stack = current_cache.get("command_stack", [])
    
    # Add new command with comprehensive metadata
    new_command = {
        "command": command_name,
        "args": args,
        "goal": goal,
        "status": "pending",
        "timestamp": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
        "execution_start": None,
        "execution_end": None,
        "result": None,
        "error": None,
        "completion_notes": None
    }
    
    command_stack.append(new_command)
    
    # Update database with new stack
    update_current_cache(user_id, {
        "command_stack": command_stack,
        "last_stack_update": datetime.now().isoformat(),
        "active_goals": [cmd.get("goal") for cmd in command_stack if cmd.get("goal")],
        "pending_commands": len([cmd for cmd in command_stack if cmd["status"] == "pending"]),
        "completed_commands": len([cmd for cmd in command_stack if cmd["status"] == "done"])
    })
    
    return new_command

def peek_stack(user_id):
    """Get the current pending command from database"""
    current_cache = get_current_cache(user_id)
    command_stack = current_cache.get("command_stack", [])
    
    if command_stack:
        return command_stack[0]
    return None

def pop_stack(user_id):
    """Remove and return the completed command from database"""
    current_cache = get_current_cache(user_id)
    command_stack = current_cache.get("command_stack", [])
    
    if command_stack:
        completed_command = command_stack.pop(0)
        
        # Update database with modified stack
        update_current_cache(user_id, {
            "command_stack": command_stack,
            "last_stack_update": datetime.now().isoformat(),
            "pending_commands": len([cmd for cmd in command_stack if cmd["status"] == "pending"]),
            "completed_commands": len([cmd for cmd in command_stack if cmd["status"] == "done"])
        })
        
        return completed_command
    return None

def mark_current_complete(user_id, result=None, error=None, completion_notes=None):
    """Mark current command as complete with results and store in database"""
    current_cache = get_current_cache(user_id)
    command_stack = current_cache.get("command_stack", [])
    
    if command_stack and command_stack[0]["status"] != "done":
        current = command_stack[0]
        current["status"] = "done"
        current["execution_end"] = datetime.now().isoformat()
        current["result"] = result
        current["error"] = error
        current["completion_notes"] = completion_notes
        
        # Update database with completion
        update_current_cache(user_id, {
            "command_stack": command_stack,
            "last_stack_update": datetime.now().isoformat(),
            "pending_commands": len([cmd for cmd in command_stack if cmd["status"] == "pending"]),
            "completed_commands": len([cmd for cmd in command_stack if cmd["status"] == "done"]),
            "last_completion": datetime.now().isoformat()
        })
        
        return current
    return None

def start_command_execution(user_id):
    """Mark command execution as started with timestamp"""
    current_cache = get_current_cache(user_id)
    command_stack = current_cache.get("command_stack", [])
    
    if command_stack and command_stack[0]["status"] == "pending":
        current = command_stack[0]
        current["execution_start"] = datetime.now().isoformat()
        current["status"] = "executing"
        
        # Update database
        update_current_cache(user_id, {
            "command_stack": command_stack,
            "last_stack_update": datetime.now().isoformat(),
            "current_execution": {
                "command": current["command"],
                "started_at": current["execution_start"],
                "goal": current.get("goal")
            }
        })
        
        return current
    return None

def has_pending_steps(user_id):
    """Check if there are pending steps in database"""
    current_cache = get_current_cache(user_id)
    command_stack = current_cache.get("command_stack", [])
    
    return any(step["status"] in ["pending", "executing"] for step in command_stack)

def get_stack_state(user_id):
    """Get complete stack state from database"""
    current_cache = get_current_cache(user_id)
    return current_cache.get("command_stack", [])

def get_current_goal(user_id):
    """Get current goal from database"""
    current_cache = get_current_cache(user_id)
    command_stack = current_cache.get("command_stack", [])
    
    if command_stack:
        return command_stack[0].get("goal")
    return None

def get_stack_summary(user_id):
    """Get comprehensive stack summary from database"""
    current_cache = get_current_cache(user_id)
    command_stack = current_cache.get("command_stack", [])
    
    if not command_stack:
        return {
            "status": "empty",
            "total_commands": 0,
            "pending": 0,
            "executing": 0,
            "completed": 0,
            "current_goal": None,
            "last_update": None
        }
    
    pending = len([cmd for cmd in command_stack if cmd["status"] == "pending"])
    executing = len([cmd for cmd in command_stack if cmd["status"] == "executing"])
    completed = len([cmd for cmd in command_stack if cmd["status"] == "done"])
    
    return {
        "status": "active" if pending > 0 or executing > 0 else "completed",
        "total_commands": len(command_stack),
        "pending": pending,
        "executing": executing,
        "completed": completed,
        "current_goal": command_stack[0].get("goal") if command_stack else None,
        "last_update": current_cache.get("last_stack_update"),
        "current_execution": current_cache.get("current_execution")
    }

def clear_completed_stack(user_id):
    """Remove all completed commands from stack and keep only pending ones"""
    current_cache = get_current_cache(user_id)
    command_stack = current_cache.get("command_stack", [])
    
    # Keep only pending and executing commands
    active_commands = [cmd for cmd in command_stack if cmd["status"] in ["pending", "executing"]]
    
    # Update database with cleaned stack
    update_current_cache(user_id, {
        "command_stack": active_commands,
        "last_stack_update": datetime.now().isoformat(),
        "stack_cleaned": datetime.now().isoformat(),
        "pending_commands": len([cmd for cmd in active_commands if cmd["status"] == "pending"]),
        "completed_commands": 0
    })
    
    return active_commands
