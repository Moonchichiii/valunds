from passports.models import CompetencePassport
from rest_framework import serializers


class PassportSerializer(serializers.ModelSerializer[CompetencePassport]):
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
