from datetime import datetime
from typing import Optional

from django.utils import timezone

from src.task.domain.models import TaskStatus


def validate_status(status: Optional[str]) -> None:
    """Ensure the status, when provided, is one of the allowed values."""
    if status is None:
        return
    if not TaskStatus.has_value(status):
        allowed = ", ".join(member.value for member in TaskStatus)
        raise ValueError(
            f"Invalid status '{status}'. Allowed values: {allowed}."
        )


def validate_due_date(
    due_date: Optional[datetime], *, allow_past: bool = False
) -> None:
    """Ensure the due date is coherent (not in the past on creation)."""
    if due_date is None:
        return
    if not allow_past and due_date < timezone.now():
        raise ValueError("due_date cannot be in the past.")
