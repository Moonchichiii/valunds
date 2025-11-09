"""
Utility functions for the Valunds platform.
"""

import re
from typing import Any

from django.utils import timezone
from django.utils.text import slugify


def now():
    """
    Get current timezone-aware datetime.

    Returns:
        datetime: Current time in UTC with timezone info
    """
    return timezone.now()


def generate_slug(text: str, max_length: int = 50) -> str:
    """
    Generate a URL-safe slug from text.

    Args:
        text: Input text to slugify
        max_length: Maximum length of the slug

    Returns:
        str: URL-safe slug

    Example:
        >>> generate_slug("Full Stack Developer @ Göteborg")
        'full-stack-developer-goteborg'
    """
    # Replace Swedish/Nordic characters
    replacements = {
        "å": "a",
        "ä": "a",
        "ö": "o",
        "æ": "ae",
        "ø": "o",
        "Å": "A",
        "Ä": "A",
        "Ö": "O",
        "Æ": "AE",
        "Ø": "O",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    slug = slugify(text)
    return slug[:max_length] if slug else "item"


def safe_get(obj: Any, attr: str, default: Any = None) -> Any:
    """
    Safely get an attribute from an object.

    Args:
        obj: Object to get attribute from
        attr: Attribute name (supports dot notation: 'user.profile.name')
        default: Default value if attribute doesn't exist

    Returns:
        Attribute value or default

    Example:
        >>> safe_get(job, "organization.owner.email", "unknown@example.com")
        'employer@company.com'
    """
    try:
        for part in attr.split("."):
            obj = getattr(obj, part, None)
            if obj is None:
                return default
        return obj
    except (AttributeError, TypeError):
        return default


def normalize_phone(phone: str) -> str:
    """
    Normalize phone number to E.164 format.

    Args:
        phone: Input phone number (various formats)

    Returns:
        str: Normalized phone number

    Example:
        >>> normalize_phone("070-123 45 67")
        '+46701234567'
    """
    # Remove all non-digit characters
    digits = re.sub(r"\D", "", phone)

    # Add Swedish country code if missing (default for Nordic platform)
    if not digits.startswith("46") and len(digits) == 10:
        digits = "46" + digits[1:]  # Remove leading 0

    return f"+{digits}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to max length with suffix.

    Args:
        text: Input text
        max_length: Maximum length (including suffix)
        suffix: Suffix to append if truncated

    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)].rstrip() + suffix
