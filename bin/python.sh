#!/bin/bash

KRYTEN_HOME=$(dirname $0)/..
export KRYTEN_HOME

. ${KRYTEN_HOME}/etc/common

exec ${PYTHON} ${PYTHONFLAGS} $*
