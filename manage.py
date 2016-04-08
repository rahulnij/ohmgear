#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":

    # ENV, provide current environment eg. Development(dev), test, production
    settings = "ohmgear.settings.%s" % (os.environ.get('ENV'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
