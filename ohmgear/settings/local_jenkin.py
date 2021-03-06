import djcelery


from base import *

DOMAIN_NAME = 'http://localhost:8000'

ALLOWED_HOSTS = ['localhost', '*', '192.168.2.146:8100']
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"},
        'simple': {
            'format': '%(levelname)s %(message)s'},
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'mysite.log',
                        'formatter': 'verbose'},
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'MYAPP': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }}

# CELERY STUFF
INSTALLED_APPS += (
    "djcelery", "apps.test_purposes",
    'django_nose'
    # "rest_framework_swagger",
    # 'raven.contrib.django.raven_compat'
)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',  # activate coverage report
    '--with-doctest',  # activate doctest: find and run docstests
    '--verbosity=2',   # verbose output
    '--with-xunit',    # enable XUnit plugin
    '--xunit-file=testreport.xml',  # the XUnit report file
    '--cover-xml',     # produle XML coverage info
    '--cover-xml-file=coverage.xml',  # the coverage info file
    # You may also specify the packages to be covered here
    '--cover-package=users,notes,businesscards,contacts,identifiers',
    '--cover-html',
    '--cover-html-dir=coverage_dir'
]
'''import raven

RAVEN_CONFIG = {
    'dsn': 'https://729dcf0cf35742559908b6eea18f6563:a91b624970fd49caba33b442ba37b499@app.getsentry.com/60299',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    #'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}
'''

djcelery.setup_loader()

BROKER_URL = 'redis://localhost:6379'
BROKER_HOST = 'localhost'
BROKER_PORT = '6379'
BROKER_USER = 'guest'
BROKER_PASSWORD = 'guest'

CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# UPLOAD URL PATHS
BCARDS_TEMPLATE_IMAGE_URL = DOMAIN_NAME


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

MIGRATION_MODULES = DisableMigrations()

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ohmgear',
        'USER': 'ohmgear',
        'PASSWORD': 'ohmgear',
        'HOST': 'localhost',
        'PORT': '',
    },
   
}
'''
 'userlocation': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ohmgear',
        'USER': 'ohmgear',
        'PASSWORD': 'ohmgear',
        'HOST': 'localhost',
        'PORT': '',
    }
'''

DEFAULT_FROM_EMAIL = 'bhoopendra.ohmgear@gmail.com'
# q@123456
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bhoopendra.ohmgear@gmail.com'
EMAIL_HOST_PASSWORD = 'q@123456'
