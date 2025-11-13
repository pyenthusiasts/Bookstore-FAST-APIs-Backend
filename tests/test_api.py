"""
Basic API tests.
"""

from fastapi import status


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"


def test_docs_available(client):
    """Test that API documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK


def test_redoc_available(client):
    """Test that ReDoc documentation is accessible."""
    response = client.get("/redoc")
    assert response.status_code == status.HTTP_200_OK
