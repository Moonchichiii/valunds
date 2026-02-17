from passports.models import CompetencePassport
from rest_framework import serializers


class PassportSerializer(serializers.ModelSerializer[CompetencePassport]):
    profile_display_name = serializers.CharField(source="profile.display_name")

    class Meta:
        model = CompetencePassport
        fields = ["id", "profile_display_name", "sector", "is_public"]


def get_passport_context(user_id: str) -> dict[str, str | bool]:
    """Return serializer-backed passport context for HTMX and DRF consumers."""
    query = CompetencePassport.objects.select_related("profile", "profile__user")
    instance = query.get(profile__user_id=user_id)
    return dict(PassportSerializer(instance).data)
def get_passport_data(user_id: str) -> dict[str, str | bool]:
    """Return serialized passport payload for HTMX and API consumers."""
    query = CompetencePassport.objects.select_related("profile", "profile__user")
    instance = query.get(profile__user_id=user_id)
    return dict(PassportSerializer(instance).data)
    class Meta:
        model = CompetencePassport
        fields = ["id", "full_name", "verification_tier", "sector"]


def get_passport_data(user_id: str) -> dict[str, str | int]:
    """Selector returning a serialized structure for HTMX and API consumers."""
    query = CompetencePassport.objects.prefetch_related("credentials")
    instance = query.get(user_id=user_id)
    return dict(PassportSerializer(instance).data)
from django.db.models import QuerySet
from passports.models import CompetencePassport


def passport_detail(user_id: str) -> CompetencePassport:
    """Return a passport with prefetched credentials to avoid N+1 queries."""
    query = CompetencePassport.objects.prefetch_related("credentials")
    return query.get(user_id=user_id)


def passport_credentials(user_id: str) -> QuerySet[CompetencePassport]:
    """Return query for passport lookup operations by user id."""
    return CompetencePassport.objects.filter(user_id=user_id).prefetch_related(
        "credentials"
    )
