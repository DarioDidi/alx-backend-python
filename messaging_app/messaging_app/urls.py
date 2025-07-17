from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

from chats.views import ConversationViewSet, MessageViewSet


main_router = routers.DefaultRouter()
main_router.register(
    r"conversations", ConversationViewSet, basename="conversations"
)

"""crate conversations router first based on default router"""
conversations_router = NestedDefaultRouter(
    main_router, r"conversations", lookup="conversation"
)
"""nest messages routing inside conversations"""
conversations_router.register(
    r"messages", MessageViewSet, basename="conversation-messages"
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),
    path("api/", include(main_router.urls)),
    path("api/", include(conversations_router.urls)),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
    # path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
