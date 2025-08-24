state = {}

def set_running(user_id, status: bool):
    state[user_id] = status

def is_running(user_id):
    return state.get(user_id, False)
