#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

exec grima-django-manage.sh loaddata "${GRIMA_DB}"/grima-django-db.json