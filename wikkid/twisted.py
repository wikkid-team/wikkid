#
# Copyright (C) 2010 Wikkid Developers
#
# This file is part of Wikkid.
#
# Wikkid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wikkid.  If not, see <http://www.gnu.org/licenses/>

"""A twisted server and resource for the wikkid wiki.

Handles the page traversal and passes the full path to the server.
The server class does the actual page rendering.
"""

import logging

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

from wikkid.server import Server


class TwistedPage(Resource):

    def __init__(self, server, logger):
        Resource.__init__(self)
        self.server = server
        self.logger = logger

    def getChild(self, name, request):
        # Yay for logging...
        self.logger.debug('getChild: %r' % name)
        return TwistedPage(self.server)

    @property
    def filepath(self):
        return '/'.join(self.path)

    def render_file(self, request):
        content = self.filestore.file_contents(self.filepath)
        # Munge the content.
        request.setHeader('Content-Type', 'text/plain')
        return content

    def render_GET(self, request):
        import pdb; pdb.set_trace()
        request.args
        self.logger.debug(request.path)
        return self.render_file(request)


class TwistedServer(object):
    """Wraps the twisted stuff..."""

    def __init__(self, filestore, user_factory, port=8080, logger=None):
        if logger is None:
            logger = logging.getLogger('wikkid')
        self.server = Server(filestore, user_factory, logger=logger)
        self.port = port
        self.logger = logger

    def run(self):
        root = TwistedPage(self.server, self.logger)
        factory = Site(root)
        reactor.listenTCP(self.port, factory)
        reactor.run()
