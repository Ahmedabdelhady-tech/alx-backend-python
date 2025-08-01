from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="chat_sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="chat_received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content[:30]}"
