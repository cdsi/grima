#!/bin/bash

GRIMAI_HOME=$(dirname $0)/..
export GRIMAI_HOME

. ${GRIMAI_HOME}/etc/common

for data in $*; do
	${PYTHON} ${PYTHONFLAGS} ${GANDALF_BIN}/grima.py ${data} &
done
