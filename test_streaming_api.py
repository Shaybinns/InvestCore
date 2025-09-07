#!/usr/bin/env python3
"""
Test script for the InvestCore streaming API
Shows real-time streaming effect with proper chunk handling
"""

import requests
import json
import time
import sys

def test_streaming_api(api_url, user_id, message):
    """Test the streaming API with real-time output"""
    
    print(f"🚀 Testing streaming API...")
    print(f"📡 URL: {api_url}")
    print(f"👤 User ID: {user_id}")
    print(f"💬 Message: {message}")
    print("=" * 50)
    
    # Prepare the request data
    data = {
        "user_id": user_id,
        "message": message
    }
    
    try:
        # Make the streaming request
        response = requests.post(
            api_url,
            json=data,
            stream=True,  # Enable streaming
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
            return
        
        print("✅ Connected! Streaming response:")
        print("-" * 30)
        
        # Process the stream in real-time
        for line in response.iter_lines(decode_unicode=True):
            if line.strip():
                try:
                    # Parse each JSON chunk
                    chunk = json.loads(line)
                    
                    # Display based on chunk type
                    if chunk.get("type") == "stream_start":
                        print(f"🎬 Stream started for user: {chunk.get('user_id')}")
                        
                    elif chunk.get("type") == "initial_response":
                        chunk_num = chunk.get("chunk_number", 1)
                        total_chunks = chunk.get("total_chunks", 1)
                        content = chunk.get("chunk", "")
                        timestamp = chunk.get("timestamp", 0)
                        
                        print(f"📝 Chunk {chunk_num}/{total_chunks}: {content}")
                        print(f"   ⏰ Timestamp: {time.ctime(timestamp)}")
                        
                    elif chunk.get("type") == "command_start":
                        command = chunk.get("command_name", "unknown")
                        print(f"⚙️  Executing command: {command}")
                        
                    elif chunk.get("type") == "command_result":
                        result = chunk.get("command_result", "")
                        executed = chunk.get("command_executed", False)
                        status = chunk.get("status", "unknown")
                        
                        print(f"📊 Command Result:")
                        print(f"   Status: {status}")
                        print(f"   Executed: {executed}")
                        if result:
                            print(f"   Result: {result[:100]}{'...' if len(result) > 100 else ''}")
                        
                    elif chunk.get("type") == "completion":
                        success = chunk.get("success", False)
                        print(f"✅ Stream completed: {'Success' if success else 'Failed'}")
                        
                    elif chunk.get("type") == "error":
                        error = chunk.get("error", "Unknown error")
                        print(f"❌ Error: {error}")
                        
                    else:
                        print(f"📦 Unknown chunk type: {chunk.get('type')}")
                        print(f"   Data: {chunk}")
                    
                    print()  # Empty line for readability
                    
                except json.JSONDecodeError as e:
                    print(f"⚠️  JSON decode error: {e}")
                    print(f"   Raw line: {line}")
                    
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function with example usage"""
    
    # Configuration - UPDATE THESE VALUES
    API_URL = "https://your-app-name.railway.app/api/chat/stream"  # Change to your Railway URL
    USER_ID = "bf98e9d2-2d3f-4632-905a-9f946026ab59"  # Your working UUID
    MESSAGE = "whats your name"  # Your test message
    
    # Check if command line arguments provided
    if len(sys.argv) > 1:
        MESSAGE = " ".join(sys.argv[1:])
    
    print("🎯 InvestCore Streaming API Tester")
    print("=" * 40)
    
    # Run the test
    test_streaming_api(API_URL, USER_ID, MESSAGE)
    
    print("\n🏁 Test completed!")

if __name__ == "__main__":
    main()
