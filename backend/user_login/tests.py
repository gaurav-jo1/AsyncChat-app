import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_user_login(client):
    user_model = get_user_model()

    # Create a user with username, email, and password
    user = user_model.objects.create_user(
        username="user1", password="password123", email="user1@example.com"
    )
    assert user.username == "user1"

    url = reverse("token_obtain_pair")

    # Test with valid username and password
    data = {"username": "user1", "password": "password123"}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data["tokens"]
    assert "refresh" in response.data["tokens"]

    # Test with valid email and password
    data = {"email": "user1@example.com", "password": "password123"}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data["tokens"]
    assert "refresh" in response.data["tokens"]

    # Test with username and no password
    data = {"username": "user1", "password": ""}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "password" in response.data["error"]

    # Test with email and no password
    data = {"email": "user1@example.com", "password": ""}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "password" in response.data["error"]

    # Test with non-existent username
    data = {"username": "nonexistentuser", "password": "password123"}
    response = client.post(url, data, format="json")
    assert "Invalid credentials" in response.data["error"]
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Test with non-existent email
    data = {"email": "nonexistent@example.com", "password": "password123"}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid credentials" in response.data["error"]

@pytest.fixture
def refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh)

def test_token_refresh(client, refresh_token):
    url = reverse("token_refresh")
    data = {"refresh": refresh_token}

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data