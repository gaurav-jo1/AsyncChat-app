import json
from uuid import UUID
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from chats.models import Message, Conversation
from django.contrib.auth.models import User
from chats.serializers import MessageSerializer
from channels.db import database_sync_to_async


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex

        return json.JSONEncoder.default(self, obj)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = None
        self.conversation_name = None
        self.conversation = None

    async def connect(self):
        self.user = self.scope["user"]

        print(self.user)

        if isinstance(self.user, AnonymousUser):
            # Reject connection for anonymous users
            await self.close()
            return

        print(f"User: {self.user}")

        await self.accept()

        self.conversation_name = (
            f"{self.scope['url_route']['kwargs']['conversation_name']}"
        )

        print(f"Conversation name: {self.conversation_name}")

        self.conversation, created = await database_sync_to_async(
            Conversation.objects.get_or_create
        )(name=self.conversation_name)

        await self.channel_layer.group_add(self.conversation_name, self.channel_name)

        self.send_json(
            {
                "type": "welcome_message",
                "message": "Welcome to the Gaurav Websocket Connection",
            }
        )

        await database_sync_to_async(self.conversation.online.add)(self.user)

        messages = self.conversation.messages.all().order_by("-timestamp")[0:10]
        message_count = await database_sync_to_async(
            self.conversation.messages.all().count
        )()
        print(f"Messages Count: {message_count}")

        # message_count = 0
        # print(f"Self Conversation: {self.conversation}")

        if message_count:
            messages = self.conversation.messages.all().order_by("-timestamp")[0:10]
            self.send_json(
                {
                    "type": "last_50_messages",
                    "messages": MessageSerializer(messages, many=True).data,
                    "has_more": message_count > 50,
                }
            )

        else:
            self.send_json(
                {
                    "type": "last_50_messages",
                    "messages": None,
                    "has_more": message_count > 50,
                }
            )

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
            # self.conversation.online.remove(self.user)
        return await super().disconnect(close_code)

    async def get_receiver(self):
        usernames = self.conversation_name.split("__")
        for username in usernames:
            if username != self.user.username:
                # This is the receiver
                return await User.objects.get(username=username)

    async def receive_json(self, text_data):
        # username = self.scope["user"].username
        type = text_data.get("type")

        if type == "greeting":
            # Send reply of greeting
            await self.channel_layer.group_send(
                self.conversation_name,
                {"type": "greeting_reply", "message": "Hey How you doing!"},
            )

        elif type == "message":
            message_text = text_data.get("message")
            username = text_data.get("username")

            message = Message.objects.create(
                from_user=self.user,
                to_user=self.get_receiver(),
                content=message_text,
                conversation=self.conversation,
            )

            await self.channel_layer.group_send(
                self.conversation_name,
                {
                    "type": "chat_message_echo",
                    "name": self.user.username,
                    "message": MessageSerializer(message).data,
                },
            )

            # Send message to room group
            await self.channel_layer.group_send(
                self.conversation_name,
                {"type": "message", "message": message_text, "username": username},
            )

    # Receive message from room group
    async def message(self, event):
        # Send message to WebSocket
        await self.send_json(event)

    async def greeting_message(self, event):
        # Send message to WebSocket
        await self.send_json(event)

    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)
