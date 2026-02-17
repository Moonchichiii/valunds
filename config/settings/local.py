"""Local development settings."""

from .base import *

DEBUG = True
SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="dev-secret-key-12345")

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://postgres:postgres@localhost:5432/valund",
    )
}

if env.bool("DJANGO_ENABLE_DEBUG_TOOLBAR", default=False):
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = ["127.0.0.1"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
