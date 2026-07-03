"""
File that contains the urls of the user app.
"""

from django.urls import path

from django_apps.user.views import UserCreateView, UserListView  # UserDetailView

APP_NAME = "user"

urlpatterns = [
    path("", UserCreateView.as_view(), name="user_list"),
    path("list/", UserListView.as_view(), name="user_list"),
    # path("detail/", UserDetailView.as_view(), name="user_detail"),
]
