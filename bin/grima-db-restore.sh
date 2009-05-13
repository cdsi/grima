#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

ARCHIVE=$1

if [ "${ARCHIVE}" = "" ]; then
	echo "Usage: $(basename $0) archive"
	exit 1
fi

sqlite3 -init ${GRIMA_ETC}/grima-db-restore.sql ${GRIMA_DB}/grima.db \
        < ${ARCHIVE}
