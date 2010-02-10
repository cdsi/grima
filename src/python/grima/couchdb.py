from __future__ import division
from __future__ import with_statement

import os

from elrond.ui import Widget

from grima.plot2 import Plot

class CouchDB(Widget):

        def show(self):
                self.plot.show()
                Widget.show(self)

        def hide(self):
                self.plot.hide()
                Widget.hide(self)

        def draw(self):
                self.plot.draw()
                Widget.draw(self)

        def __init__(self):
                Widget.__init__(self)

                path = os.environ['GRIMA_ETC']
                name = 'grima-couchdb'

                self.loadui(path, name)
                self.loaddb(path, name)

                self.plot = Plot()
                self.subplot = self.plot.subplot_new()

                container = self.builder.get_object('container')
                container.add(self.plot.widget)

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
