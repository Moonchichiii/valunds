from core.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(BaseModel, AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=[
            ("freelancer", "Freelancer"),
            ("client", "Client"),
            ("admin", "Admin"),
        ],
        default="freelancer",
    )

    class Meta:
        db_table = "auth_user"
class UserRole(models.TextChoices):
    FREELANCER = "freelancer", "Freelancer"
    CLIENT = "client", "Client"
    ADMIN = "admin", "Admin"


class CustomUser(BaseModel, AbstractUser):
class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.FREELANCER,
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
