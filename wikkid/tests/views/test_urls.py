#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests the edit views."""

from testtools.matchers import Equals
from webob import Request

from wikkid.tests import TestCase
from wikkid.tests.factory import FactoryTestCase
from wikkid.view.urls import canonical_url, parse_url


class TestCanonicalUrl(FactoryTestCase):
    """Test the wikkid.view.base.canonical_url."""

    def assertUrl(self, resource, url, view_name=None, base_url=None):
        request = Request.blank('/', base_url=base_url)
        self.assertThat(canonical_url(resource, request, view_name),
                        Equals(url))

    def test_root(self):
        factory = self.make_factory()
        root = factory.get_resource_at_path('/')
        self.assertUrl(root, '/')

    def test_root_listing(self):
        factory = self.make_factory()
        root = factory.get_resource_at_path('/')
        self.assertUrl(root, '/+listing', view_name='listing')

    def test_default(self):
        factory = self.make_factory([
            ('Home.txt', 'Some content'),
            ])
        root = factory.get_resource_at_path('/')
        self.assertUrl(root.default_resource, '/Home')

    def test_default_view(self):
        factory = self.make_factory([
            ('Home.txt', 'Some content'),
            ])
        root = factory.get_resource_at_path('/')
        self.assertUrl(root.default_resource, '/Home/+edit', view_name='edit')

    def test_wiki_page(self):
        factory = self.make_factory([
            ('SomeDir/SomePage.txt', 'Some content'),
            ])
        page = factory.get_resource_at_path('/SomeDir/SomePage')
        self.assertUrl(page, '/SomeDir/SomePage')

    def test_wiki_page_view(self):
        factory = self.make_factory([
            ('SomeDir/SomePage.txt', 'Some content'),
            ])
        page = factory.get_resource_at_path('/SomeDir/SomePage')
        self.assertUrl(page, '/SomeDir/SomePage/+edit', view_name='edit')

    def test_wiki_page_full_url(self):
        factory = self.make_factory([
            ('SomeDir.txt', 'Some content'),
            ])
        page = factory.get_resource_at_path('/SomeDir.txt')
        self.assertUrl(page, '/SomeDir')

    def test_wiki_page_full_url_with_view(self):
        factory = self.make_factory([
            ('SomeDir.txt', 'Some content'),
            ])
        page = factory.get_resource_at_path('/SomeDir.txt')
        self.assertUrl(page, '/SomeDir/+edit', view_name='edit')

    def test_other_file(self):
        factory = self.make_factory([
            ('simple.py', '#!/usr/bin/python'),
            ])
        page = factory.get_resource_at_path('/simple.py')
        self.assertUrl(page, '/simple.py')

    def test_other_file_view(self):
        factory = self.make_factory([
            ('simple.py', '#!/usr/bin/python'),
            ])
        page = factory.get_resource_at_path('/simple.py')
        self.assertUrl(page, '/simple.py/+edit', view_name='edit')

    def test_missing(self):
        factory = self.make_factory()
        missing = factory.get_resource_at_path('/MissingPage')
        self.assertUrl(missing, '/MissingPage')

    def test_missing_view(self):
        factory = self.make_factory()
        missing = factory.get_resource_at_path('/MissingPage')
        self.assertUrl(missing, '/MissingPage/+edit', view_name='edit')


class TestParseUrl(TestCase):
    """Tests for wikkid.view.base.parse_url."""

    def test_root(self):
        path, view = parse_url('/')
        self.assertEqual('/', path)
        self.assertIs(None, view)

    def test_root_view(self):
        path, view = parse_url('/+listing')
        self.assertEqual('/', path)
        self.assertEqual('listing', view)

    def test_path(self):
        path, view = parse_url('/some/path')
        self.assertEqual('/some/path', path)
        self.assertIs(None, view)

    def test_path_view(self):
        path, view = parse_url('/some/path/+view')
        self.assertEqual('/some/path', path)
        self.assertEqual('view', view)
