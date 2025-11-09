"""
Django admin configuration for core models.
"""

from django.contrib import admin

from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin interface for Address model."""

    list_display = [
        "city",
        "country",
        "postal_code",
        "is_geocoded",
        "created_at",
    ]

    list_filter = [
        "country",
        "created_at",
    ]

    search_fields = [
        "city",
        "street",
        "postal_code",
    ]

    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        ("Location", {"fields": ("street", "postal_code", "city", "region", "country")}),
        ("Geocoding", {"fields": ("latitude", "longitude"), "classes": ("collapse",)}),
        ("Metadata", {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)}),
    )
