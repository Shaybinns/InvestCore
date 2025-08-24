from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Enable CORS for app integration

# Simple configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# ============================================================================
# ESSENTIAL API ENDPOINTS FOR APP INTEGRATION
# ============================================================================

@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "InvestCore API",
        "version": "1.0.0"
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    """Main chat endpoint - handles natural language requests"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_id = data.get("user_id")
        message = data.get("message")

        if not user_id or not message:
            return jsonify({"error": "Missing user_id or message"}), 400

        # Import brain here to avoid circular imports
        try:
            from brain import handle_user_message
            response_data = handle_user_message(user_id, message)
        except ImportError as e:
            return jsonify({
                "error": f"Brain module not available: {str(e)}",
                "success": False
            }), 500
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "initial_response": response_data.get("initial_response"),
            "command_result": response_data.get("command_result"),
            "command_executed": response_data.get("command_executed", False),
            "status": response_data.get("status"),
            "command_name": response_data.get("command_name"),
            "goal": response_data.get("goal"),
            "missing_fields": response_data.get("missing_fields"),
            "has_more_steps": response_data.get("has_more_steps"),
            "error": response_data.get("error")
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}",
            "success": False
        }), 500

@app.route("/api/asset/<symbol>", methods=["GET"])
def get_asset_info(symbol: str):
    """Get detailed information about a specific asset"""
    try:
        from commands.get_asset_info import run
        
        result = run({"symbol": symbol.upper()})
        
        return jsonify({
            "success": True,
            "symbol": symbol.upper(),
            "data": result
        })
        
    except ImportError as e:
        return jsonify({
            "error": f"Asset info module not available: {str(e)}",
            "success": False
        }), 500
    except Exception as e:
        return jsonify({
            "error": f"Failed to get asset info for {symbol}: {str(e)}",
            "success": False
        }), 500

@app.route("/api/screen", methods=["POST"])
def screen_assets():
    """Screen assets based on provided filters"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        filters = data.get("filters", [])
        user_description = data.get("description", "")
        
        if not filters and not user_description:
            return jsonify({"error": "Either filters or description must be provided"}), 400
        
        try:
            from commands.screen_assets import run
            
            if user_description:
                # Parse natural language to filters
                from commands.screen_assets import parse_user_input_to_filters
                filters = parse_user_input_to_filters(user_description)
            
            result = run({"filters": filters})
        except ImportError as e:
            return jsonify({
                "error": f"Screen assets module not available: {str(e)}",
                "success": False
            }), 500
        
        return jsonify({
            "success": True,
            "filters": filters,
            "results": result
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to screen assets: {str(e)}",
            "success": False
        }), 500

@app.route("/api/market/assess", methods=["POST"])
def assess_market():
    """Assess current market conditions"""
    try:
        data = request.get_json() or {}
        
        try:
            from commands.market_assess import run
            result = run(data)
        except ImportError as e:
            return jsonify({
                "error": f"Market assess module not available: {str(e)}",
                "success": False
            }), 500
        
        return jsonify({
            "success": True,
            "assessment": result
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to assess market: {str(e)}",
            "success": False
        }), 500

@app.route("/api/sector/assess", methods=["POST"])
def assess_sector():
    """Assess specific sector performance"""
    try:
        data = request.get_json() or {}
        sector = data.get("sector")
        
        if not sector:
            return jsonify({"error": "Sector parameter is required"}), 400
            
        try:
            from commands.sector_assess import run
            result = run({"sector": sector})
        except ImportError as e:
            return jsonify({
                "error": f"Sector assess module not available: {str(e)}",
                "success": False
            }), 500
        
        return jsonify({
            "success": True,
            "sector": sector,
            "assessment": result
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to assess sector: {str(e)}",
            "success": False
        }), 500

@app.route("/api/asset/assess", methods=["POST"])
def assess_asset():
    """Assess specific asset performance and metrics"""
    try:
        data = request.get_json() or {}
        symbol = data.get("symbol")
        
        if not symbol:
            return jsonify({"error": "Symbol parameter is required"}), 400
            
        try:
            from commands.asset_assess import run
            result = run({"symbol": symbol})
        except ImportError as e:
            return jsonify({
                "error": f"Asset assess module not available: {str(e)}",
                "success": False
            }), 500
        
        return jsonify({
            "success": True,
            "symbol": symbol,
            "assessment": result
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to assess asset: {str(e)}",
            "success": False
        }), 500

@app.route("/api/financials/<symbol>", methods=["GET"])
def get_financials(symbol: str):
    """Get financial data for a specific asset"""
    try:
        try:
            from commands.get_financials import run
            result = run({"symbol": symbol.upper()})
        except ImportError as e:
            return jsonify({
                "error": f"Financials module not available: {str(e)}",
                "success": False
            }), 500
        
        return jsonify({
            "success": True,
            "symbol": symbol.upper(),
            "financials": result
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get financials for {symbol}: {str(e)}",
            "success": False
        }), 500

@app.route("/api/earnings/<symbol>", methods=["GET"])
def get_earnings(symbol: str):
    """Get earnings data for a specific asset"""
    try:
        try:
            from commands.get_earnings import run
            result = run({"symbol": symbol.upper()})
        except ImportError as e:
            return jsonify({
                "error": f"Earnings module not available: {str(e)}",
                "success": False
            }), 500
        
        return jsonify({
            "success": True,
            "symbol": symbol.upper(),
            "earnings": result
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get earnings for {symbol}: {str(e)}",
            "success": False
        }), 500

@app.route("/api/macros", methods=["GET"])
def get_macros():
    """Get macroeconomic data and indicators"""
    try:
        try:
            from commands.get_macros import run
            result = run({})
        except ImportError as e:
            return jsonify({
                "error": f"Macros module not available: {str(e)}",
                "success": False
            }), 500
        
        return jsonify({
            "success": True,
            "macro_data": result
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get macro data: {str(e)}",
            "success": False
        }), 500

@app.route("/api/search/web", methods=["POST"])
def search_web():
    """Search the web for financial information"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        query = data.get("query")
        
        if not query:
            return jsonify({"error": "Query parameter is required"}), 400
            
        try:
            from commands.search_web import run
            result = run({"query": query})
        except ImportError as e:
            return jsonify({
                "error": f"Web search module not available: {str(e)}",
                "success": False
            }), 500
        
        return jsonify({
            "success": True,
            "query": query,
            "results": result
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to search web: {str(e)}",
            "success": False
        }), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "success": False,
        "available_endpoints": [
            "/api/health",
            "/api/chat",
            "/api/asset/<symbol>",
            "/api/screen",
            "/api/market/assess",
            "/api/sector/assess",
            "/api/asset/assess",
            "/api/financials/<symbol>",
            "/api/earnings/<symbol>",
            "/api/macros",
            "/api/search/web"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "success": False
    }), 500

# ============================================================================
# MAIN APPLICATION
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"🚀 Starting InvestCore API on {host}:{port}")
    print(f"📱 App endpoints available at http://{host}:{port}/api/")
    print(f"🔍 Health check at http://{host}:{port}/api/health")
    print(f"🌍 Railway deployment ready!")
    
    app.run(host=host, port=port, debug=False)
