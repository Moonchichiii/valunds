from accounts.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.services import profile_initialize_for_user


@receiver(post_save, sender=CustomUser)
def ensure_profile_for_user(
    sender: type[CustomUser],
    instance: CustomUser,
    created: bool,
    **_: object,
) -> None:
    """Automatically provision profile records for newly registered users."""
    _ = sender
    if created:
        profile_initialize_for_user(
            instance,
            full_name=instance.get_full_name(),
        )
