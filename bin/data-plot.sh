#!/bin/bash

. `dirname $0`/../etc/common
PROG=`basename $0`

for data in $*; do
	${PYTHON} ${PYTHONFLAGS} ${GANDALF_BIN}/data-plot.py ${data} &
done
