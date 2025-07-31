from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.response import Response

# from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters


from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


from messaging.serializers import (
    ConversationSerializer,
    MessageSerializer,
)

from .models import Message, Conversation, Users


class MessageViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving messages.
    """

    lookup_field = "message_uuid"
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ["created_at", "sender"]
    permission_classes = IsParticipantOfConversation
    filterset_class = MessageFilter

    def list(self, req, pk=None):
        unread_messages = Message.unread_msgs.all()
        # queryset = Message.objects.filter(conversation=pk)
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)
        # return self.get_paginated_response(
        #    self.paginate_queryset(serializer.data)
        # )

    def retrieve(self, request, pk=None):
        # msg = get_object_or_404(Message, pk=pk)
        msg = Message.objects.select_related("blog").get(message_id=pk)
        self.mark_read(msg)
        msg = Message.get_all_children(True)
        serializer = MessageSerializer(msg)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """

        permission_classes = IsParticipantOfConversation
        return [permission() for permission in permission_classes]

    def mark_read(self, msg):
        if self.request.user == msg.sender:
            msg.read = True
            msg.save()

    # def get_serializer(self):
    #    return MessageSerializer(data)


class ConversationViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving conversation messages.
    """

    lookup_field = "conversation_id"
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ["participants"]
    permission_classes = IsParticipantOfConversation
    pagination_class = MessagePagination

    def retrieve(self, request, pk=None):
        convo = get_object_or_404(Conversation, pk=pk)
        serializer = ConversationSerializer(convo)
        return Response(serializer.data)

    def create(self, req):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """

        permission_classes = IsParticipantOfConversation
        return [permission() for permission in permission_classes]
        # return Response(serializer.data, status=status.HTTP_403_FORBIDDEN


def delete_user(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "DELETE":
        user = get_object_or_404(Users, username=request.user.username)
        user.delete()
        return HttpResponseRedirect("/")
