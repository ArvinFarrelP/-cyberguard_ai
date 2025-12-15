"""
Django settings for cyberguardai project.
Optimized for local development & Railway deployment.
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

# =========================
# ENVIRONMENT
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file (for local & Railway)
load_dotenv(BASE_DIR / ".env")

# =========================
# SECURITY
# =========================

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "dev-key-123-change-this-in-production")

DEBUG = os.environ.get("DEBUG", "False") == "True"

# Railway domains
RAILWAY_STATIC_URL = os.environ.get("RAILWAY_STATIC_URL", "")
ALLOWED_HOSTS = []

# Tambahkan domain Railway dan localhost
if RAILWAY_STATIC_URL:
    ALLOWED_HOSTS.append(RAILWAY_STATIC_URL)
else:
    # Untuk Railway, izinkan semua subdomain railway.app
    ALLOWED_HOSTS.extend([
        "*.railway.app",
        "*.up.railway.app",
        "localhost",
        "127.0.0.1",
        "[::1]",
    ])

# CSRF settings untuk Railway
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "https://*.up.railway.app",
]

if RAILWAY_STATIC_URL:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_STATIC_URL}")

# Security settings untuk production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "chatbot",
]

# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files (Railway)
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =========================
# URL & TEMPLATES
# =========================

ROOT_URLCONF = "cyberguardai.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cyberguardai.wsgi.application"

# =========================
# DATABASE
# =========================

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False,
    )
}

# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Whitenoise configuration
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_USE_FINDERS = True

# =========================
# DEFAULT PRIMARY KEY
# =========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# API KEYS & CONFIGURATION
# =========================

# Gunakan GEMINI_API_KEY (lebih spesifik)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
# Backup: GOOGLE_API_KEY (untuk kompatibilitas)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# Logging configuration untuk debug Railway
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
