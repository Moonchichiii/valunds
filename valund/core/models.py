from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    FREELANCER = "freelancer", "Freelancer"
    CLIENT = "client", "Client"
    ADMIN = "admin", "Admin"


class VerificationTier(models.IntegerChoices):
    BASIC = 1, "Tier 1"
    VERIFIED = 2, "Tier 2"
    TRUSTED = 3, "Tier 3"


class EscrowStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    FUNDED = "funded", "Funded"
    RELEASED = "released", "Released"
    DISPUTED = "disputed", "Disputed"


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.FREELANCER)


class CompetencePassport(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="passport")
    verification_tier = models.PositiveSmallIntegerField(
        choices=VerificationTier.choices,
        default=VerificationTier.BASIC,
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True)


class Credential(models.Model):
    passport = models.ForeignKey(
        CompetencePassport,
        on_delete=models.CASCADE,
        related_name="credentials",
    )
    title = models.CharField(max_length=255)
    issuing_body = models.CharField(max_length=255)
    license_id = models.CharField(max_length=128, blank=True)
    expires_at = models.DateField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)


class Booking(models.Model):
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings_as_freelancer",
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings_as_client",
    )
    title = models.CharField(max_length=255)
    amount_sek = models.DecimalField(max_digits=10, decimal_places=2)
    escrow_status = models.CharField(
        max_length=20,
        choices=EscrowStatus.choices,
        default=EscrowStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews_left")
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["booking", "reviewer", "reviewee"],
                name="unique_review_direction_per_booking",
            )
        ]
