# Django settings for app project.
import os
import sys

from unipath import Path
from os.path import abspath, dirname, join, normpath
from celery.schedules import crontab

########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

BASE_URL = os.environ.get('BASE_URL', 'https://www.movements.org')
BASE_ADMIN_URL = os.environ.get('BASE_ADMIN_URL', 'https://admin.movements.org')

PROJECT_DIR = Path(__file__).ancestor(3)
########## END PATH CONFIGURATION

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION

########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Guerilla Software', 'contact@guerillasoftware.net'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.lite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION

########## ENABLE ADMIN
# Enable django admin and urls
ADMIN_ENABLED = os.environ.get('ADMIN_ENABLED', 'false').lower() == 'true'
########## END ENABLE ADMIN

########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en'

LOCALE_PATHS = (
    PROJECT_DIR.child("locale"),
)

ugettext = lambda s: s
LANGUAGES = [
    ('ar', ugettext('Arabic')),
    ('en', ugettext('English')),
    ('zh-cn', ugettext('Chinese')),
    ('uk', ugettext('Ukrainian')),
    ('ru', ugettext('Russian')),
    ('fa', ugettext('Persian')),
    ('fr', ugettext('French')),
    ('es', ugettext('Spanish')),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = os.environ.get('SECRET_KEY', '')
########## END SECRET CONFIGURATION

########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']
########## END SITE CONFIGURATION

########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    PROJECT_DIR.child("fixtures"),
)
########## END FIXTURE CONFIGURATION

########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'cms.context_processors.cms_settings',
    'django.contrib.messages.context_processors.messages',
    'allauth.account.context_processors.account',
    'constance.context_processors.config',
    'allauth.socialaccount.context_processors.socialaccount',
    'postman.context_processors.inbox',
    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',
    'django.core.context_processors.static',
    'app.context_processors.string_constants',
    'app.context_processors.app_settings',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    PROJECT_DIR.child("templates"),
)
########## END TEMPLATE CONFIGURATION

########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'app.users.middleware.CsrfLoginMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'app.middleware.UserProfileLocaleMiddleware',
    #'app.market.middleware.NoUserProfile',
    'app.users.middleware.FirstLoginMiddleware',
    #'app.users.middleware.ForceTwoFactorForStaffMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
)

if ADMIN_ENABLED:
    MIDDLEWARE_CLASSES += ('cms.middleware.toolbar.ToolbarMiddleware',)

MIDDLEWARE_CLASSES += ('cms.middleware.language.LanguageCookieMiddleware',)
########## END MIDDLEWARE CONFIGURATION

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'rosetta': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'notso-unique-snowflake'
    },
    'default': {
        #'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'unique-snowflake'
    },
}
########## END CACHE CONFIGURATION

########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'app.urls'
########## END URL CONFIGURATION


########## AUTHENTICATION CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/topics/auth/customizing/
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
########## END AUTHENTICATION CONFIGURATION

########## APP CONFIGURATION
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

if ADMIN_ENABLED:
    DJANGO_APPS += ('django.contrib.admin',)

THIRD_PARTY = (
    'treebeard',
    'filer',
    'reversion',
    'djangocms_text_ckeditor',  # note this needs to be above the 'cms' entry
    'cms',
    'menus',
    'sekizai',
    'djangocms_admin_style',
    'djangocms_video',
    'djangocms_column',
    'django_extensions',
    'cmsplugin_filer_file',
    'cmsplugin_filer_image',
    'cmsplugin_filer_link',
    'adminplus',
    'easy_thumbnails',
    'sorl.thumbnail',
    'rosetta',
    'modeltranslation',
    'pagination',
    'json_field',
    'tinymce',
    'haystack',
    'postman',
    'south',
    'djcelery_email',
    'allauth',
    'constance',
    'constance.backends.database',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin',
    'adminsortable2',
    'avatar',
    'widget_tweaks',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'app',
    'app.users',
    'app.reporting',
    'app.market',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + LOCAL_APPS
########## END APP CONFIGURATION

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOG_PATH = ''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'ERROR',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
            'stream': sys.stderr
        },
        'null': {
            'level': 'ERROR',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['mail_admins', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'notifications': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
########## END LOGGING CONFIGURATION

########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'app.wsgi.application'
########## END WSGI CONFIGURATION

########## SOUTH CONFIGURATION
# https://south.readthedocs.org/en/latest/
SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}
########## END SOUTH CONFIGURATION

########## WEB ASSET CONFIGURATION
# http://django-assets.readthedocs.org/en/latest/
ASSETS_DEBUG = True
ASSETS_ROOT = STATIC_ROOT

JST_COMPILER = '_.template'

STATICFILES_FINDERS += (
    'django_assets.finders.AssetsFinder',
)

INSTALLED_APPS += (
    'django_assets',
)
########## END WEB ASSET CONFIGURATION

########## EASY THUMBNAIL CONFIGURATION
# http://easy-thumbnails.readthedocs.org/en/latest/index.html
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.background',
    'easy_thumbnails.processors.filters',
)
########## END EASY THUMBNAIL CONFIGURATION

