import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_activity():
    return {
        "name": "Test Club",
        "details": {
            "description": "A test activity for unit testing",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 10,
            "participants": []
        }
    }