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
import urllib.parse
from wsgiref.util import shift_path_info

from breezy import urlutils
from webob import Request, Response
from webob.exc import HTTPException, HTTPNotFound

from wikkid.context import ExecutionContext
from wikkid.dispatcher import get_view
from wikkid.fileutils import FileIterable
from wikkid.model.factory import ResourceFactory
from wikkid.skin.loader import Skin
from wikkid.view.urls import parse_url


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
        res.etag = '%s-%s-%s' % (
            os.path.getmtime(filename), os.path.getsize(filename),
            hash(filename))
        return res

    else:
        return HTTPNotFound()


class WikkidApp(object):
    """The main wikkid application."""

    def __init__(self, filestore, skin_name=None, execution_context=None):
        if execution_context is None:
            execution_context = ExecutionContext()
        self.execution_context = execution_context
        self.filestore = filestore
        self.resource_factory = ResourceFactory(self.filestore)
        # Need to load the initial templates for the skin.
        if skin_name is None:
            skin_name = 'default'
        self.skin = Skin(skin_name)
        self.logger = logging.getLogger('wikkid')

    def preprocess_environ(self, environ):
        request = Request(environ)
        path = urllib.parse.unquote(request.path)
        script_name = self.execution_context.script_name
        # Firstly check to see if the path is the same as the script_name
        if path != script_name and not path.startswith(script_name + '/'):
            raise HTTPNotFound()

        shifted_prefix = ''
        while shifted_prefix != script_name:
            shifted = shift_path_info(environ)
            shifted_prefix = '{0}/{1}'.format(shifted_prefix, shifted)
        # Now we are just interested in the path_info having ignored the
        # script name.
        path = urllib.parse.unquote(request.path_info)
        if path == '':
            path = '/'  # Explicitly be the root (we need the /)
        return request, path

    def _get_view(self, request, path):
        """Get the view for the path specified."""
        resource_path, action = parse_url(path)
        model = self.resource_factory.get_resource_at_path(resource_path)
        return get_view(model, action, request, self.execution_context)

    def process_call(self, environ):
        """The actual implementation of dealing with the call."""
        # TODO: reject requests that aren't GET or POST
        try:
            request, path = self.preprocess_environ(environ)
        except HTTPException as e:
            return e

        if path == '/favicon.ico':
            if self.skin.favicon is not None:
                return serve_file(self.skin.favicon)
            else:
                return HTTPNotFound()

        if path.startswith('/static/'):
            if self.skin.static_dir is not None:
                static_dir = self.skin.static_dir.rstrip(os.sep) + os.sep
                static_file = os.path.abspath(
                    urlutils.joinpath(static_dir, path[8:]))
                if static_file.startswith(static_dir):
                    return serve_file(static_file)
                else:
                    return HTTPNotFound()
            else:
                return HTTPNotFound()

        try:
            view = self._get_view(request, path)
            return view.render(self.skin)
        except HTTPException as e:
            return e

    def get_view(self, environ):
        """Allow an app user to get the wikkid view for a particular call."""
        request, path = self.preprocess_environ(environ)
        return self._get_view(request, path)

    def __call__(self, environ, start_response):
        """The WSGI bit."""
        response = self.process_call(environ)
        return response(environ, start_response)
