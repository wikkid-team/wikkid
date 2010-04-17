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

"""Tests for the wikkid.model.server."""

from testtools import TestCase

from wikkid.view.binary import BinaryFile
from wikkid.view.pages import (
    DirectoryListingPage,
    MissingPage,
    OtherTextPage,
    WikiPage,
    )
from wikkid.model.server import expand_wiki_name, Server
from wikkid.tests.fakes import TestUser
from wikkid.filestore.volatile import FileStore

# TODO: make a testing filestore that can produce either a volatile filestore
# or a bzr filestore.

class ServerTestCase(TestCase):

    def make_server(self, content=None):
        """Make a server with a volatile filestore."""
        filestore = FileStore(content)
        return Server(filestore)


class TestServer(ServerTestCase):
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

    def setUp(self):
        ServerTestCase.setUp(self)
        self.user = TestUser('test@emample.com', 'Test User')

    def test_get_page_directory(self):
        # A directory
        server = self.make_server([
                ('some-dir/', None),
                ])
        page = server.get_page('/some-dir', self.user)
        self.assertIsInstance(page, DirectoryListingPage)

    def test_get_page_source_file(self):
        # A text file that isn't .txt
        server = self.make_server([
                ('test.cpp', '// Some source'),
                ])
        page = server.get_page('/test.cpp', self.user)
        self.assertIsInstance(page, OtherTextPage)

    def test_get_page_wiki_page(self):
        # wiki pages end with a .txt
        server = self.make_server([
                ('a-wiki-page.txt', "Doesn't need caps."),
                ])
        page = server.get_page('/a-wiki-page.txt', self.user)
        self.assertIsInstance(page, WikiPage)

    def test_get_page_missing_page(self):
        # A missing file renders a missing page view.
        server = self.make_server()
        page = server.get_page('/Missing', self.user)
        self.assertIsInstance(page, MissingPage)

    def test_get_page_missing_file_with_suffix(self):
        # A missing file renders a missing page view.
        server = self.make_server()
        page = server.get_page('/missing.cpp', self.user)
        self.assertIsInstance(page, MissingPage)

    def test_get_page_wiki_no_suffix(self):
        # A wiki page can be accessed without the .txt
        server = self.make_server([
                ('WikiPage.txt', "Works with caps too."),
                ])
        page = server.get_page('/WikiPage', self.user)
        self.assertIsInstance(page, WikiPage)

    def test_get_page_wiki_with_matching_dir(self):
        # If the path matches a directory, but the .txt file exists with the
        # same name, then return return the wiki page.
        server = self.make_server([
                ('WikiPage.txt', "Works with caps too."),
                ('WikiPage/SubPage.txt', "A sub page."),
                ])
        page = server.get_page('/WikiPage', self.user)
        self.assertIsInstance(page, WikiPage)
        self.assertEqual('/WikiPage', page.request_path)
        self.assertEqual('WikiPage.txt', page.resource.path)

    def test_get_page_wiki_in_subdir(self):
        # If the path matches a directory, but the .txt file exists with the
        # same name, then return return the wiki page.
        server = self.make_server([
                ('WikiPage/SubPage.txt', "A sub page."),
                ])
        page = server.get_page('/WikiPage/SubPage', self.user)
        self.assertIsInstance(page, WikiPage)

    def test_get_page_root_path_no_front_page(self):
        # If the path matches a directory, but the .txt file exists with the
        # same name, then return return the wiki page.
        server = self.make_server()
        page = server.get_page('/', self.user)
        self.assertIsInstance(page, MissingPage)
        self.assertEqual('/', page.request_path)

    def test_get_page_root_file_exists(self):
        # If the path matches a directory, but the .txt file exists with the
        # same name, then return return the wiki page.
        server = self.make_server([
                ('Home.txt', "The first page."),
                ])
        page = server.get_page('/', self.user)
        self.assertIsInstance(page, WikiPage)
        self.assertEqual('/', page.request_path)
        self.assertEqual('Home.txt', page.resource.path)

    def test_get_page_binary_file(self):
        # Images are served as binary files.
        server = self.make_server([
                ('image.png', "An image."),
                ])
        page = server.get_page('/image.png', self.user)
        self.assertIsInstance(page, BinaryFile)

    def test_update_page_new_file(self):
        # update_page will add a new file if it doesn't exist.
        server = self.make_server()
        server.update_page(
            '/NewPage', self.user, None, 'page content', 'add new page')
        page = server.get_page('/NewPage', self.user)
        self.assertIsInstance(page, WikiPage)
        self.assertEqual('/NewPage', page.request_path)
        self.assertEqual('NewPage.txt', page.resource.path)


