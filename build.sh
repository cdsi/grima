#!/bin/bash

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

for x in ${GRIMA_EXTRAS}; do
	${GRIMA_HOME}/extras/${x}/build.sh $*
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
done

cd ${GRIMA_HOME}

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

[ -x build-setup.sh ] && ${GRIMA_HOME}/build-setup.sh

if [ "${EVERYTHING}" = "1" ] || [ "${BACKENDS}" = "1" ]; then
	[ "${FORCE:=0}" != "0" ] || [ ! -f Makefile.in ] && ./bootstrap.sh
	[ "${FORCE:=0}" != "0" ] || [ ! -f Makefile    ] && ./run-configure.sh

	make.sh tags install
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi
if [ "${EVERYTHING}" = "1" ] || [ "${JUST_PYTHON}" = "1" ]; then
	python.sh setup.py develop
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi
if [ "${EVERYTHING}" = "1" ] || [ "${JUST_JAVA}" = "1" ]; then
        if [ -f build.xml ]; then
                ant.sh jar
                [ $? != 0 ] && echo "ERROR!!!" && exit 1
        fi
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
fi

exit 0
