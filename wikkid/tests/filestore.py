#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The base test class for filestores."""

from datetime import datetime, timedelta

from wikkid.filestore import FileExists
from wikkid.interface.filestore import FileType, IFile, IFileStore


class TestFileStore(object):
    """Tests for the filestore and files."""

    def test_filestore_provides_IFileStore(self):
        filestore = self.make_filestore()
        self.assertProvides(filestore, IFileStore)

    def test_file_provides_IFile(self):
        filestore = self.make_filestore([('README', b'not much')])
        readme = filestore.get_file('README')
        self.assertProvides(readme, IFile)

    def test_file_gives_content(self):
        filestore = self.make_filestore([('README', b'Content')])
        readme = filestore.get_file('README')
        self.assertEqual(b'Content', readme.get_content())

    def assertDirectoryFileType(self, f):
        self.assertEqual(FileType.DIRECTORY, f.file_type)

    def assertTextFileType(self, f):
        self.assertEqual(FileType.TEXT_FILE, f.file_type)

    def assertBinaryFileType(self, f):
        self.assertEqual(FileType.BINARY_FILE, f.file_type)

    def test_file_type(self):
        filestore = self.make_filestore(
            [('README', b'Content'),
             ('lib/', None),
             ('lib/foo', b'dummy data'),
             ('image.jpg', b'pretend image'),
             ('binary-file', b'a\0binary\0file'),
             ('simple.txt', b'A text file'),
             ('source.cpp', b'A cpp file')])
        self.assertDirectoryFileType(filestore.get_file('lib'))
        self.assertTextFileType(filestore.get_file('README'))
        self.assertTextFileType(filestore.get_file('simple.txt'))
        self.assertTextFileType(filestore.get_file('source.cpp'))
        self.assertBinaryFileType(filestore.get_file('image.jpg'))
        self.assertBinaryFileType(filestore.get_file('binary-file'))

    def test_mimetype(self):
        filestore = self.make_filestore(
            [('README', b'Content'),
             ('lib/', None),
             ('lib/data', b'dummy data'),
             ('image.jpg', b'pretend image'),
             ('binary-file', b'a\0binary\0file'),
             ('simple.txt', b'A text file'),
             ('source.cpp', b'A cpp file')])
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
        filestore.update_file('first/second/third', b'content\n', user,
                              None)
        self.assertDirectory(filestore, 'first')
        self.assertDirectory(filestore, 'first/second')
        third = filestore.get_file('first/second/third')
        self.assertEqual(b'content\n', third.get_content())

    def test_updating_file_with_directory_clash(self):
        filestore = self.make_filestore(
            [('first', b'content')])
        user = None
        self.assertRaises(
            FileExists, filestore.update_file,
            'first/second', b'content', user, None)

    def test_updating_existing_file(self):
        filestore = self.make_filestore(
            [('README', b'Content'),
             ])
        user = 'Eric the viking <eric@example.com>'
        parent_rev = filestore.get_file('README').last_modified_in_revision
        filestore.update_file('README', b'new content\n', user, parent_rev)
        readme = filestore.get_file('README')
        self.assertEqual(b'new content\n', readme.get_content())

    def test_list_directory_non_existant(self):
        filestore = self.make_filestore()
        listing = filestore.list_directory('missing')
        self.assertIs(None, listing)

    def test_listing_directory_empty(self):
        filestore = self.make_filestore(
            [('empty/', None),
             ])
        listing = filestore.list_directory('empty')
        self.assertEqual([], listing)

    def test_listing_directory_of_a_file(self):
        # If a listing is attempted of a file, then None is returned.
        filestore = self.make_filestore(
            [('some-file', b'content'),
             ])
        listing = filestore.list_directory('some-file')
        self.assertIs(None, listing)

    def test_listing_directory_root(self):
        filestore = self.make_filestore(
            [('some-file', b'content'),
             ('another-file', b'a'),
             ('directory/', None),
             ('directory/subfile', b'b'),
             ])
        listing = filestore.list_directory(None)
        self.assertEqual(
            ['another-file', 'directory', 'some-file'],
            sorted(f.base_name for f in listing))

    def test_listing_directory_subdir(self):
        filestore = self.make_filestore(
            [('some-file', b'content'),
             ('another-file', b'a'),
             ('directory/', None),
             ('directory/subfile', b'b'),
             ('directory/another', b'a'),
             ])
        listing = filestore.list_directory('directory')
        self.assertEqual(
            ['another', 'subfile'],
            sorted(f.base_name for f in listing))

    def test_last_modified(self):
        # Make sure that the timestamp and author are recorded.
        start = datetime.utcnow() - timedelta(5)
        filestore = self.make_filestore()
        filestore.update_file(
            'new-file.txt',
            b'some content',
            'Test Author <test@example.com>',
            None)
        curr = filestore.get_file('new-file.txt')
        end = datetime.utcnow() + timedelta(5)
        # A new line is added to the end too.
        self.assertEqual(
            'Test Author <test@example.com>',
            curr.last_modified_by)

        self.assertTrue(
            start <= curr.last_modified_date <= end,
            '%r <= %r <= %r' % (start, curr.last_modified_date, end))
