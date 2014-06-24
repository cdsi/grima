#!/bin/sh -e

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

FILENAME="$1"

if [ "${FILENAME}" = "" ]; then
    FILENAME="${GRIMA_DATA}"/grima-django-load.json
fi

exec grima-django-manage.sh loaddata "${FILENAME}"
