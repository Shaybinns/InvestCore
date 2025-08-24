#!/usr/bin/env python3
"""
Minimal test script to isolate Railway startup issues
"""

import os
import sys

def main():
    print("🚀 Minimal Test Script Starting...")
    print("=" * 40)
    
    # Check basic environment
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")
    
    # Check if we can import Flask
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
        
        # Create minimal app
        app = Flask(__name__)
        
        @app.route('/')
        def hello():
            return "Hello from minimal test!"
        
        @app.route('/health')
        def health():
            return "OK"
        
        # Start server
        port = int(os.getenv('PORT', 5000))
        print(f"Starting minimal server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
