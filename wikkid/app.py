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
import mimetypes
import os.path
import urllib

from bzrlib import urlutils
from webob import Request, Response
from webob.exc import HTTPNotFound

from wikkid.skin.loader import Skin


def serve_file(filename):
    if os.path.exists(filename):
        basename = urlutils.basename(filename)
        content_type = mimetypes.guess_type(basename)[0]
        f = open(filename, 'rb')
        try:
            return Response(
                f.read(), content_type=content_type)
        finally:
            f.close()
    else:
        return HTTPNotFound()


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
                response = serve_file(self.skin.favicon)
            else:
                response = HTTPNotFound()
        elif path.startswith('/static/'):
            if self.skin.static_dir is not None:
                response = serve_file(
                    urlutils.joinpath(
                        self.skin.static_dir, path[8:]))
            else:
                response = HTTPNotFound()
        else:
            response = Response(
                'Hello %s!' % request.params.get('name', 'World'))
        return response(environ, start_response)
