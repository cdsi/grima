#!/bin/sh

GRIMA_HOME="$(dirname $0)"/..
export GRIMA_HOME

. "${GRIMA_HOME}"/etc/common

OPTION="$1"

case "${OPTION}" in
        *restore-defaults)
                rm -f "${GRIMA_ETC}"/grima-couchdb.ini
                shift
        ;;
esac

if [ ! -f "${GRIMA_ETC}"/grima-couchdb.ini ]; then
        cp "${GRIMA_ETC}"/grima-couchdb.ini.in "${GRIMA_ETC}"/grima-couchdb.ini
fi

echo $$ > "${GRIMA_RUN}"/grima-couchdb.pid

exec python.sh "${GRIMA_BIN}"/grima-couchdb.py "$@"
