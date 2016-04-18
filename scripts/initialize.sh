#!/bin/bash

set -e
set -x

export WORKON_HOME=/var/www/python/envs
. /usr/local/bin/virtualenvwrapper.sh

#mkvirtualenv ohmgear_jenkins

workon ohmgear

#pip install -r requirements/

