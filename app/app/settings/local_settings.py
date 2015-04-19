from .base import *
import sys

ADMINS = (
    ('GS Admin', 'contact@guerillasoftware.net'),
)

SETTINGS_TYPE = 'LOCAL'
ASSETS_DEBUG = True
COMPRESS_ENABLED = False

MEDIA_ROOT = PROJECT_DIR.child("media")
STATIC_ROOT = PROJECT_DIR.child("static")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'movements',                      # Or path to database file if using sqlite3.
        'USER': 'movements',                      # Not used with sqlite3.
        'PASSWORD': 'movements',                  # Not used with sqlite3.
        'HOST': 'localhost',                # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8080/solr'
    }
}

if os.environ.get('SITES_REDIRECT', 'false').lower() == 'true':
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('app.middleware.SitesRedirect', )

if 'test' in sys.argv or 'tests' in sys.argv:
    SOUTH_TESTS_MIGRATE = False
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': 'http://127.0.0.1:8080/solr/test_core'
        }
    }

# EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
# EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', False)
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'guerillasoftwaretest@gmail.com')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '@V:;]fNo?Gn<yxck')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@movements.org')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sandbox.kybervision@gmail.com'
EMAIL_HOST_PASSWORD = 'hortonCVT'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'sandbox.kybervision@gmail.com'


PROJECT_PATH = '/home/alexander/projects/movements/app'

# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
INSTALLED_APPS += (
    #'debug_toolbar',
    'fixture_magic',
)

#MIDDLEWARE_CLASSES += (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
#)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)
########## END TOOLBAR CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'rosetta': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'notso-unique-snowflake'
    },
    'default': {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379:1",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    },
}
########## END CACHE CONFIGURATION

######## GOOGLE TRANSLATE API KEY
GOOGLE_TRANSLATE_API_KEY = "AIzaSyAytchLuU7GTVWpH3Ckt1ilD6aK1FNF2eg"
GOOGLE_TRANSLATE_BASE = "https://www.googleapis.com/language/translate/v2?"
######## END GOOGLE TRANSLATE API KEY
