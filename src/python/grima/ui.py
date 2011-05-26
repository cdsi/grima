from __future__ import division
from __future__ import with_statement

import os

from elrond.ui import Widget

class Example(Widget):

        def __init__(self):
                Widget.__init__(self)

                path = os.environ['GRIMA_ETC']
                name = 'grima-example-widget'

                self.loadui(path, name)
                self.loaddb(path, name)

class ExampleApp(Widget):

        def __init__(self, *args, **kwargs):
                Widget.__init__(self, *args, **kwargs)

                path = os.environ['GRIMA_ETC']
                name = 'grima-example-app'

                self.loadui(path, name)
                self.loaddb(path, name)

# $Id:$
#
# Local Variables:
# indent-tabs-mode: nil
# python-continuation-offset: 2
# python-indent: 8
# End:
# vim: ai et si sw=8 ts=8
