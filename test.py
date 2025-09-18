import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_app_is_working(client):
    """Check root route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello World!" in response.data


def test_not_found_page(client):
    """Check 404 response for invalid route"""
    response = client.get('/does-not-exist')
    assert response.status_code == 404


def test_post_request(client):
    """Check POST route (if supported)"""
    response = client.post('/', data={"key": "value"})
    # Adjust expected status based on your app's behavior
    assert response.status_code in [200, 405]


def test_json_response(client):
    """Check if an API route returns JSON (example: /api/hello)"""
    response = client.get('/api/hello')
    if response.status_code == 200:
        json_data = response.get_json()
        assert "message" in json_data
        assert json_data["message"] == "Hello from API"


def test_headers(client):
    """Check headers returned by the app"""
    response = client.get('/')
    assert "Content-Type" in response.headers
    assert "text" in response.headers["Content-Type"]

