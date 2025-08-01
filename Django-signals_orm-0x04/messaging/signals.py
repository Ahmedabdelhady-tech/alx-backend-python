from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model

User = get_user_model


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


@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
