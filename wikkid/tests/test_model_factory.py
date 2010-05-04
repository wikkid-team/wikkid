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

"""Tests for the wikkid.model.factory module."""

from testtools import TestCase

from wikkid.model.factory import ResourceFactory
from wikkid.filestore.volatile import FileStore

# TODO: make a testing filestore that can produce either a volatile filestore
# or a bzr filestore.

class FactoryTestCase(TestCase):

    def make_factory(self, content=None):
        """Make a factory with a volatile filestore."""
        filestore = FileStore(content)
        return ResourceFactory(filestore)


class TestFactoryGetResourceAtPath(FactoryTestCase):
    """Test the get_resource_at_path method of the Factory class."""

    def test_get_resource_at_path_root_no_content(self):
        # If the root file is selected, and there is no content, there is no
        # read_filename or file_resource, but there is a write_filename for
        # the default home page.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/')
        self.assertEqual('/', info.path)
        self.assertEqual('Home.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_root_has_page(self):
        # If the root file is selected, and there is a home page, this is
        # returned.
        factory = self.make_factory([
                ('Home.txt', 'the home page'),
                ])
        info = factory.get_resource_at_path('/')
        self.assertEqual('/', info.path)
        self.assertEqual('Home.txt', info.write_filename)
        self.assertEqual('Home.txt', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_missing_file(self):
        # A missing file as no read filename, nor resource, but does have
        # a write file name.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/missing-file')
        self.assertEqual('/missing-file', info.path)
        self.assertEqual('missing-file.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_existing_file_no_suffix(self):
        # If a file is requested that exists but has no suffix, it is returned
        # unaltered.
        factory = self.make_factory([
                ('README', 'A readme file'),
                ])
        info = factory.get_resource_at_path('/README')
        self.assertEqual('/README', info.path)
        self.assertEqual('README', info.write_filename)
        self.assertEqual('README', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_missing_file_not_text(self):
        # A missing file is requested, but has a suffix, don't attempt to add
        # a .txt to it.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/missing-file.cpp')
        self.assertEqual('/missing-file.cpp', info.path)
        self.assertEqual('missing-file.cpp', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_directory(self):
        # A directory without a matching text file doesn't have a
        # read_filename either, but does have a dir_resource.
        factory = self.make_factory([
                ('SomeDir/', None),
                ])
        info = factory.get_resource_at_path('/SomeDir')
        self.assertEqual('/SomeDir', info.path)
        self.assertEqual('SomeDir.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertEqual('SomeDir', info.dir_resource.path)

    def test_get_resource_at_path_directory_with_page(self):
        # A directory with a matching text file has a text resource and a dir
        # resource.
        factory = self.make_factory([
                ('SomeDir/', None),
                ('SomeDir.txt', 'Some content'),
                ])
        info = factory.get_resource_at_path('/SomeDir')
        self.assertEqual('/SomeDir', info.path)
        self.assertEqual('SomeDir.txt', info.write_filename)
        self.assertEqual('SomeDir.txt', info.file_resource.path)
        self.assertIsNot('SomeDir', info.dir_resource)

    def test_get_resource_at_path_page_no_directory(self):
        # A directory with a matching text file has a text resource and a dir
        # resource.
        factory = self.make_factory([
                ('SomeDir.txt', 'Some content'),
                ])
        info = factory.get_resource_at_path('/SomeDir')
        self.assertEqual('/SomeDir', info.path)
        self.assertEqual('SomeDir.txt', info.write_filename)
        self.assertEqual('SomeDir.txt', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_subdirs_missing_file(self):
        # The path info reflects the request path.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/a/b/c/d')
        self.assertEqual('/a/b/c/d', info.path)
        self.assertEqual('a/b/c/d.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_subdirs_existing_file(self):
        # The path info reflects the request path.
        factory = self.make_factory([
                ('a/b/c/d.txt', 'a text file'),
                ])
        info = factory.get_resource_at_path('/a/b/c/d')
        self.assertEqual('/a/b/c/d', info.path)
        self.assertEqual('a/b/c/d.txt', info.write_filename)
        self.assertEqual('a/b/c/d.txt', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_subdirs_existing_file_and_dir(self):
        # The path info reflects the request path.
        factory = self.make_factory([
                ('a/b/c/d.txt', 'a text file'),
                ('a/b/c/d/e.txt', 'another text file'),
                ])
        info = factory.get_resource_at_path('/a/b/c/d')
        self.assertEqual('/a/b/c/d', info.path)
        self.assertEqual('a/b/c/d.txt', info.write_filename)
        self.assertEqual('a/b/c/d.txt', info.file_resource.path)
        self.assertEqual('a/b/c/d', info.dir_resource.path)


class TestFactoryGetPreferredPath(FactoryTestCase):
    """Tests for the get_preferred_path method of the Factory class."""

    def test_home_preferred(self):
        factory = self.make_factory()
        self.assertEqual('/', factory.get_preferred_path('/'))
        self.assertEqual('/', factory.get_preferred_path('/Home'))
        self.assertEqual('/', factory.get_preferred_path('/Home.txt'))

    def test_default_preferred(self):
        factory = self.make_factory()
        factory.DEFAULT_PATH = 'FrontPage'
        self.assertEqual('/', factory.get_preferred_path('/'))
        self.assertEqual('/', factory.get_preferred_path('/FrontPage'))
        self.assertEqual('/', factory.get_preferred_path('/FrontPage.txt'))

    def test_image_preferred(self):
        factory = self.make_factory()
        self.assertEqual(
            '/foo/bar.jpg',
            factory.get_preferred_path('/foo/bar.jpg'))

    def test_text_preferred(self):
        factory = self.make_factory()
        self.assertEqual('/README', factory.get_preferred_path('/README'))
        self.assertEqual('/a.b.txt', factory.get_preferred_path('/a.b.txt'))
        self.assertEqual('/a', factory.get_preferred_path('/a.txt'))
        self.assertEqual('/a/b', factory.get_preferred_path('/a/b.txt'))


class TestFactoryGetParentInfo(FactoryTestCase):
    """Test the get_parent_info method of the Factory class."""

    def test_get_parent_info_root(self):
        # The parent of root is None.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/')
        self.assertIs(None, factory.get_parent_info(info))

    def test_get_parent_info_page(self):
        # If a non default page in the root directory is asked for, the parent
        # of that page is the default page.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/MissingPage')
        parent = factory.get_parent_info(info)
        self.assertEqual('/', parent.path)

    def test_get_parent_subdir(self):
        factory = self.make_factory()
        info = factory.get_resource_at_path('/SomePage/SubPage')
        parent = factory.get_parent_info(info)
        self.assertEqual('/SomePage', parent.path)
