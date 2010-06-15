#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the model objects."""

from operator import attrgetter

from wikkid.interface.resource import IDirectoryResource
from wikkid.tests.factory import FactoryTestCase


class TestDirectoryResource(FactoryTestCase):

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

    def test_user_for_file(self):
        """Test that the user is a user object."""
        factory = self.make_factory()
        page = factory.get_resource_at_path('/testing')
        page.put_bytes(
            'hello world', 'Test User <test@example.com>', None, None)
        new_page = factory.get_resource_at_path('/testing')
        user = new_page.last_modified_by
        self.assertEqual('Test User', user.display_name)
        self.assertEqual('test@example.com', user.email)

