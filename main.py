# main.py
from brain import handle_user_message

user_id = "a220247d-b621-4b8d-9653-f1f1d6b8f105"

print("Portfolio AI is ready. Type your message below:")

while True:
    message = input("You: ")
    if message.lower() in ["exit", "quit"]:
        break
    reply = handle_user_message(user_id, message)
    print(f"Portfolio AI: {reply}")
