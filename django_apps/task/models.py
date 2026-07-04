"""
Models for the task app.
"""

from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from django_apps.core.models import BaseModel


class TaskStatus(models.TextChoices):
    """Status choices for a task (kept in sync with the domain enum)."""

    PENDING = "pendiente", "Pendiente"
    COMPLETED = "completada", "Completada"
    POSTPONED = "pospuesta", "Pospuesta"


class Task(BaseModel):
    """A task in the to-do list.

    Inherits ``created_at``, ``updated_at``, ``deleted_at`` and ``is_active``
    from :class:`BaseModel`. Logical deletion is handled by setting
    ``is_active`` to ``False`` (which fills ``deleted_at``).
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING,
    )
    due_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks",
    )
    created_by_name = models.CharField(max_length=150, blank=True)
    historical = HistoricalRecords()

    class Meta:
        ordering = ["due_date", "-created_at"]

    def __str__(self):
        return self.title
