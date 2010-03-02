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

"""The server class for the wiki."""

import logging
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor


class Server(object):
    """The DWiki server.
    """

    def __init__(self, filestore, user_factory, skin=None):
        """Construct the DWiki server.

        :param filestore: An `IFileStore` instance.
        :param skin: A particular skin to use.
        """
        self.filestore = filestore
        self.user_factory = user_factory
        # Need to load the initial templates for the skin.
        self.skin = skin


    def load_templates(self):
        """Load the wiki template for the skin."""



## Twisted bits...

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
        try:
            import pdb; pdb.set_trace()
            request.args
            trace.note(request.path)
            return self.render_file(request)
        except NotFound:
            return "<html><body><h1>No file</h1>%s" % self.filepath


class TwistedServer(object):
    """Wraps the twisted stuff..."""

    def __init__(self, filestore, user_factory, port=8080):

        self.server = Server(filestore, user_factory)
        self.port = port
        self.logger = logging.getLogger('dwiki')

    def run(self):
        root = TwistedPage(self.server, self.logger)
        factory = Site(root)
        reactor.listenTCP(self.port, factory)
        reactor.run()
