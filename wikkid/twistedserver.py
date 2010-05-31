#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

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

    def get_view(self, request, action):
        path = request.path
        user = self.user_factory.create(request)
        model = self.resource_factory.get_resource_at_path(path)
        return get_view(model, action, request, user)

    def render_GET(self, request):
        self.logger.debug('args: %s', request.args)
        self.logger.debug('path: %s', request.path)
        action = request.args.get('view', [None])[0]
        view = self.get_view(request, action)
        # TODO: what to do with none?
        return view.render(self.skin)

    def render_POST(self, request):
        self.logger.debug('args: %s', request.args)
        self.logger.debug('path: %s', request.path)
        action = request.args.get('action', [None])[0]
        view = self.get_view(request, action)
        # TODO: what to do with none?
        return view.render(self.skin)


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
        # Is there anyway to set the host?
        self.logger.info('Wiki instance running at http://localhost:%d' % self.port)
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
