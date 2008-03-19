#!/bin/bash

KRYTEN_HOME=$(dirname $0)
. ${KRYTEN_HOME}/etc/common

cd ${KRYTEN_HOME}

TARGET="$1"
TARGET=${TARGET:="test"}

${PYTHON} ${PYTHONFLAGS} setup.py ${TARGET}
[ $? != 0 ] && echo "ERROR!!!" && exit 1

exit 0
