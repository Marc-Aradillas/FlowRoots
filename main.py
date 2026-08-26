import os
import json
from flask import Flask, render_template, send_from_directory, jsonify, request

# Create Flask app and set static/template folders
app = Flask(__name__, static_folder='web', template_folder='web')

# --- Flask Routes ---
@app.route('/')
def home():
    return render_template('index.html')

# Fetch events dynamically
@app.route('/api/events')
def get_events():
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, 'data', 'events.json')
    
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            events = json.load(f)
        return jsonify(events)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty list with 200 status code so frontend loads cleanly
        return jsonify([]), 200

# Serve assets dynamically
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

# Explicitly serve JS, CSS, and root images without catching HTML requests
@app.route('/<filename>.css')
@app.route('/<filename>.js')
@app.route('/<filename>.png')
@app.route('/<filename>.jpg')
def static_files(filename):
    # Extracts extension dynamically
    ext = request.path.split('.')[-1]
    return send_from_directory(app.static_folder, f"{filename}.{ext}")

# --- Web Server Entry Point ---
if __name__ == "__main__":
    print("Starting FlowRoots website at http://localhost:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)