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

from webob import Request, Response


class WikkidApp(object):
    """The main wikkid application."""

    def __init__(self, filestore):
        self.filestore = filestore

    def __call__(self, environ, start_response):
        """The WSGI bit."""
        request = Request(environ)
        response = Response(
            'Hello %s!' % request.params.get('name', 'World'))
        return response(environ, start_response)
