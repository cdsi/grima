#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

grima_record ${JAVA} ${JAVAFLAGS} ${GRIMA_JAVAFLAGS} "$@"
exec ${JAVA} ${JAVAFLAGS} ${GRIMA_JAVAFLAGS} "$@"
