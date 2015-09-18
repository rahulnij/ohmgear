"""
WSGI config for ohmgear project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import socket
import re
#----------- clavax:Set setting according server -------------------------#
HOSTNAME = socket.gethostname().lower().split('.')[0].replace('-','')
if re.search('clavax',  HOSTNAME):
   settings = "ohmgear.settings.local"
else:
   settings = "ohmgear.settings.server"
#----------- End Setting -------------------------------------------#

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

application = get_wsgi_application()
