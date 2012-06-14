# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2012 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A means of storing execution context."""

DEFAULT_FORMAT = 'rest'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8080


class ExecutionContext(object):
    """Store run-time execution context data.

    This is the Encapsulate Context pattern.
    """

    def __init__(self, host=None, port=None, default_format=None,
                 script_name=None):
        """Create an execution context for the application.

        :param host: The hostname that content is being served from.
        :param port: The port that is being listened on.
        :param default_format: The default wiki format for pages that
            don't specify any.
        """
        if host is None:
            host = DEFAULT_HOST
        if port is None:
            port = DEFAULT_PORT
        if default_format is None:
            default_format = DEFAULT_FORMAT
        self.host = host
        self.port = port
        self.default_format = default_format
        # TODO: make sure the script_name if set starts with a slash and
        # doesn't finish with one.
        if script_name is None:
            script_name = ''
        self.script_name = script_name.rstrip('/')
