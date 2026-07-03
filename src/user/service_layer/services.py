from src.user.domain.repository import AbstractUserUnitOfWork
from src.user.domain import models


class CreateUser:
    def __init__(
        self,
        uow: AbstractUserUnitOfWork,
    ):
        self.uow = uow

    def create(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        phone_number: str,
        document: str,
        code_phone: str,
    ) -> dict:
        with self.uow:
            user = self.uow.users.get_by_email(email)
            if user is not None:
                raise ValueError("User already exists")
            user = self.uow.users.create(
                models.User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    document=document,
                    phone_number=phone_number,
                    code_phone=code_phone,
                )
            )
            self.uow.commit()
            return self.uow.users.to_dict(user)

