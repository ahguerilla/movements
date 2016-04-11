from .base import *
import sys

########## DEBUG CONFIGURATION
ADMINS = (
    ('GS Admin', 'contact@guerillasoftware.net'),
)

DEBUG = True
ASSETS_DEBUG = True
COMPRESS_ENABLED = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
BASE_URL = 'http://localhost:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('RDS_DB_NAME', ''),
        'USER': os.environ.get('RDS_USERNAME', ''),
        'PASSWORD': os.environ.get('RDS_PASSWORD', ''),
        'HOST': os.environ.get('RDS_HOSTNAME', ''),
        'PORT': os.environ.get('RDS_PORT', ''),
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

########## EMAIL CONFIGURATION
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', False)
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', '')
########## END EMAIL CONFIGURATION

########## DEBUG TOOLBAR CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
INSTALLED_APPS += (
    #'debug_toolbar',
    'fixture_magic',
)

# MIDDLEWARE_CLASSES += (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
# )

# DEBUG_TOOLBAR_PATCH_SETTINGS = False

INTERNAL_IPS = ('127.0.0.1',)
########## END DEBUG TOOLBAR CONFIGURATION

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
GOOGLE_TRANSLATE_API_KEY = os.environ.get('GOOGLE_TRANSLATE_API_KEY', '')
GOOGLE_TRANSLATE_BASE = "https://www.googleapis.com/language/translate/v2?"
######## END GOOGLE TRANSLATE API KEY


SOUTH_MIGRATION_MODULES = {}
LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['loggers']['django.db'] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': False,
}
BASE_URL = 'http://localhost:8000'
TINYMCE_JS_URL = 'http://localhost:8000/admintinymce/tiny_mce.js'
TINYMCE_JS_ROOT = 'http://localhost:8000/admintinymce/tiny_mce'
########## END DEBUG CONFIGURATION
