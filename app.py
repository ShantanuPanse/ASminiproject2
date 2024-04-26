from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.exceptions import RequestEntityTooLarge  # Import exception for 413 error

app = Flask(__name__)

# Define a limit for the file size (5 MB in bytes)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

ALLOWED_EXTENSIONS = {'docx', 'pdf'}

def allowed_file(filename):
    # Check if the file has one of the allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:  # Check if there's a file in the request
            return redirect(url_for('failure'))
        
        file = request.files['file']

        if file.filename == '':  # Check if the filename is empty
            return redirect(url_for('failure'))

        if file and allowed_file(file.filename):
            # If the file has a valid extension and is within size limit
            if request.content_length <= app.config['MAX_CONTENT_LENGTH']:
                return redirect(url_for('success'))
            else:
                return redirect(url_for('failure'))
        else:
            return redirect(url_for('failure'))

    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

# Custom error handler for 413 Request Entity Too Large
@app.errorhandler(RequestEntityTooLarge)
def handle_large_file_error(e):
    # Redirect to failure page with custom message or additional info
    return redirect(url_for('failure'))

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
