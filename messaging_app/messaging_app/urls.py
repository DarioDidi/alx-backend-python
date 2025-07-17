from django.contrib import admin
from django.urls import include, path

# from rest_framework import routers
# from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_nested.routers import NestedDefaultRouter


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
    # path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
