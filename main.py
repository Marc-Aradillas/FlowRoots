import os
import json
from flask import Flask, render_template, send_from_directory, jsonify

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
        with open(data_path, 'r') as f:
            events = json.load(f)
        return jsonify(events)
    except FileNotFoundError:
        return jsonify({"error": "Events file not found"}), 404

# Serve assets dynamically
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

# Catch-all for static web files (index.html, JS, CSS)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# --- Web Server Entry Point ---
if __name__ == "__main__":
    print("Starting FlowRoots website at http://localhost:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)