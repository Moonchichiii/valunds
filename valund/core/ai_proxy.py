"""Privacy-safe projection helpers for AI calls."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

PERSONNUMMER_PATTERN = re.compile(r"\b\d{6}[-+]?\d{4}\b")
POSTAL_CODE_PATTERN = re.compile(r"\b\d{3}\s?\d{2}\b")


@dataclass(frozen=True)
class AnonymizedCompetenceProfile:
    verification_tier: int
    headline: str
    summary: str
    credential_summaries: list[str]


def _scrub_text(value: str) -> str:
    redacted = PERSONNUMMER_PATTERN.sub("[REDACTED_PERSONNUMMER]", value)
    redacted = POSTAL_CODE_PATTERN.sub("[REDACTED_POSTCODE]", redacted)
    for token in ("name", "address"):
        redacted = re.sub(rf"\b{token}\b", "[REDACTED]", redacted, flags=re.IGNORECASE)
    return redacted


def passport_to_anonymized_profile(
    passport_payload: dict[str, Any],
) -> AnonymizedCompetenceProfile:
    """Map raw passport payload to an LLM-safe profile."""
    tier = int(passport_payload.get("verification_tier", 1))
    headline = _scrub_text(str(passport_payload.get("headline", "")))
    summary = _scrub_text(str(passport_payload.get("summary", "")))
    credentials = passport_payload.get("credentials", [])

    credential_summaries: list[str] = []
    if isinstance(credentials, list):
        for credential in credentials:
            if isinstance(credential, dict):
                title = _scrub_text(str(credential.get("title", "")))
                issuer = _scrub_text(str(credential.get("issuing_body", "")))
                credential_summaries.append(f"{title} (issuer: {issuer})")

    return AnonymizedCompetenceProfile(
        verification_tier=tier,
        headline=headline,
        summary=summary,
        credential_summaries=credential_summaries,
    )
