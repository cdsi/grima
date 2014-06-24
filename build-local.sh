#!/bin/sh -e

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

if [ "${SKIP_QUESTIONS}" = "" ]; then
        echo -n "Delete the database? [y/N] "
        read answer
        case "${answer}" in
                [yY]*)
                        grima-db-delete.sh || true
                ;;
        esac
fi

grima-db-load.sh || true
# TODO: [ $? != 0 ] && exit 1

exit 0
