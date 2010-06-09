#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A WSGI application for Wikkid.

TODO:
 * serving the static files
 * url handling
 * redirects
 * skins
 * users - I'm thinking that we should do the users as a middleware.
   That way we can just add to the environ for the user.
"""

import logging
import urllib

from webob import exc, Request, Response


from wikkid.skin.loader import Skin


class WikkidApp(object):
    """The main wikkid application."""

    def __init__(self, filestore, skin_name=None):
        self.filestore = filestore
        # Need to load the initial templates for the skin.
        if skin_name is None:
            skin_name = 'default'
        self.skin = Skin(skin_name)
        self.logger = logging.getLogger('wikkid')

    def __call__(self, environ, start_response):
        """The WSGI bit."""
        request = Request(environ)

        self.logger.info('request.path: %s', request.path)
        path = urllib.unquote(request.path)
        if path == '/favicon.ico':
            if self.skin.favicon is not None:
                icon = open(self.skin.favicon, 'rb')
                try:
                    response = Response(
                        icon.read(), content_type='image/x-icon')
                finally:
                    icon.close()
            else:
                response = exc.HTTPNotFound()
        elif path.startswith('/static'):
            response = exc.HTTPNotFound()
        else:
            response = Response(
                'Hello %s!' % request.params.get('name', 'World'))
        return response(environ, start_response)
