from core.ai_proxy import passport_to_anonymized_profile


def test_passport_to_anonymized_profile_redacts_sensitive_fields() -> None:
    payload = {
        "verification_tier": 3,
        "headline": "Name: Ada Lovelace",
        "summary": "Personnummer 850709-9805, address 123 45 Stockholm",
        "credentials": [
            {
                "title": "Machine Operator",
                "issuing_body": "Name Authority",
            }
        ],
    }

    profile = passport_to_anonymized_profile(payload)

    assert profile.verification_tier == 3
    assert "Ada" in profile.headline
    assert "[REDACTED]" in profile.headline
    assert "[REDACTED_PERSONNUMMER]" in profile.summary
    assert "[REDACTED_POSTCODE]" in profile.summary
    assert "[REDACTED]" in profile.credential_summaries[0]
