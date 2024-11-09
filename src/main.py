from flask import Flask, flash, request, render_template_string, redirect, url_for
import os
from werkzeug.utils import secure_filename
import hashlib


ALLOWED_EXTENSIONS = {'txt'}
MAX_FILES = 5

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100000
app.secret_key = os.urandom(24)

file_groups = {}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_file_hash(file_stream, hash_algo='sha256'):
    hash_func = hashlib.new(hash_algo)
    for chunk in iter(lambda: file_stream.read(4096), b""):
        hash_func.update(chunk)
    file_stream.seek(0)
    return hash_func.hexdigest()

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>File Analyzer</title>
</head>
<body>
    <h1>File Analyzer</h1>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="files" accept=".txt" multiple>
        <input type="submit" value="Analyze">
        <a href="{{ url_for('clear_results') }}">
            <button type="button">Clear Results</button>
        </a>
    </form>
    <hr>
    <h2>Results</h2>
    {% if file_groups %}
        <table border="1">
            <tr>
                <th>File Hash</th>
                <th>File Name</th>
                <th>File Size (bytes)</th>
            </tr>
            {% for file_hash, files in sorted_file_groups %}
                <tr>
                    <td rowspan="{{ files|length }}">{{ file_hash }}</td>
                    <td>{{ files[0]['filename'] }}</td>
                    <td>{{ files[0]['size'] }}</td>
                </tr>
                {% for file in files[1:] %}
                    <tr>
                        <td>{{ file['filename'] }}</td>
                        <td>{{ file['size'] }}</td>
                    </tr>
                {% endfor %}
            {% endfor %}
        </table>
    {% endif %}
    
</body>
</html>
"""

# Home page
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        
        if not uploaded_files or all(file.filename == '' for file in uploaded_files):
            flash("No files selected.")
            return render_template_string(html_template, file_groups=file_groups)
        
        if len(uploaded_files) > MAX_FILES:
            flash(f"Up to {MAX_FILES} files can be analyzed.")
            return render_template_string(html_template, file_groups=file_groups)
        
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(0)
                
                if file_size > 0:  
                    filename = secure_filename(file.filename)
                    file_hash = calculate_file_hash(file.stream)

                    if file_hash not in file_groups:
                        file_groups[file_hash] = []
                    file_groups[file_hash].append({
                        'filename': filename,
                        'size': file_size
                    })
                else:
                    flash(f"{file.filename} is empty and will not be analyzed.")
                file.seek(0)  
            else:
                flash(f"{file.filename} is not a valid file type.")
    
    sorted_file_groups = sorted(file_groups.items(), key=lambda x: len(x[1]), reverse=True)
    
    return render_template_string(html_template, file_groups=file_groups, sorted_file_groups=sorted_file_groups)


# Clear results
@app.route('/clear', methods=['GET'])
def clear_results():
    file_groups.clear()
    flash("Results cleared.")
    return redirect(url_for('upload_file'))


if __name__ == '__main__':
    app.run(debug=True)