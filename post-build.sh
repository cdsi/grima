#!/bin/sh -e

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

grima-django-migrate.sh
grima-django-load.sh

exit 0
