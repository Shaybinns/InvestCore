#!/usr/bin/env python3
"""
Railway startup script for InvestCore API
This script handles environment setup and provides better error reporting
"""

import os
import sys
import traceback

def main():
    print("🚀 InvestCore API - Railway Startup")
    print("=" * 50)
    
    # Check environment variables
    print("🔍 Checking environment...")
    required_vars = ['RAPIDAPI_KEY', 'OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            print(f"❌ Missing: {var}")
        else:
            print(f"✅ Found: {var}")
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("💡 Make sure to set these in Railway dashboard > Variables")
        return 1
    
    # Check Python path
    print("\n🔍 Checking Python path...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")
    
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        print(f"Added {current_dir} to Python path")
    
    # Test imports
    print("\n🔍 Testing imports...")
    try:
        from flask import Flask
        print("✅ Flask imported")
    except Exception as e:
        print(f"❌ Flask import failed: {e}")
        return 1
    
    try:
        from brain import handle_user_message
        print("✅ Brain module imported")
    except Exception as e:
        print(f"❌ Brain import failed: {e}")
        traceback.print_exc()
        return 1
    
    try:
        from commands.get_asset_info import run
        print("✅ Commands imported")
    except Exception as e:
        print(f"❌ Commands import failed: {e}")
        traceback.print_exc()
        return 1
    
    # Start the API server
    print("\n🚀 Starting API server...")
    try:
        from api_server import app
        
        port = int(os.getenv('PORT', 5000))
        host = os.getenv('HOST', '0.0.0.0')
        
        print(f"📱 Server starting on {host}:{port}")
        print(f"🔍 Health check will be available at /api/health")
        
        app.run(host=host, port=port, debug=False)
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    if exit_code != 0:
        print(f"\n❌ Startup failed with exit code {exit_code}")
        print("💡 Check the logs above for details")
        sys.exit(exit_code)
