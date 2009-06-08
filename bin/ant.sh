#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

grima_record ${ANT} ${ANTFLAGS} ${GRIMA_ANTFLAGS} "$@"
exec ${ANT} ${ANTFLAGS} ${GRIMA_ANTFLAGS} "$@"
