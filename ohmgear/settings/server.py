from base import *
DEBUG = False
SITE_ROOT="/var/www/websites/ohmgear/"
STATIC_ROOT = "/var/www/websites/ohmgear/ohmgear/static/"
ALLOWED_HOSTS = ['0.0.0.0']
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