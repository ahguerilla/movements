### This is for the live testing environment

from .base import *
import os

ADMINS = (
    ('Guerilla Support', 'support@guerillasoftware.net'),
)

########## ASSETS CONFIGURATION
COMPRESS_ENABLED = True
DEBUG = False
ASSETS_DEBUG = False
ASSETS_AUTO_BUILD = False
ASSETS_ROOT = normpath(join(SITE_ROOT, 'static'))
########## END ASSETS CONFIGURATION


########## AWS CONFIGURATION
INSTALLED_APPS = INSTALLED_APPS + ('storages', )
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
AWS_STORAGE_BUCKET_NAME = 'exhangivist-testing-media'
AWS_HEADERS = {
    'Cache-Control': 'max-age=315360000',
}
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'app.s3storage.StaticRootS3BotoStorage'
AWS_QUERYSTRING_AUTH = False
MEDIA_URL = 'https://d1vw9gf2oosnrq.cloudfront.net/'
STATIC_URL = 'https://d1vw9gf2oosnrq.cloudfront.net/static/'
########## END AWS CONFIGURATION

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('app.middleware.SSLRedirect', )

if os.environ.get('SITES_REDIRECT', 'false').lower() == 'true':
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('app.middleware.SitesRedirect', )

if ADMIN_ENABLED:
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('app.users.middleware.ForceTwoFactorForStaffMiddleware', )

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
AVATAR_DEFAULT_URL = 'https://www.movements.org/static/avatar/img/default.jpg'

SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', True)
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', False)
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Movements.Org <noreply@movements.org>')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': os.environ.get('SOLR_URL', ''),
    },
}

CELERY_BROKER = os.environ.get('CELERY_BROKER', '')
CELERY_EMAIL_TASK_CONFIG = {
    'rate_limit': '4/s',
}

ALLOWED_HOSTS = [
    '.exchangivist.org',
    '.exchangivist.org.',
    '.movements.org',
    '.movements.org.',
    '.elasticbeanstalk.com',
    '.elasticbeanstalk.com.',
]

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'rosetta': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'notso-unique-snowflake'
    },
    'default': {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_CACHE_LOCATION', ''),
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

# Reverse id for cms pages.
CMS_PAGE_TERMS = 'acceptable_use_policy'

TWO_FACTOR_SMS_GATEWAY = 'two_factor.gateways.twilio.gateway.Twilio'
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_CALLER_ID = os.environ.get('TWILIO_CALLER_ID', '')

######## TINY MCE CONFIGURATION
TINYMCE_JS_URL = 'https://admin.movements.org/admintinymce/tiny_mce.js'
TINYMCE_JS_ROOT = 'https://admin.movements.org/admintinymce/tiny_mce'
######## END TINY MCE CONFIGURATION