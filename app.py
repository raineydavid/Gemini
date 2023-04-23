from flask import Flask, render_template, request, jsonify
import webview
from threading import Thread
import pandas as pd
import embedding  # Import the embedding module

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    # Check if 'query' parameter is present in the request form
    if 'query' not in request.form:
        return jsonify({'error': 'Missing query parameter'}), 400

    query = request.form['query']
    
    # Load the DataFrame from a CSV
    df = pd.read_csv('memories.csv')
    
    # Get the response from the model
    response = embedding.ask(query, df, clear_messages=False, self_aware=False)
    
    # Check if response is valid
    if not response:
        return jsonify({'error': 'Failed to generate response'}), 400

    return jsonify({'response': response})


def run_flask_app():
    app.run(debug=False, threaded=True)  # Set debug=False and threaded=True

if __name__ == '__main__':
    print('Starting Flask app...')
    t = Thread(target=run_flask_app)
    t.start()

    # Open the webview window
    webview.create_window('Ask Gemini', 'http://127.0.0.1:5000/')
    webview.start()
