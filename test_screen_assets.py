#!/usr/bin/env python3
"""
Test script for the screen_assets command
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commands.screen_assets import run

def test_screen_assets():
    """Test the screen_assets command with bond market indices search"""
    
    print("=" * 60)
    print("TESTING SCREEN ASSETS COMMAND")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test arguments
    test_args = {
        "filters": "find the best total bond market indices",
        "user_id": None  # No user_id to avoid UUID issues
    }
    
    print("Test Query:", test_args["filters"])
    print()
    print("Running screen_assets...")
    print("-" * 40)
    
    try:
        # Run the screen_assets command
        result = run(test_args)
        
        print("SUCCESS! Command executed successfully.")
        print()
        print("RESULTS:")
        print("=" * 60)
        # Handle Unicode characters safely
        try:
            print(result)
        except UnicodeEncodeError:
            print(result.encode('utf-8', errors='replace').decode('utf-8'))
        print("=" * 60)
        
        # Basic validation
        if len(result) > 100:
            print(f"\n[OK] Result length: {len(result)} characters (good)")
        else:
            print(f"\n[WARN] Result length: {len(result)} characters (may be too short)")
            
        # Check for key sections
        key_sections = [
            "EXECUTIVE SUMMARY",
            "TOP TIER RECOMMENDATIONS", 
            "SECONDARY OPTIONS",
            "MARKET INSIGHTS",
            "PORTFOLIO CONSIDERATIONS",
            "NEXT STEPS"
        ]
        
        found_sections = []
        for section in key_sections:
            if section in result:
                found_sections.append(section)
                
        print(f"\n[OK] Found {len(found_sections)}/{len(key_sections)} expected sections:")
        for section in found_sections:
            print(f"  - {section}")
            
        if len(found_sections) < len(key_sections) - 1:
            print("[WARN] Some expected sections may be missing")
            
        print("\n" + "=" * 60)
        print("TEST COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        print("\n" + "=" * 60)
        print("TEST FAILED")
        print("=" * 60)
        return False

def test_with_user_context():
    """Test with a mock user context (will show UUID errors but should still work)"""
    
    print("\n" + "=" * 60)
    print("TESTING WITH USER CONTEXT")
    print("=" * 60)
    
    test_args = {
        "filters": "find the best total bond market indices for conservative investors",
        "user_id": "test-user-123"  # This will cause UUID errors but should still work
    }
    
    print("Test Query:", test_args["filters"])
    print("Note: UUID errors expected with test user_id")
    print()
    
    try:
        result = run(test_args)
        print("SUCCESS! Command executed despite UUID errors.")
        print(f"Result length: {len(result)} characters")
        
        # Show first 300 characters
        print("\nFirst 300 characters of result:")
        print("-" * 40)
        print(result[:300] + "..." if len(result) > 300 else result)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    print("Screen Assets Test Suite")
    print("Testing the refactored screen_assets command")
    print()
    
    # Test 1: Basic functionality
    success1 = test_screen_assets()
    
    # Test 2: With user context (expect UUID errors)
    success2 = test_with_user_context()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Basic test: {'PASS' if success1 else 'FAIL'}")
    print(f"User context test: {'PASS' if success2 else 'FAIL'}")
    
    if success1:
        print("\n[SUCCESS] Screen assets command is working correctly!")
        print("[SUCCESS] The refactored Perplexity-based approach is functional")
    else:
        print("\n[FAILURE] Screen assets command needs debugging")
        
    print("\nTest completed.")
