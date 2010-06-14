#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A WSGI application for Wikkid.

TODO:
 * url handling
 * redirects <- I am here
 * users - I'm thinking that we should do the users as a middleware.
   That way we can just add to the environ for the user.
"""

import logging
import mimetypes
import os.path
import re
import urllib

from bzrlib import urlutils
from webob import Request, Response
from webob.exc import HTTPException, HTTPNotFound

from wikkid.dispatcher import get_view
from wikkid.model.factory import ResourceFactory
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


VIEW_MATCHER = re.compile('^(.*)/\+(\w+)$')


def parse_url(path):
    """Convert a path into a resource path and a view."""
    match = VIEW_MATCHER.match(path)
    if match is not None:
        resource_path, view = match.groups()
        if resource_path == '':
            resource_path = '/'
        return (resource_path, view)
    else:
        return (path, None)


class WikkidApp(object):
    """The main wikkid application."""

    def __init__(self, filestore, skin_name=None):
        self.filestore = filestore
        self.resource_factory = ResourceFactory(self.filestore)
        # Need to load the initial templates for the skin.
        if skin_name is None:
            skin_name = 'default'
        self.skin = Skin(skin_name)
        self.logger = logging.getLogger('wikkid')

    def __call__(self, environ, start_response):
        """The WSGI bit."""
        request = Request(environ)

        # TODO: reject requests that aren't GET or POST

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
            resource_path, action = parse_url(path)
            model = self.resource_factory.get_resource_at_path(resource_path)
            try:
                view = get_view(model, action, request)
                response = view.render(self.skin)
            except HTTPException, e:
                response = e

        return response(environ, start_response)
