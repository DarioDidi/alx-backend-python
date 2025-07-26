from rest_framework.permissions import BasePermission
from .models import Conversation


class IsParticipantOfConversation(BasePermission):
    message = "Access Denied!"

    def has_permission(self, request, view):
        obj = request.GET["pk"] or request.POST["pk"]
        convo = Conversation.objects.get(pk=obj)
        user_id = request.user.pk
        return convo.participants.filter(id=user_id).exists()

    def has_object_permission(self, request, view, obj):

        # Instance must have an attribute named `owner`.
        return obj.participants.filter(request.user).exists()
