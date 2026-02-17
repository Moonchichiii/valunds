from django.contrib.auth import get_user_model
from django.db import transaction
from passports.models import Credential, CredentialStatus

User = get_user_model()


@transaction.atomic
def credential_verify_tier3(credential_id: str, admin_user: User) -> Credential:
    """Upgrade a credential to tier-3 verification safely under row lock."""
    credential = Credential.objects.select_for_update().get(id=credential_id)
    credential.status = CredentialStatus.VERIFIED
    credential.verified_by = admin_user
    credential.save(update_fields=["status", "verified_by", "updated_at"])
    return credential
