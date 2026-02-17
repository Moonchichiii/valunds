from typing import Any

from passports.models import CompetencePassport


def get_passport_data(user_id: Any) -> dict[str, Any]:
    """Serialized passport payload for UI/API."""
    passport = CompetencePassport.objects.select_related("profile").get(
        profile__user_id=user_id
    )
    return {
        "id": str(passport.id),
        "sector": passport.sector,
        "verified": passport.profile.is_identity_verified,
    }
