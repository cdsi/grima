#!/bin/bash

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

for data in $*; do
	${PYTHON} ${PYTHONFLAGS} ${GRIMA_BIN}/grima-plot.py ${data} &
done
