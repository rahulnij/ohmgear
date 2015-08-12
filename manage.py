#!/usr/bin/env python
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
   
   
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
