from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from shared.enum import StrEnum


class TaskStatus(StrEnum):
    """Allowed states for a task."""

    PENDING = "pendiente"
    COMPLETED = "completada"
    POSTPONED = "pospuesta"


@dataclass
class Task:
    title: str
    id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    created_by: Optional[int] = None
    created_by_name: Optional[str] = None
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
