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
