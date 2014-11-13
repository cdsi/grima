#!/bin/sh -e

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

DJANGO_SETTINGS_MODULE=grima.www.settings
export DJANGO_SETTINGS_MODULE

exec python.sh ${GRIMA_BIN}/grima-django-manage.py "$@" -v 0
