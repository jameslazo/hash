import pytest
from src.main import app
import io


# Test client fixture to test the Flask app
@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    data = {
        'files': (io.BytesIO(b'test'), 'test.txt')
    }
    response = client.post('/', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'<h1>File Analyzer</h1>' in response.data
    assert b'</form>' in response.data
    assert b'</body>' in response.data
    assert b'</html>' in response.data
    assert b'<h2>Results</h2>' in response.data
    assert b'<th>File Name</th>' in response.data    
    assert b'<td>test.txt</td>' in response.data