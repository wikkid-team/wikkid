#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.model.factory module."""

from wikkid.interface.resource import (
    IBinaryFile,
    IDirectoryResource,
    IMissingResource,
    IRootResource,
    ISourceTextFile,
    IWikiTextFile,
    )
from wikkid.tests.factory import FactoryTestCase

# TODO: make a testing filestore that can produce either a volatile filestore
# or a bzr filestore.


class TestFactoryGetResourceAtPath(FactoryTestCase):
    """Test the get_resource_at_path method of the Factory class."""

    def test_get_resource_at_path_root_no_content(self):
        # If the root file is selected, and there is no content, there is no
        # read_filename or file_resource, but there is a write_filename for
        # the default home page.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/')
        self.assertProvides(info, IRootResource)
        self.assertEqual('/', info.path)
        self.assertIs(None, info.get_dir_name())
        self.assertIs(None, info.dir_resource)
        self.assertFalse(info.has_home_page)

    def test_get_resource_at_path_root_has_page(self):
        # If the root file is selected, and there is a home page, this is
        # returned.
        factory = self.make_factory([
                ('Home.txt', b'the home page'),
                ])
        info = factory.get_resource_at_path('/')
        self.assertProvides(info, IRootResource)
        self.assertEqual('/', info.path)
        self.assertIs(None, info.get_dir_name())
        self.assertIs(None, info.dir_resource)
        self.assertEqual('Home.txt', info.file_resource.path)
        self.assertTrue(info.has_home_page)

    def test_get_resource_at_path_missing_file(self):
        # A missing file as no read filename, nor resource, but does have
        # a write file name.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/missing-file')
        self.assertProvides(info, IMissingResource)
        self.assertEqual('/missing-file', info.path)
        self.assertEqual('missing-file.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_existing_file_no_suffix(self):
        # If a file is requested that exists but has no suffix, it is returned
        # unaltered, and is interpreted as a wiki page.
        factory = self.make_factory([
                ('README', b'A readme file'),
                ])
        info = factory.get_resource_at_path('/README')
        self.assertProvides(info, IWikiTextFile)
        self.assertEqual('/README', info.path)
        self.assertEqual('README', info.write_filename)
        self.assertEqual('README', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_missing_file_not_text(self):
        # A missing file is requested, but has a suffix, don't attempt to add
        # a .txt to it.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/missing-file.cpp')
        self.assertProvides(info, IMissingResource)
        self.assertEqual('/missing-file.cpp', info.path)
        self.assertEqual('missing-file.cpp', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_not_text(self):
        # If a file is reqeusted that has a suffix that isn't text,
        # a source text file object is returned,
        factory = self.make_factory([
                ('sample.cpp', b'A c++ file'),
                ])
        info = factory.get_resource_at_path('/sample.cpp')
        self.assertProvides(info, ISourceTextFile)
        self.assertEqual('/sample.cpp', info.path)
        self.assertEqual('sample.cpp', info.write_filename)
        self.assertEqual('sample.cpp', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_binary_file(self):
        # If a file exists and is binary, a binary file is returned.
        factory = self.make_factory([
                ('sample.png', b'A picture'),
                ])
        info = factory.get_resource_at_path('/sample.png')
        self.assertProvides(info, IBinaryFile)
        self.assertEqual('/sample.png', info.path)
        self.assertEqual('sample.png', info.write_filename)
        self.assertEqual('sample.png', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_directory(self):
        # A directory without a matching text file doesn't have a
        # read_filename either, but does have a dir_resource.
        factory = self.make_factory([
                ('SomeDir/', None),
                ])
        info = factory.get_resource_at_path('/SomeDir')
        self.assertProvides(info, IDirectoryResource)
        self.assertEqual('/SomeDir', info.path)
        self.assertEqual('SomeDir.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertEqual('SomeDir', info.get_dir_name())

    def test_get_resource_at_path_directory_with_page(self):
        # A directory with a matching text file has a text resource and a dir
        # resource.
        factory = self.make_factory([
                ('SomeDir/', None),
                ('SomeDir.txt', b'Some content'),
                ])
        info = factory.get_resource_at_path('/SomeDir')
        self.assertProvides(info, IWikiTextFile)
        self.assertEqual('/SomeDir', info.path)
        self.assertEqual('SomeDir.txt', info.write_filename)
        self.assertEqual('SomeDir.txt', info.file_resource.path)
        self.assertIsNot('SomeDir', info.dir_resource)

    def test_get_resource_at_path_page_no_directory(self):
        # A directory with a matching text file has a text resource and a dir
        # resource.
        factory = self.make_factory([
                ('SomeDir.txt', b'Some content'),
                ])
        info = factory.get_resource_at_path('/SomeDir')
        self.assertProvides(info, IWikiTextFile)
        self.assertEqual('/SomeDir', info.path)
        self.assertEqual('SomeDir.txt', info.write_filename)
        self.assertEqual('SomeDir.txt', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_subdirs_missing_file(self):
        # The path info reflects the request path.
        factory = self.make_factory()
        info = factory.get_resource_at_path('/a/b/c/d')
        self.assertProvides(info, IMissingResource)
        self.assertEqual('/a/b/c/d', info.path)
        self.assertEqual('a/b/c/d.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_subdirs_existing_file(self):
        # The path info reflects the request path.
        factory = self.make_factory([
                ('a/b/c/d.txt', b'a text file'),
                ])
        info = factory.get_resource_at_path('/a/b/c/d')
        self.assertProvides(info, IWikiTextFile)
        self.assertEqual('/a/b/c/d', info.path)
        self.assertEqual('a/b/c/d.txt', info.write_filename)
        self.assertEqual('a/b/c/d.txt', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_resource_at_path_subdirs_existing_file_and_dir(self):
        # The path info reflects the request path.
        factory = self.make_factory([
                ('a/b/c/d.txt', b'a text file'),
                ('a/b/c/d/e.txt', b'another text file'),
                ])
        info = factory.get_resource_at_path('/a/b/c/d')
        self.assertProvides(info, IWikiTextFile)
        self.assertEqual('/a/b/c/d', info.path)
        self.assertEqual('a/b/c/d.txt', info.write_filename)
        self.assertEqual('a/b/c/d.txt', info.file_resource.path)
        self.assertEqual('a/b/c/d', info.dir_resource.path)


class TestFactoryGetPreferredPath(FactoryTestCase):
    """Tests for the get_preferred_path method of the Factory class."""

    def test_home_preferred(self):
        factory = self.make_factory()
        self.assertEqual('/Home', factory.get_preferred_path('/'))
        self.assertEqual('/Home', factory.get_preferred_path('/Home'))
        self.assertEqual('/Home', factory.get_preferred_path('/Home.txt'))

    def test_default_preferred(self):
        factory = self.make_factory()
        factory.DEFAULT_PATH = 'FrontPage'
        self.assertEqual(
            '/FrontPage', factory.get_preferred_path('/'))
        self.assertEqual(
            '/FrontPage', factory.get_preferred_path('/FrontPage'))
        self.assertEqual(
            '/FrontPage', factory.get_preferred_path('/FrontPage.txt'))

    def test_image_preferred(self):
        factory = self.make_factory()
        self.assertEqual(
            '/foo/bar.jpg', factory.get_preferred_path('/foo/bar.jpg'))

    def test_text_preferred(self):
        factory = self.make_factory()
        self.assertEqual('/README', factory.get_preferred_path('/README'))
        self.assertEqual('/a.b.txt', factory.get_preferred_path('/a.b.txt'))
        self.assertEqual('/a', factory.get_preferred_path('/a.txt'))
        self.assertEqual('/a/b', factory.get_preferred_path('/a/b.txt'))
