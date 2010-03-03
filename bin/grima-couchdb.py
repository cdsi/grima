from __future__ import division
from __future__ import with_statement

from optparse import OptionParser

from elrond.ui import Window
from grima.couchdb import CouchDB

op = OptionParser('%prog [options]')

op.add_option('--title', action='store', dest='title', default=None,
              help='title to be used in couchdb window')
op.add_option('--deletable', action='store', dest='deletable', default=True,
              help='When disabled the couchdb window is not closable.')

(options, args) = op.parse_args()

couchdb = CouchDB()

window = Window(widget=couchdb)
window.title = options.title
window.deletable = options.deletable

window.show()
window.run()

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
