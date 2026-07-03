"""
File with the task views.
"""

# Standard Library
import logging
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django_apps.task.filters import TaskFilter
from django_apps.task.models import Task, TaskStatus
from django_apps.utils.views.generic_decorators import GenerateSwagger
from django_apps.utils.views.generic_views import ListCoreView
from django_apps.utils.views.mixins import APIErrorsMixin, LoggingRequestViewMixin
from django_apps.utils.views.pagination import CorePagination
from src.task.adapters.unit_of_work import TaskUnitOfWork
from src.task.service_layer.services import (
    ChangeTaskStatus,
    CreateTask,
    DeleteTask,
    UpdateTask,
)

logger = logging.getLogger(__name__)


class TaskOutputSerializer(serializers.Serializer):
    """Read representation of a task, shared by every write endpoint."""

    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    status = serializers.CharField()
    due_date = serializers.DateTimeField(allow_null=True, required=False)
    created_by_name = serializers.CharField(allow_blank=True, required=False)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)


@GenerateSwagger(swagger_auto_schema)
class TaskCreateView(LoggingRequestViewMixin, APIErrorsMixin, APIView):
    """Create a new task (POST)."""

    permission_classes = [AllowAny]

    class InputPostSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        description = serializers.CharField(
            required=False, allow_blank=True, default=""
        )
        status = serializers.ChoiceField(choices=TaskStatus.values, required=False)
        due_date = serializers.DateTimeField(required=False, allow_null=True)
        created_by_name = serializers.CharField(
            max_length=150, required=False, allow_blank=True, default=""
        )

    class OutputPostSerializer(TaskOutputSerializer):
        pass

    def post(self, request):
        input_serializer = self.InputPostSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        _task = CreateTask(uow=TaskUnitOfWork()).create(
            **input_serializer.validated_data
        )
        output = self.OutputPostSerializer(instance=_task)
        return Response(data=output.data, status=status.HTTP_201_CREATED)


@GenerateSwagger(swagger_auto_schema)
class TaskDetailView(LoggingRequestViewMixin, APIErrorsMixin, APIView):
    """Update (PUT/PATCH) or logically delete (DELETE) a single task."""

    permission_classes = [AllowAny]

    class InputPutSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        description = serializers.CharField(allow_blank=True, default="")
        status = serializers.ChoiceField(choices=TaskStatus.values)
        due_date = serializers.DateTimeField(required=False, allow_null=True)
        created_by_name = serializers.CharField(
            max_length=150, required=False, allow_blank=True, default=""
        )

    class InputPatchSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False, allow_blank=True)
        status = serializers.ChoiceField(choices=TaskStatus.values, required=False)
        due_date = serializers.DateTimeField(required=False, allow_null=True)
        created_by_name = serializers.CharField(
            max_length=150, required=False, allow_blank=True
        )

    class OutputPutSerializer(TaskOutputSerializer):
        pass

    class OutputPatchSerializer(TaskOutputSerializer):
        pass

    def put(self, request, task_id):
        input_serializer = self.InputPutSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        _task = UpdateTask(uow=TaskUnitOfWork()).update(
            task_id=task_id, **input_serializer.validated_data
        )
        output = self.OutputPutSerializer(instance=_task)
        return Response(data=output.data, status=status.HTTP_200_OK)

    def patch(self, request, task_id):
        input_serializer = self.InputPatchSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        _task = UpdateTask(uow=TaskUnitOfWork()).update(
            task_id=task_id, **input_serializer.validated_data
        )
        output = self.OutputPatchSerializer(instance=_task)
        return Response(data=output.data, status=status.HTTP_200_OK)

    def delete(self, request, task_id):
        DeleteTask(uow=TaskUnitOfWork()).delete(task_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


@GenerateSwagger(swagger_auto_schema)
class TaskChangeStatusView(LoggingRequestViewMixin, APIErrorsMixin, APIView):
    """Change only the status of a task (PATCH)."""

    permission_classes = [AllowAny]

    class InputPatchSerializer(serializers.Serializer):
        status = serializers.ChoiceField(choices=TaskStatus.values)

    class OutputPatchSerializer(TaskOutputSerializer):
        pass

    def patch(self, request, task_id):
        input_serializer = self.InputPatchSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        _task = ChangeTaskStatus(uow=TaskUnitOfWork()).change(
            task_id=task_id, status=input_serializer.validated_data["status"]
        )
        output = self.OutputPatchSerializer(instance=_task)
        return Response(data=output.data, status=status.HTTP_200_OK)


@GenerateSwagger(swagger_auto_schema)
class TaskListView(APIErrorsMixin, ListCoreView):
    """List tasks (GET). Logically deleted tasks are excluded by default.

    Supports optional filtering by ``status``, due date range
    (``due_date_after`` / ``due_date_before``) and free text ``search``,
    plus ordering via ``ordering``.
    """

    permission_classes = [AllowAny]

    class OutputGetSerializer(TaskOutputSerializer):
        pass

    serializer_class = OutputGetSerializer
    queryset = Task.objects.filter(is_active=True)
    pagination_class = CorePagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = TaskFilter
    ordering_fields = ["due_date", "created_at", "status", "title"]
    ordering = ["due_date"]


@GenerateSwagger(swagger_auto_schema)
class TaskUpcomingView(APIErrorsMixin, ListCoreView):
    """List active, not-completed tasks due within a time window (GET).

    Criterion: tasks whose ``due_date`` falls between now and
    ``now + N days``. ``N`` defaults to ``settings.TASK_UPCOMING_DEFAULT_DAYS``
    (7 days) and can be overridden with the ``?days=`` query parameter.
    """

    permission_classes = [AllowAny]

    class OutputGetSerializer(TaskOutputSerializer):
        pass

    serializer_class = OutputGetSerializer
    pagination_class = CorePagination

    def _get_window_days(self) -> int:
        raw_days = self.request.query_params.get("days")
        if raw_days is None:
            return settings.TASK_UPCOMING_DEFAULT_DAYS
        try:
            days = int(raw_days)
        except (TypeError, ValueError):
            raise ValidationError({"days": ["Must be an integer."]})
        if days < 0:
            raise ValidationError({"days": ["Must be a positive integer."]})
        return days

    def get_queryset(self):
        now = timezone.now()
        deadline = now + timedelta(days=self._get_window_days())
        return (
            Task.objects.filter(
                is_active=True,
                due_date__isnull=False,
                due_date__gte=now,
                due_date__lte=deadline,
            )
            .exclude(status=TaskStatus.COMPLETED)
            .order_by("due_date")
        )
