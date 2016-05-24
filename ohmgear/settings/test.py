from base import *

DOMAIN_NAME = 'http://sgtest.kinbow.com'

DEBUG = False
ALLOWED_HOSTS = ['*']

LOG_PATH = '/home/kinbow/ohmgear/logs'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(levelname)s, %(asctime)s]  [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"},
        'simple': {
            'format': '%(levelname)s %(message)s'},
    },
    'handlers': {
        'criticalfile': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': '%s/critical.log' % (LOG_PATH),
            'formatter': 'verbose'
        },
        'errorfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '%s/error.log' % (LOG_PATH),
            'formatter': 'verbose'
        },
        'warningfile': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '%s/warning.log' % (LOG_PATH),
            'formatter': 'verbose'
        },
        'kinbowfile': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': '%s/kinbow.log' % (LOG_PATH),
            'formatter': 'verbose'
        },
        'debugfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '%s/debug.log' % (LOG_PATH),
            'formatter': 'simple'
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['debugfile'],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },
        'apps': {
            'handlers': [
                'debugfile',
                'errorfile',
                'criticalfile'
            ],
            'level': 'DEBUG',
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_db',
        'USER': 'root',
        'PASSWORD': 'jL56mbFuwK',
        'HOST': 'test-kbsingpgresql.cg5v0c82f0c4.ap-southeast-1.rds.amazonaws.com',
        'PORT': '',
    },
    'userlocation': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'OGPostgres2',
        'USER': 'OGAdmin',
        'PASSWORD': 'OG132465',
        'HOST': 'ogpostgres3.cdibcw5lvsbm.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# email settings
DEFAULT_FROM_EMAIL = 'welcome@kinbow.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIAI3I37YRQ6STIPN6A'
EMAIL_HOST_PASSWORD = 'Am37x7uVJFkUu3vmAE0oAg2u0nZ35NUTrZjAZRioh2w3'

# CELERY STUFF
INSTALLED_APPS += ("djcelery", )
import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://test-kbsingredis.peu3xj.0001.apse1.cache.amazonaws.com'
BROKER_HOST = 'test-kbsingredis.peu3xj.0001.apse1.cache.amazonaws.com'
BROKER_PORT = '6379'
BROKER_USER = 'guest'
BROKER_PASSWORD = 'guest'

CELERY_RESULT_BACKEND = 'redis://test-kbsingredis.peu3xj.0001.apse1.cache.amazonaws.com'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ("apps.email.views")
