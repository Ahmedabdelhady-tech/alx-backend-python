from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=MessageHistory)
def log_message_edits(sender, instace, **kwargs):
    if not instace.pk:
        return
    try:
        old_message = Message.objects.get(pk=instace.pk)
    except Message.DoesNotExist:
        return

    if instace.content != old_message.content:
        MessageHistory.objects.create(
            message=old_message, old_content=old_message.content
        )
        instace.edited = True
