#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for method and classes in wikkid.app."""

from wikkid.app import parse_url
from wikkid.tests import TestCase


class TestParseUrl(TestCase):
    """Tests for parse_url."""

    def test_root(self):
        path, view = parse_url('/')
        self.assertEqual('/', path)
        self.assertIs(None, view)

    def test_root_view(self):
        path, view = parse_url('/+latest')
        self.assertEqual('/', path)
        self.assertEqual('latest', view)

    def test_page(self):
        path, view = parse_url('/Home/SubPage')
        self.assertEqual('/Home/SubPage', path)
        self.assertIs(None, view)

    def test_page_view(self):
        path, view = parse_url('/Home/SubPage/+edit')
        self.assertEqual('/Home/SubPage', path)
        self.assertEqual('edit', view)
