# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A WSGI application for Wikkid."""

import logging
import mimetypes
import os.path
import urllib

from bzrlib import urlutils
from webob import Request, Response
from webob.exc import HTTPException, HTTPNotFound

from wikkid.dispatcher import get_view
from wikkid.model.factory import ResourceFactory
from wikkid.skin.loader import Skin
from wikkid.view.urls import parse_url
from wikkid.fileutils import FileIterable
from wikkid.context import ExecutionContext


def serve_file(filename):
    if os.path.exists(filename):
        basename = urlutils.basename(filename)
        content_type = mimetypes.guess_type(basename)[0]

        res = Response(content_type=content_type, conditional_response=True)
        res.app_iter = FileIterable(filename)
        res.content_length = os.path.getsize(filename)
        res.last_modified = os.path.getmtime(filename)
        # Todo: is this the best value for the etag? 
        # perhaps md5 would be a better alternative
        res.etag = '%s-%s-%s' % (os.path.getmtime(filename),
            os.path.getsize(filename),
            hash(filename))
        return res

    else:
        return HTTPNotFound()


class WikkidApp(object):
    """The main wikkid application."""

    def __init__(self, filestore, skin_name=None, 
                 execution_context = ExecutionContext()):
        self.execution_context = execution_context
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
        path = urllib.unquote(request.path)
        if path == '/favicon.ico':
            if self.skin.favicon is not None:
                response = serve_file(self.skin.favicon)
            else:
                response = HTTPNotFound()
        elif path.startswith('/static/'):
            if self.skin.static_dir is not None:
                static_dir = self.skin.static_dir.rstrip(os.sep) + os.sep
                static_file = os.path.abspath(
                    urlutils.joinpath(static_dir, path[8:]))
                if static_file.startswith(static_dir):
                    response = serve_file(static_file)
                else:
                    response = HTTPNotFound()
            else:
                response = HTTPNotFound()
        else:
            resource_path, action = parse_url(path)
            model = self.resource_factory.get_resource_at_path(resource_path)
            try:
                view = get_view(model, action, request, self.execution_context)
                response = view.render(self.skin)
            except HTTPException, e:
                response = e

        return response(environ, start_response)
