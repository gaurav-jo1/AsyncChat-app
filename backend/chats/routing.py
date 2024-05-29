from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("chat/<conversation_name>/", consumers.ChatConsumer.as_asgi()),
    path(
        "user/<user_username>/",
        consumers.UserChatConsumer.as_asgi(),
    ),
]
