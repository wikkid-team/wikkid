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

"""Tests for the wikkid.bzr.FileStore."""

from wikkid.bzr.filestore import FileStore
from wikkid.errors import FileExists
from wikkid.interfaces import IFile, IFileStore
from wikkid.tests import ProvidesMixin

from bzrlib.tests import TestCaseWithTransport


class TestBzrFileStore(TestCaseWithTransport, ProvidesMixin):
    """Tests for the bzr filestore and files."""

    def make_filestore(self, contents=None):
        tree = self.make_branch_and_tree('.')
        if contents:
            self.build_tree_contents(contents)
        tree.smart_add(['.'])
        tree.commit(message='Initial commit', authors=['test@example.com'])
        return FileStore(tree)

    def test_filestore_provides_IFileStore(self):
        filestore = self.make_filestore()
        self.assertProvides(filestore, IFileStore)

    def test_file_provides_IFile(self):
        filestore = self.make_filestore([('README', 'not much')])
        readme = filestore.get_file('README')
        self.assertProvides(readme, IFile)

    def test_file_gives_content(self):
        filestore = self.make_filestore([('README', 'Content')])
        readme = filestore.get_file('README')
        self.assertEqual('Content', readme.get_content())

    def test_file_is_directory(self):
        filestore = self.make_filestore(
            [('README', 'Content'),
             ('lib/', None)])
        self.assertFalse(filestore.get_file('README').is_directory)
        self.assertTrue(filestore.get_file('lib').is_directory)

    def test_file_is_binary(self):
        filestore = self.make_filestore(
            [('README', 'Content'),
             ('image.png', 'some\0zero\0containing\0string'),
             ('lib/', None)])
        self.assertFalse(filestore.get_file('README').is_binary)
        self.assertTrue(filestore.get_file('lib').is_binary)
        self.assertTrue(filestore.get_file('image.png').is_binary)

    def test_nonexistant_file(self):
        filestore = self.make_filestore()
        readme = filestore.get_file('README')
        self.assertIs(None, readme)

    def assertDirectory(self, filestore, path):
        """The filestore should have a directory at path."""
        location = filestore.get_file(path)
        self.assertTrue(location.is_directory)

    def test_updating_file_adds_directories(self):
        filestore = self.make_filestore()
        user = 'Eric the viking <eric@example.com>'
        filestore.update_file('first/second/third', 'content', user,
                              None)
        self.assertDirectory(filestore, 'first')
        self.assertDirectory(filestore, 'first/second')
        third = filestore.get_file('first/second/third')
        self.assertEqual('content', third.get_content())

    def test_updating_file_with_directory_clash(self):
        filestore = self.make_filestore(
            [('first', 'content')])
        user = None
        self.assertRaises(
            FileExists, filestore.update_file,
            'first/second', 'content', user, None)

    def test_updating_existing_file(self):
        filestore = self.make_filestore(
            [('README', 'Content'),
             ])
        user = 'Eric the viking <eric@example.com>'
        filestore.update_file('README', 'new content', user,
                              None)
        readme = filestore.get_file('README')
        self.assertEqual('new content', readme.get_content())
