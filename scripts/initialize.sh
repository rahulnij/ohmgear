#!/bin/bash

set -e
# set -x

WORKON_HOME=/var/www/python/envs
. $WORKON_HOME/ohmgear/bin/activate

pep8 apps/ ohmgear/ > pep8.log || true
pylint apps/ ohmgear >  pylint.log || true


