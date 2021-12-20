#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the model objects."""

from operator import attrgetter

from wikkid.interface.resource import (
    IDefaultPage, IDirectoryResource, IMissingResource, IRootResource,
    IWikiTextFile)
from wikkid.tests.factory import FactoryTestCase


class TestBaseRootResource(FactoryTestCase):
    """Tests for BaseResource.root_resource."""

    def test_root_can_get_root(self):
        """Even the root resource can get the root resource."""
        factory = self.make_factory()
        resource = factory.get_resource_at_path('/')
        root = resource.root_resource
        self.assertProvides(root, IRootResource)

    def test_missing_can_get_root(self):
        """Even the root resource can get the root resource."""
        factory = self.make_factory()
        resource = factory.get_resource_at_path('/MissingPage')
        root = resource.root_resource
        self.assertProvides(root, IRootResource)


class TestBaseDefaultResource(FactoryTestCase):
    """Tests for BaseResource.default_resource."""

    def test_default_when_missing(self):
        """If the default is missing, then a missing resource is returned for
        the default path.
        """
        factory = self.make_factory()
        resource = factory.get_resource_at_path('/')
        home = resource.default_resource
        self.assertProvides(home, IMissingResource)
        self.assertProvides(home, IDefaultPage)
        self.assertEqual('/Home', home.preferred_path)

    def test_default_when_exists(self):
        """If the default exists, the default wiki page is returned."""
        factory = self.make_factory([
                ('Home.txt', 'Some content'),
                ])
        resource = factory.get_resource_at_path('/')
        home = resource.default_resource
        self.assertProvides(home, IWikiTextFile)
        self.assertProvides(home, IDefaultPage)
        self.assertEqual('/Home', home.preferred_path)

    def test_default_different_name(self):
        """If the default name has been overridden, then the default_resource
        attribute returns the correct name.
        """
        factory = self.make_factory([
                ('FrontPage.txt', 'Some content'),
                ])
        factory.DEFAULT_PATH = 'FrontPage'
        resource = factory.get_resource_at_path('/')
        home = resource.default_resource
        self.assertProvides(home, IWikiTextFile)
        self.assertProvides(home, IDefaultPage)
        self.assertEqual('/FrontPage', home.preferred_path)


class TestBaseParent(FactoryTestCase):
    """Tests for the BaseResource.parent attribute."""

    def test_parent_for_root(self):
        """Root shouldn't have a parent."""
        factory = self.make_factory()
        root = factory.get_root_resource()
        self.assertIs(None, root.parent)

    def test_parent_for_default(self):
        """The default's parent should be root."""
        factory = self.make_factory()
        home = factory.get_default_resource()
        parent = home.parent
        self.assertProvides(parent, IRootResource)

    def test_parent_for_page(self):
        """Any page in the root directory has root as its parent."""
        factory = self.make_factory([
                ('SomeDir.txt', 'Some content'),
                ])
        home = factory.get_resource_at_path('/SomeDir')
        parent = home.parent
        self.assertProvides(parent, IRootResource)

    def test_parent_for_subpage(self):
        """The path of the parent should be the parent directory."""
        factory = self.make_factory([
                ('SomeDir/', None),
                ('SomeDir.txt', 'Some content'),
                ])
        missing = factory.get_resource_at_path('/SomeDir/NoPage')
        parent = missing.parent
        expected = factory.get_resource_at_path('/SomeDir')
        self.assertEquals(expected.preferred_path, parent.preferred_path)


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
