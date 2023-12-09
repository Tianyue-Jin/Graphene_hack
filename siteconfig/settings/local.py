"""
Django local.py DEV MODE Settings Example Template
Copy this to local.py and edit setting as required.
DO NOT COMMIT THE local.py FILE TO THE REPOSITORY
See https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# wads-wagtail Optional Features
# ------------------------------------------------------------------------

ENABLE_LDAP = False # True|False
ENABLE_DEBUG_TOOLBAR = False # True|False

# Wagtail Site Settings
# ------------------------------------------------------------------------
# Base URL to use when referring to full URLs within the Wagtail admin
# backend - e.g. in notification emails.
# Don't include '/admin' or a trailing slash

WAGTAIL_SITE_NAME = 'Productivity Lab Test'
WAGTAILADMIN_BASE_URL = 'localhost' # usually localhost for dev

# Security
# ------------------------------------------------------------------------

SECRET_KEY = '+&(q7qo=uc262!q^4ynd4tnpl1+=7_0pl99shu*79k1d))7n@y'

# Email
# ------------------------------------------------------------------------

DEFAULT_FROM_EMAIL = f'{WAGTAIL_SITE_NAME} - <no-reply@manchester.ac.uk>'

# Database
# ------------------------------------------------------------------------
# Use Postgresql by default rather than sqlite3

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'productivity_lab',
        'USER': 'productivity_lab',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Hosts
# ------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# REQUIRED if DEBUG is False
# WSL2: if not serving on localhost:8000 add IP from running `ifconfig`

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Language
# ------------------------------------------------------------------------

LANGUAGE_CODE = 'en-gb'

# Search Backends
# ------------------------------------------------------------------------
# See: https://docs.wagtail.io/en/v2.7/topics/search/backends.html#backends
# If using postgresql (now default db) use its search features

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
        'INDEX': 'acrc_deploy',
    },
}

# REST Framework
# ------------------------------------------------------------------------
# See: https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiYW5uZ2xlZHNvbiIsImEiOiJjazIwejM3dmwwN2RkM25ucjljOTBmM240In0.2jLikF_JryviovmLE3rKew'

ARCGIS_ACCESS_TOKEN = 'AAPK5d0c0e1b7ce74c57a81834c04c0be482tQ4reA29iAioqijSwOb0OW0s32YTPIZkqZNSSp8VnbjiCFBW3ie-nEtTZV2a4MSs'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"rich": {"datefmt": "[%X]"}},
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "level": "DEBUG",
            "rich_tracebacks": True,
        }
    },
    "loggers": {
        "django": {"handlers": ["console"]}
    },
}