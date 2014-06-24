#!/bin/sh -e

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

print_usage_and_die()
{
    echo "Usage: $(basename $0) [--start | --stop | --make-cert]"
    exit 1
}

OPTION="$1"

case "${OPTION}" in
    *start)
	lighttpd -f ${GRIMA_ETC}/lighttpd.conf
	;;
    *stop)
	[ -f ${GRIMA_RUN}/lighttpd.pid ] && \
	    kill $(cat ${GRIMA_RUN}/lighttpd.pid)
	;;
    *make-cert)
	/usr/sbin/make-ssl-cert /usr/share/ssl-cert/ssleay.cnf \
	    ${GRIMA_ETC}/lighttpd.pem --force-overwrite
	;;
    *)
	print_usage_and_die
	;;
esac
