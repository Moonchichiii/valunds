from __future__ import annotations

from django.db import transaction
from django.utils import timezone
from passports.models import Credential, VerificationStatus


@transaction.atomic
def credential_verify_tier3(credential_id: str) -> Credential:
    """Mark a credential as verified under row lock to avoid race conditions."""
    credential = Credential.objects.select_for_update().get(id=credential_id)
    credential.status = VerificationStatus.VERIFIED
    credential.save(update_fields=["status", "updated_at"])
    return credential


def credential_audit_expiry() -> int:
    """Flag expired licenses so marketplace matching remains compliant."""
    expired_count = Credential.objects.filter(
        expiry_date__lt=timezone.now().date(),
        status=VerificationStatus.VERIFIED,
    ).update(status=VerificationStatus.EXPIRED)
    return int(expired_count)
