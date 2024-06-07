import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from chats.models import Message, User_Conversation


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
def test_user(db):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(
        username="testuser", password="password123", email="test_user@example.com"
    )

    return test_user


@pytest.fixture
def refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh)


@pytest.fixture
def access_token_user(user):
    refresh = AccessToken.for_user(user)
    return str(refresh)


@pytest.fixture
def access_token_testuser(test_user):
    refresh = AccessToken.for_user(test_user)
    return str(refresh)


@pytest.fixture
def load_messages(user, test_user):

    user_conv = User_Conversation.objects.create(
        name=f"{user}_{test_user}", from_user=user, to_user=test_user
    )

    Message.objects.create(
        from_user=user,
        to_user=test_user,
        content="Hello World!",
        conversation_user=user_conv,
    )
