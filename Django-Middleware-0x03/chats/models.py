import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.

#Custom user model to extend the default Django user model
class CustomUser(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    username = None  # Disable username field
    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Required fields for user creation

    def __str__(self):
        return f"{self.first_name} {self.last_name})"
    
# Conversation model to represent a chat between users
class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation between {self.conversation_id}"
    
# Message model to represent messages in a conversation
class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.email}"