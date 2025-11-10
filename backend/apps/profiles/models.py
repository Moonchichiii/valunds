from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt


class Profile(models.Model):
    """User profile with encrypted PII storage."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    phone = encrypt(models.TextField(blank=True, null=True, help_text=_("E.164 format preferred")))
    address_line1 = encrypt(models.TextField(blank=True, null=True))
    address_line2 = encrypt(models.TextField(blank=True, null=True))
    postal_code = encrypt(models.TextField(blank=True, null=True))
    city = encrypt(models.TextField(blank=True, null=True))
    region = encrypt(models.TextField(blank=True, null=True))  # county / län / fylke
    country = models.CharField(max_length=2, default="SE")  # ISO 3166-1 alpha-2

    # Preferences
    language = models.CharField(max_length=8, default="en")
    marketing_opt_in = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        return f"Profile<{self.user_id}>"
