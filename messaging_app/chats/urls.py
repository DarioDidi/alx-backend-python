from django.urls import include, path
from chats.views import ConversationViewSet, MessageViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(
    r"conversations", ConversationViewSet, basename="conversations"
)
router.register(r"messages", MessageViewSet, basename="messages")


urlpatterns = [
    path("", include((router.urls, "chats"), namespace="chats")),
]
