from flask import (Flask, render_template, request, send_from_directory,
                   redirect, url_for, flash)
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)

# Needed for flash() messages. In real deployment, set it as an environment variable.
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',
                      'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def unique_filename(filename):
    """report.pdf -> report_1.pdf -> report_2.pdf if names already exist."""
    name, ext = os.path.splitext(filename)
    candidate = filename
    counter = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], candidate)):
        candidate = f"{name}_{counter}{ext}"
        counter += 1
    return candidate


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # Opening /upload directly in the browser (GET) just goes back home
    if request.method == 'GET':
        return redirect(url_for('home'))

    file = request.files.get('file')

    if file is None or file.filename == '':
        flash('No file selected.')
        return redirect(url_for('home'))

    if not allowed_file(file.filename):
        flash('This file type is not allowed.')
        return redirect(url_for('home'))

    filename = secure_filename(file.filename)
    if filename == '':
        flash('Invalid file name.')
        return redirect(url_for('home'))

    filename = unique_filename(filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash(f'"{filename}" uploaded successfully.')
    return redirect(url_for('view_files'))


@app.errorhandler(413)
def file_too_large(e):
    flash('File is too large. Maximum size is 16 MB.')
    return redirect(url_for('home'))


@app.route('/files')
def view_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(path):
            size = round(os.path.getsize(path) / 1024, 2)  # KB
            upload_time = datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y-%m-%d %H:%M:%S")
            files.append({'name': filename, 'size': size, 'time': upload_time})
    files.sort(key=lambda f: f['time'], reverse=True)  # newest first
    return render_template('files.html', files=files)


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filename = secure_filename(filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        os.remove(path)
        flash(f'"{filename}" deleted.')
    else:
        flash('File not found.')
    return redirect(url_for('view_files'))


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')