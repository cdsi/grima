#!/bin/sh

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

DISTCLEAN="$(cat ${GRIMA_HOME}/distclean.list | sed -e 's/ /xYz/g')"

for x in ${DISTCLEAN}; do
        f=$(echo ${x} | sed -e 's/xYz/ /g';)
        rm -rf "${GRIMA_HOME}"/"${f}"
done

# To re-create distclean.list:
#
# cd "${GRIMA_HOME}"
# git clean -d -f x
# yes | ./build.sh && ./test.sh
# git status -s | grep -e ^[?] | sed 's/^.. \+//' | sort > distclean.list
