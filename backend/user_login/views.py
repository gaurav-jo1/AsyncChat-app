from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .serializers import UserCredentialsSerializer

# Create your views here.
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = UserCredentialsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            # Attempt to authenticate the user
            if username and password:
                user = authenticate(username=username, password=password)
            elif email and password:
                try:
                    user = User.objects.get(email=email)
                    user = authenticate(username=user.username, password=password)
                except User.DoesNotExist:
                    user = None
            else:
                return Response(
                    {"error": "Missing credentials"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Check if user is authenticated and generate tokens
            if user is not None:
                refresh = RefreshToken.for_user(user)

                return Response(
                    {"tokens": {"refresh": str(refresh), "access": str(refresh.access_token)}, "username": str(user)},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
