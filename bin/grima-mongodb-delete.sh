#!/bin/sh

GRIMA_HOME=$(dirname $0)/..
export GRIMA_HOME

. ${GRIMA_HOME}/etc/common

exec mongo "$@" grima < ${GRIMA_ETC}/grima-mongodb-delete.js
