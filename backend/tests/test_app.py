"""Module providing a function printing python version."""

# backend/tests/test_app.py
from flask.testing import FlaskClient


def test_health_check(client: FlaskClient):
    response = client.get("/post")  # or your main route
    assert response.status_code == 200
