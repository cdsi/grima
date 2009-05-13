#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

sqlite3 -init ${GRIMA_ETC}/grima-db-delete.sql ${GRIMA_DB}/grima.db \
	'.exit'
