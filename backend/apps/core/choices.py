"""
Core choice enums for the Valunds platform.
"""

from django.db import models


class UserRole(models.TextChoices):
    """
    User role types in the platform.

    - EMPLOYER: Can post jobs, view applications, hire
    - JOB_SEEKER: Can apply to jobs, build CV, get matched
    - STAFF: Platform staff with analytics and moderation access
    """

    EMPLOYER = "EMPLOYER", "Employer"
    JOB_SEEKER = "JOB_SEEKER", "Job Seeker"
    STAFF = "STAFF", "Staff"


class ApplicationStatus(models.TextChoices):
    """Application workflow states."""

    SUBMITTED = "SUBMITTED", "Submitted"
    UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
    INTERVIEW = "INTERVIEW", "Interview"
    OFFER = "OFFER", "Offer"
    REJECTED = "REJECTED", "Rejected"
    HIRED = "HIRED", "Hired"
    WITHDRAWN = "WITHDRAWN", "Withdrawn"


class JobStatus(models.TextChoices):
    """Job posting states."""

    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    PAUSED = "PAUSED", "Paused"
    CLOSED = "CLOSED", "Closed"
    ARCHIVED = "ARCHIVED", "Archived"


class ContractStatus(models.TextChoices):
    """Contract workflow states."""

    DRAFT = "DRAFT", "Draft"
    SENT = "SENT", "Sent"
    SIGNED = "SIGNED", "Signed"
    ACTIVE = "ACTIVE", "Active"
    COMPLETED = "COMPLETED", "Completed"
    VOID = "VOID", "Void"


class ModerationStatus(models.TextChoices):
    """Content moderation states."""

    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    FLAGGED = "FLAGGED", "Flagged"
    REJECTED = "REJECTED", "Rejected"
