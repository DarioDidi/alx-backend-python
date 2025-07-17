from rest_framework import serializers

from .models import Conversation, Message, Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("first_name", "last_name", "phone_number", "id")


class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    id = serializers.CharField(max_length=80)

    class Meta:
        model = Conversation

        fields = ["conversationid", "participants", "created_at", "messages"]

    def get_messages(self, obj):
        ret = Message.objects.filter(conversation=obj)
        if not len(ret):
            raise serializers.ValidationError("Empty conversation")
        return MessageSerializer(ret, many=True).data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
