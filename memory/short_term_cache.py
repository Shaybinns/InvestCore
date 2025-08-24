cache = {}

def get_recent_conversation(user_id: str) -> str:
    return "\n".join(cache.get(user_id, []))

def add_to_recent_conversation(user_id: str, message: str):
    cache.setdefault(user_id, []).append(message)
    if len(cache[user_id]) > 10:
        cache[user_id] = cache[user_id][-10:]
