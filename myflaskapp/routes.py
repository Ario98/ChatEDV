from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import os
import tempfile
from myflaskapp import app  # Notice how we're importing app
import requests

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

from io import StringIO

@app.route('/upload', methods=['POST'])
def upload():
    if 'csv_file' in request.files:
        file = request.files['csv_file']
        if file and allowed_file(file.filename):
            # Read the CSV data and create DataFrame
            data_frame = pd.read_csv(file)

            #print(data_frame.head()) - works

            # Return the DataFrame data as JSON response
            return jsonify(data_frame=data_frame.head().to_dict())

    # Return an empty response if the file upload fails
    return jsonify(data_frame={})



@app.route('/chat', methods=['POST'])
def chat():
    bot_response = None  # Initialize the bot_response variable

    # Get user input from the form
    user_input = request.form['user_input']

    # Make API call to ChatGPT
    api_url = 'https://api.openai.com/v1/chat/completions'
    response = requests.post(api_url, json={
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': user_input}],
        'max_tokens': 100,
        'temperature': 0.7,
        'model': 'gpt-3.5-turbo'
    }, headers={
        'Authorization': 'Bearer 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'
    })

    if response.status_code == 200:
        bot_response = response.json()['choices'][0]['message']['content']
    else:
        bot_response = 'Error: Unable to process the request'

    # Return the bot response as JSON response
    return jsonify(bot_response=bot_response)



