#!/bin/sh

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

for x in ${GRIMA_EXTRAS}; do
	${GRIMA_HOME}/extras/${x}/distclean.sh "$@"
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
done

DISTCLEAN="$(cat ${GRIMA_HOME}/distclean.list | sed -e 's/ /xYz/g')"

for x in ${DISTCLEAN}; do
        f=$(echo ${x} | sed -e 's/xYz/ /g';)
        rm -rf "${GRIMA_HOME}"/"${f}"
done
