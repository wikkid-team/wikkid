#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.view module."""

from testtools import TestCase

from wikkid.view.utils import expand_wiki_name, title_for_filename


class TestExpandWikiName(TestCase):
    """Tests for expand_wiki_name."""

    def test_expand_wiki_name(self):
        self.assertEqual('simple.txt', expand_wiki_name('simple.txt'))
        self.assertEqual('nonMatching', expand_wiki_name('nonMatching'))
        self.assertEqual('README', expand_wiki_name('README'))
        self.assertEqual('Home', expand_wiki_name('Home'))
        self.assertEqual('Front Page', expand_wiki_name('FrontPage'))
        self.assertEqual('FrontPage.txt', expand_wiki_name('FrontPage.txt'))
        self.assertEqual('A Simple Page', expand_wiki_name('ASimplePage'))
        self.assertEqual('FTP Example', expand_wiki_name('FTPExample'))
        self.assertEqual(
            'A Simple FTP Example',
            expand_wiki_name('ASimpleFTPExample'))


class TesttitleForFilename(TestCase):
    """Tests for title_for_filename."""

    def test_title_for_filename(self):
        self.assertEqual('simple', title_for_filename('simple.txt'))
        self.assertEqual('simple.cpp', title_for_filename('simple.cpp'))
        self.assertEqual('Front Page', title_for_filename('FrontPage'))
        self.assertEqual('Front Page', title_for_filename('FrontPage.txt'))
        self.assertEqual('FrontPage.cpp', title_for_filename('FrontPage.cpp'))
