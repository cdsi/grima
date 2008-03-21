#!/bin/bash

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

cd ${GRIMA_HOME}

./configure ${GRIMA_CONFIGUREFLAGS}
[ $? != 0 ] && echo "ERROR!!!" && exit 1

exit 0
