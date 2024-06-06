]import os
from flask import Flask, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def remove_gps_data(file_path):
    # Use exiftool to remove GPS data
    subprocess.run(['exiftool', '-gps:all=', '-overwrite_original', file_path])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            remove_gps_data(filepath)

            return send_file(filepath, as_attachment=True, download_name=filename)
    return '''
    <!doctype html>
    <title>Picturewho</title>
    <h1>Upload the image you wanna do what you came here to do</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Define the application object for Gunicorn
application = app

if __name__ == '__main__':
    # Run the app using Gunicorn
    application.run(debug=True)
