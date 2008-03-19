#!/bin/bash

KRYTEN_HOME=$(dirname $0)
. ${KRYTEN_HOME}/etc/common

cd ${KRYTEN_HOME}

aclocal
automake --add-missing --copy --force-missing --foreign
autoconf
