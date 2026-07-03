from django.db import transaction

# import abc
from src.shared.domain.service_layer.unit_of_work import AbstractUnitOfWork


class DjangoUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.__has_transaction = None
        super().__init__()

    def __enter__(self):
        self.__has_transaction = not transaction.get_autocommit()
        if not self.__has_transaction:
            transaction.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args):
        if not self.__has_transaction:
            super().__exit__(*args)
            transaction.set_autocommit(True)

    def _commit(self):
        if self.__has_transaction:
            return
        transaction.commit()

    def rollback(self):
        if self.__has_transaction:
            return
        transaction.rollback()
