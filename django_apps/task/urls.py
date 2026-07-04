"""
File that contains the urls of the task app.
"""

from django.urls import path

from django_apps.task.views import (
    TaskChangeStatusView,
    TaskCreateView,
    TaskDetailView,
    TaskHistoryView,
    TaskListView,
    TaskUpcomingView,
)

APP_NAME = "task"

urlpatterns = [
    path("", TaskCreateView.as_view(), name="task_create"),
    path("list/", TaskListView.as_view(), name="task_list"),
    path("upcoming/", TaskUpcomingView.as_view(), name="task_upcoming"),
    path("<int:task_id>/", TaskDetailView.as_view(), name="task_detail"),
    path(
        "<int:task_id>/status/",
        TaskChangeStatusView.as_view(),
        name="task_change_status",
    ),
    path(
        "<int:task_id>/history/",
        TaskHistoryView.as_view(),
        name="task_history",
    ),
]
