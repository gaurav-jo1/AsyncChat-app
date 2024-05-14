from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
import jwt
from rest_framework.exceptions import AuthenticationFailed


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
            return

        token = query_params.split("=")[1]
        scope["token"] = token
        scope["user"] = await get_user(scope)

        return await self.app(scope, receive, send)


@database_sync_to_async
def get_user(scope):
    if "token" not in scope:
        raise ValueError(
            "Cannot find token in scope. You should wrap your consumer in "
            "TokenAuthMiddleware."
        )
    token = scope["token"]
    user = None
    try:
        access_token = AccessToken(token)
        user_id = access_token.payload.get("user_id")
        user = User.objects.get(id=user_id)
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")
    except User.DoesNotExist:
        raise AuthenticationFailed("User not found")

    return user or AnonymousUser()
