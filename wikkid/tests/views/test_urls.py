#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests the edit views."""

from wikkid.tests import TestCase
from wikkid.tests.factory import FactoryTestCase
from wikkid.view.urls import canonical_url, parse_url


class TestCanonicalUrl(FactoryTestCase):
    """Test the wikkid.view.base.canonical_url."""

    def test_root(self):
        factory = self.make_factory()
        root = factory.get_resource_at_path('/')
        self.assertEqual('/', canonical_url(root))

    def test_root_listing(self):
        factory = self.make_factory()
        root = factory.get_resource_at_path('/')
        self.assertEqual('/+listing', canonical_url(root, 'listing'))

    def test_default(self):
        factory = self.make_factory([
            ('Home.txt', 'Some content'),
            ])
        root = factory.get_resource_at_path('/')
        self.assertEqual('/Home', canonical_url(root.default_resource))

    def test_default_view(self):
        factory = self.make_factory([
            ('Home.txt', 'Some content'),
            ])
        root = factory.get_resource_at_path('/')
        self.assertEqual(
            '/Home/+edit',
            canonical_url(root.default_resource, 'edit'))

    def test_wiki_page(self):
        factory = self.make_factory([
            ('SomeDir/SomePage.txt', 'Some content'),
            ])
        page = factory.get_resource_at_path('/SomeDir/SomePage')
        self.assertEqual('/SomeDir/SomePage', canonical_url(page))

    def test_wiki_page_view(self):
        factory = self.make_factory([
            ('SomeDir/SomePage.txt', 'Some content'),
            ])
        page = factory.get_resource_at_path('/SomeDir/SomePage')
        self.assertEqual(
            '/SomeDir/SomePage/+edit', canonical_url(page, 'edit'))

    def test_wiki_page_full_url(self):
        factory = self.make_factory([
            ('SomeDir.txt', 'Some content'),
            ])
        page = factory.get_resource_at_path('/SomeDir.txt')
        self.assertEqual('/SomeDir', canonical_url(page))

    def test_wiki_page_full_url_with_view(self):
        factory = self.make_factory([
            ('SomeDir.txt', 'Some content'),
            ])
        page = factory.get_resource_at_path('/SomeDir.txt')
        self.assertEqual('/SomeDir/+edit', canonical_url(page, 'edit'))

    def test_other_file(self):
        factory = self.make_factory([
            ('simple.py', '#!/usr/bin/python'),
            ])
        page = factory.get_resource_at_path('/simple.py')
        self.assertEqual('/simple.py', canonical_url(page))

    def test_other_file_view(self):
        factory = self.make_factory([
            ('simple.py', '#!/usr/bin/python'),
            ])
        page = factory.get_resource_at_path('/simple.py')
        self.assertEqual('/simple.py/+edit', canonical_url(page, 'edit'))

    def test_missing(self):
        factory = self.make_factory()
        root = factory.get_resource_at_path('/MissingPage')
        self.assertEqual('/MissingPage', canonical_url(root))

    def test_missing_view(self):
        factory = self.make_factory()
        root = factory.get_resource_at_path('/MissingPage')
        self.assertEqual('/MissingPage/+edit', canonical_url(root, 'edit'))


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


