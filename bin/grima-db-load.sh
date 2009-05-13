#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

grima-db-create.sh

sqlite3 -init ${GRIMA_ETC}/grima-db-load.sql ${GRIMA_DB}/grima.db \
	'.exit'
