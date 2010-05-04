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

"""Tests for the wikkid.view module."""

from testtools import TestCase

from wikkid.view.base import expand_wiki_name


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
