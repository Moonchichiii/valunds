import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from decouple import Config, Csv, RepositoryEnv
from decouple import config as base_config

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BASE_DIR.parent

DJANGO_ENV = os.getenv("DJANGO_ENV", "dev")
env_path = REPO_ROOT / f".env.{DJANGO_ENV}"
config = Config(RepositoryEnv(str(env_path))) if env_path.exists() else base_config

# Core Settings
SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = config(
    "DJANGO_ALLOWED_HOSTS", cast=Csv(), default="localhost,127.0.0.1"
)

# Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "drf_spectacular",
    "axes",
    "ratelimit",
    "anymail",
    "cloudinary",
    "cloudinary_storage",
    "apps.core",
    "apps.accounts",
    "apps.authn",
    "apps.profiles",
    "apps.jobs",
    "apps.applications",
    "apps.matching",
    "apps.cv",
    "apps.contracts",
    "apps.ratings",
    "apps.moderation",
    "apps.scheduling",
    "apps.payments",
    "apps.search",
    "apps.api",
]

SITE_ID = 1

# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
# Database
DATABASE_URL = config("DATABASE_URL", default="")
DATABASE_URL = config("DATABASE_URL", default="")
if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Internationalization
LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Stockholm"
USE_I18N = True
USE_TZ = True

# Static Files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
    "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
}

# Cloudinary
CLOUDINARY_URL = config("CLOUDINARY_URL", default="")

# CORS
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv(), default="")
CORS_ALLOW_CREDENTIALS = True

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {"TITLE": "Valund API", "VERSION": "0.1.0"}

# JWT Settings
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}

# Email Configuration
ANYMAIL = {
    "MAILGUN_API_KEY": config("MAILGUN_API_KEY", default=""),
    "MAILGUN_SENDER_DOMAIN": config("MAILGUN_SENDER_DOMAIN", default=""),
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"

# Security Settings
CSP_DEFAULT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:", "blob:", "*.cloudinary.com")

# Axes Configuration
AXES_FAILURE_LIMIT = config("AXES_FAILURE_LIMIT", cast=int, default=5)

# Localization
LOCALE_PATHS = [BASE_DIR / "locale"]

# Model Configuration
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom User Model
# AUTH_USER_MODEL = "accounts.User"
