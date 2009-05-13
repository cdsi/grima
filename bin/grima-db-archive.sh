#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

sqlite3 -init ${GRIMA_ETC}/grima-db-archive.sql ${GRIMA_DB}/grima.db \
	'.exit' > ${GRIMA_DB}/grima.$(date +'%F-%s').sql
