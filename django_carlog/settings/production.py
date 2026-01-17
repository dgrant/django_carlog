"""Production settings for Render deployment."""

import os

import dj_database_url

from .base import *


# Security settings
SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = False

# Allowed hosts from environment
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Add Render's default domain pattern
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# CSRF trusted origins for HTTPS
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host]

# Database configuration - use DATABASE_URL from Render PostgreSQL
# Falls back to MySQL config for production with external MySQL
DATABASE_URL = os.environ.get("DATABASE_URL")
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
