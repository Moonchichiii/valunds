from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from profiles.models import Profile


def profile_get_searchable_base() -> QuerySet[Profile]:
    """Base queryset for marketplace discovery using verified identities only."""
    return Profile.objects.filter(
        is_identity_verified=True,
        user__is_active=True,
    ).select_related("user")


async def profile_get_searchable_base_async() -> list[Profile]:
    """Async selector for I/O-heavy profile discovery contexts."""
    return await sync_to_async(list)(profile_get_searchable_base())
