"""
Core abstract models and shared models for the Valunds platform.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Abstract model providing automatic created_at and updated_at timestamps.

    All models should inherit this for audit trail.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
        help_text=_("Timestamp when this record was created"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
        help_text=_("Timestamp when this record was last updated"),
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class UUIDModel(models.Model):
    """
    Abstract model providing UUID as primary key.

    Use this for models exposed in public APIs to avoid sequential ID enumeration.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID"),
        help_text=_("Unique identifier (UUID)"),
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract model providing soft delete functionality.

    Records are marked as deleted but not removed from the database.
    Use custom manager to filter out deleted records by default.
    """

    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_("Is deleted"),
        help_text=_("Soft delete flag - record is hidden but not removed"),
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Deleted at"),
        help_text=_("Timestamp when this record was soft-deleted"),
    )

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        """Mark this record as deleted."""
        from django.utils import timezone

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self) -> None:
        """Restore a soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


class Address(UUIDModel, TimeStampedModel):
    """
    Reusable address model for profiles and organizations.

    Supports Nordic countries (SE, NO, DK, FI, IS) primarily.
    """

    # Core address fields
    street = models.CharField(max_length=255, blank=True, verbose_name=_("Street address"))
    postal_code = models.CharField(max_length=20, blank=True, verbose_name=_("Postal code"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    region = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Region/State"),
        help_text=_("E.g., län, fylke, landsdel"),
    )
    country = models.CharField(
        max_length=2,
        default="SE",
        verbose_name=_("Country"),
        help_text=_("ISO 3166-1 alpha-2 code (SE, NO, DK, FI, IS)"),
    )

    # Optional geocoding (for future map features)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name=_("Latitude")
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, verbose_name=_("Longitude")
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        indexes = [
            models.Index(fields=["country", "city"]),
            models.Index(fields=["postal_code"]),
        ]

    def __str__(self) -> str:
        """Human-readable address string."""
        parts = [self.street, self.postal_code, self.city, self.country]
        return ", ".join(filter(None, parts))

    @property
    def is_geocoded(self) -> bool:
        """Check if this address has geocoding data."""
        return self.latitude is not None and self.longitude is not None
