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

from wikkid.errors import FileExists
from wikkid.interfaces import FileType, IFile, IFileStore


class TestFileStore:
    """Tests for the filestore and files."""

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

    def assertDirectoryFileType(self, f):
        self.assertEqual(FileType.DIRECTORY, f.file_type)

    def assertTextFileType(self, f):
        self.assertEqual(FileType.TEXT_FILE, f.file_type)

    def assertBinaryFileType(self, f):
        self.assertEqual(FileType.BINARY_FILE, f.file_type)

    def test_file_type(self):
        filestore = self.make_filestore(
            [('README', 'Content'),
             ('lib/', None),
             ('image.jpg', 'pretend image'),
             ('binary-file', 'a\0binary\0file'),
             ('simple.txt', 'A text file'),
             ('source.cpp', 'A cpp file')])
        self.assertDirectoryFileType(filestore.get_file('lib'))
        self.assertTextFileType(filestore.get_file('README'))
        self.assertTextFileType(filestore.get_file('simple.txt'))
        self.assertTextFileType(filestore.get_file('source.cpp'))
        self.assertBinaryFileType(filestore.get_file('image.jpg'))
        self.assertBinaryFileType(filestore.get_file('binary-file'))

    def test_mimetype(self):
        filestore = self.make_filestore(
            [('README', 'Content'),
             ('lib/', None),
             ('image.jpg', 'pretend image'),
             ('binary-file', 'a\0binary\0file'),
             ('simple.txt', 'A text file'),
             ('source.cpp', 'A cpp file')])
        self.assertIs(None, filestore.get_file('lib').mimetype)
        self.assertIs(None, filestore.get_file('README').mimetype)
        self.assertEqual(
            'text/plain', filestore.get_file('simple.txt').mimetype)
        self.assertEqual(
            'text/x-c++src', filestore.get_file('source.cpp').mimetype)
        self.assertEqual(
            'image/jpeg', filestore.get_file('image.jpg').mimetype)
        self.assertIs(None, filestore.get_file('binary-file').mimetype)

    def test_nonexistant_file(self):
        filestore = self.make_filestore()
        readme = filestore.get_file('README')
        self.assertIs(None, readme)

    def assertDirectory(self, filestore, path):
        """The filestore should have a directory at path."""
        location = filestore.get_file(path)
        self.assertDirectoryFileType(location)

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
