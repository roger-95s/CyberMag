"""Module providing a function printing python version."""

# backend/tests/test_app.py
from flask.testing import FlaskClient
import pytest
from backend.app import app  # adjust import


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client: FlaskClient):
    response = client.get("/api/reports")  # or your main route
    assert response.status_code == 200
