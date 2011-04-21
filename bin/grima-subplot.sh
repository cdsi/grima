#!/bin/sh

GRIMA_HOME="$(dirname $0)"/..
export GRIMA_HOME

. "${GRIMA_HOME}"/etc/common

OPTION="$1"

case "${OPTION}" in
        *restore-defaults)
                rm -f "${GRIMA_ETC}"/grima-subplot-widget.ini
                shift
        ;;
esac

if [ ! -f "${GRIMA_ETC}"/grima-subplot-widget.ini ]; then
        cp "${GRIMA_ETC}"/grima-subplot-widget.ini.in "${GRIMA_ETC}"/grima-subplot-widget.ini
fi

echo $$ > "${GRIMA_RUN}"/grima-subplot.pid

exec python.sh "${GRIMA_BIN}"/grima-subplot.py "$@"
