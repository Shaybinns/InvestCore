#!/usr/bin/env python3
"""
Simple test script for InvestCore AI
"""

from brain import handle_user_message

def main():
    print("🤖 InvestCore AI - Financial Assistant")
    print("=" * 50)
    print("Type 'quit' to exit")
    print()
    
    user_id = "test_user"
    
    while True:
        try:
            # Get user input
            user_message = input("You: ").strip()
            
            if user_message.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if user_message.lower() == 'debug':
                from memory.short_term_cache import cache
                from memory.long_term_db import user_logs
                print(f"\n🔍 DEBUG INFO:")
                print(f"Short-term cache entries: {len(cache)}")
                print(f"Long-term storage entries: {len(user_logs)}")
                if cache:
                    for user_id, messages in cache.items():
                        print(f"  User '{user_id}' has {len(messages)} messages:")
                        for i, msg in enumerate(messages, 1):
                            print(f"    {i}. {msg}")
                if user_logs:
                    for user_id, logs in user_logs.items():
                        print(f"  Long-term storage for '{user_id}':")
                        for i, log in enumerate(logs, 1):
                            print(f"    {i}. {log['result']}")
                continue
            
            if not user_message:
                continue
            
            # Process the message
            print("\n🤖 Processing...")
            response = handle_user_message(user_id, user_message)
            
            print(f"\nAI: {response}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("-" * 50)

if __name__ == "__main__":
    main() 