import requests
import json
import time

def test_streaming_endpoint():
    """Test the streaming chat endpoint"""
    
    # Your Railway URL
    url = "https://investcore-production.up.railway.app/api/chat/stream"
    
    # Test data
    data = {
        "user_id": "test123",
        "message": "whats the price of Nvidia stock right now"
    }
    
    print("🚀 Testing streaming endpoint...")
    print(f"📡 URL: {url}")
    print(f"📝 Message: {data['message']}")
    print("=" * 50)
    
    try:
        # Make the streaming request
        response = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'},
            stream=True  # Important for streaming!
        )
        
        if response.status_code == 200:
            print("✅ Stream started successfully!")
            print("📊 Receiving data chunks...\n")
            
            # Process the streaming response
            for line in response.iter_lines():
                if line:
                    # Decode the line and parse JSON
                    chunk = line.decode('utf-8')
                    try:
                        data_chunk = json.loads(chunk)
                        
                        # Pretty print each chunk
                        chunk_type = data_chunk.get('type', 'unknown')
                        timestamp = data_chunk.get('timestamp', 0)
                        
                        print(f"📦 {chunk_type.upper()}:")
                        print(f"   ⏰ Timestamp: {timestamp}")
                        
                        # Handle different chunk types
                        if chunk_type == 'stream_start':
                            print(f"   🆔 User ID: {data_chunk.get('user_id')}")
                        elif chunk_type == 'initial_response':
                            print(f"   📝 Chunk {data_chunk.get('chunk_number')}/{data_chunk.get('total_chunks')}")
                            print(f"   💬 Text: {data_chunk.get('chunk')}")
                        elif chunk_type == 'command_start':
                            print(f"   🚀 Command: {data_chunk.get('command_name')}")
                            print(f"   💭 Message: {data_chunk.get('message')}")
                        elif chunk_type == 'command_result':
                            print(f"   ✅ Executed: {data_chunk.get('command_executed')}")
                            print(f"   📊 Status: {data_chunk.get('status')}")
                            if data_chunk.get('command_result'):
                                print(f"   📋 Result: {data_chunk.get('command_result')}")
                        elif chunk_type == 'completion':
                            print(f"   🎉 Success: {data_chunk.get('success')}")
                        elif chunk_type == 'error':
                            print(f"   ❌ Error: {data_chunk.get('error')}")
                        
                        print()
                        
                    except json.JSONDecodeError:
                        print(f"❌ Failed to parse JSON: {chunk}")
                        
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_streaming_endpoint()
