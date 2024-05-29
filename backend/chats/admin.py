from django.contrib import admin
from chats.models import Conversation, Message, User_Conversation

# Register your models here.

admin.site.register(User_Conversation)
admin.site.register(Conversation)
admin.site.register(Message)
