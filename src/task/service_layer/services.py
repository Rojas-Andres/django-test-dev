from datetime import datetime
from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from src.task.domain import models
from src.task.domain.repository import AbstractTaskUnitOfWork
from src.task.domain.validators import validate_due_date, validate_status


class TaskNotFound(ObjectDoesNotExist):
    """Raised when a task does not exist or has been logically deleted.

    Subclasses ``ObjectDoesNotExist`` so ``APIErrorsMixin`` maps it to an
    HTTP 404 response automatically.
    """


class CreateTask:
    def __init__(self, uow: AbstractTaskUnitOfWork):
        self.uow = uow

    def create(
        self,
        title: str,
        description: Optional[str] = None,
        status: Optional[str] = None,
        due_date: Optional[datetime] = None,
        created_by_name: Optional[str] = None,
    ) -> dict:
        validate_status(status)
        validate_due_date(due_date)
        with self.uow:
            task = self.uow.tasks.create(
                models.Task(
                    title=title,
                    description=description,
                    status=status or models.TaskStatus.PENDING.value,
                    due_date=due_date,
                    created_by_name=created_by_name,
                )
            )
            self.uow.commit()
            return self.uow.tasks.to_dict(task)


class UpdateTask:
    def __init__(self, uow: AbstractTaskUnitOfWork):
        self.uow = uow

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        due_date: Optional[datetime] = None,
        created_by_name: Optional[str] = None,
    ) -> dict:
        validate_status(status)
        # On update we allow past due dates (a task may already be overdue).
        validate_due_date(due_date, allow_past=True)
        with self.uow:
            task = self.uow.tasks.update(
                models.Task(
                    id=task_id,
                    title=title,
                    description=description,
                    status=status,
                    due_date=due_date,
                    created_by_name=created_by_name,
                )
            )
            if task is None:
                raise TaskNotFound(f"Task {task_id} not found.")
            self.uow.commit()
            return self.uow.tasks.to_dict(task)


class ChangeTaskStatus:
    def __init__(self, uow: AbstractTaskUnitOfWork):
        self.uow = uow

    def change(self, task_id: int, status: str) -> dict:
        validate_status(status)
        with self.uow:
            task = self.uow.tasks.update(
                models.Task(id=task_id, title=None, status=status)
            )
            if task is None:
                raise TaskNotFound(f"Task {task_id} not found.")
            self.uow.commit()
            return self.uow.tasks.to_dict(task)


class DeleteTask:
    def __init__(self, uow: AbstractTaskUnitOfWork):
        self.uow = uow

    def delete(self, task_id: int) -> dict:
        with self.uow:
            task = self.uow.tasks.delete(task_id)
            if task is None:
                raise TaskNotFound(f"Task {task_id} not found.")
            self.uow.commit()
            return self.uow.tasks.to_dict(task)
