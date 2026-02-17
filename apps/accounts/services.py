from __future__ import annotations

import re
from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction


def _coerce_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_identifier(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z]", "", value).lower()


def _build_username(user_data: dict[str, Any]) -> str:
    provider = _coerce_str(user_data.get("provider")).lower() or "oidc"
    nordic_identifier = _normalize_identifier(
        _coerce_str(user_data.get("nordic_identifier"))
    )
    subject = _normalize_identifier(_coerce_str(user_data.get("sub")))

    if nordic_identifier:
        base_username = f"{provider}_{nordic_identifier}"
    elif subject:
        base_username = f"{provider}_{subject}"
    else:
        email = _coerce_str(user_data.get("email")).lower()
        local_part = email.split("@", maxsplit=1)[0] if email else "user"
        base_username = f"{provider}_{_normalize_identifier(local_part) or 'user'}"

    return base_username[:150]


def _next_available_username(user_model: Any, base_username: str) -> str:
    if not user_model.objects.filter(username=base_username).exists():
        return base_username

    for counter in range(1, 10_000):
        suffix = f"_{counter}"
        candidate = f"{base_username[: 150 - len(suffix)]}{suffix}"
        if not user_model.objects.filter(username=candidate).exists():
            return candidate

    raise RuntimeError("Could not allocate unique username for OIDC account")


@transaction.atomic
def account_create_from_oidc(user_data: dict[str, Any]) -> Any:
    """Match or create a user from Nordic OIDC claims inside one transaction."""
    user_model = get_user_model()

    normalized_email = _coerce_str(user_data.get("email")).lower()
    first_name = _coerce_str(user_data.get("first_name"))
    last_name = _coerce_str(user_data.get("last_name"))
    username_base = _build_username(user_data)

    user = user_model.objects.select_for_update().filter(username=username_base).first()
    if user is None and normalized_email:
        user = (
            user_model.objects.select_for_update()
            .filter(email__iexact=normalized_email)
            .order_by("id")
            .first()
        )

    if user is None:
        username = _next_available_username(user_model, username_base)
        user = user_model(
            username=username,
            email=normalized_email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_unusable_password()
        user.save()
        return user

    update_fields: list[str] = []
    if normalized_email and not _coerce_str(user.email):
        user.email = normalized_email
        update_fields.append("email")
    if first_name and not _coerce_str(user.first_name):
        user.first_name = first_name
        update_fields.append("first_name")
    if last_name and not _coerce_str(user.last_name):
        user.last_name = last_name
        update_fields.append("last_name")

    if update_fields:
        user.save(update_fields=update_fields)

    return user
