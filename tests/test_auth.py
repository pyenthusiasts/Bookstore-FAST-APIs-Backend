"""
Authentication tests.
"""

from fastapi import status


def test_register_user(client, test_user_data):
    """Test user registration."""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_user(client, test_user_data):
    """Test that registering a duplicate user fails."""
    # Register first user
    client.post("/api/v1/auth/register", json=test_user_data)
    # Try to register again
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client, test_user_data):
    """Test successful login."""
    # Register user first
    client.post("/api/v1/auth/register", json=test_user_data)
    # Login
    response = client.post(
        "/api/v1/auth/token",
        data={"username": test_user_data["username"], "password": test_user_data["password"]},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user_data):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/token",
        data={"username": test_user_data["username"], "password": "wrongpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, test_user_data):
    """Test getting current user information."""
    # Register and login
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/v1/auth/token",
        data={"username": test_user_data["username"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]

    # Get current user
    response = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == test_user_data["username"]


def test_unauthorized_access(client):
    """Test that accessing protected endpoints without token fails."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
