#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.formatter.creoleformatter module."""

from textwrap import dedent
from BeautifulSoup import BeautifulSoup

from wikkid.formatter.creoleformatter import CreoleFormatter
from wikkid.tests import TestCase


class TestCreoleFormatter(TestCase):
    """Tests for the creole formatter."""

    def setUp(self):
        TestCase.setUp(self)
        self.formatter = CreoleFormatter()

    def test_simple_text(self):
        # A simple heading and a paragraph.
        text = dedent("""\
            == Nice Heading

            Simple sentence.
            """)
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result)
        self.assertEqual('Nice Heading', soup.h2.string)
        self.assertEqual('Simple sentence.', soup.p.string)

    def test_wiki_links(self):
        # A paragraph containing a wiki word.
        text = "A link to the FrontPage helps."
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result)
        self.assertEqual('FrontPage', soup.a['href'])
