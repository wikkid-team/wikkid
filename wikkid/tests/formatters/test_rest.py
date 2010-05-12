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

"""Tests for the wikkid.formatter.rest module."""

from textwrap import dedent
from BeautifulSoup import BeautifulSoup

from wikkid.formatter.rest import RestructuredTextFormatter
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
        soup = BeautifulSoup(result)
        self.assertEqual('Nice Heading', soup.h1.string)
        self.assertEqual('Simple sentence.', soup.p.string)
