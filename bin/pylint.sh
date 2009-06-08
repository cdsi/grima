#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

grima_record python.sh $(which pylint) "$@"
exec python.sh $(which pylint) "$@"
