from flask import Flask

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
    <form action="/analyze" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".txt">
        <input type="submit" value="Analyze">
    </form>
</body>
</html>
"""

# Define the home page
@app.route('/')
def home():
    return html_template

if __name__ == '__main__':
    app.run(debug=True)