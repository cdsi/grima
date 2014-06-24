#!/bin/sh -e

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

if [ -x ${GRIMA_HOME}/test-local.sh ]; then
	${GRIMA_HOME}/test-local.sh
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
        "${GRIMA_BIN}"/make.sh coverage-report # TODO: test-report
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi
if [ "${EVERYTHING}" = "1" ] || [ "${JUST_PYTHON}" = "1" ]; then
        "${GRIMA_BIN}"/nosetests.sh
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi
if [ "${EVERYTHING}" = "1" ] || [ "${JUST_JAVA}" = "1" ]; then
	if [ -f build.xml ]; then
		${GRIMA_BIN}/ant.sh test
		[ $? != 0 ] && echo "ERROR!!!" && exit 1
	fi
fi

exit 0
