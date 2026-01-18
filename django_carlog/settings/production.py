"""Production settings for Render deployment."""

import os
import sys

import dj_database_url

from .base import *


# Security settings
SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

# Allowed hosts from environment
_allowed_hosts_env = os.environ.get("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_env.split(",") if h.strip()]

# Add Render's default domain pattern
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Always allow Render domain patterns (wildcard and explicit)
# This ensures the app works even if RENDER_EXTERNAL_HOSTNAME isn't set
ALLOWED_HOSTS.extend([
    ".onrender.com",  # Wildcard for all Render subdomains
    "django-carlog.onrender.com",  # Explicit hostname
])

# Remove duplicates while preserving order
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))

# CSRF trusted origins for HTTPS
# Note: ALLOWED_HOSTS uses ".domain.com" for wildcards, but CSRF_TRUSTED_ORIGINS uses "*.domain.com"
CSRF_TRUSTED_ORIGINS = []
for host in ALLOWED_HOSTS:
    if host:
        if host.startswith("."):
            # Convert ".domain.com" wildcard to "*.domain.com" format for CSRF
            CSRF_TRUSTED_ORIGINS.append(f"https://*{host}")
        else:
            CSRF_TRUSTED_ORIGINS.append(f"https://{host}")

# Database configuration - use DATABASE_URL from Render PostgreSQL
# Falls back to MySQL config for production with external MySQL
DATABASE_URL = os.environ.get("DATABASE_URL")

# Debug logging - print to stdout so it appears in Render logs
print(f"[DJANGO_CARLOG] DEBUG mode: {DEBUG}", file=sys.stderr)
print(f"[DJANGO_CARLOG] ALLOWED_HOSTS: {ALLOWED_HOSTS}", file=sys.stderr)
print(f"[DJANGO_CARLOG] CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}", file=sys.stderr)
print(f"[DJANGO_CARLOG] RENDER_EXTERNAL_HOSTNAME: {RENDER_EXTERNAL_HOSTNAME}", file=sys.stderr)
print(f"[DJANGO_CARLOG] DATABASE_URL set: {bool(DATABASE_URL)}", file=sys.stderr)
if DATABASE_URL:
    # Render PostgreSQL (simplest for testing)
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # External MySQL (for production with your own MySQL server)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DB_NAME", "carlog"),
            "USER": os.environ.get("DB_USER", "carlog"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "3306"),
            "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
        }
    }

# Security middleware settings for HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Static files with WhiteNoise
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Logging configuration for Render - output to stdout/stderr
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "trips": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
