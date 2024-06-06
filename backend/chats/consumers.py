from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from chats.models import Message, Conversation, User_Conversation
from chats.serializers import MessageSerializer, UserSerializer
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from channels.db import database_sync_to_async
from django.contrib.auth.models import User


class UserChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = None
        self.to_user = None
        self.conversation_name = None
        self.conversation = None

    async def connect(self):
        self.user = self.scope["user"]

        # Reject connection for anonymous users
        if isinstance(self.user, AnonymousUser):
            await self.close()

        # Accept the connection
        await self.accept()

        # Send a welcome message
        await self.send_json(
            {
                "type": "welcome_message",
                "message": "Welcome to the Websocket Connection",
            }
        )

        to_username = f"{self.scope['url_route']['kwargs']['user_username']}"

        # Get User for the db
        try:
            self.to_user = await database_sync_to_async(User.objects.get)(
                username=to_username
            )
        except User.DoesNotExist:
            # Reject connection if a user does not exist
            await self.close(code=4001)

        try:
            try:

                self.conversation = await database_sync_to_async(
                    User_Conversation.objects.get
                )(name=f"{self.user}_{self.to_user}")

            except User_Conversation.DoesNotExist:
                self.conversation = await database_sync_to_async(
                    User_Conversation.objects.get
                )(name=f"{self.to_user}_{self.user}")

        except User_Conversation.DoesNotExist:
            self.conversation = await database_sync_to_async(
                User_Conversation.objects.create
            )(
                name=f"{self.user}_{self.to_user}",
                from_user=self.user,
                to_user=self.to_user,
            )

        self.conversation_name = self.conversation.name

        await self.channel_layer.group_add(
            self.conversation_name,
            self.channel_name,
        )

        # Mark the user as online in the conversation
        await database_sync_to_async(self.conversation.join)(self.user)

        # Get the User online
        users_list = await self.get_online_users()

        # Send User Online status to Chat
        await self.channel_layer.group_send(
            self.conversation_name,
            {
                "type": "user_online_status",
                "users": users_list,
            },
        )

        messages = await database_sync_to_async(Message.objects.filter)(
            conversation_user=self.conversation.id
        )

        # Send the last 10 messages to the client
        message_serilaizer = await self.serialize_messages(messages)
        
        await self.send_json(
            {
                "type": "last_50_messages",
                "messages": message_serilaizer,
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await database_sync_to_async(self.conversation.leave)(self.user)

        # # Get the User online
        users_list = await self.get_online_users()

        # Send User Online status to Chat
        await self.channel_layer.group_send(
            self.conversation_name,
            {
                "type": "user_online_status",
                "users": users_list,
            },
        )

        return await super().disconnect(close_code)

    async def receive_json(self, content):
        message_type = content["type"]

        if message_type == "chat_message":
            message_text = content.get("message")

            message = await database_sync_to_async(Message.objects.create)(
                from_user=self.user,
                to_user=self.to_user,
                content=message_text,
                conversation_user=self.conversation,
            )

            serialized_message = await self.serialize_single_message(message)

            await self.channel_layer.group_send(
                self.conversation_name,
                {
                    "type": "chat_message_echo",
                    "message": serialized_message,
                },
            )

    # Receive message from room group
    async def chat_message_echo(self, event):
        # Send message to WebSocket
        await self.send_json(event)

    async def user_online_status(self, event):
        # Send message to WebSocket

        await self.send_json(event)

    @sync_to_async
    def serialize_single_message(self, message):
        return MessageSerializer(message).data

    @sync_to_async
    def serialize_messages(self, messages):
        return MessageSerializer(messages, many=True).data

    async def get_online_users(self):
        online_users = await database_sync_to_async(list)(
            self.conversation.online_users.all()
        )

        return UserSerializer(online_users, many=True).data


class ChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = None
        self.conversation_name = None
        self.conversation = None

    async def connect(self):
        # Authenticate the user
        self.user = self.scope["user"]

        # Reject connection for anonymous users
        if isinstance(self.user, AnonymousUser):
            self.close()
            return

        # Accept the connection
        await self.accept()

        # Send a welcome message
        await self.send_json(
            {
                "type": "welcome_message",
                "message": "Welcome to the Websocket Connection",
            }
        )

        # Extract the conversation name from the URL route
        self.conversation_name = (
            f"{self.scope['url_route']['kwargs']['conversation_name']}"
        )

        self.conversation, created = await database_sync_to_async(
            Conversation.objects.get_or_create
        )(name=self.conversation_name)

        # Add the connection to the conversation group asynchronously
        await self.channel_layer.group_add(
            self.conversation_name,
            self.channel_name,
        )

        # Add the user as a member of the conversation
        await database_sync_to_async(self.conversation.add_member)(self.user)

        # Mark the user as online in the conversation
        await database_sync_to_async(self.conversation.join)(self.user)

        # Fetch the last 10 messages from the conversation
        messages = await database_sync_to_async(
            lambda: self.conversation.messages.all().order_by("timestamp")[0:10]
        )()

        message_count = await database_sync_to_async(
            lambda: self.conversation.messages.all().count()
        )()

    async def disconnect(self, close_code):
        # Leave room group
        if self.user.is_authenticated:
            # send the leave event to the room
            await self.channel_layer.group_send(
                self.conversation_name,
                {
                    "type": "user_leave",
                    "user": self.user.username,
                },
            )

        await sync_to_async(self.conversation.leave)(self.user)

        return await super().disconnect(close_code)

    async def get_receiver(self):
        receiver = self.conversation.members.exclude(pk=self.user.pk)

        if receiver:
            return receiver.first()
        else:
            raise ObjectDoesNotExist("No user found.")

        # self.conversation.members.all(User!=self.user.username)

    async def receive_json(self, content):
        message_type = content["type"]

        if message_type == "greeting":
            # Send reply of greeting
            await self.send_json(
                {
                    "type": "greeting_message",
                    "message": "Hey How you doing!",
                }
            )

        if message_type == "chat_message":
            message_text = content.get("message")

            message = await database_sync_to_async(Message.objects.create)(
                from_user=self.user,
                to_user=self.user,
                content=message_text,
                conversation=self.conversation,
            )

            serialized_message = await self.serialize_single_message(message)

            await self.channel_layer.group_send(
                self.conversation_name,
                {
                    "type": "chat_message_echo",
                    "message": serialized_message,
                },
            )

    # Receive message from room group
    async def chat_message_echo(self, event):
        # Send message to WebSocket
        await self.send_json(event)

    async def greeting_message(self, event):
        # Send message to WebSocket
        await self.send_json(event)

    async def user_leave(self, event):
        await self.send_json(event)

    @sync_to_async
    def serialize_messages(self, messages):
        return MessageSerializer(messages, many=True).data

    @sync_to_async
    def serialize_single_message(self, message):
        return MessageSerializer(message).data
