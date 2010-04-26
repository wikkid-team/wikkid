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

from wikkid.dispatcher import get_view
from wikkid.skin.loader import Skin


class TwistedPage(Resource):

    def __init__(self, resource_factory, logger, user_factory, skin):
        Resource.__init__(self)
        self.resource_factory = resource_factory
        self.logger = logger
        self.user_factory = user_factory
        self.skin = skin

    def getChild(self, name, request):
        # Yay for logging...
        self.logger.debug('getChild: %r' % name)
        return TwistedPage(
            self.resource_factory, self.logger, self.user_factory, self.skin)

    @property
    def filepath(self):
        return '/'.join(self.path)

    def render_page(self, request, page):
        content_type, content = page.render(self.skin)
        if content_type.startswith('text/'):
            content_type = "%s; charset=utf-8" % content_type
            content = content.encode('utf-8')
        request.setHeader('Content-Type', content_type)
        return content

    def get_view(self, request, action):
        path = request.path
        user = self.user_factory.create(request)
        model = self.resource_factory.get_resource_at_path(path)
        return get_view(model, action, request, user)

    def render_GET(self, request):
        self.logger.debug('args: %s', request.args)
        self.logger.debug('path: %s', request.path)
        # TODO: make this 'view' instead of 'action'
        action = request.args.get('action', [None])[0]
        view = self.get_view(request, action)
        # TODO: what to do with none?
        return self.render_page(request, view)

    def render_POST(self, request):
        self.logger.debug('args: %s', request.args)
        self.logger.debug('path: %s', request.path)
        action = request.args.get('action', [None])[0]
        view = self.get_view(request, action)
        # TODO: what to do with none?
        return self.render_page(request, view)


class TwistedServer(object):
    """Wraps the twisted stuff..."""

    def __init__(self, resource_factory, user_factory, port=8080,
                 skin_name=None):
        self.resource_factory = resource_factory
        self.port = port
        self.logger = logging.getLogger('wikkid')
        self.user_factory = user_factory
        # Need to load the initial templates for the skin.
        if skin_name is None:
            skin_name = 'default'
        self.skin = Skin(skin_name)

    def run(self):
        self.logger.info('Listening on port %d' % self.port)
        root = TwistedPage(
            self.resource_factory, self.logger, self.user_factory, self.skin)
        if self.skin.favicon is not None:
            root.putChild('favicon.ico', File(self.skin.favicon))
        if self.skin.static_dir is not None:
            # Perhaps have the 'static' name configurable to avoid potential
            # conflict with a static directory in a branch that the user cares
            # about.
            root.putChild('static', File(self.skin.static_dir))
        factory = Site(root)
        reactor.listenTCP(self.port, factory)
        reactor.run()
