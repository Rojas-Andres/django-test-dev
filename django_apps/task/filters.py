from django.db.models import Q
from django_filters import rest_framework as filters

from django_apps.task.models import Task


class TaskFilter(filters.FilterSet):
    """Optional filters for the task list.

    - ``status``: exact match against an allowed status.
    - ``due_date_after`` / ``due_date_before``: due date range (ISO 8601).
    - ``search``: case-insensitive text search on title and description.
    """

    status = filters.CharFilter()
    due_date_after = filters.IsoDateTimeFilter(field_name="due_date", lookup_expr="gte")
    due_date_before = filters.IsoDateTimeFilter(
        field_name="due_date", lookup_expr="lte"
    )
    search = filters.CharFilter(method="filter_search")

    class Meta:
        model = Task
        fields = ["status", "due_date_after", "due_date_before", "search"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
