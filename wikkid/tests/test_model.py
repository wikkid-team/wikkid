#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the model objects."""

from operator import attrgetter

from testtools import TestCase

from wikkid.filestore.volatile import FileStore
from wikkid.interface.resource import IDirectoryResource
from wikkid.model.factory import ResourceFactory
from wikkid.tests import ProvidesMixin


class TestDirectoryResource(TestCase, ProvidesMixin):

    def make_factory(self, content=None):
        """Make a server with a volatile filestore."""
        filestore = FileStore(content)
        return ResourceFactory(filestore)

    def test_implements_interface(self):
        """DirectoryResource implements IDirectoryResource."""
        factory = self.make_factory([
                ('SomeDir/', None),
                ])
        dir_resource = factory.get_resource_at_path('/SomeDir')
        self.assertProvides(dir_resource, IDirectoryResource)

    def test_directory_and_pages(self):
        """Both the directory and wiki page are returned."""
        factory = self.make_factory([
                ('SomeDir/', None),
                ('SomeDir.txt', 'Some content'),
                ])
        dir_resource = factory.get_resource_at_path('/')
        listing = dir_resource.get_listing()
        some_dir, some_wiki = sorted(
            listing, key=attrgetter('path'))
        self.assertEqual('/SomeDir', some_dir.path)
        self.assertEqual('/SomeDir.txt', some_wiki.path)
