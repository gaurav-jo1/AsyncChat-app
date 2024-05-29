from rest_framework import serializers
from .models import User_profile

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = User_profile
        fields = ['user', 'username', 'avatar', 'email']

    def get_username(self, obj):
        return obj.user.username
    
    def get_email(self, obj):
        return obj.user.email

