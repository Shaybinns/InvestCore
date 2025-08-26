from flask import Flask, request, jsonify, render_template_string
import requests
import json
import time

app = Flask(__name__)

# HTML template for the improved testing dashboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>InvestCore AI Chatbot - Testing Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .chat-section {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            height: 600px;
            display: flex;
            flex-direction: column;
        }
        
        .chat-header {
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .chat-header h2 {
            color: #667eea;
            font-size: 1.8rem;
            margin-bottom: 5px;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
            margin-bottom: 20px;
            border: 1px solid #e9ecef;
        }
        
        .message {
            margin: 15px 0;
            padding: 15px 20px;
            border-radius: 15px;
            max-width: 80%;
            word-wrap: break-word;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .user-message { 
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px;
        }
        
        .ai-message { 
            background: white;
            border: 2px solid #e9ecef;
            margin-right: auto;
            border-bottom-left-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .ai-message.thinking {
            background: #fff3cd;
            border-color: #ffeaa7;
            font-style: italic;
        }
        
        .ai-message.error {
            background: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }
        
        .ai-message.success {
            background: #d4edda;
            border-color: #c3e6cb;
            color: #155724;
        }
        
        .chat-input {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .chat-input input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s ease;
        }
        
        .chat-input input:focus {
            border-color: #667eea;
        }
        
        .chat-input button {
            padding: 15px 25px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: transform 0.2s ease;
        }
        
        .chat-input button:hover {
            transform: translateY(-2px);
        }
        
        .chat-input button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .status-card {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
        }
        
        .status-card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online { background: #28a745; }
        .status-offline { background: #dc3545; }
        
        .quick-actions {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .quick-actions h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }
        
        .quick-action-btn {
            display: block;
            width: 100%;
            padding: 12px 15px;
            margin: 8px 0;
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: left;
            font-size: 14px;
        }
        
        .quick-action-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .api-info {
            background: white;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .api-info h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }
        
        .endpoint-list {
            list-style: none;
            font-size: 12px;
            color: #666;
        }
        
        .endpoint-list li {
            margin: 5px 0;
            padding: 5px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .endpoint-list li:last-child {
            border-bottom: none;
        }
        
        .typing-indicator {
            display: none;
            padding: 15px 20px;
            background: #f8f9fa;
            border-radius: 15px;
            margin: 15px 0;
            font-style: italic;
            color: #666;
        }
        
        .typing-indicator.show {
            display: block;
        }
        
        .typing-dots {
            display: inline-block;
            animation: typing 1.4s infinite;
        }
        
        @keyframes typing {
            0%, 20% { content: "●○○"; }
            40% { content: "●●○"; }
            60% { content: "●●●"; }
            80%, 100% { content: "○○○"; }
        }
        
        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .chat-section {
                height: 500px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 InvestCore AI Chatbot</h1>
            <p>Your intelligent investment research assistant</p>
        </div>
        
        <div class="dashboard-grid">
            <!-- Main Chat Section -->
            <div class="chat-section">
                <div class="chat-header">
                    <h2>💬 Chat with InvestCore AI</h2>
                    <p>Ask me about stocks, markets, portfolio analysis, and more!</p>
                </div>
                
                <div class="chat-messages" id="chat-messages">
                    <div class="message ai-message">
                        👋 Hello! I'm InvestCore AI, your investment research assistant. I can help you with:
                        <br><br>
                        📊 Stock analysis and screening<br>
                        📈 Market and sector assessments<br>
                        💰 Financial data and earnings<br>
                        🌍 Macroeconomic insights<br>
                        🔍 Web research and news<br>
                        <br>
                        What would you like to know about today?
                    </div>
                </div>
                
                <div class="typing-indicator" id="typing-indicator">
                    <span class="typing-dots">●○○</span> AI is thinking...
                </div>
                
                <div class="chat-input">
                    <input type="text" id="user-input" placeholder="Ask me anything about investments..." onkeypress="if(event.key=='Enter') sendMessage()">
                    <button onclick="sendMessage()" id="send-btn">Send</button>
                </div>
            </div>
            
            <!-- Sidebar -->
            <div class="sidebar">
                <!-- API Status -->
                <div class="status-card">
                    <h3>🔌 API Status</h3>
                    <p><span class="status-indicator" id="status-indicator"></span><span id="api-status">Checking...</span></p>
                    <button onclick="checkHealth()" style="margin-top: 15px; padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 10px; cursor: pointer;">🔄 Refresh</button>
                </div>
                
                <!-- Quick Actions -->
                <div class="quick-actions">
                    <h3>⚡ Quick Actions</h3>
                    <button class="quick-action-btn" onclick="sendQuickMessage('Analyze AAPL stock')">📊 Analyze AAPL</button>
                    <button class="quick-action-btn" onclick="sendQuickMessage('What is the current market sentiment?')">📈 Market Sentiment</button>
                    <button class="quick-action-btn" onclick="sendQuickMessage('Screen for tech stocks with high growth')">🔍 Screen Tech Stocks</button>
                    <button class="quick-action-btn" onclick="sendQuickMessage('Get financial data for TSLA')">💰 TSLA Financials</button>
                    <button class="quick-action-btn" onclick="sendQuickMessage('What are the latest earnings trends?')">📊 Earnings Trends</button>
                </div>
                
                <!-- API Info -->
                <div class="api-info">
                    <h3>🔗 Available Endpoints</h3>
                    <ul class="endpoint-list">
                        <li><strong>POST</strong> /api/chat - Main chat</li>
                        <li><strong>GET</strong> /api/asset/{symbol} - Asset info</li>
                        <li><strong>POST</strong> /api/screen - Asset screening</li>
                        <li><strong>POST</strong> /api/market/assess - Market analysis</li>
                        <li><strong>GET</strong> /api/financials/{symbol} - Financial data</li>
                        <li><strong>GET</strong> /api/earnings/{symbol} - Earnings data</li>
                        <li><strong>GET</strong> /api/macros - Macro indicators</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = 'http://localhost:5000';
        let isProcessing = false;
        
        // Check API health on load
        window.onload = function() {
            checkHealth();
        };
        
        async function checkHealth() {
            const statusIndicator = document.getElementById('status-indicator');
            const apiStatus = document.getElementById('api-status');
            
            try {
                const response = await fetch(API_BASE + '/api/health');
                const data = await response.json();
                
                if (response.ok) {
                    statusIndicator.className = 'status-indicator status-online';
                    apiStatus.innerHTML = 'Online - ' + data.status;
                    apiStatus.style.color = '#28a745';
                } else {
                    throw new Error(data.error || 'Unknown error');
                }
            } catch (error) {
                statusIndicator.className = 'status-indicator status-offline';
                apiStatus.innerHTML = 'Offline - ' + error.message;
                apiStatus.style.color = '#dc3545';
            }
        }
        
        function sendQuickMessage(message) {
            document.getElementById('user-input').value = message;
            sendMessage();
        }
        
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');
            const message = input.value.trim();
            
            if (!message || isProcessing) return;
            
            // Add user message
            addMessage('user', message);
            input.value = '';
            
            // Show typing indicator
            showTypingIndicator();
            
            // Disable input and button
            isProcessing = true;
            input.disabled = true;
            sendBtn.disabled = true;
            
            try {
                const response = await fetch(API_BASE + '/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: 'test_user_' + Date.now(),
                        message: message
                    })
                });
                
                const data = await response.json();
                
                // Hide typing indicator
                hideTypingIndicator();
                
                if (data.success) {
                    // Show initial response
                    if (data.initial_response) {
                        addMessage('ai', data.initial_response);
                    }
                    
                    // Show command result if available
                    if (data.command_result && data.command_result !== data.initial_response) {
                        addMessage('ai', data.command_result, 'success');
                    }
                    
                    // Show error if any
                    if (data.error) {
                        addMessage('ai', 'Error: ' + data.error, 'error');
                    }
                } else {
                    addMessage('ai', 'Error: ' + (data.error || 'Unknown error'), 'error');
                }
                
            } catch (error) {
                hideTypingIndicator();
                addMessage('ai', 'Connection Error: ' + error.message, 'error');
            } finally {
                // Re-enable input and button
                isProcessing = false;
                input.disabled = false;
                sendBtn.disabled = false;
                input.focus();
            }
        }
        
        function showTypingIndicator() {
            document.getElementById('typing-indicator').classList.add('show');
        }
        
        function hideTypingIndicator() {
            document.getElementById('typing-indicator').classList.remove('show');
        }
        
        function addMessage(type, content, style = '') {
            const messagesDiv = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            
            messageDiv.className = `message ${type}-message`;
            if (style) messageDiv.classList.add(style);
            
            // Format content with line breaks
            content = content.replace(/\\n/g, '<br>');
            
            messageDiv.innerHTML = content;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // Auto-resize input on focus
        document.getElementById('user-input').addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
        });
        
        document.getElementById('user-input').addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return HTML_TEMPLATE

@app.route('/api/health')
def dashboard_health():
    """Health check for the dashboard itself"""
    return jsonify({
        "status": "healthy",
        "service": "InvestCore Testing Dashboard",
        "version": "2.0.0",
        "message": "Dashboard is running"
    })

if __name__ == '__main__':
    print("🚀 Starting InvestCore AI Chatbot Testing Dashboard...")
    print("📱 Open http://localhost:5001 in your browser")
    print("🔗 Make sure your API server is running on http://localhost:5000")
    print("💡 Use the quick action buttons to test different scenarios")
    print("🔍 Check the sidebar for API status and available endpoints")
    
    try:
        app.run(host='0.0.0.0', port=5001, debug=False)
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
        print("💡 Try using a different port if 5001 is already in use")
        exit(1)
