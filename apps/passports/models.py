from __future__ import annotations

from core.models import BaseModel
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.db import models


class VerificationTier(models.IntegerChoices):
    BASIC = 1, "Tier 1 - Basic"
    VERIFIED = 2, "Tier 2 - Verified"
    AUTHORITATIVE = 3, "Tier 3 - Authoritative"


class CredentialStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    VERIFIED = "verified", "Verified"


class CompetencePassport(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="passport",
    )
    verification_tier = models.PositiveSmallIntegerField(
        choices=VerificationTier.choices,
        default=VerificationTier.BASIC,
    )
    sector = models.CharField(max_length=64, default="general")
    headline = models.CharField(max_length=255)
    summary = models.TextField(blank=True)

    class Meta:
        indexes = [
            GinIndex(
                SearchVector("headline", "summary", "sector"),
                name="passport_search_gin_idx",
            )
        ]

    @property
    def full_name(self) -> str:
        return self.user.get_full_name() or self.user.username

    headline = models.CharField(max_length=255)
    summary = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Passport<{self.user_id}> tier={self.verification_tier}"


class Credential(BaseModel):
    passport = models.ForeignKey(
        CompetencePassport,
        on_delete=models.CASCADE,
        related_name="credentials",
    )
    title = models.CharField(max_length=255)
    issuing_body = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=CredentialStatus.choices,
        default=CredentialStatus.PENDING,
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="verified_credentials",
    )

    def __str__(self) -> str:
        return f"Credential<{self.title}> status={self.status}"
