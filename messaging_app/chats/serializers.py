from rest_framework.serializers import ModelSerializer

from models import Conversation, Message, Users


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ("first_name", "last_name", "phone_number", "id")


class ConversationSerializer(ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
