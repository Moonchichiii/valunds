from core.models import BaseModel
from django.conf import settings
from django.db import models


class NordicRegion(models.TextChoices):
    SWEDEN = "SE", "Sweden"
    NORWAY = "NO", "Norway"
    DENMARK = "DK", "Denmark"
    FINLAND = "FI", "Finland"
    ICELAND = "IS", "Iceland"


class Profile(BaseModel):
    """Identity hub for personal data separated from authentication concerns."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    display_name = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to="profiles/avatars/", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    region = models.CharField(
        max_length=2,
        choices=NordicRegion.choices,
        default=NordicRegion.SWEDEN,
    )
    preferred_language = models.CharField(max_length=5, default="sv-se")

    is_identity_verified = models.BooleanField(default=False)
    last_verified_at = models.DateTimeField(null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"Profile: {self.display_name or self.user.username}"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        indexes = [models.Index(fields=["region", "is_identity_verified"])]
