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

"""Tests for the model objects."""

from operator import attrgetter

from testtools import TestCase

from wikkid.filestore.volatile import FileStore
from wikkid.interface.resource import IDirectoryResource
from wikkid.model.factory import ResourceFactory
from wikkid.tests import ProvidesMixin


class TestDirectoryResource(TestCase, ProvidesMixin):

    def make_server(self, content=None):
        """Make a server with a volatile filestore."""
        filestore = FileStore(content)
        return ResourceFactory(filestore)

    def test_implements_interface(self):
        """DirectoryResource implements IDirectoryResource."""
        server = self.make_server([
                ('SomeDir/', None),
                ])
        dir_resource = server.get_resource_at_path('/SomeDir')
        self.assertProvides(dir_resource, IDirectoryResource)

    def test_directory_and_pages(self):
        """Both the directory and wiki page are returned."""
        server = self.make_server([
                ('SomeDir/', None),
                ('SomeDir.txt', 'Some content'),
                ])
        dir_resource = server.get_resource_at_path('/')
        listing = dir_resource.get_listing()
        some_dir, some_wiki = sorted(
            listing, key=attrgetter('path'))
        self.assertEqual('/SomeDir', some_dir.path)
        self.assertEqual('/SomeDir.txt', some_wiki.path)
