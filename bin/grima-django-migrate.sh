#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

grima-django-manage.sh syncdb --noinput
# TODO: grima-django-manage.sh migrate grima.www.appname
