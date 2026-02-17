from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    FREELANCER = "freelancer", "Freelancer"
    CLIENT = "client", "Client"
    ADMIN = "admin", "Admin"


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.FREELANCER,
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