########## CONSTANCE CONGIF CONFIGURATION
# Todo: Remove this, and make application settings
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_DATABASE_CACHE_BACKEND = 'default'
CONSTANCE_CONFIG = {
    'ACTIVATE_USER_EMAIL': (
        '', 'Email address to send the activation email after user confirms his/her email address.'),
    'REPORT_POST_EMAIL': ('', 'Email address to send a notifaction once a user sends a report.'),
    'NO_REPLY_EMAIL': ('guerillasoftwaretest@gmail.com',
                       'Email address used by this program to send various notifications to users and administrators.'),
    'GOOGLE_ANALYTICS': ('', 'Google analytics'),
    'GOOGLE_TAG_MANAGER': ('', 'Google tag manager'),
    'DONATE_BUTTON_LOGGED_IN': ('', 'The HTML for the donate button in the navbar'),
    'DONATE_BUTTON_LANDING': ('', 'The HTML for the donate button on the landing page'),
    'TRANSLATED_LANGUAGES': ('en,',
                             "Comma seperated list of translated language codes. Must be  two characters and one of: (('af', 'Afrikaans'), ('ar', 'Arabic'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('el', 'Greek'), ('en', 'English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy-nl', 'Frisian'), ('ga', 'Irish'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('nb', 'Norwegian Bokmal'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('th', 'Thai'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('vi', 'Vietnamese'), ('zh-cn', 'Simplified Chinese'), ('zh-tw', 'Traditional Chinese'))"),
    'BLOG_URL': ('http://blog.movements.org/', 'Link to Movements blog'),
}
########## END CONSTANCE CONGIF CONFIGURATION

########## DJANGO ALL AUTH CONFIGURATION
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_DISPLAY = 'app.users.utils.get_full_name'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 5
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'administrator', 'test']
ACCOUNT_SIGNUP_FORM_CLASS = 'app.users.forms.SignupForm'
ACCOUNT_ADAPTER = 'app.users.views.AccAdapter'
SOCIALACCOUNT_AVATAR_SUPPORT = False
SOCIALACCOUNT_AUTO_SIGNUP = False
########## END DJANGO ALL AUTH CONFIGURATION

########## HAYSTACK CONFIGURATION
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
########## END HAYSTACK CONFIGURATION

########## AVATAR CONFIGURATION
AUTO_GENERATE_AVATAR_SIZES = (40, 100, 50)
########## END AVATAR CONFIGURATION

########## POSTMAN CONFIGURATION
POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISABLE_USER_EMAILING = True  # default is False
POSTMAN_AUTO_MODERATE_AS = True  # default is None
########## END POSTMAN CONFIGURATION

########## CELERY CONFIGURATION
CELERY_BROKER = 'amqp://guest@localhost//'
CELERYBEAT_SCHEDULE = {
    'update-salesforce': {
        'task': 'update_salesforce',
        'schedule': crontab(minute=0),
        'args': None
    },
}
CELERY_TIMEZONE = 'UTC'
########## END CELERY CONFIGURATION

########## SALESFORCE INTEGRATION CONFIGURATION
SALESFORCE_INTEGRATION_ENABLED = os.environ.get('SALESFORCE_INTEGRATION_ENABLED', 'false').lower() == 'true'
SALESFORCE_USERNAME = os.environ.get('SALESFORCE_USERNAME', '')
SALESFORCE_PASSWORD = os.environ.get('SALESFORCE_PASSWORD', '')
SALESFORCE_CLIENT_ID = os.environ.get('SALESFORCE_CLIENT_ID', '')
SALESFORCE_CLIENT_SECRET = os.environ.get('SALESFORCE_CLIENT_SECRET', '')
SALESFORCE_USE_SANDBOX = os.environ.get('SALESFORCE_USE_SANDBOX', 'true').lower() == 'true'
########## END SALESFORCE INTEGRATION CONFIGURATION

########## TWO FACTOR CONFIGURATION
#LOGIN_URL = reverse_lazy('two_factor:login')
TWO_FACTOR_SMS_GATEWAY = 'two_factor.gateways.twilio.gateway.Twilio'
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_CALLER_ID = os.environ.get('TWILIO_CALLER_ID', '')
########## END TWO FACTOR CONFIGURATION

########## TINYMCE CONFIGURATION
TINYMCE_DEFAULT_CONFIG = {
    'mode': "textareas",
    'theme': "advanced",
    'theme_advanced_buttons1': "bold,italic,underline,link,unlink,bullist,undo",
    'theme_advanced_buttons2': "",
    'theme_advanced_buttons3': "",
    'cleanup_on_startup': True,
    'valid_elements': "a[href|target=_blank],strong/b,br,p,ul,li,em,p",
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = False
########## END TINYMCE CONFIGURATION

########## MODEL TRANSLATION CONFIGURATION
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_TRANSLATION_REGISTRY = 'app.translation'
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en',)
########## END MODEL TRANSLATION CONFIGURATION

########## GOOGLE TRANSLATION CONFIGURATION
GOOGLE_TRANS_URL = "https://www.googleapis.com/language/translate/v2?"
GOOGLE_DETECT_API_URL = "https://www.googleapis.com/language/translate/v2/detect?"
########## END GOOGLE TRANSLATION CONFIGURATION

########## TRANSLATION SYSTEM CONFIGURATION
from django.utils.timezone import timedelta
POST_TRANSLATION_TIME = timedelta(minutes=2)
COMMENT_TRANSLATION_TIME = timedelta(minutes=1)
########## END TRANSLATION SYSTEM CONFIGURATION

########## DJANGO CMS CONFIGURATION
from cms_settings import *
########## END DJANGO CMS CONFIGURATION

########## GENERAL MOVEMENTS CONFIGURATION
LOGIN_REDIRECT_URL = '/exchange'
ROSETTA_CACHE_NAME = 'rosetta'
PAGE_SIZE = 12
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
########## END GENERAL MOVEMENTS CONFIGURATION
