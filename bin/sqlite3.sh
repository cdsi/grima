#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

grima_record ${SQLITE3} ${SQLITE3FLAGS} ${GRIMA_SQLITE3FLAGS} "$@"
exec ${SQLITE3} ${SQLITE3FLAGS} ${GRIMA_SQLITE3FLAGS} "$@"
