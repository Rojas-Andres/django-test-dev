from src.shared.domain.service_layer.unit_of_work import AbstractUnitOfWork
from typing import Any, Optional
from django.contrib.auth.hashers import make_password

# Standard Library
from abc import ABC, abstractmethod
from src.user.domain import models


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[models.User]:
        raise NotImplementedError

    @abstractmethod
    def create(self, user: models.User) -> models.User:
        raise NotImplementedError

    @abstractmethod
    def to_dict(self, user: models.User) -> dict:
        raise NotImplementedError

class AbstractUserUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.users: AbstractUserRepository
        return super().__enter__()
