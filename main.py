import os
from modules import learn, discover, contribute
from chatbot import bot
from flask import Flask, render_template, send_from_directory, jsonify
import json

# Create Flask app and set folders
app = Flask(__name__, static_folder='web', template_folder='web')

# --- Flask Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Fetch events dynamically
@app.route('/api/events')
def get_events():
    data_path = os.path.join('data', 'events.json')
    with open(data_path, 'r') as f:
        events = json.load(f)
    return jsonify(events)

# Fetch assets dynamically
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)


# --- CLI Menu Logic ---
def main_menu():
    while True:
        print("\n================================")
        print("   Welcome to the FlowRoots App")
        print("================================")
        print("Please choose an option:")
        print("1. Learn about styles or history")
        print("2. Discover events, crews, or music")
        print("3. Contribute or share content")
        print("4. Chat with the AI Assistant")
        print("5. Exit")
        
        choice = input("> ").strip()
        
        if choice == "1":
            learn.menu()
        elif choice == "2":
            discover.menu()
        elif choice == "3":
            contribute.menu()
        elif choice == "4":
            bot.chat()
        elif choice == "5":
            print("Thanks for using FlowRoots! Goodbye 👋")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 5.")


# --- Entry Point ---
if __name__ == "__main__":
    print("Select mode:")
    print("1. Run Web App (Flask)")
    print("2. Run Command-Line Menu")
    mode = input("> ").strip()

    if mode == "1":
        print("Starting FlowRoots website at http://localhost:5000 ...")
        app.run(debug=True)
    elif mode == "2":
        main_menu()
    else:
        print("Invalid selection. Exiting.")