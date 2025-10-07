#!/usr/bin/env python3
"""
Simple script to update user long-term information in InvestCore
Usage: python update_user_info.py
"""

import json
from memory.long_term_db import (
    create_user_profile,
    update_portfolio_holdings,
    update_portfolio_performance,
    add_user_transaction,
    update_user_goals,
    update_user_pathway,
    get_user_data_summary
)

def print_template():
    """Print the template format for user data"""
    print("\n" + "="*60)
    print("USER DATA UPDATE TEMPLATE")
    print("="*60)
    
    print("\n1. USER PROFILE DATA:")
    profile_template = {
        "risk_tolerance": "conservative | moderate | aggressive",
        "investment_goal": "retirement | wealth_building | income_generation | education | other",
        "asset_preferences": {
            "stocks": "percentage (0-100)",
            "bonds": "percentage (0-100)", 
            "etfs": "percentage (0-100)",
            "crypto": "percentage (0-100)",
            "real_estate": "percentage (0-100)"
        },
        "industry_preferences": {
            "technology": "high | medium | low | none",
            "healthcare": "high | medium | low | none",
            "finance": "high | medium | low | none",
            "energy": "high | medium | low | none",
            "consumer": "high | medium | low | none"
        },
        "investment_style": "value | growth | dividend | index | active | passive"
    }
    print(json.dumps(profile_template, indent=2))
    
    print("\n2. PORTFOLIO HOLDINGS:")
    holdings_template = {
        "AAPL": {"shares": 100, "avg_cost": 150.00},
        "MSFT": {"shares": 50, "avg_cost": 300.00},
        "VTI": {"shares": 200, "avg_cost": 220.00}
    }
    print(json.dumps(holdings_template, indent=2))
    
    print("\n3. PORTFOLIO PERFORMANCE:")
    performance_template = {
        "total_value": 50000.00,
        "total_cost": 45000.00,
        "total_return": 5000.00,
        "return_percentage": 11.11,
        "ytd_return": 8.5,
        "monthly_return": 2.1
    }
    print(json.dumps(performance_template, indent=2))
    
    print("\n4. TRANSACTION:")
    transaction_template = {
        "type": "buy | sell | dividend | split",
        "symbol": "AAPL",
        "shares": 10,
        "price": 150.00,
        "total": 1500.00,
        "date": "2024-01-15",
        "notes": "Added to position"
    }
    print(json.dumps(transaction_template, indent=2))
    
    print("\n5. INVESTMENT GOALS:")
    goals_template = {
        "short_term": {
            "target_amount": 10000,
            "timeframe": "1 year",
            "description": "Emergency fund"
        },
        "medium_term": {
            "target_amount": 50000,
            "timeframe": "5 years", 
            "description": "House down payment"
        },
        "long_term": {
            "target_amount": 1000000,
            "timeframe": "20 years",
            "description": "Retirement fund"
        }
    }
    print(json.dumps(goals_template, indent=2))
    
    print("\n6. INVESTMENT PATHWAY:")
    pathway_template = {
        "strategy": "dollar_cost_averaging | lump_sum | rebalancing",
        "frequency": "monthly | quarterly | annually",
        "target_allocation": {
            "stocks": 70,
            "bonds": 20,
            "cash": 10
        },
        "rebalancing_threshold": 5,
        "notes": "Focus on growth stocks with dividend yield"
    }
    print(json.dumps(pathway_template, indent=2))
    
    print("\n" + "="*60)

def get_user_input():
    """Get user input for updating data"""
    print("\nEnter the USER ID to update:")
    user_id = input("User ID: ").strip()
    
    if not user_id:
        print("Error: User ID is required!")
        return None, None
    
    print("\nWhat would you like to update?")
    print("1. User Profile")
    print("2. Portfolio Holdings") 
    print("3. Portfolio Performance")
    print("4. Add Transaction")
    print("5. Investment Goals")
    print("6. Investment Pathway")
    print("7. View Current Data")
    
    choice = input("\nEnter choice (1-7): ").strip()
    
    return user_id, choice

def update_profile(user_id):
    """Update user profile"""
    print("\nEnter profile data (press Enter to skip fields):")
    
    risk_tolerance = input("Risk Tolerance (conservative/moderate/aggressive): ").strip()
    investment_goal = input("Investment Goal (retirement/wealth_building/income_generation/education/other): ").strip()
    investment_style = input("Investment Style (value/growth/dividend/index/active/passive): ").strip()
    
    # Asset preferences
    print("\nAsset Preferences (enter percentages 0-100):")
    asset_prefs = {}
    for asset in ["stocks", "bonds", "etfs", "crypto", "real_estate"]:
        value = input(f"{asset.capitalize()} (%): ").strip()
        if value:
            try:
                asset_prefs[asset] = float(value)
            except ValueError:
                print(f"Invalid percentage for {asset}, skipping...")
    
    # Industry preferences
    print("\nIndustry Preferences (high/medium/low/none):")
    industry_prefs = {}
    for industry in ["technology", "healthcare", "finance", "energy", "consumer"]:
        value = input(f"{industry.capitalize()}: ").strip()
        if value in ["high", "medium", "low", "none"]:
            industry_prefs[industry] = value
    
    profile_data = {
        "risk_tolerance": risk_tolerance if risk_tolerance else None,
        "investment_goal": investment_goal if investment_goal else None,
        "investment_style": investment_style if investment_style else None,
        "asset_preferences": asset_prefs if asset_prefs else {},
        "industry_preferences": industry_prefs if industry_prefs else {}
    }
    
    # Remove None values
    profile_data = {k: v for k, v in profile_data.items() if v is not None}
    
    if create_user_profile(user_id, profile_data):
        print("✅ Profile updated successfully!")
    else:
        print("❌ Failed to update profile!")

