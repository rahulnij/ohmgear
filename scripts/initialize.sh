#!/bin/bash

set -e
# set -x

WORKON_HOME=/var/www/python/envs
. $WORKON_HOME/ohmgear/bin/activate

./manage.py test --settings='ohmgear.settings.local'

pep8 apps/ ohmgear/ > pep8.log || true
pylint --rcfile=pylint.cfg -f parseable apps/ ohmgear/ > pylint.log || true


