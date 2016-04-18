#!/bin/bash

set -e
# set -x

WORKON_HOME=/var/www/python/envs
. $WORKON_HOME/ohmgear/bin/activate

#mkvirtualenv ohmgear_jenkins

#workon ohmgear

pep8 * > pep8.log || true
#pip install -r requirements/

