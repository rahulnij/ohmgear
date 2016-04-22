"""
WSGI config for ohmgear project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# ENV, provide current environment eg. Development(dev), test, production
settings = "ohmgear.settings.%s" % (os.environ.get('ENV'))


os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

application = get_wsgi_application()
