from flask import render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
import os
import tempfile
from myflaskapp import app  # Notice how we're importing app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    data_frame = None  # Start with no DataFrame
    if request.method == 'POST':
        # check if the post request has the file part
        if 'csv_file' in request.files:
            file = request.files['csv_file']
            if file.filename == '':
                print('No file selected for uploading')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                with tempfile.TemporaryDirectory() as tmpdirname:
                    filepath = os.path.join(tmpdirname, filename)
                    file.save(filepath)
                    df = pd.read_csv(filepath) # Read the CSV data
                    data_frame = df.head(10).to_html()  # Convert the DataFrame to HTML here
                    # After reading, the temporary directory and all its contents are automatically removed
    return render_template('index.html', data_frame=data_frame)
