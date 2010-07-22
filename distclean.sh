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
# svn-clean
# yes | ./build.sh
# ./test.sh
# svn st --no-ignore | grep -e ^[I?] | grep -v 'extras/' | sed 's/^. \+//' | sort > distclean.list
