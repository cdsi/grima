#!/bin/bash

KRYTENI_HOME=$(dirname $0)/..
export KRYTENI_HOME

. ${KRYTENI_HOME}/etc/common

exec ${PYTHON} ${PYTHONFLAGS} $*
