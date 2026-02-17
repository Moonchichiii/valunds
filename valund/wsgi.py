"""WSGI config for Valund."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "valund.settings")

application = get_wsgi_application()
