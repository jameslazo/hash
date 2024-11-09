from flask import Flask, request, render_template_string

app = Flask(__name__)

# Hash app HTML
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>File Analyzer</title>
</head>
<body>
    <h1>File Analyzer</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="files" accept=".txt" multiple>
        <input type="submit" value="Analyze">
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
def home():
    files = []
    if request.method == 'POST':
        uploaded_files = request.files.getlist("files")
        for file in uploaded_files:
            file_data = {"filename": file.filename}
            files.append(file_data)

    return render_template_string(html_template, files=files)

if __name__ == '__main__':
    app.run(debug=True)