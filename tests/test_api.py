"""
Basic API tests for health and authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200


def test_docs_endpoint():
    """Test that API docs are accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_invalid_endpoint():
    """Test that invalid endpoints return 404."""
    response = client.get("/this-does-not-exist")
    assert response.status_code == 404


# Add more tests as needed:
# - def test_signup()
# - def test_login()
# - def test_create_api_key()
# - def test_chat_without_auth()
# - def test_ingest_without_auth()
