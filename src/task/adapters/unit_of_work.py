from django_apps.utils.adapters import unit_of_work
from src.task.adapters.django_repository import TaskDjangoRepository
from src.task.domain.repository import AbstractTaskUnitOfWork


class TaskUnitOfWork(unit_of_work.DjangoUnitOfWork, AbstractTaskUnitOfWork):
    def __enter__(self):
        self.tasks = TaskDjangoRepository()
        return super().__enter__()
