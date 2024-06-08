import pytest
import json
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from backend.asgi import application
from channels.db import database_sync_to_async
from chats.models import Message


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_consumer(user, access_token_user, test_user):

    assert test_user.username == "testuser"

    websocket_communicator = WebsocketCommunicator(
        application,
        f"/user/{test_user.username}/?token={access_token_user}",
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

    # await websocket_communicator.send_json_to()

    # Close the communicator
    await websocket_communicator.disconnect()


from chats.models import User_Conversation


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_chats_consumer_second(access_token_testuser, user, test_user):

    assert user.username == "user1"

    websocket_communicator = WebsocketCommunicator(
        application,
        f"/user/{user.username}/?token={access_token_testuser}",
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

    # Create a User conversation

    user_conversation = await database_sync_to_async(User_Conversation.objects.create)(
        name=f"{test_user}_{user}",
        from_user=test_user,
        to_user=user,
    )

    # Save a message
    msg_content = "Hello World!"

    await database_sync_to_async(Message.objects.create)(
        from_user=test_user,
        to_user=user,
        content=msg_content,
        conversation_user=user_conversation,
    )

    # Receive last 50 messages
    last_messages_str = await websocket_communicator.receive_from()
    last_messages_json = json.loads(last_messages_str)

    # Check the format and content of the last 50 messages
    assert last_messages_json["type"] == "last_50_messages"

    assert (
        last_messages_json["messages"][0]["from_user"]["username"] == test_user.username
    )
    assert last_messages_json["messages"][0]["to_user"]["username"] == user.username
    assert last_messages_json["messages"][0]["content"] == msg_content
    assert last_messages_json["messages"][0]["read"] == False

    # Receive and check the broadcasted chat message
    response = await websocket_communicator.receive_from()
    response_json = json.loads(response)
    assert response_json["type"] == "user_online_status"
    assert response_json["users"][0]["username"] == test_user.username

    # Close the communicator
    await websocket_communicator.disconnect()
