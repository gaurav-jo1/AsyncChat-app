from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self) -> str:
        return f"{self.name} ({str(self.get_online_count())})"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )

    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_from_me"
    )

    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_to_me"
    )
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"From {self.from_user.username} to {self.to_user.username}: {self.content} [{self.timestamp}]"
