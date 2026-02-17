from passports.models import CompetencePassport
from rest_framework import serializers


class PassportSerializer(serializers.ModelSerializer[CompetencePassport]):
    profile_display_name = serializers.CharField(source="profile.display_name")

    class Meta:
        model = CompetencePassport
        fields = ["id", "profile_display_name", "sector", "is_public"]


def get_passport_data(user_id: str) -> dict[str, str | bool]:
    """Return serialized passport payload for HTMX and API consumers."""
    query = CompetencePassport.objects.select_related("profile", "profile__user")
    instance = query.get(profile__user_id=user_id)
    return dict(PassportSerializer(instance).data)
