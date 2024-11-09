import pytest
from src.main import app


# Test client fixture to test the Flask app
@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h1>File Analyzer</h1>' in response.data
    assert b'</form>' in response.data
    assert b'</body>' in response.data
    assert b'</html>' in response.data
    post = client.post('/', data={'files': 'test.txt'})
    assert post.status_code == 200