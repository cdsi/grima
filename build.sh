#!/bin/sh -e

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

POST_BUILD=
[ ! -f configure ] && POST_BUILD="${GRIMA_HOME}"/post-build.sh

if [ -x ${GRIMA_HOME}/build-local.sh ]; then
	${GRIMA_HOME}/build-local.sh
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi

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

if [ "${EVERYTHING}" = "1" ] || [ "${BACKENDS}" = "1" ]; then
	[ "${FORCE:=0}" != "0" ] || [ ! -f Makefile.in ] && ./bootstrap.sh
	[ "${FORCE:=0}" != "0" ] || [ ! -f Makefile    ] && ./run-configure.sh

	${GRIMA_BIN}/make.sh tags quick-install
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi
if [ "${EVERYTHING}" = "1" ] || [ "${JUST_PYTHON}" = "1" ]; then
	${GRIMA_BIN}/python.sh setup.py --quiet develop
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi
if [ "${EVERYTHING}" = "1" ] || [ "${JUST_JAVA}" = "1" ]; then
	if [ -f build.xml ]; then
		${GRIMA_BIN}/ant.sh jar
		[ $? != 0 ] && echo "ERROR!!!" && exit 1
	fi
fi

[ -x "${POST_BUILD}" ] && "${POST_BUILD}"

exit 0
