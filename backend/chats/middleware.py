from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenBackendError


class JWTAuthMiddleware:
    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        query_params = scope["query_string"].decode()
        if not query_params:
            await send(
                {
                    "type": "websocket.close",
                    "code": 4000,
                    "reason": "Invalid token parameter",
                }
            )

        token = query_params.split("=")[1]

        scope["token"] = token
        try:
            user = await get_user(scope)
        except TokenBackendError as ex:
            print(f"Token Backend Error: {ex}")
            await send(
                {
                    "type": "websocket.close",
                    "code": 4011,  # Custom code for authentication failure
                    "reason": "Token is invalid or expired",
                }
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            await send(
                {
                    "type": "websocket.close",
                    "code": 5000,  # Custom code for internal server error
                    "reason": "Internal server error",
                }
            )
            return

        if isinstance(user, AnonymousUser):
            return user

        scope["user"] = user

        return await self.app(scope, receive, send)


@database_sync_to_async
def get_user(scope):
    token = scope["token"]
    
    access_token = AccessToken(token)
    
    user_id = access_token.payload.get("user_id")
    
    user = User.objects.get(id=user_id)
    
    return user or AnonymousUser()
