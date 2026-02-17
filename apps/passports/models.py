from __future__ import annotations

from core.models import BaseModel
from django.db import models
from profiles.models import Profile


class CompetenceSector(models.TextChoices):
    HEALTHCARE = "HEALTH", "Healthcare & Medical"
    INDUSTRIAL = "INDUS", "Industrial & Blue-Collar"
    TECH = "TECH", "Technology"


class VerificationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    VERIFIED = "VERIFIED", "Verified"
    EXPIRED = "EXPIRED", "Expired"


class CompetencePassport(BaseModel):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="passport",
    )
    sector = models.CharField(max_length=10, choices=CompetenceSector.choices)


class Credential(BaseModel):
    passport = models.ForeignKey(
        CompetencePassport,
        on_delete=models.CASCADE,
        related_name="credentials",
    )
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"
