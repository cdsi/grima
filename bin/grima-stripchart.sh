#!/bin/sh -e

GRIMA_HOME="$(dirname $0)"/..
export GRIMA_HOME

. "${GRIMA_HOME}"/etc/common

OPTION="$1"

case "${OPTION}" in
        *restore-defaults)
                rm -f "${GRIMA_ETC}"/grima-plot2.ini
                shift
        ;;
esac

if [ ! -f "${GRIMA_ETC}"/grima-plot2.ini ]; then
        cp "${GRIMA_ETC}"/grima-plot2.ini.in "${GRIMA_ETC}"/grima-plot2.ini
fi

echo $$ > "${GRIMA_RUN}"/grima-stripchart.pid

exec python.sh "${GRIMA_BIN}"/grima-stripchart.py "$@"
