from src.user.adapters.django_repository import UserDjangoRepository

# from src.shared.domain.service_layer import unit_of_work
from django_apps.utils.adapters import unit_of_work


class UserUnitOfWork(unit_of_work.DjangoUnitOfWork):
    def __enter__(self):
        self.users = UserDjangoRepository()
        return super().__enter__()
