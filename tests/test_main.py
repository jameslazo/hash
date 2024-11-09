import pytest
from src.main import app
import io


# Test client fixture to test the Flask app
@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


def test_get_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1>File Analyzer</h1>' in response.data
    assert b'input type="file"' in response.data
    assert b'input type="submit' in response.data
    assert b'<h2>Results</h2>' in response.data


def test_post_home(client):
    data = {
        'files': (io.BytesIO(b'test'), 'test.txt')
    }
    response = client.post('/', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'<th>File Name</th>' in response.data    
    assert b'<td>test.txt</td>' in response.data


def test_post_clear_files(client):
    data = {
        'files': (io.BytesIO(b'test'), 'test.txt')
    }
    response = client.post('/', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'<th>File Name</th>' in response.data    
    assert b'<td>test.txt</td>' in response.data
    response = client.get('/clear', follow_redirects=True)
    assert b'<td>test.txt</td>' not in response.data


def test_upload_multiple_files(client):
    data = {
        'files': [
            (io.BytesIO(b"file1 content"), 'file1.txt'),
            (io.BytesIO(b"file2 content"), 'file2.txt')
        ]
    }
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert b'file1.txt' in response.data 
    assert b'file2.txt' in response.data
    data = {}


def test_empty_file_upload(client):
    data = {
        'files': (io.BytesIO(b""), 'empty.txt') 
    }
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert b'is empty and will not be analyzed' in response.data
    data = {}


def test_large_file_upload(client):
    large_file = b"A" * (5*10**6)
    data = {
        'files': (io.BytesIO(large_file), 'large.txt')
    }
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert b'Request Entity Too Large' in response.data
    data = {}


def test_invalid_file_type(client):
    data = {
        'files': (io.BytesIO(b"img data"), 'test.jpg')
    }
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert b'is not a valid file type' in response.data
    data = {}


def test_no_file_selected(client):
    response = client.post('/', data={}, content_type='multipart/form-data')
    assert b'No files selected' in response.data

