from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

# Shared counter
counter = {"value": 0}
counter_safe = {"value": 0}

# Lock for thread-safe operations
counter_lock = threading.Lock()

@app.route('/')
def home():
    return jsonify({
        "message": "Distributed Counter API",
        "endpoints": {
            "/increment": "Increment without lock (unsafe)",
            "/increment-safe": "Increment with lock (safe)",
            "/reset": "Reset both counters",
            "/status": "Get current counter values"
        }
    })

@app.route('/increment', methods=['POST'])
def increment_unsafe():
    """Increment WITHOUT lock - demonstrates lost updates"""
    global counter
    
    # Read current value
    current = counter["value"]
    
    # Simulate some processing delay (makes race condition more visible)
    time.sleep(0.001)
    
    # Write back incremented value
    counter["value"] = current + 1
    
    return jsonify({
        "counter": counter["value"],
        "safe": False
    })

@app.route('/increment-safe', methods=['POST'])
def increment_safe():
    """Increment WITH lock - thread-safe"""
    global counter_safe
    
    with counter_lock:
        # Read current value
        current = counter_safe["value"]
        
        # Simulate some processing delay
        time.sleep(0.001)
        
        # Write back incremented value
        counter_safe["value"] = current + 1
        result = counter_safe["value"]
    
    return jsonify({
        "counter": result,
        "safe": True
    })

@app.route('/reset', methods=['POST'])
def reset():
    """Reset both counters to zero"""
    global counter, counter_safe
    counter["value"] = 0
    counter_safe["value"] = 0
    
    return jsonify({
        "message": "Counters reset",
        "unsafe_counter": 0,
        "safe_counter": 0
    })

@app.route('/status', methods=['GET'])
def status():
    """Get current status of both counters"""
    return jsonify({
        "unsafe_counter": counter["value"],
        "safe_counter": counter_safe["value"]
    })

if __name__ == '__main__':
    print("🚀 Starting Distributed Counter Server...")
    print("📊 Endpoints:")
    print("   - POST /increment (unsafe)")
    print("   - POST /increment-safe (safe)")
    print("   - POST /reset")
    print("   - GET /status")
    print("\n✅ Server running on http://localhost:5000\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)