def update_holdings(user_id):
    """Update portfolio holdings"""
    print("\nEnter portfolio holdings (JSON format):")
    print("Example: {\"AAPL\": {\"shares\": 100, \"avg_cost\": 150.00}}")
    
    holdings_input = input("Holdings JSON: ").strip()
    
    if not holdings_input:
        print("No holdings data provided!")
        return
    
    try:
        holdings = json.loads(holdings_input)
        if update_portfolio_holdings(user_id, holdings):
            print("✅ Portfolio holdings updated successfully!")
        else:
            print("❌ Failed to update portfolio holdings!")
    except json.JSONDecodeError:
        print("❌ Invalid JSON format!")

def update_performance(user_id):
    """Update portfolio performance"""
    print("\nEnter portfolio performance (JSON format):")
    print("Example: {\"total_value\": 50000.00, \"total_return\": 5000.00}")
    
    performance_input = input("Performance JSON: ").strip()
    
    if not performance_input:
        print("No performance data provided!")
        return
    
    try:
        performance = json.loads(performance_input)
        if update_portfolio_performance(user_id, performance):
            print("✅ Portfolio performance updated successfully!")
        else:
            print("❌ Failed to update portfolio performance!")
    except json.JSONDecodeError:
        print("❌ Invalid JSON format!")

def add_transaction(user_id):
    """Add a transaction"""
    print("\nEnter transaction data (JSON format):")
    print("Example: {\"type\": \"buy\", \"symbol\": \"AAPL\", \"shares\": 10, \"price\": 150.00}")
    
    transaction_input = input("Transaction JSON: ").strip()
    
    if not transaction_input:
        print("No transaction data provided!")
        return
    
    try:
        transaction = json.loads(transaction_input)
        if add_user_transaction(user_id, transaction):
            print("✅ Transaction added successfully!")
        else:
            print("❌ Failed to add transaction!")
    except json.JSONDecodeError:
        print("❌ Invalid JSON format!")

def update_goals(user_id):
    """Update investment goals"""
    print("\nEnter investment goals (JSON format):")
    print("Example: {\"short_term\": {\"target_amount\": 10000, \"timeframe\": \"1 year\"}}")
    
    goals_input = input("Goals JSON: ").strip()
    
    if not goals_input:
        print("No goals data provided!")
        return
    
    try:
        goals = json.loads(goals_input)
        if update_user_goals(user_id, goals):
            print("✅ Investment goals updated successfully!")
        else:
            print("❌ Failed to update investment goals!")
    except json.JSONDecodeError:
        print("❌ Invalid JSON format!")

def update_pathway(user_id):
    """Update investment pathway"""
    print("\nEnter investment pathway (JSON format):")
    print("Example: {\"strategy\": \"dollar_cost_averaging\", \"frequency\": \"monthly\"}")
    
    pathway_input = input("Pathway JSON: ").strip()
    
    if not pathway_input:
        print("No pathway data provided!")
        return
    
    try:
        pathway = json.loads(pathway_input)
        if update_user_pathway(user_id, pathway):
            print("✅ Investment pathway updated successfully!")
        else:
            print("❌ Failed to update investment pathway!")
    except json.JSONDecodeError:
        print("❌ Invalid JSON format!")

def view_current_data(user_id):
    """View current user data"""
    print(f"\n📊 Current data for user: {user_id}")
    print("-" * 50)
    
    summary = get_user_data_summary(user_id)
    
    if summary.get("status") == "no_data":
        print("❌ No data found for this user!")
        return
    
    print(f"Status: {summary.get('status', 'unknown')}")
    print(f"Profile Completeness: {summary.get('profile_completeness', '0%')}")
    print(f"Created: {summary.get('created_at', 'unknown')}")
    print(f"Has Portfolio: {'Yes' if summary.get('has_portfolio') else 'No'}")
    print(f"Transaction Count: {summary.get('transaction_count', 0)}")
    print(f"Has Goals: {'Yes' if summary.get('has_goals') else 'No'}")
    print(f"Has Pathway: {'Yes' if summary.get('has_pathway') else 'No'}")
    
    if summary.get('risk_tolerance'):
        print(f"Risk Tolerance: {summary['risk_tolerance']}")
    if summary.get('investment_goal'):
        print(f"Investment Goal: {summary['investment_goal']}")
    if summary.get('investment_style'):
        print(f"Investment Style: {summary['investment_style']}")

def main():
    """Main function"""
    print("🚀 InvestCore User Data Updater")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Show template format")
        print("2. Update user data")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            print_template()
        elif choice == "2":
            user_id, update_choice = get_user_input()
            
            if not user_id:
                continue
                
            if update_choice == "1":
                update_profile(user_id)
            elif update_choice == "2":
                update_holdings(user_id)
            elif update_choice == "3":
                update_performance(user_id)
            elif update_choice == "4":
                add_transaction(user_id)
            elif update_choice == "5":
                update_goals(user_id)
            elif update_choice == "6":
                update_pathway(user_id)
            elif update_choice == "7":
                view_current_data(user_id)
            else:
                print("❌ Invalid choice!")
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
