#!/bin/sh

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

cd ${GRIMA_HOME}

libtoolize --automake --copy --force
aclocal ${GRIMA_ACLOCALFLAGS}
autoheader
automake --add-missing --copy --force-missing --foreign
autoconf
