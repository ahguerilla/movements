from .base import *

MEDIA_ROOT = PROJECT_DIR.child("media")
STATIC_ROOT = PROJECT_DIR.child("static")

DEBUG = False
ASSETS_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ahr',                      # Or path to database file if using sqlite3.
        'USER': 'ahr',                      # Not used with sqlite3.
        'PASSWORD': 'hMWQWaJmxM2xSUmmCLRPw41CB',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'guerillasoftwaretest@gmail.com'
EMAIL_HOST_PASSWORD = '@V:;]fNo?Gn<yxck'


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8080/solr'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8080/solr/mysite',
    },
}

