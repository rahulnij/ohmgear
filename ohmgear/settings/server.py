from base import *
DEBUG = False
SITE_ROOT="/var/www/websites/ohmgear/"
STATIC_ROOT = "/var/www/websites/ohmgear/ohmgear/static/"
SECRET_KEY = '3-6ostd%53*04ccinr@c0^y!)^op6ue@ekd-cka86^90+z=jln'
ALLOWED_HOSTS = ['192.168.2.129']
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