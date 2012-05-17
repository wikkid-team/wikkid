#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for method and classes in wikkid.app."""

import os.path

from webob.request import environ_from_url

from wikkid.app import WikkidApp
from wikkid.filestore.volatile import FileStore
from wikkid.tests import TestCase


class TestApp(TestCase):

    def test_traverse_above_static_not_possible_with_relative_path(self):
        """
        Traversal above the static folder, by forging a malicious request with
        a relative path for example, is not possible.
        """
        environ = environ_from_url("/static/../page.html")

        def start_response(status, headers):
            self.assertEqual("404 Not Found", status)

        filestore = FileStore()
        app = WikkidApp(filestore)
        app(environ, start_response)

    def test_traverse_above_static_not_possible_with_absolute_path(self):
        """
        Traversal above the static folder, by forging a malicious request
        including an absolute path for example, is not possible.
        """
        this_file = os.path.abspath(__file__)
        environ = environ_from_url("/static/" + this_file)

        def start_response(status, headers):
            self.assertEqual("404 Not Found", status)

        filestore = FileStore()
        app = WikkidApp(filestore)
        app(environ, start_response)

    def test_getting_static_style_css_works(self):

        environ = environ_from_url("/static/default.css")

        def start_response(status, headers):
            self.assertEqual("200 OK", status)

        filestore = FileStore()
        app = WikkidApp(filestore)
        app(environ, start_response)

    def test_getting_static_style_css_works_with_script_name(self):

        environ = environ_from_url("/static/default.css")
        environ['SCRIPT_NAME'] = '/test'
        def start_response(status, headers):
            self.assertEqual("200 OK", status)

        filestore = FileStore()
        app = WikkidApp(filestore)
        app(environ, start_response)
