"""Unified Nordic identity provider adapter definitions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class IdentityProviderConfig:
    provider_key: str
    display_name: str
    country_codes: tuple[str, ...]
    protocol: str = "oidc"


NORDIC_IDENTITY_PROVIDERS: dict[str, IdentityProviderConfig] = {
    "bankid": IdentityProviderConfig(
        provider_key="bankid",
        display_name="BankID",
        country_codes=("SE", "NO"),
    ),
    "mitid": IdentityProviderConfig(
        provider_key="mitid",
        display_name="MitID",
        country_codes=("DK",),
    ),
    "ftn": IdentityProviderConfig(
        provider_key="ftn",
        display_name="Finnish Trust Network",
        country_codes=("FI",),
    ),
}