class TestServerGetInfo(ServerTestCase):
    """Test the get_info method of the Server class."""

    def test_get_info_root_no_content(self):
        # If the root file is selected, and there is no content, there is no
        # read_filename or file_resource, but there is a write_filename for
        # the default home page.
        server = self.make_server()
        info = server.get_info('/')
        self.assertEqual('/', info.path)
        self.assertEqual('Home.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_info_root_has_page(self):
        # If the root file is selected, and there is a home page, this is
        # returned.
        server = self.make_server([
                ('Home.txt', 'the home page'),
                ])
        info = server.get_info('/')
        self.assertEqual('/', info.path)
        self.assertEqual('Home.txt', info.write_filename)
        self.assertEqual('Home.txt', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_info_missing_file(self):
        # A missing file as no read filename, nor resource, but does have
        # a write file name.
        server = self.make_server()
        info = server.get_info('/missing-file')
        self.assertEqual('/missing-file', info.path)
        self.assertEqual('missing-file.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_info_existing_file_no_suffix(self):
        # If a file is requested that exists but has no suffix, it is returned
        # unaltered.
        server = self.make_server([
                ('README', 'A readme file'),
                ])
        info = server.get_info('/README')
        self.assertEqual('/README', info.path)
        self.assertEqual('README', info.write_filename)
        self.assertEqual('README', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_info_missing_file_not_text(self):
        # A missing file is requested, but has a suffix, don't attempt to add
        # a .txt to it.
        server = self.make_server()
        info = server.get_info('/missing-file.cpp')
        self.assertEqual('/missing-file.cpp', info.path)
        self.assertEqual('missing-file.cpp', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_info_directory(self):
        # A directory without a matching text file doesn't have a
        # read_filename either, but does have a dir_resource.
        server = self.make_server([
                ('SomeDir/', None),
                ])
        info = server.get_info('/SomeDir')
        self.assertEqual('/SomeDir', info.path)
        self.assertEqual('SomeDir.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertEqual('SomeDir', info.dir_resource.path)

    def test_get_info_directory_with_page(self):
        # A directory with a matching text file has a text resource and a dir
        # resource.
        server = self.make_server([
                ('SomeDir/', None),
                ('SomeDir.txt', 'Some content'),
                ])
        info = server.get_info('/SomeDir')
        self.assertEqual('/SomeDir', info.path)
        self.assertEqual('SomeDir.txt', info.write_filename)
        self.assertEqual('SomeDir.txt', info.file_resource.path)
        self.assertIsNot('SomeDir', info.dir_resource)

    def test_get_info_page_no_directory(self):
        # A directory with a matching text file has a text resource and a dir
        # resource.
        server = self.make_server([
                ('SomeDir.txt', 'Some content'),
                ])
        info = server.get_info('/SomeDir')
        self.assertEqual('/SomeDir', info.path)
        self.assertEqual('SomeDir.txt', info.write_filename)
        self.assertEqual('SomeDir.txt', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_info_subdirs_missing_file(self):
        # The path info reflects the request path.
        server = self.make_server()
        info = server.get_info('/a/b/c/d')
        self.assertEqual('/a/b/c/d', info.path)
        self.assertEqual('a/b/c/d.txt', info.write_filename)
        self.assertIs(None, info.file_resource)
        self.assertIs(None, info.dir_resource)

    def test_get_info_subdirs_existing_file(self):
        # The path info reflects the request path.
        server = self.make_server([
                ('a/b/c/d.txt', 'a text file'),
                ])
        info = server.get_info('/a/b/c/d')
        self.assertEqual('/a/b/c/d', info.path)
        self.assertEqual('a/b/c/d.txt', info.write_filename)
        self.assertEqual('a/b/c/d.txt', info.file_resource.path)
        self.assertIs(None, info.dir_resource)

    def test_get_info_subdirs_existing_file_and_dir(self):
        # The path info reflects the request path.
        server = self.make_server([
                ('a/b/c/d.txt', 'a text file'),
                ('a/b/c/d/e.txt', 'another text file'),
                ])
        info = server.get_info('/a/b/c/d')
        self.assertEqual('/a/b/c/d', info.path)
        self.assertEqual('a/b/c/d.txt', info.write_filename)
        self.assertEqual('a/b/c/d.txt', info.file_resource.path)
        self.assertEqual('a/b/c/d', info.dir_resource.path)


class TestServerGetPreferredPath(ServerTestCase):
    """Tests for the get_preferred_path method of the Server class."""

    def test_home_preferred(self):
        server = self.make_server()
        self.assertEqual('/', server.get_preferred_path('/'))
        self.assertEqual('/', server.get_preferred_path('/Home'))
        self.assertEqual('/', server.get_preferred_path('/Home.txt'))

    def test_default_preferred(self):
        server = self.make_server()
        server.DEFAULT_PATH = 'FrontPage'
        self.assertEqual('/', server.get_preferred_path('/'))
        self.assertEqual('/', server.get_preferred_path('/FrontPage'))
        self.assertEqual('/', server.get_preferred_path('/FrontPage.txt'))

    def test_image_preferred(self):
        server = self.make_server()
        self.assertEqual(
            '/foo/bar.jpg',
            server.get_preferred_path('/foo/bar.jpg'))

    def test_text_preferred(self):
        server = self.make_server()
        self.assertEqual('/README', server.get_preferred_path('/README'))
        self.assertEqual('/a.b.txt', server.get_preferred_path('/a.b.txt'))
        self.assertEqual('/a', server.get_preferred_path('/a.txt'))
        self.assertEqual('/a/b', server.get_preferred_path('/a/b.txt'))


class TestServerGetParentInfo(ServerTestCase):
    """Test the get_parent_info method of the Server class."""

    def test_get_parent_info_root(self):
        # The parent of root is None.
        server = self.make_server()
        info = server.get_info('/')
        self.assertIs(None, server.get_parent_info(info))

    def test_get_parent_info_page(self):
        # If a non default page in the root directory is asked for, the parent
        # of that page is the default page.
        server = self.make_server()
        info = server.get_info('/MissingPage')
        parent = server.get_parent_info(info)
        self.assertEqual('/', parent.path)
        self.assertEqual('Home', parent.title)

    def test_get_parent_subdir(self):
        server = self.make_server()
        info = server.get_info('/SomePage/SubPage')
        parent = server.get_parent_info(info)
        self.assertEqual('/SomePage', parent.path)


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
