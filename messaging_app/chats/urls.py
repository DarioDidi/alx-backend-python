from django.urls import include, path
from chats.views import ConversationViewSet, MessageViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(
    r"new/conversation", ConversationViewSet, basename="conversation"
)
router.register(r"new/message", MessageViewSet, basename="message")


urlpatterns = [
    path("", include((router.urls, "chats"), namespace="chats")),
]
