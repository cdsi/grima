#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

grima_record ${PYTHON} ${PYTHONFLAGS} ${GRIMA_PYTHONFLAGS} "$@"
exec ${PYTHON} ${PYTHONFLAGS} ${GRIMA_PYTHONFLAGS} "$@"
