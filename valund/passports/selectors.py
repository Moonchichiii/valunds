from django.db.models import QuerySet

from valund.passports.models import CompetencePassport


def passport_detail(user_id: str) -> CompetencePassport:
    """Return a passport with prefetched credentials to avoid N+1 queries."""
    query = CompetencePassport.objects.prefetch_related("credentials")
    return query.get(user_id=user_id)


def passport_credentials(user_id: str) -> QuerySet[CompetencePassport]:
    """Return query for passport lookup operations by user id."""
    return CompetencePassport.objects.filter(user_id=user_id).prefetch_related(
        "credentials"
    )
