#!/bin/sh

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

echo -n "Delete the database? [y/N] "
read answer
case "${answer}" in
	[yY]*)
                grima-db-delete.sh
	;;
esac

grima-db-load.sh
# TODO: [ $? != 0 ] && exit 1

exit 0
