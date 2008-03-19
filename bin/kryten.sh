#!/bin/bash

KRYTENI_HOME=$(dirname $0)/..
export KRYTENI_HOME

. ${KRYTENI_HOME}/etc/common

for data in $*; do
	${PYTHON} ${PYTHONFLAGS} ${GANDALF_BIN}/kryten.py ${data} &
done
