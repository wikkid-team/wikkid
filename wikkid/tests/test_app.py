#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for method and classes in wikkid.app."""

import os.path

from testtools.matchers import IsInstance
from webob.request import environ_from_url

from wikkid.app import WikkidApp
from wikkid.context import ExecutionContext
from wikkid.filestore.volatile import FileStore
from wikkid.view.missing import MissingPage
from wikkid.view.wiki import WikiPage
from wikkid.tests import TestCase


class TestApp(TestCase):

    def assert_not_found(self, status, headers):
        self.assertEqual("404 Not Found", status)

    def assert_ok(self, status, headers):
        self.assertEqual("200 OK", status)

    def test_traverse_above_static_not_possible_with_relative_path(self):
        """
        Traversal above the static folder, by forging a malicious request with
        a relative path for example, is not possible.
        """
        environ = environ_from_url("/static/../page.html")
        filestore = FileStore()
        app = WikkidApp(filestore)
        app(environ, self.assert_not_found)

    def test_traverse_above_static_not_possible_with_absolute_path(self):
        """
        Traversal above the static folder, by forging a malicious request
        including an absolute path for example, is not possible.
        """
        this_file = os.path.abspath(__file__)
        environ = environ_from_url("/static/" + this_file)
        filestore = FileStore()
        app = WikkidApp(filestore)
        app(environ, self.assert_not_found)

    def test_getting_static_style_css_works(self):

        environ = environ_from_url("/static/default.css")
        filestore = FileStore()
        app = WikkidApp(filestore)
        app(environ, self.assert_ok)

    def test_getting_static_style_css_works_with_script_name(self):

        environ = environ_from_url("/test/static/default.css")
        filestore = FileStore()
        context = ExecutionContext(script_name="/test")
        app = WikkidApp(filestore, execution_context=context)
        app(environ, self.assert_ok)

    def test_getting_static_style_css_works_with_script_name_multiple_segments(self):
        environ = environ_from_url("/p/project-name/wiki/static/default.css")
        filestore = FileStore()
        context = ExecutionContext(script_name="/p/project-name/wiki")
        app = WikkidApp(filestore, execution_context=context)
        app(environ, self.assert_ok)

    def test_getting_anything_outside_script_name_fails(self):
        environ = environ_from_url("/foo/bar")
        filestore = FileStore()
        context = ExecutionContext(script_name="/test")
        app = WikkidApp(filestore, execution_context=context)
        app(environ, self.assert_not_found)

    def test_get_view(self):
        environ = environ_from_url("/Home")
        filestore = FileStore()
        context = ExecutionContext()
        app = WikkidApp(filestore, execution_context=context)
        view = app.get_view(environ)
        self.assertThat(view, IsInstance(MissingPage))

    def test_get_home_view(self):
        environ = environ_from_url("/Home")
        filestore = FileStore([
                ('Home.txt', 'Welcome Home.')])
        context = ExecutionContext()
        app = WikkidApp(filestore, execution_context=context)
        view = app.get_view(environ)
        self.assertThat(view, IsInstance(WikiPage))
