from __future__ import division
from __future__ import with_statement

import gobject

from elrond.widgets import Alignment

from grima.plot2 import Plot
from grima.ui import Example

class GrimaExampleWidget(Alignment):
        __gtype_name__ = 'GrimaExampleWidget'

        def __init__(self):
                Alignment.__init__(self)

                self.subwidget = Example()
                self.add(self.subwidget.widget)

gobject.type_register(GrimaExampleWidget)

class PlotWidget(Alignment):
        __gtype_name__ = 'PlotWidget'

        def __init__(self):
                Alignment.__init__(self)

                self.subwidget = Plot()
                self.add(self.subwidget.widget)

gobject.type_register(PlotWidget)

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
