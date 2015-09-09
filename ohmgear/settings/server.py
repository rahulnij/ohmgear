from base import *
#DOMAIN_NAME = 'http://ohmgear.in'http://192.168.2.129:8018
DOMAIN_NAME = 'http://192.168.2.129:8018'
DEBUG = True
SITE_ROOT="/var/www/websites/ohmgear/"
STATIC_ROOT = "/var/www/websites/ohmgear/ohmgear/static/"
#ALLOWED_HOSTS = ['192.168.2.129']
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