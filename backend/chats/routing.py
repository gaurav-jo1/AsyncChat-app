from django.urls import path

from chats.consumers import ChatConsumer

websocket_urlpatterns = [
    path(r"", ChatConsumer.as_asgi()),
]
