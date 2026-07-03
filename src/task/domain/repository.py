# Standard Library
from abc import ABC, abstractmethod
from typing import List, Optional

from src.shared.domain.service_layer.unit_of_work import AbstractUnitOfWork
from src.task.domain import models


class AbstractTaskRepository(ABC):
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[models.Task]:
        raise NotImplementedError

    @abstractmethod
    def create(self, task: models.Task) -> models.Task:
        raise NotImplementedError

    @abstractmethod
    def update(self, task: models.Task) -> Optional[models.Task]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> Optional[models.Task]:
        """Soft delete: mark the task as inactive."""
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[models.Task]:
        raise NotImplementedError

    @abstractmethod
    def to_dict(self, task: models.Task) -> dict:
        raise NotImplementedError


class AbstractTaskUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.tasks: AbstractTaskRepository
        return super().__enter__()
