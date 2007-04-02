#!/bin/bash

. `dirname $0`/../etc/common
PROG=`basename $0`

exec ${PYTHON} ${PYTHONFLAGS} ${GANDALF_BIN}/data-plot.py $*
