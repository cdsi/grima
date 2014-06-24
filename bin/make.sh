#!/bin/sh -e

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

grima_record ${MAKE} ${MAKEFLAGS} ${GRIMA_MAKEFLAGS} "$@"
exec ${MAKE} ${MAKEFLAGS} ${GRIMA_MAKEFLAGS} "$@"
