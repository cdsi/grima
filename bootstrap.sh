#!/bin/sh -e

GRIMA_HOME=$(dirname $0)
. ${GRIMA_HOME}/etc/common

cd ${GRIMA_HOME}

GTKDOCSIZE="$(which gtkdocize 2> /dev/null || true)"
if [ -x "${GTKDOCSIZE}" ]; then
        "${GTKDOCSIZE}" --copy --flavour no-tmpl
else
        echo "EXTRA_DIST=" > "${GRIMA_HOME}"/gtk-doc.make
fi
libtoolize --automake --copy --force
aclocal ${ACLOCALFLAGS}
autoheader
automake --add-missing --copy --force-missing --foreign
autoconf
