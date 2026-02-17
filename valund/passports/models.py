from django.conf import settings
from django.db import models


class VerificationTier(models.IntegerChoices):
    BASIC = 1, "Tier 1 - Basic"
    VERIFIED = 2, "Tier 2 - Verified"
    AUTHORITATIVE = 3, "Tier 3 - Authoritative"


class CompetencePassport(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="passport",
    )
    verification_tier = models.PositiveSmallIntegerField(
        choices=VerificationTier.choices,
        default=VerificationTier.BASIC,
    )
    headline = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Passport<{self.user_id}> tier={self.verification_tier}"
