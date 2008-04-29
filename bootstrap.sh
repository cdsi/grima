#!/bin/bash

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

cd ${GRIMA_HOME}

aclocal ${ACLOCALFLAGS}
automake --add-missing --copy --force-missing --foreign
autoconf
