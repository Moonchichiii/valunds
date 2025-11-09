from datetime import timedelta
import os
from pathlib import Path

from decouple import Config, Csv, RepositoryEnv, config as base_config
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

DJANGO_ENV = os.getenv("DJANGO_ENV", "dev")
env_path = BASE_DIR / f".env.{DJANGO_ENV}"
config = Config(RepositoryEnv(str(env_path))) if env_path.exists() else base_config

# Core Settings
SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv(), default="localhost,127.0.0.1")

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
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
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
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.DefaultPagination",
    "PAGE_SIZE": 20,
}

SPECTACULAR_SETTINGS = {"TITLE": "Valund API", "VERSION": "0.1.0"}

# JWT Settings
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}

# Email Configuration (generic SMTP)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="no-reply@valunds.com")

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
AUTH_USER_MODEL = "accounts.User"

# Authentication backends (needed for django-allauth)
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Allauth / dj-rest-auth (email-first)
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_ADAPTER = "allauth.account.adapter.DefaultAccountAdapter"

# dj-rest-auth → use the canonical flag name
REST_USE_JWT = True

# Let allauth know there is no username field on the custom user
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# dj-rest-auth serializers
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "apps.accounts.serializers.CustomRegisterSerializer",
}
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "apps.accounts.serializers.UserSerializer",
}

# CSRF trusted origins (add your frontend URL(s) in .env)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", cast=Csv(), default="http://localhost,https://localhost"
)

# (Optional but recommended) If you'll be behind a proxy/ingress in prod
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
