from .models import Notification, Message, MessageHistory, Users
from django.db.models.signals import (
    post_delete,
    post_save,
    pre_delete,
    pre_save,
)
from django.dispatch import receiver


@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    if created:
        message = instance.content
        actor = instance.sender
        recepient = instance.receiver

        Notification.objects.create(
            recepient=recepient,
            actor=actor,
            target=message,
            verb="Sent a message",
        )


@receiver(pre_save, sender=Message)
def save_old_message(sender, instance, created, **kwargs):
    if not created:
        sender.edited = True
        MessageHistory.objects.create(
            old_content=sender.content,
            orig_message=sender,
            sender=sender.sender,
        )


@receiver(pre_delete, sender=Message)
def delete_repo(sender, instance, **kwargs):
    sender.file_results.delete()
    sender.file_results = None


"""post_delete signal on the User model to delete all messages, notifications,
and message histories associated with the user"""


@receiver(post_delete, sender=Users)
def delete_related_objects(sender, instance, **kwargs):
    Message.objects.filter(sender=instance.user_id).delete()
    Notification.objects.filter(actor=instance.user_id).delete()
    MessageHistory.objects.filter(sender=instance.user_id).delete()
