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
from twisted.web.static import File
from twisted.internet import reactor


class TwistedPage(Resource):

    def __init__(self, server, logger):
        Resource.__init__(self)
        self.server = server
        self.logger = logger

    def getChild(self, name, request):
        # Yay for logging...
        self.logger.debug('getChild: %r' % name)
        return TwistedPage(self.server, self.logger)

    @property
    def filepath(self):
        return '/'.join(self.path)

    def render_file(self, request):
        # content = self.filestore.file_contents(self.filepath)
        # Munge the content.
        # Strip the leading / from the path.
        path = request.path.lstrip('/')
        page = self.server.get_page(path)
        content_type, content = page.render()
        if content_type.startswith('text/'):
            content_type = "%s; charset=utf-8" % content_type
            content = content.encode('utf-8')
        request.setHeader('Content-Type', content_type)
        return content

    def render_GET(self, request):
        self.logger.debug('args: %s', request.args)
        self.logger.debug('path: %s', request.path)
        return self.render_file(request)


class TwistedServer(object):
    """Wraps the twisted stuff..."""

    def __init__(self, server, port=8080):
        self.server = server
        self.port = port
        self.logger = logging.getLogger('wikkid')

    def run(self):
        self.logger.info('Listening on port %d' % self.port)
        root = TwistedPage(self.server, self.logger)
        skin = self.server.skin
        if skin.favicon is not None:
            root.putChild('favicon.ico', File(skin.favicon))
        if skin.static_dir is not None:
            # Perhaps have the 'static' name configurable to avoid potential
            # conflict with a static directory in a branch that the user cares
            # about.
            root.putChild('static', File(skin.static_dir))
        factory = Site(root)
        reactor.listenTCP(self.port, factory)
        reactor.run()
