#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.formatter.rest module."""

from textwrap import dedent
from bs4 import BeautifulSoup

from wikkid.formatter.restformatter import RestructuredTextFormatter
from wikkid.tests import TestCase


class TestRestructuredTextFormatter(TestCase):
    """Tests for the ReST formatter."""

    def setUp(self):
        TestCase.setUp(self)
        self.formatter = RestructuredTextFormatter()

    def test_simple_text(self):
        # A simple heading and a paragraph.
        text = dedent("""\
            Nice Heading
            ============

            Simple sentence.
            """)
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result, features="lxml")
        self.assertEqual('Nice Heading', soup.h1.string)
        self.assertEqual('Simple sentence.', soup.p.string)
