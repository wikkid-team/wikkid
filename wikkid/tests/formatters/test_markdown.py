# -*- coding: utf-8 -*-
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.formatter.markdownformatter module."""

from textwrap import dedent

from bs4 import BeautifulSoup

# The markdown formatter is optional.  If the MarkdownFormatter is not
# available, the tests are skipped.
try:
    from wikkid.formatter.markdownformatter import MarkdownFormatter
    has_markdown = True
except ImportError:
    has_markdown = False
from wikkid.tests import TestCase


class TestMarkdownFormatter(TestCase):
    """Tests for the markdown formatter."""

    def setUp(self):
        TestCase.setUp(self)
        if has_markdown:
            self.formatter = MarkdownFormatter()
        else:
            self.skip('markdown formatter not available')

    def test_simple_headings(self):
        # A simple heading and a paragraph.
        text = dedent("""\
            Heading 1
            =========

            Heading 2
            ---------

            Simple sentence.
            """)
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result, features="lxml")
        self.assertEqual('Heading 1', soup.h1.string)
        self.assertEqual('Heading 2', soup.h2.string)
        # We don't care about whitespace on <p> tags, and markdown inserts
        # newlines.
        self.assertEqual('Simple sentence.', soup.p.string.strip())

    def test_detailed_headings(self):
        text = dedent("""\
            # Heading 1

            ## Heading 2

            ### Heading 3

            #### Heading 4

            ##### Heading 5

            ###### Heading 6""")
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result, features="lxml")
        self.assertEqual('Heading 1', soup.h1.string)
        self.assertEqual('Heading 2', soup.h2.string)
        self.assertEqual('Heading 3', soup.h3.string)
        self.assertEqual('Heading 4', soup.h4.string)
        self.assertEqual('Heading 5', soup.h5.string)
        self.assertEqual('Heading 6', soup.h6.string)

    def test_inline_link(self):
        # A paragraph containing a wiki word.
        text = "A link to the [FrontPage](http://127.0.0.1) helps."
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result, features="lxml")
        self.assertEqual('http://127.0.0.1', soup.a['href'])

    def test_reference_link(self):
        # A paragraph containing a wiki word.
        text = dedent("""\
            This is [an example][id] reference-style link.

            [id]: http://127.0.0.1
            """)
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result, features="lxml")
        self.assertEqual('http://127.0.0.1', soup.a['href'])

    def test_emphasis(self):
        texts = ('We can have *emphasis* and **strong** as well!',
                 'We can have _emphasis_ and __strong__ as well!')
        for text in texts:
            result = self.formatter.format('filename', text)
            soup = BeautifulSoup(result, features="lxml")
            self.assertEqual('emphasis', soup.em.string)
            self.assertEqual('strong', soup.strong.string)

    def test_blockquote(self):
        text = dedent("""\
            > This is a block quoted paragraph
            > that spans multiple lines.
            """)
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result, features="lxml")
        self.assertTrue(soup.blockquote is not None)

    def test_lists(self):
        text = dedent("""\
            Some Text.

             * UL 1
             * UL 2
             * UL 3

            Some More Text!

             1. OL 1
             2. OL 2
             7. OL 3
             """)
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result, features="lxml")

        self.assertIsNot(None, soup.ul)
        ulNodes = soup.ul.findAll('li')
        self.assertEqual(
            ['UL 1', 'UL 2', 'UL 3'],
            [node.string.strip() for node in ulNodes])

        self.assertIsNot(None, soup.ol)
        olNodes = soup.ol.findAll('li')
        self.assertEqual(
            ['OL 1', 'OL 2', 'OL 3'],
            [node.string.strip() for node in olNodes])

    def test_code_blocks(self):
        text = dedent("""\
            Some Normal Text.

                Some Code inside pre tags

            More Normal text.
            """)
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result, features="lxml")
        self.assertEqual(
            soup.pre.code.string.strip(), 'Some Code inside pre tags')

    def test_hr(self):
        # test different HR types:
        texts = ('* * *',
                 '***',
                 '*********',
                 '- - - -',
                 '------------------')
        for text in texts:
            result = self.formatter.format('filename', text)
            soup = BeautifulSoup(result, features="lxml")
            self.assertIsNot(None, soup.hr)

    def test_code(self):
        text = 'use the `printf()` function'
        result = self.formatter.format('filename', text)
        soup = BeautifulSoup(result, features="lxml")
        self.assertEqual('printf()', soup.code.string)

    def test_unicode(self):
        # Test the unicode support of the markdown formatter.
        text = u'\N{SNOWMAN}'
        result = self.formatter.format('format', text)
        soup = BeautifulSoup(result, features="lxml")
        self.assertEqual(soup.p.string.strip(), text)
