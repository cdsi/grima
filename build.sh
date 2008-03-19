#!/bin/bash

KRYTEN_HOME=$(dirname $0)
. ${KRYTEN_HOME}/etc/common

cd ${KRYTEN_HOME}

TARGET="$1"
TARGET=${TARGET:="develop"}

[ "${FORCE:=0}" != "0" ] || [ ! -f Makefile.in ] && ./bootstrap.sh
[ "${FORCE:=0}" != "0" ] || [ ! -f Makefile    ] && ./run-configure.sh

make -k tags install
[ $? != 0 ] && echo "ERROR!!!" && exit 1

${PYTHON} ${PYTHONFLAGS} setup.py ${TARGET}
[ $? != 0 ] && echo "ERROR!!!" && exit 1

exit 0
