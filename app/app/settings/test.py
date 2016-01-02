from __future__ import absolute_import

from .base import *

########## TEST SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_ROOT = SITE_ROOT
ASSETS_ROOT = SITE_ROOT + '/static'
TEST_DISCOVER_PATTERN = "test_*.py"
SECRET_KEY = 've4&7oc3yk+g-_1ob4n_$vwn_os!=t#zn38p)fw6^q9h1a()-b'
ASSETS_DEBUG = False
COOKIE_DOMAIN = None
BASE_URL = 'http://localhost:8000'
########## IN-MEMORY TEST DATABASE
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
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8080/solr'
    }
}

SOUTH_TESTS_MIGRATE = False