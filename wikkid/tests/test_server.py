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

"""Tests for the wikkid.server."""

from testtools import TestCase

from wikkid.interfaces import FileType
from wikkid.server import Server
from wikkid.tests.fakes import TestUserFactory
from wikkid.volatile.filestore import FileStore

# TODO: make a testing filestore that can produce either a volatile filestore
# or a bzr filestore.


class TestServer(TestCase):
    """Tests for the Wikkid Server.

    I'm going to write a few notes here.  I want to make sure that the server
    has meaningful names, but also is functional enough.  I have been thinking
    over the last few days that the IFile inteface needs to expose the file-id
    of the underlying file for those cases where the file is moved by one
    person, and edited by another.  I makes sense to use the functionality of
    bzr here to have good editing while moving the file.

    Also since I want this designed in a way that it will integrate well into
    Launchpad, we need to expose partial rendering of the underlying files
    through the interface.  There may well be images or binaries stored as
    part of the branch that need to be served directly (or as directly as
    possible), but also we need to be able to access the rendered page before
    any rendering into a skin.

    I want to provide meaningful directory type listings, but that also means
    doing the on-the-fly conversion of files to 'wiki pages'.  We then want to
    be able to traverse a directory, and product a list of tuples (or objects)
    which define the display name, filename, and mimetype.

    Wiki pages are going to be quite tightly defined.  Must have a wiki name
    (Sentence case joined word), ending in '.txt'.

    What should we do about HTML files that are stored in the branch?
    """

    def make_server(self, content=None):
        """Make a server with a volatile filestore."""
        filestore = FileStore(content)
        return Server(filestore, TestUserFactory())

    def test_missing_resource(self):
        # If the path doesn't exist in the filestore, then the resoruce info
        # shows a missing status.
        server = self.make_server()
        info = server.get_info('a-file')
        self.assertEqual(FileType.MISSING, info.status)
        self.assertEqual('a-file', info.path)
        self.assertIs(None, info.display_name)
        self.assertIs(None, info.mimetype)

    def test_text_file(self):
        # A normal text file is text/plain.
        server = self.make_server([
                ('readme.txt', 'A readme file.')])
        info = server.get_info('readme.txt')
        self.assertEqual(FileType.TEXT_FILE, info.status)
        self.assertEqual('readme.txt', info.path)
        self.assertEqual('readme.txt', info.display_name)
        self.assertEqual('text/plain', info.mimetype)

    def test_text_file_non_root_dir(self):
        # The path of the info is the full path, but the display name is the
        # filename.
        server = self.make_server([
                ('somedir/readme.txt', 'A readme file.')])
        info = server.get_info('somedir/readme.txt')
        self.assertEqual(FileType.TEXT_FILE, info.status)
        self.assertEqual('somedir/readme.txt', info.path)
        self.assertEqual('readme.txt', info.display_name)
        self.assertEqual('text/plain', info.mimetype)

    def test_cpp_file(self):
        # A C++ source file has a specific mime type.
        server = self.make_server([
                ('test.cpp', '// This is a comment.')])
        info = server.get_info('test.cpp')
        self.assertEqual(FileType.TEXT_FILE, info.status)
        self.assertEqual('text/x-c++src', info.mimetype)

    def test_image(self):
        # An image is binary.
        server = self.make_server([
                ('test.jpg', 'Some\0binary\0content')])
        info = server.get_info('test.jpg')
        self.assertEqual(FileType.BINARY_FILE, info.status)
        self.assertEqual('image/jpeg', info.mimetype)

