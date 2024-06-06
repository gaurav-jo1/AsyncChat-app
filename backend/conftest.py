import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user(db):
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username="user1", password="password123", email="user1@example.com"
    )
    return user

@pytest.fixture
def refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh)

@pytest.fixture
def access_token(user):
    refresh = AccessToken.for_user(user)
    return str(refresh)