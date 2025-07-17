import uuid
from django.utils.translation import gettext_lazy as _

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

"""import uuid", "email", "password", "user_id", "first_name", "last_name", "phone_number", "primary_key"""


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(blank=False, max_length=60)
    last_name = models.CharField(blank=False, max_length=60)
    phone_number = models.CharField(blank=False, max_length=13)
    password = models.CharField(_("password"), max_length=128)


class Conversation(models.Model):
    # users = models.ManyToManyField(Users)
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(Users)


"""message_id", "message_body", "sent_at", "created_at"""


class Message(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message_id = models.UUIDField(defaul=uuid.uuid4, editable=False)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
