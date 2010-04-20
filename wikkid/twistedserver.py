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

    def __init__(self, server, logger, user_factory, skin_name=None):
        Resource.__init__(self)
        self.server = server
        self.logger = logger
        self.user_factory = user_factory
        # Need to load the initial templates for the skin.
        if skin_name is None:
            skin_name = 'default'
        self.skin = Skin(skin_name)

    def getChild(self, name, request):
        # Yay for logging...
        self.logger.debug('getChild: %r' % name)
        return TwistedPage(self.server, self.logger, self.user_factory)

    @property
    def filepath(self):
        return '/'.join(self.path)

    def render_page(self, request, page):
        content_type, content = page.render()
        if content_type.startswith('text/'):
            content_type = "%s; charset=utf-8" % content_type
            content = content.encode('utf-8')
        request.setHeader('Content-Type', content_type)
        return content

    def get_view(self, request, action):
        path = request.path
        user = self.user_factory.create(request)
        model = self.server.get_info(path)
        view_class = get_view(model, action)
        return view_class(self.skin, model, path, user)

    def render_GET(self, request):
        self.logger.debug('args: %s', request.args)
        self.logger.debug('path: %s', request.path)
        action = request.args.get('action', [None])[0]
        view = self.get_view(request, action)
        return self.render_page(request, view)

    def render_POST(self, request):
        self.logger.debug('args: %s', request.args)
        self.logger.debug('path: %s', request.path)
        path = request.path
        user = self.user_factory.create(request)
        if request.args.get('action') == ['save']:
            content = request.args['content'][0]
            message = request.args['message'][0]
            if 'rev-id' in request.args:
                rev_id = request.args['rev-id'][0]
            else:
                rev_id = None
            page = self.server.update_page(
                path, user, rev_id, content, message)
            # Here is where we could check the page for a redirect following
            # the post for a good update.
            return self.render_page(request, page)
        # If this isn't a save, pretend it is a get.
        return self.render_GET(request)


class TwistedServer(object):
    """Wraps the twisted stuff..."""

    def __init__(self, server, user_factory, port=8080):
        self.server = server
        self.port = port
        self.logger = logging.getLogger('wikkid')
        self.user_factory = user_factory

    def run(self):
        self.logger.info('Listening on port %d' % self.port)
        root = TwistedPage(self.server, self.logger, self.user_factory)
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
