from base import *
#DOMAIN_NAME = 'http://ohmgear.in'
DOMAIN_NAME = 'http://ohmgear.clavax.us'
SITE_ROOT="/var/www/websites/ohmgear/"
STATIC_ROOT = "/var/www/websites/ohmgear/ohmgear/static/"
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ohmgear',
        'USER': 'clavax',
        'PASSWORD': 'tech',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# CELERY STUFF
INSTALLED_APPS += ("djcelery", )
import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://127.0.0.1:6379'
BROKER_HOST = '127.0.0.1'
BROKER_PORT = '6379'
BROKER_USER = 'guest'
BROKER_PASSWORD = 'guest'

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS=("apps.email.views")