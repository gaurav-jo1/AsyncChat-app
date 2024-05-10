from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"]

        if query_string:
            try:
                token = self.extract_token(query_string)
                if token:
                    access_token = AccessToken(token)
                    user_id = access_token.payload.get("user_id")
                    if user_id:
                        scope["user"] = await self.get_user(user_id)
                    else:
                        scope["user"] = AnonymousUser()
                else:
                    scope["user"] = AnonymousUser()
            except Exception as e:
                print(f"Error parsing token: {e}")
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    def extract_token(self, query_string):
        try:
            token = query_string.decode().split("=")[1]
            return token
        except IndexError:
            return None

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)