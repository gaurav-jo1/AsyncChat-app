import json
from uuid import UUID
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import JsonWebsocketConsumer
from chats.models import Message, Conversation
from chats.serializers import MessageSerializer
from asgiref.sync import async_to_sync
from django.core.exceptions import ObjectDoesNotExist


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex

        return json.JSONEncoder.default(self, obj)


class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = None
        self.conversation_name = None
        self.conversation = None

    def connect(self):
        self.user = self.scope["user"]
        print(f"Self User: {self.user}")

        if isinstance(self.user, AnonymousUser):
            # Reject connection for anonymous users
            self.close()
            return

        self.accept()

        self.send_json(
            {
                "type": "welcome_message",
                "message": "Welcome to the Gaurav Websocket Connection",
            }
        )

        self.conversation_name = (
            f"{self.scope['url_route']['kwargs']['conversation_name']}"
        )

        self.conversation, created = Conversation.objects.get_or_create(
            name=self.conversation_name
        )

        self.channel_layer.group_add(self.conversation_name, self.channel_name)

        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        # Adding User as a Member
        self.conversation.add_member(self.user)

        # Making User Online
        self.conversation.join(self.user)

        messages = self.conversation.messages.all().order_by("-timestamp")[0:10]
        message_count = self.conversation.messages.all().count()

        print(f"Message Count {message_count}")

        self.send_json(
            {
                "type": "last_50_messages",
                "messages": MessageSerializer(messages, many=True).data,
                "has_more": message_count > 5,
            }
        )

    def disconnect(self, close_code):
        # Leave room group

        if self.user.is_authenticated:
            # send the leave event to the room
            self.channel_layer.group_send(
                self.conversation_name,
                {
                    "type": "user_leave",
                    "user": self.user.username,
                },
            )

        self.conversation.leave(self.user)
        return super().disconnect(close_code)

    def get_receiver(self):
        receiver = self.conversation.members.exclude(pk=self.user.pk)

        if receiver:
            return receiver.first()
        else:
            raise ObjectDoesNotExist("No user found.")

        # self.conversation.members.all(User!=self.user.username)

    def receive_json(self, content):
        type = content["type"]
        print(f"Greeting from {self.user.username}")

        if type == "greeting":
            # Send reply of greeting
            self.send_json(
                {
                    "type": "greeting_message",
                    "message": "Hey How you doing!",
                }
            )

        if type == "chat_message":
            message_text = content.get("message")

            message = Message.objects.create(
                from_user=self.user,
                to_user=self.get_receiver(),
                content=message_text,
                conversation=self.conversation,
            )

            async_to_sync(
                self.channel_layer.group_send(
                    self.conversation_name,
                    {
                        "type": "chat_message_echo",
                        "name": self.user.username,
                        "message": MessageSerializer(message),
                    },
                )
            )

    def greeting_message(self, event):
        # Send message to WebSocket
        self.send_json(event)

    # Receive message from room group
    def chat_message_echo(self, event):
        # Send message to WebSocket
        self.send_json(event)

    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)
