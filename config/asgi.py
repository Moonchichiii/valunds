"""ASGI config for Valund, ready for uvicorn high-concurrency execution."""
"""ASGI config for Valund."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_asgi_application()
