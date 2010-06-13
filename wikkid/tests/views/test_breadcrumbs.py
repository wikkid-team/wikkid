#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

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
        view = self.get_view(factory, '/Home')
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home')])

    def test_page_missing(self):
        # If the page is at the root of the tree, but isn't home, then the
        # first breadcrumb is home, and the second is the page.
        factory = self.make_factory()
        view = self.get_view(factory, '/SamplePage')
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home'),
             ('Sample Page', '/SamplePage')])

    def test_nested_page_missing(self):
        # If the Home page is selected, but there is no content, the
        # breadcrumb is still Home.
        factory = self.make_factory()
        view = self.get_view(factory, '/SamplePage/SubPage/Next')
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home'),
             ('Sample Page', '/SamplePage'),
             ('Sub Page', '/SamplePage/SubPage'),
             ('Next', '/SamplePage/SubPage/Next')])

    def test_source_file_missing(self):
        # If a non-wiki style name is selected, the breadcrumbs are as a wiki
        # page.
        factory = self.make_factory()
        view = self.get_view(factory, '/wikkid/views/base.py')
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home'),
             ('wikkid', '/wikkid'),
             ('views', '/wikkid/views'),
             ('base.py', '/wikkid/views/base.py')])

    def test_source_file_existing(self):
        # If the Home page is selected, but there is no content, the
        # breadcrumb is still Home.
        factory = self.make_factory([
                ('wikkid/views/base.py', 'A python file'),
                ])
        view = self.get_view(factory, '/wikkid/views/base.py')
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home'),
             ('wiki root', '/?view=listing'),
             ('wikkid', '/wikkid?view=listing'),
             ('views', '/wikkid/views?view=listing'),
             ('base.py', '/wikkid/views/base.py')])

    def test_directory_breadcrumbs_root(self):
        # Directory breadcrumbs start with Home, and then list the
        # directories, where the urls for the directories are the listing
        # urls.
        factory = self.make_factory()
        view = self.get_view(factory, '/', 'listing')
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home'),
             ('wiki root', '/?view=listing')])

    def test_directory_breadcrumbs_nested(self):
        # For each directory after the root, a listing crumb is added.
        # Names are not wiki expanded.
        factory = self.make_factory([
                ('SomePage/SubPage/Nested.txt', 'some text')])
        view = self.get_view(factory, '/SomePage/SubPage', 'listing')
        self.assertBreadcrumbs(
            view,
            [('Home', '/Home'),
             ('wiki root', '/?view=listing'),
             ('SomePage', '/SomePage?view=listing'),
             ('SubPage', '/SomePage/SubPage')])
