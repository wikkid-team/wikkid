#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for wikkid.formatter.registry."""

from textwrap import dedent

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

    def test_default_exists(self):
        content, formatter = get_wiki_formatter(
            'some content', 'rest')
        self.assertEqual('some content', content)
        self.assertEqual(
            'RestructuredTextFormatter', formatter.__class__.__name__)

    def test_specify_creole(self):
        content, formatter = get_wiki_formatter(
            dedent("""\
                # creole
                some content
                """), 'rest')
        self.assertEqual('some content\n', content)
        self.assertEqual('CreoleFormatter', formatter.__class__.__name__)

    def test_specify_missing(self):
        content, formatter = get_wiki_formatter(
            dedent("""\
                # missing
                some content
                """), 'rest')
        self.assertEqual('# missing\nsome content\n', content)
        self.assertEqual(
            'RestructuredTextFormatter', formatter.__class__.__name__)

    def test_specify_extra_whitespace(self):
        content, formatter = get_wiki_formatter(
            dedent("""\
                #\t\tcreole
                some content
                """), 'rest')
        self.assertEqual('some content\n', content)
        self.assertEqual('CreoleFormatter', formatter.__class__.__name__)

    def test_specify_extra_params(self):
        content, formatter = get_wiki_formatter(
            dedent("""\
                # creole extra params
                some content
                """), 'rest')
        self.assertEqual('some content\n', content)
        self.assertEqual('CreoleFormatter', formatter.__class__.__name__)

    def test_specify_creole_case_insensitive(self):
        content, formatter = get_wiki_formatter(
            dedent("""\
                # CREOLE
                some content
                """), 'rest')
        self.assertEqual('some content\n', content)
        self.assertEqual('CreoleFormatter', formatter.__class__.__name__)
