from django_filters import rest_framework as filters

from django_apps.user.models import User


class UserFilter(filters.FilterSet):
    email = filters.CharFilter()

    class Meta:
        model = User
        fields = ["email"]
