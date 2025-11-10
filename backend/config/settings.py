"""
Django settings for Valund project.
"""

from datetime import timedelta
import os
from pathlib import Path

from decouple import Config, Csv, RepositoryEnv
import dj_database_url


# =============================================================================
# PATH & ENVIRONMENT CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DJANGO_ENV = os.getenv("DJANGO_ENV", "dev")
env_path = BASE_DIR / f".env.{DJANGO_ENV}"
config = Config(RepositoryEnv(str(env_path)))


# =============================================================================
# CORE DJANGO SETTINGS
# =============================================================================

SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv(), default="localhost,127.0.0.1")
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
SITE_ID = 1
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =============================================================================
# INSTALLED APPLICATIONS
# =============================================================================

INSTALLED_APPS = [
    # Django Core Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third Party Apps - Authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    # Third Party Apps - API & Utils
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # Third Party Apps - Security & Storage
    "axes",
    "cloudinary",
    "cloudinary_storage",
    "django_cryptography",
    # Local Apps
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


# =============================================================================
# MIDDLEWARE CONFIGURATION
# =============================================================================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
]


# =============================================================================
# TEMPLATE CONFIGURATION
# =============================================================================

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


# =============================================================================
# DATABASE CONFIGURATION & Cache Settings
# =============================================================================

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

REDIS_URL = config("REDIS_URL", default="")

if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            "KEY_PREFIX": "valund",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "valund-local",
        }
    }


RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"
RATELIMIT_CACHE_PREFIX = "rl:"
# RATELIMIT_VIEW = "apps.api.views.ratelimited"  # only for middleware-based global blocking

# =============================================================================
# INTERNATIONALIZATION & LOCALIZATION
# =============================================================================

LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Stockholm"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locale"]


# =============================================================================
# STATIC FILES & MEDIA CONFIGURATION
# =============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    "default": {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"},
}

# Cloudinary Configuration
CLOUDINARY_URL = config("CLOUDINARY_URL", default="")


# =============================================================================
# CORS CONFIGURATION
# =============================================================================

# Frontend base (env-driven)
FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:5173")

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    cast=Csv(),
    default=f"{FRONTEND_URL},https://valunds.se,https://www.valunds.se",
)
CORS_ALLOW_CREDENTIALS = True


# =============================================================================
# DJANGO REST FRAMEWORK CONFIGURATION
# =============================================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.DefaultPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/min",
        "user": "300/min",
        # Scoped:
        "me": "60/min",
        "profile": "30/min",
        "login": "15/min",
        "password_reset": "5/min",
    },
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "EXCEPTION_HANDLER": "apps.core.exceptions.problem_exception_handler",
}

if DEBUG:
    # Nice to have the browsable API in dev only
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
        *REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"],
        "rest_framework.renderers.BrowsableAPIRenderer",
    )


# API Documentation
SPECTACULAR_SETTINGS = {
    "TITLE": "Valund API",
    "VERSION": "0.1.0",
    "SERVERS": [{"url": "/api"}],
    "SECURITY": [{"bearerAuth": []}],
    "COMPONENTS": {
        "securitySchemes": {
            "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }
    },
}


# =============================================================================
# JWT AUTHENTICATION CONFIGURATION
# =============================================================================

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}


# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="send.one.com")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=465)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=True)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=False)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="Valunds <kontakt@valunds.se>")
SERVER_EMAIL = config("SERVER_EMAIL", default="errors@valunds.se")

# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "blob:", "*.cloudinary.com")

# Axes (Brute Force Protection)
AXES_ENABLED = True
AXES_FAILURE_LIMIT = config("AXES_FAILURE_LIMIT", cast=int, default=5)
AXES_COOLOFF_TIME = timedelta(hours=1)
AXES_LOCK_OUT_AT_FAILURE = True
AXES_RESET_ON_SUCCESS = True
AXES_USERNAME_FORM_FIELD = "email"

# CSRF Protection
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    cast=Csv(),
    default=f"{FRONTEND_URL},https://valunds.se,https://www.valunds.se",
)

# Cookie SameSite settings
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# Environment-specific security settings
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False

# Common security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # if behind proxy


# =============================================================================
# AUTHENTICATION & USER MODEL CONFIGURATION
# =============================================================================

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Authentication Backends
AUTHENTICATION_BACKENDS = (
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# =============================================================================
# DJANGO-ALLAUTH CONFIGURATION
# =============================================================================

# ---- Compatibility flags for dj-rest-auth (keep these for backwards support) ----
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# ---- Modern allauth configuration ----
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_PREVENT_ENUMERATION = True

# Signup Configuration
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]

# Email Verification
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Valunds] "

# Protocol for allauth-generated links
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http" if DJANGO_ENV == "dev" else "https"

# Redirects after email confirmation (SPA handles the UX)
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = f"{FRONTEND_URL}/auth/verified"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = f"{FRONTEND_URL}/app"

# W001 on some allauth versions
SILENCED_SYSTEM_CHECKS = ["account.W001"]

# Social Account Providers
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config("GOOGLE_CLIENT_ID", default=""),
            "secret": config("GOOGLE_CLIENT_SECRET", default=""),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "offline"},
    },
    "github": {
        "APP": {
            "client_id": config("GITHUB_CLIENT_ID", default=""),
            "secret": config("GITHUB_CLIENT_SECRET", default=""),
            "key": "",
        },
        "SCOPE": ["user:email"],
    },
}


# =============================================================================
# DJ-REST-AUTH CONFIGURATION
# =============================================================================

REST_AUTH = {
    "USE_JWT": True,
    "TOKEN_MODEL": None,
    "SESSION_LOGIN": False,
}

# Custom Serializers
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "apps.accounts.serializers.CustomRegisterSerializer",
}
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "apps.accounts.serializers.UserSerializer",
}
