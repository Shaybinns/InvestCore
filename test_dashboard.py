from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

# HTML template for the testing dashboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>InvestCore API Testing Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .chat-box { background: white; border-radius: 10px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .input-area { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"] { flex: 1; padding: 12px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
        button { padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        .message { margin: 15px 0; padding: 15px; border-radius: 8px; }
        .user-message { background: #e3f2fd; border-left: 4px solid #2196f3; }
        .ai-initial { background: #f3e5f5; border-left: 4px solid #9c27b0; }
        .ai-result { background: #e8f5e8; border-left: 4px solid #4caf50; }
        .error { background: #ffebee; border-left: 4px solid #f44336; }
        .streaming { animation: fadeIn 0.5s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .status { font-size: 12px; color: #666; margin-top: 5px; }
        .api-info { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 15px; margin: 20px 0; }
        .endpoint-test { background: white; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .response-box { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; margin: 10px 0; font-family: monospace; font-size: 12px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 InvestCore API Testing Dashboard</h1>
        
        <div class="api-info">
            <h3>📡 API Status</h3>
            <p><strong>Base URL:</strong> <span id="api-url">http://localhost:5000</span></p>
            <p><strong>Status:</strong> <span id="api-status">Checking...</span></p>
            <button onclick="checkHealth()">🔄 Check Health</button>
        </div>

        <div class="chat-box">
            <h2>💬 Chat Testing</h2>
            <p>Test the <code>/api/chat</code> endpoint with real API calls</p>
            
            <div class="input-area">
                <input type="text" id="user-input" placeholder="Ask me anything about stocks, markets, etc..." onkeypress="if(event.key=='Enter') sendMessage()">
                <button onclick="sendMessage()">Send</button>
                <button onclick="sendMessageStream()" style="background: #28a745;">🚀 Stream</button>
                <button onclick="testStreamEndpoint()" style="background: #ffc107; color: #000;">🧪 Test Stream</button>
            </div>
            
            <div id="chat-messages"></div>
        </div>

        <div class="endpoint-test">
            <h2>🧪 Endpoint Testing</h2>
            <p>Test other API endpoints</p>
            
            <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                <input type="text" id="asset-symbol" placeholder="Stock symbol (e.g., AAPL)" value="AAPL">
                <button onclick="testAssetInfo()">Test Asset Info</button>
                <button onclick="testFinancials()">Test Financials</button>
                <button onclick="testEarnings()">Test Earnings</button>
            </div>
            
            <div id="endpoint-results"></div>
        </div>
    </div>

    <script>
        const API_BASE = 'http://localhost:5000';
        
        // Check API health on load
        window.onload = function() {
            checkHealth();
        };
        
        async function checkHealth() {
            try {
                const response = await fetch(API_BASE + '/api/health');
                const data = await response.json();
                document.getElementById('api-status').innerHTML = '✅ Online - ' + data.status;
                document.getElementById('api-status').style.color = '#28a745';
            } catch (error) {
                document.getElementById('api-status').innerHTML = '❌ Offline - ' + error.message;
                document.getElementById('api-status').style.color = '#dc3545';
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;
            
            // Add user message
            addMessage('user', message);
            input.value = '';
            
            try {
                const response = await fetch(API_BASE + '/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: 'test_user',
                        message: message
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Show initial response
                    if (data.initial_response) {
                        addMessage('ai-initial', data.initial_response, 'Initial AI Response');
                    }
                    
                    // Show command result
                    if (data.command_result) {
                        addMessage('ai-result', data.command_result, 'Command Result');
                    }
                    
                    // Show status info
                    addStatusInfo(data);
                } else {
                    addMessage('error', 'Error: ' + (data.error || 'Unknown error'));
                }
                
            } catch (error) {
                addMessage('error', 'API Error: ' + error.message);
            }
        }

        async function sendMessageStream() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;
            
            console.log('🚀 Starting streaming request for:', message);
            
            // Add user message
            addMessage('user', message);
            input.value = '';
            
            // Clear previous AI messages for this conversation
            const messagesDiv = document.getElementById('chat-messages');
            const aiMessages = messagesDiv.querySelectorAll('.ai-initial, .ai-result');
            aiMessages.forEach(msg => msg.remove());
            
            try {
                console.log('📡 Fetching from streaming endpoint...');
                const response = await fetch(API_BASE + '/api/chat/stream', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: 'test_user',
                        message: message
                    })
                });

                console.log('📥 Response received:', response.status, response.headers.get('content-type'));

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const reader = response.body.getReader();
                const decoder = new TextDecoder();

                console.log('📖 Starting to read stream...');

                while (true) {
                    const { done, value } = await reader.read();
                    
                    if (done) {
                        console.log('✅ Stream complete');
                        break;
                    }
                    
                    const chunk = decoder.decode(value);
                    console.log('📦 Received chunk:', chunk);
                    
                    const lines = chunk.split('\n').filter(line => line.trim());
                    console.log('📝 Parsed lines:', lines);
                    
                    for (const line of lines) {
                        try {
                            const data = JSON.parse(line);
                            console.log('🎯 Parsed data:', data);
                            
                            switch (data.type) {
                                case 'initial_response':
                                    console.log('🚀 Adding initial response');
                                    addMessage('ai-initial', data.message, '🚀 Initial Response');
                                    break;
                                    
                                case 'command_result':
                                    console.log('⚡ Adding command result');
                                    addMessage('ai-result', data.result || 'No result', '⚡ Command Result');
                                    break;
                                    
                                case 'completion':
                                    console.log('✅ Adding completion');
                                    addMessage('ai-result', '✅ Complete!', 'Status');
                                    break;
                                    
                                default:
                                    console.log('❓ Unknown response type:', data);
                            }
                        } catch (parseError) {
                            console.error('❌ Failed to parse JSON:', line, parseError);
                        }
                    }
                }
            } catch (error) {
                console.error('💥 Streaming error:', error);
                addMessage('error', 'Streaming Error: ' + error.message);
            }
        }
        
        async function testStreamEndpoint() {
            console.log('🧪 Testing stream endpoint...');
            
            try {
                const response = await fetch(API_BASE + '/api/chat/stream', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: 'test_user',
                        message: 'test message'
                    })
                });
                
                console.log('📥 Test response:', response.status, response.headers.get('content-type'));
                
                if (response.ok) {
                    addMessage('ai-result', `✅ Stream endpoint working! Status: ${response.status}, Content-Type: ${response.headers.get('content-type')}`, 'Test Result');
                } else {
                    addMessage('error', `❌ Stream endpoint failed! Status: ${response.status}`, 'Test Result');
                }
            } catch (error) {
                console.error('💥 Test error:', error);
                addMessage('error', `❌ Test failed: ${error.message}`, 'Test Result');
            }
        }
        
        function addMessage(type, content, label = '') {
            const messagesDiv = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            let html = '';
            if (label) {
                html += `<strong>${label}:</strong><br>`;
            }
            html += content.replace(/\\n/g, '<br>');
            
            messageDiv.innerHTML = html;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function addStatusInfo(data) {
            const messagesDiv = document.getElementById('chat-messages');
            const statusDiv = document.createElement('div');
            statusDiv.className = 'message';
            statusDiv.style.background = '#f8f9fa';
            statusDiv.style.fontSize = '12px';
            statusDiv.style.color = '#666';
            
            let statusInfo = `Status: ${data.status}`;
            if (data.command_name) statusInfo += ` | Command: ${data.command_name}`;
            if (data.command_executed !== undefined) statusInfo += ` | Executed: ${data.command_executed}`;
            if (data.has_more_steps !== undefined) statusInfo += ` | More Steps: ${data.has_more_steps}`;
            
            statusDiv.innerHTML = statusInfo;
            messagesDiv.appendChild(statusDiv);
        }
        
        async function testAssetInfo() {
            const symbol = document.getElementById('asset-symbol').value.toUpperCase();
            if (!symbol) return;
            
            try {
                const response = await fetch(API_BASE + '/api/asset/' + symbol);
                const data = await response.json();
                showEndpointResult('Asset Info for ' + symbol, data);
            } catch (error) {
                showEndpointResult('Asset Info Error', { error: error.message });
            }
        }
        
        async function testFinancials() {
            const symbol = document.getElementById('asset-symbol').value.toUpperCase();
            if (!symbol) return;
            
            try {
                const response = await fetch(API_BASE + '/api/financials/' + symbol);
                const data = await response.json();
                showEndpointResult('Financials for ' + symbol, data);
            } catch (error) {
                showEndpointResult('Financials Error', { error: error.message });
            }
        }
        
        async function testEarnings() {
            const symbol = document.getElementById('asset-symbol').value.toUpperCase();
            if (!symbol) return;
            
            try {
                const response = await fetch(API_BASE + '/api/earnings/' + symbol);
                const data = await response.json();
                showEndpointResult('Earnings for ' + symbol, data);
            } catch (error) {
                showEndpointResult('Earnings Error', { error: error.message });
            }
        }
        
        function showEndpointResult(title, data) {
            const resultsDiv = document.getElementById('endpoint-results');
            const resultDiv = document.createElement('div');
            resultDiv.className = 'endpoint-test';
            resultDiv.innerHTML = `
                <h4>${title}</h4>
                <div class="response-box">${JSON.stringify(data, null, 2)}</div>
            `;
            resultsDiv.appendChild(resultDiv);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return HTML_TEMPLATE

if __name__ == '__main__':
    print("🚀 Starting InvestCore Testing Dashboard...")
    print("📱 Open http://localhost:5001 in your browser")
    print("🔗 Make sure your API server is running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5001, debug=False)
