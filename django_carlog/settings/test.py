import os

from .base import *


DEBUG = True

# Allow Django to run synchronous database operations in async contexts
# This is needed for pytest-playwright E2E tests
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

# Secret key for testing only
SECRET_KEY = "test-secret-key-not-for-production-use-only-in-tests"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

# Faster password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable email verification for tests
ACCOUNT_EMAIL_VERIFICATION = "none"

# Root URL conf for tests
ROOT_URLCONF = "django_carlog.urls"
