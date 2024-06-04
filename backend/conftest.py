import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    def get_authenticated_client(username):
        user_model = get_user_model()
        user = user_model.objects.create_user(username=username, password="password123")
        client = APIClient()
        client.login(username=username, password="password123")
        return client, user

    return get_authenticated_client
