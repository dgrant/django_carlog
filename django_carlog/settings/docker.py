"""Docker/production settings for Linode deployment."""

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *


SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
SITE_ID = int(os.environ.get("SITE_ID", "1"))
DEBUG = False

allowed_hosts_env = os.environ.get("DJANGO_ALLOWED_HOSTS")
if not allowed_hosts_env:
    msg = "DJANGO_ALLOWED_HOSTS environment variable must be set for docker settings."
    raise ImproperlyConfigured(msg)
ALLOWED_HOSTS = allowed_hosts_env.split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "carlog"),
        "USER": os.environ.get("DB_USER", "carlog"),
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "172.17.0.1"),  # Docker host gateway
        "PORT": os.environ.get("DB_PORT", ""),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
            "collation": "utf8mb4_unicode_ci",
        },
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname}: {name}.{message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": os.environ.get("LOG_LEVEL", "INFO"),
    },
}

# Auth settings
LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/"

# Security headers (nginx handles SSL termination)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host and host != "*"]
