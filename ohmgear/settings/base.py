# ----------------------------------------------#
# Developer Name: Sajid
# Creation Date: 2015/08/04
# Notes: Main setting file
# ----------------------------------------------#
"""
Django settings for ohmgear project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3-6ostd%53*04ccinr@c0^y!)^op6ue@ekd-cka86^90+z=jln'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


DJANGO_APPS = (
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.gis',
    'simple_history',
    'ckeditor',
)

PROJECT_APPS = (
    'apps.users',
    'apps.notes',
    'apps.businesscards',
    'apps.contacts',
    'apps.identifiers',
    'apps.vacationcard',
    'apps.email',
    'apps.promocode',
    'apps.folders',
    'apps.feedbacks',
    'apps.staticpages',
    'apps.usersetting',
    'apps.groups',
    'apps.userlocation',
    'apps.sendrequest',
    'apps.awsserver',
    # 'common.image_lib',

)

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS

DJANGO_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware'
)

PROJECT_MIDDLEWARE_CLASSES = (
    'apps.users.mobile_detect_middleware.MobileDetectionMiddleware',
)

MIDDLEWARE_CLASSES = DJANGO_MIDDLEWARE_CLASSES + PROJECT_MIDDLEWARE_CLASSES
# ------------------------- Custome setting ------------------------------------#
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'ohmgear.custom_exception_handler.custom_exception_handler',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'UPLOADED_FILES_USE_URL': True,
}
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = (
    'ohmgear.auth_backends.UsersModelBackend',
)
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)

# ----------------------- End setting -------------------------------------------#


ROOT_URLCONF = 'ohmgear.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'ohmgear/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.static',
                'django.core.context_processors.static'
            ],
        },
    },
]

WSGI_APPLICATION = 'ohmgear.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASE_ROUTERS = [
    'ohmgear.databaseroutes.userlocationrouter.UserLocationRouter'
]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
JET_THEME = 'green'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(MEDIA_ROOT, 'static')

STATICFILES_DIRS = ()


BCARDS_TEMPLATE_IMAGE = os.path.join(MEDIA_ROOT, 'bcards_template_image')
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
