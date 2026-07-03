from src.user.domain.repository import AbstractUserRepository
from django_apps.user.models import User
from src.user.domain import models
from django.contrib.auth.hashers import make_password
from datetime import datetime


class UserDjangoRepository(AbstractUserRepository):
    def get_by_email(self, email):
        _user = User.objects.filter(email=email).first()
        return self.to_domain(_user) if _user else None

    def to_domain(self, model: User) -> models.User:
        user = models.User(
            id=model.pk,
            password=model.password,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            is_active=model.is_active,
            last_login=model.last_login,
            created_at=model.created_at,
            updated_at=model.updated_at,
            locked_until=model.locked_until,
            failed_attempts=model.failed_attempts,
        )
        return user

    def to_dict(self, user: models.User) -> dict:
        return {
            "id": user.id,
            "password": user.password,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "last_login": user.last_login,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "locked_until": user.locked_until,
            "failed_attempts": user.failed_attempts,
        }

    def create(self, user: models.User) -> models.User:
        password = make_password(user.password)
        user = User.objects.create(
            password=password,
            email=user.email or "",
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        return self.to_domain(user)
