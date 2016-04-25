#!/bin/bash

set -e
# set -x

WORKON_HOME=/var/www/python/envs
. $WORKON_HOME/ohmgear/bin/activate
export NOSE_INCLUDE_EXE=1
./manage.py test --settings='ohmgear.settings.local_jenkin'

pep8 apps/ ohmgear/ common/> pep8.log || true
pylint --rcfile=pylint.cfg -f parseable apps/ ohmgear/ common/> pylint.log || true


