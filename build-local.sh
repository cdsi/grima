#!/bin/sh

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

echo -n "Delete the database? [y/N] "
read answer
case "${answer}" in
	[yY]*)
		echo "Deleting: ${GRIMA_DB}"
		rm -f "${GRIMA_DB}"/*
	;;
esac

grima-db-load.sh > ${GRIMA_LOG}/db.log 2>&1
[ $? != 0 ] && grep 'ERROR!!!' ${GRIMA_LOG}/db.log && exit 1

exit 0
