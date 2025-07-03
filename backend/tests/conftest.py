"""# backend/tests/conftest.py
# This file sets up the test environment for the Flask application"""

from backend.app import app as flask_app
from backend.models import Base, engine
import pytest


@pytest.fixture(scope="module")
def client():
    # Set up the DB schema (e.g., create reports table)
    Base.metadata.create_all(bind=engine)

    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

    # Teardown after test run
    Base.metadata.drop_all(bind=engine)
