#!/bin/bash

KRYTEN_HOME=$(dirname $0)
. ${KRYTEN_HOME}/etc/common

for x in ${KRYTEN_EXTRAS}; do
	${KRYTEN_HOME}/extras/${x}/clean.sh $*
	[ $? != 0 ] && echo "ERROR!!!" && exit 1
done

cd ${KRYTEN_HOME}

TARGET="$1"
TARGET=${TARGET:="clean"}

${PYTHON} ${PYTHONFLAGS} setup.py ${TARGET}
[ $? != 0 ] && echo "ERROR!!!" && exit 1

make -k uninstall distclean
[ $? != 0 ] && echo "ERROR!!!" && exit 1

exit 0
