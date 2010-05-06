#
# Copyright (C) 2010 Wikkid Developers
#
# This file is part of Wikkid.
#
# Wikkid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wikkid.  If not, see <http://www.gnu.org/licenses/>

"""Tests the breadcrumbs for the views."""

from wikkid.dispatcher import get_view
from wikkid.tests.factory import FactoryTestCase
from wikkid.tests.fakes import TestRequest, TestUser


class TestBreadcrumbs(FactoryTestCase):
    """The breadcrumbs lead the user back home."""

    # Don't test the breadcrumbs for the root object directly here as it will
    # redirect to Home.  TODO: add a test browser test for this.

    def setUp(self):
        super(TestBreadcrumbs, self).setUp()
        self.user = TestUser('test@example.com', 'Test User')
        self.request = TestRequest()

    def assertBreadcrumbs(self, view, expected):
        """Make sure the breadcrumbs from view are the expected ones."""
        crumbs = [(crumb.title, crumb.path) for crumb in view.breadcrumbs]
        self.assertEqual(expected, crumbs)

    def test_home_missing(self):
        # If the Home page is selected, but there is no content, the
        # breadcrumb is still Home.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/Home')
        view = get_view(info, None, self.request, self.user)
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home')])

    def test_page_missing(self):
        # If the page is at the root of the tree, but isn't home, then the
        # first breadcrumb is home, and the second is the page.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/SamplePage')
        view = get_view(info, None, self.request, self.user)
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home'),
             ('Sample Page', '/SamplePage')])

    def test_nested_page_missing(self):
        # If the Home page is selected, but there is no content, the
        # breadcrumb is still Home.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/SamplePage/SubPage/Next')
        view = get_view(info, None, self.request, self.user)
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home'),
             ('Sample Page', '/SamplePage'),
             ('Sub Page', '/SamplePage/SubPage'),
             ('Next', '/SamplePage/SubPage/Next')])

    def test_source_file_missing(self):
        # If the Home page is selected, but there is no content, the
        # breadcrumb is still Home.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/wikkid/views/base.py')
        view = get_view(info, None, self.request, self.user)
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home'),
             ('wikkid', '/wikkid'),
             ('views', '/wikkid/views'),
             ('base.py', '/wikkid/views/base.py')])

    def test_directory_breadcrumbs_root(self):
        # Directory breadcrumbs start with Home, and then list the
        # directories, where the urls for the directories are the listing
        # urls.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/')
        view = get_view(info, 'listing', self.request, self.user)
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home'),
             ('wiki root', '/?view=listing')])

