import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.store import clear_store


@pytest.fixture(autouse=True)
def reset_store():
    """Reset the in-memory store before and after each test."""
    clear_store()
    yield
    clear_store()


@pytest.fixture
def client():
    """Provide a fresh TestClient for each test."""
    return TestClient(app)
