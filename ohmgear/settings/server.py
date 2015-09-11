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