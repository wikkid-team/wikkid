#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for wikkid.formatter.registry."""


from wikkid.formatter.registry import get_wiki_formatter
from wikkid.tests import TestCase


class TestGetWikiFormtter(TestCase):
    """Tests for get_wiki_formatter."""

    def test_default_missing(self):
        self.assertRaises(
            KeyError,
            get_wiki_formatter,
            'some content',
            'missing')

