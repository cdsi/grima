import gobject
import gtk

from grima.plot2 import Plot

class PlotWidget(gtk.Alignment):
        __gtype_name__ = 'PlotWidget'

        def __init__(self):
                gtk.Alignment.__init__(self)

                self.plot = Plot()
                self.add(self.plot.widget)

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
