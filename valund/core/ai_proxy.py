from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

PERSONNUMMER_RE = re.compile(r"\b\d{6}[-+]?\d{4}\b")
EMAIL_RE = re.compile(r"\b[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\+?\d[\d\s-]{7,}\d")


@dataclass(frozen=True)
class AnonymizedCompetenceProfile:
    profile_id: str
    verification_tier: int
    skills: list[str]
    credentials: list[dict[str, Any]]
    narrative: str


def scrub_text(value: str) -> str:
    redacted = PERSONNUMMER_RE.sub("[REDACTED_PERSONNUMMER]", value)
    redacted = EMAIL_RE.sub("[REDACTED_EMAIL]", redacted)
    redacted = PHONE_RE.sub("[REDACTED_PHONE]", redacted)
    return redacted


def anonymize_passport(passport_payload: dict[str, Any]) -> AnonymizedCompetenceProfile:
    """Convert a passport payload into an LLM-safe profile.

    The payload must not forward names, personnummer, or exact address fields.
    """
    raw_skills = passport_payload.get("skills", [])
    skills = [scrub_text(str(skill)) for skill in raw_skills]

    raw_credentials = passport_payload.get("credentials", [])
    credentials: list[dict[str, Any]] = []
    for credential in raw_credentials:
        title = scrub_text(str(credential.get("title", "")))
        issuing_body = scrub_text(str(credential.get("issuing_body", "")))
        credentials.append(
            {
                "title": title,
                "issuing_body": issuing_body,
                "expires_at": credential.get("expires_at"),
            }
        )

    narrative = scrub_text(str(passport_payload.get("summary", "")))
    return AnonymizedCompetenceProfile(
        profile_id=str(passport_payload.get("passport_id", "unknown")),
        verification_tier=int(passport_payload.get("verification_tier", 1)),
        skills=skills,
        credentials=credentials,
        narrative=narrative,
    )
