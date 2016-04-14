from base import *
#DOMAIN_NAME = 'http://ohmgear.in'
DOMAIN_NAME = 'http://ohmgear.clavax.us'
SITE_ROOT = "/home/ohmgear/ohmgear/"
DEBUG = False
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

DEFAULT_FROM_EMAIL = 'welcome@kinbow.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER =  'bhoopendra.ohmgear@gmail.com'
EMAIL_HOST_PASSWORD =  'q@123456'

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
CELERY_IMPORTS = ("apps.email.views")
