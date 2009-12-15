#!/bin/sh

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

cd ${GRIMA_HOME}

OPTION="$1"

EXTENSIONFLAGS="--enable-java=${GRIMA_SRC}/java --enable-python=${GRIMA_SRC}/python"

case "${OPTION}" in
	*disable-extensions)
		EXTENSIONFLAGS="--enable-java=no --with-java=no \
			 --enable-python=no --with-python=no"
	;;
esac

./configure --disable-static ${GRIMA_CONFIGUREFLAGS} ${EXTENSIONFLAGS}
[ $? != 0 ] && echo "ERROR!!!" && exit 1

exit 0
