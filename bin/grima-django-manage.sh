#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

exec python.sh ${GRIMA_BIN}/grima-django-manage.py "$@" -v 0
