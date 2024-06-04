from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class User_profile(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default=None)

    def __str__(self):
            return self.user.username
