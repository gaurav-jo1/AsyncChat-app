import pytest
from rest_framework import status
from user_profile.models import User_profile
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
def test_get_users():
    user_model = get_user_model()
    usernames = ["test_user", "test_user1", "test_user2", "John"]

    # Create test users and their profiles
    for username in usernames:
        user = user_model.objects.create_user(
            username=username, password="password123", email=f"{username}@example.com"
        )
        User_profile.objects.create(user=user)

    main_user = user_model.objects.get(username="John")

    assert main_user.username == "John"

    access_token = AccessToken.for_user(user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + str(access_token))

    url = reverse("Get_users_list")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 3

    expected_usernames = ["test_user", "test_user1", "test_user2"]
    for user_data in response.data:
        assert user_data["username"] in expected_usernames
        assert user_data["email"] == f"{user_data['username']}@example.com"
        assert user_data["avatar"] is None
