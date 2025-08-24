# main.py
from brain import handle_user_message

user_id = "test_user"

print("Portfolio AI is ready. Type your message below:")

while True:
    message = input("You: ")
    if message.lower() in ["exit", "quit"]:
        break
    reply = handle_user_message(user_id, message)
    print(f"Portfolio AI: {reply}")
