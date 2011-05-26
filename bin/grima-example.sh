#!/bin/sh

GRIMA_HOME="$(dirname "$0")"/..
export GRIMA_HOME

. "${GRIMA_HOME}"/etc/common

OPTION="$1"

case "${OPTION}" in
        *restore-defaults)
                rm -f "${GRIMA_ETC}"/grima-example-widget.ini
                shift
        ;;
esac

if [ ! -f "${GRIMA_ETC}"/grima-example-widget.ini ]; then
        cp "${GRIMA_ETC}"/grima-example-widget.ini.in "${GRIMA_ETC}"/grima-example-widget.ini
fi

echo $$ > "${GRIMA_RUN}"/grima-example.pid

exec python.sh "${GRIMA_BIN}"/grima-example.py "$@"
