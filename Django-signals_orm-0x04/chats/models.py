import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Q

from django.db import models

from .managers import UnreadMessagesManager


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    first_name = models.CharField(blank=False, max_length=60)
    last_name = models.CharField(blank=False, max_length=60)
    phone_number = models.CharField(blank=False, max_length=13)
    password = models.CharField(_("password"), max_length=128)


class Conversation(models.Model):
    # users = models.ManyToManyField(Users)
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    participants = models.ManyToManyField(Users)


class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    sender = models.ForeignKey(Users, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    unread_msgs = UnreadMessagesManager()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
    )
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_children_filters(self, include_self=True):
        filters = Q(pk=0)

        if include_self:
            filters |= Q(pk=self.pk)

        for reply in Message.objects.filter(parent=self):
            _r = reply.get_children_filters(include_self=True)
            if _r:
                filters |= _r

        return filters

    def get_all_children(self, include_self=True):
        return Message.objects.filter(self.get_children_filters(include_self))


class MessageHistory(models.Model):
    old_content = models.TextField()
    sender = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    orig_message = models.ForeignKey(Message)
    history_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )


class Notification(models.Model):
    recepient = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="actions"
    )
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeFiels(auto_now=True)

    def get_model_type(self):
        return self.__class__.__name__
