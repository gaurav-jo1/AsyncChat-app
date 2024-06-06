import pytest
import json
from django.contrib.auth import get_user_model
from chats.consumers import UserChatConsumer
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from channels.routing import ProtocolTypeRouter, URLRouter
from chats.middleware import JWTAuthMiddleware
from chats.routing import websocket_urlpatterns


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_consumer(user, access_token):

    UserModel = get_user_model()

    # Create a user with username, email, and password
    test_user = await database_sync_to_async(UserModel.objects.create_user)(
        username="testuser", password="password123", email="testuser@example.com"
    )

    assert test_user.username == "testuser"

    # Create the WebSocket communicator with the entire application including middleware
    websocket_application = ProtocolTypeRouter(
        {"websocket": JWTAuthMiddleware(URLRouter(websocket_urlpatterns))}
    )

    websocket_communicator = WebsocketCommunicator(
        websocket_application,
        f"/user/{test_user.username}/?token={access_token}",
    )

    # Connect to the websocket
    connected, _ = await websocket_communicator.connect()
    assert connected

    # Receive welcome message
    welcome_msg_str = await websocket_communicator.receive_from()
    welcome_msg_json = json.loads(welcome_msg_str)

    # Check the format and content of the welcome message
    assert welcome_msg_json["type"] == "welcome_message"
    assert welcome_msg_json["message"] == "Welcome to the Websocket Connection"

    # Receive last 50 messages
    last_messages_str = await websocket_communicator.receive_from()
    last_messages_json = json.loads(last_messages_str)

    # Check the format and content of the last 50 messages
    assert last_messages_json["type"] == "last_50_messages"
    assert isinstance(last_messages_json["messages"], list)

    # Receive and check the broadcasted chat message
    response = await websocket_communicator.receive_from()
    response_json = json.loads(response)
    assert response_json["type"] == "user_online_status"
    assert response_json["users"] == [{"username": f"{user.username}"}]

    chat_message = {"type": "chat_message", "message": "Hello, World!"}

    response = await websocket_communicator.send_json_to(chat_message)

    # Receive and check the broadcasted chat message
    response = await websocket_communicator.receive_from()
    response_json = json.loads(response)
    assert response_json["type"] == "chat_message_echo"
    assert response_json["message"]["content"] == "Hello, World!"
    assert response_json["message"]["from_user"]["username"] == user.username
    assert response_json["message"]["to_user"]["username"] == test_user.username
    assert response_json["message"]["read"] == False

    # print(f"Respose JSON:{response_json}")

    # await websocket_communicator.send_json_to()

    # Close the communicator
    await websocket_communicator.disconnect()
