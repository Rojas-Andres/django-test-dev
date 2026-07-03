"""
File for URL configuration.
"""

import os

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django_project.views import HealtCheck

schema_view = get_schema_view(
    openapi.Info(
        title="Stack Django",
        default_version="latest",
        description="Documentation of the stack django",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", HealtCheck.as_view(), name="healtcheck"),
    path("api/user/", include("django_apps.user.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
CONFIG_SETTINGS = os.getenv("CONFIG_SETTINGS")
