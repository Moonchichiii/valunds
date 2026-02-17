from __future__ import annotations

from typing import Any

from accounts.identity_providers import extract_nordic_user_data
from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.dispatch import receiver
from profiles.services import profile_create_from_idp


def _sync_verified_profile(sociallogin: Any, payload: dict[str, str]) -> None:
    if not payload.get("nordic_identifier"):
        return

    profile_create_from_idp(
        sociallogin.user,
        {
            "full_name": payload.get("full_name", ""),
            "region": payload.get("region", "SE"),
        },
    )


@receiver(social_account_added)
def on_social_account_added(
    sender: Any,
    request: Any,
    sociallogin: Any,
    **_: object,
) -> None:
    _ = sender, request
    payload = extract_nordic_user_data(sociallogin, {})
    _sync_verified_profile(sociallogin, payload)


@receiver(social_account_updated)
def on_social_account_updated(
    sender: Any,
    request: Any,
    sociallogin: Any,
    **_: object,
) -> None:
    _ = sender, request
    payload = extract_nordic_user_data(sociallogin, {})
    _sync_verified_profile(sociallogin, payload)
