# -*- coding: utf-8 -*-
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.formatter.textileformatter module."""

from textwrap import dedent

from bs4 import BeautifulSoup

# The textile formatter is optional.  If the MarkdownFormatter is not
# available, the tests are skipped.
try:
    from wikkid.formatter.textileformatter import TextileFormatter
    has_textile = True
except ImportError:
    has_textile = False
from wikkid.tests import TestCase


class TestTextileFormatter(TestCase):
    """Tests for the textile formatter."""

    def setUp(self):
        TestCase.setUp(self)
        if has_textile:
            self.formatter = TextileFormatter()
        else:
            self.skip('textile formatter not available')

    def test_detailed_headings(self):
        text = dedent("""\
            h1. Heading 1

            h2. Heading 2

            h3. Heading 3

            h4. Heading 4

            h5. Heading 5

            h6. Heading 6
            """)
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result)
        self.assertEqual('Heading 1', soup.h1.string)
        self.assertEqual('Heading 2', soup.h2.string)
        self.assertEqual('Heading 3', soup.h3.string)
        self.assertEqual('Heading 4', soup.h4.string)
        self.assertEqual('Heading 5', soup.h5.string)
        self.assertEqual('Heading 6', soup.h6.string)

    def test_inline_link(self):
        # A paragraph containing a wiki word.
        text = 'A link to the "FrontPage":http://127.0.0.1 helps.'
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result)
        self.assertEqual('http://127.0.0.1', soup.a['href'])

    def test_emphasis(self):
        text = 'We can have _emphasis_ and *strong* as well!'
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result)
        self.assertEqual('emphasis', soup.em.string)
        self.assertEqual('strong', soup.strong.string)

    def test_blockquote(self):
        text = dedent('''\
            Some Text

            bq. This is a block quoted paragraph
            that spans multiple lines.

            Some more text.
            ''')
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result)
        self.assertTrue(soup.blockquote is not None)

    def test_lists(self):
        text = dedent('''\
            Some Text.

            * UL 1
            * UL 2
            * UL 3

            Some More Text!

            # OL 1
            # OL 2
            # OL 3
            ''')
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result)

        self.assertTrue(soup.ul)
        ulNodes = soup.ul.findAll('li')
        for i in range(3):
            self.assertEqual('UL %d' % (i+1), ulNodes[i].string.strip())

        self.assertTrue(soup.ol)
        olNodes = soup.ol.findAll('li')
        for i in range(3):
            self.assertEqual('OL %d' % (i+1), olNodes[i].string.strip())

    def test_code_blocks(self):
        text = dedent('''\
            Some Normal Text.

            @Some Code inside pre tags@

            More Normal text.
            ''')
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result)
        self.assertEqual(soup.code.string.strip(), 'Some Code inside pre tags')

    def test_unicode(self):
        # Test the unicode support of the textile formatter.
        text = u'\N{SNOWMAN}'
        result = self.formatter.format('format', text)
        soup = BeautifulSoup(result)
        self.assertEqual(soup.p.string.strip(), text)
