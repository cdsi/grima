#!/bin/bash

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

for x in ${GRIMA_EXTRAS}; do
	${GRIMA_HOME}/extras/${x}/test.sh $*
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
done

cd ${GRIMA_HOME}

TARGET="$1"
TARGET=${TARGET:="test"}

${PYTHON} ${PYTHONFLAGS} setup.py ${TARGET}
[ $? != 0 ] && echo "ERROR!!!" && exit 1

exit 0
