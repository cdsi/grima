#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

exec ${GRIMA_BIN}/sqlite3.sh -init ${GRIMA_ETC}/grima-db-dump.sql ${GRIMA_DB}/grima.db \
	'.exit'
