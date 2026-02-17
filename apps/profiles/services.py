from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import transaction
from django.utils import timezone
from profiles.models import NordicRegion, Profile

if TYPE_CHECKING:
    from accounts.models import CustomUser


@transaction.atomic
def profile_create_from_idp(user: CustomUser, idp_data: dict[str, str]) -> Profile:
    """Create or update a profile from Nordic identity provider data."""
    region = idp_data.get("region", NordicRegion.SWEDEN)

    profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            "display_name": idp_data.get("full_name", ""),
            "region": region,
            "is_identity_verified": True,
            "last_verified_at": timezone.now(),
        },
    )

    if not created:
        profile.display_name = idp_data.get("full_name", profile.display_name)
        profile.region = region
        profile.is_identity_verified = True
        profile.last_verified_at = timezone.now()
        profile.save(
            update_fields=[
                "display_name",
                "region",
                "is_identity_verified",
                "last_verified_at",
                "updated_at",
            ]
        )

    return profile


@transaction.atomic
def profile_initialize_for_user(
    user: CustomUser,
    *,
    full_name: str = "",
    region: str = NordicRegion.SWEDEN,
) -> Profile:
    """Create a default verified profile after successful authentication."""
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={
            "display_name": full_name,
            "region": region,
            "is_identity_verified": True,
            "last_verified_at": timezone.now(),
        },
    )
    return profile
