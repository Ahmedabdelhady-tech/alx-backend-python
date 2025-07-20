import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Custom User model extending AbstractUser
class User(AbstractUser):
    class Role(models.TextChoices):
        GUEST = "guest", "Guest"
        HOST = "host", "Host"
        ADMIN = "admin", "Admin"

    # Remove username field and use email as unique identifier
    username = None
    email = models.EmailField(unique=True, verbose_name="email address")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.GUEST, null=False
    )
    created_at = models.DateTimeField(default=timezone.now)

    # Set email as the username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Conversation model to track participants
class Conversation(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [models.Index(fields=["id"]), models.Index(fields=["created_at"])]
        ordering = ["-created_at"]

    def __str__(self):
        participants = ", ".join([str(user) for user in self.participants.all()[:3]])
        return f"Conversation ({self.id}) with {participants}"


# Message model containing sender and conversation
class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["sent_at"]),
            models.Index(fields=["conversation", "sent_at"]),
        ]
        ordering = ["-sent_at"]

    def __str__(self):
        return (
            f"Message from {self.sender} at {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
        )
