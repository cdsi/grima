#!/bin/bash

KRYTEN_HOME=$(dirname $0)
. ${KRYTEN_HOME}/etc/common

cd ${KRYTEN_HOME}

./configure ${KRYTEN_CONFIGUREFLAGS}
[ $? != 0 ] && echo "ERROR!!!" && exit 1

exit 0
