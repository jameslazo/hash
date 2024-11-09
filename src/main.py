from flask import Flask, flash, request, render_template_string, redirect, url_for
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100000
app.secret_key = os.urandom(24)

uploaded_files_data = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    {% if files %}
        <table border="1">
            <tr>
                <th>File Name</th>
            </tr>
            {% for file in files %}
                <tr>
                    <td>{{ file['filename'] }}</td>
                </tr>
            {% endfor %}
        </table>
    {% endif %}
    
</body>
</html>
"""

# Define the home page
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        
        if not uploaded_files or all(file.filename == '' for file in uploaded_files):
            flash("No files selected.")
            return render_template_string(html_template, files=uploaded_files_data)
        
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                file.seek(0, 2) 
                if file.tell() > 0:  
                    filename = secure_filename(file.filename)
                    file_data = {'filename': filename}
                    uploaded_files_data.append(file_data)
                else:
                    flash(f"{file.filename} is empty and will not be analyzed.")
                file.seek(0)  
            else:
                flash(f"{file.filename} is not a valid file type.")

    return render_template_string(html_template, files=uploaded_files_data)


@app.route('/clear', methods=['GET'])
def clear_results():
    uploaded_files_data.clear()
    flash("Results cleared.")
    return redirect(url_for('upload_file'))


if __name__ == '__main__':
    app.run(debug=True)