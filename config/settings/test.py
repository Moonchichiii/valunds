"""Test settings."""

from .base import *

SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="test-secret-key")
DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.sqlite3",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
