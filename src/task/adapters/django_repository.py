from typing import List, Optional

from django_apps.task.models import Task
from src.task.domain import models
from src.task.domain.repository import AbstractTaskRepository

# Fields that can be written from the domain model into the ORM instance.
WRITABLE_FIELDS = (
    "title",
    "description",
    "status",
    "due_date",
    "created_by_name",
)


class TaskDjangoRepository(AbstractTaskRepository):
    def _get_active_instance(self, task_id: int) -> Optional[Task]:
        return Task.objects.filter(id=task_id, is_active=True).first()

    def get_by_id(self, task_id: int) -> Optional[models.Task]:
        instance = self._get_active_instance(task_id)
        return self.to_domain(instance) if instance else None

    def create(self, task: models.Task) -> models.Task:
        instance = Task.objects.create(
            title=task.title,
            description=task.description or "",
            status=task.status or models.TaskStatus.PENDING.value,
            due_date=task.due_date,
            created_by_name=task.created_by_name or "",
        )
        return self.to_domain(instance)

    def update(self, task: models.Task) -> Optional[models.Task]:
        instance = self._get_active_instance(task.id)
        if instance is None:
            return None
        for field in WRITABLE_FIELDS:
            value = getattr(task, field)
            if value is not None:
                setattr(instance, field, value)
        instance.save()
        return self.to_domain(instance)

    def delete(self, task_id: int) -> Optional[models.Task]:
        instance = self._get_active_instance(task_id)
        if instance is None:
            return None
        instance.is_active = False
        # BaseModel.save() sets deleted_at when the instance is inactive.
        instance.save()
        return self.to_domain(instance)

    def list(self) -> List[models.Task]:
        return [
            self.to_domain(instance)
            for instance in Task.objects.filter(is_active=True)
        ]

    def to_domain(self, model: Task) -> models.Task:
        return models.Task(
            id=model.pk,
            title=model.title,
            description=model.description,
            status=model.status,
            due_date=model.due_date,
            created_by_name=model.created_by_name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )

    def to_dict(self, task: models.Task) -> dict:
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "due_date": task.due_date,
            "created_by_name": task.created_by_name,
            "is_active": task.is_active,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "deleted_at": task.deleted_at,
        }
