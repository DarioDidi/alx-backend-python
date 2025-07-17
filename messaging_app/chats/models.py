from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    pass


class conversation(models.Model):
    users = models.ManyToManyField(Users)


class message(models.Model):
    sender = models.ForeignKey(Users, on_delete=models.CASCADE)
    conversation = models.ForeignKey(conversation, on_delete=models.CASCADE)
