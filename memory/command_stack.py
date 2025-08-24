stack = {}

def push_stack(user_id, command_name, args, goal=None):
    stack.setdefault(user_id, []).append({
        "command": command_name,
        "args": args,
        "status": "pending",
        "goal": goal
    })

def peek_stack(user_id):
    if user_id in stack and stack[user_id]:
        return stack[user_id][0]
    return None

def pop_stack(user_id):
    if user_id in stack and stack[user_id]:
        return stack[user_id].pop(0)

def mark_current_complete(user_id):
    if user_id in stack and stack[user_id]:
        current = stack[user_id][0]
        if current["status"] != "done":
            current["status"] = "done"

def has_pending_steps(user_id):
    return any(step["status"] != "done" for step in stack.get(user_id, []))

def get_stack_state(user_id):
    return stack.get(user_id, [])

def get_current_goal(user_id):
    if user_id in stack and stack[user_id]:
        return stack[user_id][0].get("goal")
    return None
