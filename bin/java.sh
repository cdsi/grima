#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

exec ${JAVA} ${JAVAFLAGS} ${GRIMA_JAVAFLAGS} "$@"
