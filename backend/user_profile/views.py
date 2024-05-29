from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

# from django.contrib.auth.models import Use
from rest_framework.response import Response
from rest_framework import status
from user_profile.models import User_profile
from .serializers import UserProfileSerializer


# Create your views here.
class Get_Users(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users_list = User_profile.objects.all()
        
        # Except the Current User

        serializer = UserProfileSerializer(users_list, many=True).data

        return Response(
            data=serializer,
            status=status.HTTP_200_OK,
        )
