#!/bin/bash

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

EVERYTHING=1
OPTION=$1

case "${OPTION}" in
	*backends)
		EVERYTHING=0
		BACKENDS=1
	;;
	*python)
		EVERYTHING=0
		JUST_PYTHON=1
	;;
	*java)
		EVERYTHING=0
		JUST_JAVA=1
	;;
	*extensions)
		EVERYTHING=0
		JUST_PYTHON=1
		JUST_JAVA=1
	;;
esac

cd ${GRIMA_HOME}

if [ "${EVERYTHING}" = "1" ] || [ "${JUST_JAVA}" = "1" ]; then
	[ -f build.xml ] && ant.sh clean
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi
if [ "${EVERYTHING}" = "1" ] || [ "${JUST_PYTHON}" = "1" ]; then
	python.sh setup.py clean
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi
if [ "${EVERYTHING}" = "1" ] || [ "${BACKENDS}" = "1" ]; then
	make.sh -k uninstall distclean
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi

for x in ${GRIMA_EXTRAS}; do
	${GRIMA_HOME}/extras/${x}/clean.sh "$@"
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
done

if [ -x ${GRIMA_HOME}/clean-local.sh ]; then
        ${GRIMA_HOME}/clean-local.sh
        [ $? != 0 ] && echo "ERROR!!!" && exit 1
fi

exit 0
