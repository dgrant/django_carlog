from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'carlog_django',                      # Or path to database file if using sqlite3.
        'USER': 'carlog_django',                      # Not used with sqlite3.
        'PASSWORD': 'carlog_django',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}

#INSTALLED_APPS += ('debug_toolbar',)
#INTERNAL_IPS = ("127.0.0.1", )
#DEBUG_TOOLBAR_CONFIG = {'DISABLE_PANELS': ['debug_toolbar.panels.redirects.RedirectsPanel']}
#MIDDLEWARE_CLASSES += \
#    ("debug_toolbar.middleware.DebugToolbarMiddleware", )
