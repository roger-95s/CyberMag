# backend/tests/test_app.py
import pytest
from . import app  # adjust import

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')  # or your main route
    assert response.status_code == 200