from django.db import transaction
from passports.models import Credential, VerificationStatus


@transaction.atomic
def credential_verify_tier3(credential_id: str) -> Credential:
    """Safely verify a credential."""
    credential = Credential.objects.select_for_update().get(id=credential_id)
    credential.status = VerificationStatus.VERIFIED
    credential.save()
    return credential
