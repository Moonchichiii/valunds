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
