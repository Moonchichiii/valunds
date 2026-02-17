from __future__ import annotations

from core.models import BaseModel
from django.db import models
from profiles.models import Profile


class CompetenceSector(models.TextChoices):
    HEALTHCARE = "HEALTH", "Healthcare & Medical"
    INDUSTRIAL = "INDUS", "Industrial & Blue-Collar"
    EDUCATION = "EDU", "Education & Teaching"
    TECH = "TECH", "Technology & Creative"


class VerificationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending Verification"
    VERIFIED = "VERIFIED", "Tier 3 - Verified"
    EXPIRED = "EXPIRED", "Expired/Requires Refresh"
    REJECTED = "REJECTED", "Rejected"


class CompetencePassport(BaseModel):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="passport",
    )
    sector = models.CharField(
        max_length=10,
        choices=CompetenceSector.choices,
        default=CompetenceSector.TECH,
    )
    is_public = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Passport<{self.profile_id}>:{self.sector}"


class Credential(BaseModel):
    """Individual certifications and licenses linked to a competence passport."""

    passport = models.ForeignKey(
        CompetencePassport,
        on_delete=models.CASCADE,
        related_name="credentials",
    )
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )
    evidence_file = models.FileField(
        upload_to="passports/evidence/",
        null=True,
        blank=True,
    )

    class Meta:
        indexes = [models.Index(fields=["status", "expiry_date"])]

    def __str__(self) -> str:
        return f"Credential<{self.name}>:{self.status}"
