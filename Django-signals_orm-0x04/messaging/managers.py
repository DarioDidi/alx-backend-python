from django.db import models


class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(read=False)

    def unread_for_user(self, user):
        return super().get_queryset().filter(read=False, receiver=user)
