from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'carlog_django',                      # Or path to database file if using sqlite3.
        'USER': 'carlog_django',                      # Not used with sqlite3.
        'PASSWORD': 'carlog_django',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
		'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
	},
    }
}
