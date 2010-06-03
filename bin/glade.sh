#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

grima_record ${GLADE} ${GLADEFLAGS} ${GRIMA_GLADEFLAGS} "$@"
exec ${GLADE} ${GLADEFLAGS} ${GRIMA_GLADEFLAGS} "$@"
