from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from accounts.services import account_create_from_oidc
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


@dataclass(frozen=True)
class IdentityProviderConfig:
    provider_key: str
    display_name: str
    country_codes: tuple[str, ...]
    identity_claims: tuple[str, ...]
    protocol: str = "oidc"


NORDIC_IDENTITY_PROVIDERS: dict[str, IdentityProviderConfig] = {
    "bankid": IdentityProviderConfig(
        provider_key="bankid",
        display_name="BankID",
        country_codes=("SE", "NO"),
        identity_claims=("ssn", "personal_identity_number", "national_id"),
    ),
    "mitid": IdentityProviderConfig(
        provider_key="mitid",
        display_name="MitID",
        country_codes=("DK",),
        identity_claims=("cpr", "civil_registration_number", "national_id"),
    ),
    "ftn": IdentityProviderConfig(
        provider_key="ftn",
        display_name="Finnish Trust Network",
        country_codes=("FI",),
        identity_claims=("hetu", "national_id", "ssn"),
    ),
}

_PROVIDER_REGION_MAP: dict[str, str] = {
    "bankid-se": "SE",
    "bankid-no": "NO",
    "bankid": "SE",
    "mitid": "DK",
    "ftn": "FI",
}


def _coerce_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_provider_key(raw_provider: str, claims: dict[str, Any]) -> str:
    provider = _coerce_str(raw_provider).lower() or "oidc"
    country = _coerce_str(
        claims.get("country") or claims.get("issuing_country")
    ).upper()
    if provider == "bankid" and country == "NO":
        return "bankid-no"
    if provider == "bankid" and country == "SE":
        return "bankid-se"
    return provider


def _extract_nordic_identifier(provider_key: str, claims: dict[str, Any]) -> str:
    provider_config = NORDIC_IDENTITY_PROVIDERS.get(provider_key.split("-")[0])
    claim_keys: tuple[str, ...]
    if provider_config is None:
        claim_keys = ("national_id", "ssn", "cpr", "hetu")
    else:
        claim_keys = provider_config.identity_claims

    for claim_key in claim_keys:
        candidate = _coerce_str(claims.get(claim_key))
        if candidate:
            return re.sub(r"[^0-9A-Za-z-]", "", candidate)
    return ""


def extract_nordic_user_data(
    sociallogin: Any,
    data: dict[str, Any],
) -> dict[str, str]:
    claims = dict(sociallogin.account.extra_data)
    claims.update(data)

    provider_key = _normalize_provider_key(sociallogin.account.provider, claims)
    given_name = _coerce_str(claims.get("given_name") or claims.get("first_name"))
    family_name = _coerce_str(claims.get("family_name") or claims.get("last_name"))
    full_name = _coerce_str(claims.get("name") or f"{given_name} {family_name}".strip())

    region = (
        _coerce_str(claims.get("country")).upper()
        or _PROVIDER_REGION_MAP.get(provider_key, "SE")
    )

    return {
        "provider": provider_key,
        "sub": _coerce_str(claims.get("sub") or sociallogin.account.uid),
        "email": _coerce_str(claims.get("email")),
        "first_name": given_name,
        "last_name": family_name,
        "full_name": full_name,
        "locale": _coerce_str(claims.get("locale")),
        "region": region,
        "nordic_identifier": _extract_nordic_identifier(provider_key, claims),
    }


class NordicOIDCAdapter(DefaultSocialAccountAdapter):
    """Allauth adapter for Nordic OIDC providers with claim normalization."""

    def populate_user(
        self,
        request: Any,
        sociallogin: Any,
        data: dict[str, Any],
    ):
        _ = request
        user_data = extract_nordic_user_data(sociallogin, data)
        return account_create_from_oidc(user_data)

    def save_user(
        self,
        request: Any,
        sociallogin: Any,
        form: Any | None = None,
    ):
        form_data: dict[str, Any] = {}
        if form is not None and hasattr(form, "cleaned_data"):
            raw_form_data = form.cleaned_data
            if isinstance(raw_form_data, dict):
                form_data = raw_form_data

        user_data = extract_nordic_user_data(sociallogin, form_data)
        user = account_create_from_oidc(user_data)
        sociallogin.user = user
        sociallogin.save(request)
        return user
