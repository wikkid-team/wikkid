#
# Copyright (C) 2012 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.filestore.git.FileStore."""

from dulwich.repo import MemoryRepo

from wikkid.filestore.git import (
    FileStore,
    )
from wikkid.tests import ProvidesMixin, TestCase
from wikkid.tests.filestore import TestFileStore


class TestGitFileStore(TestCase, ProvidesMixin, TestFileStore):
    """Tests for the git filestore and files."""

    def make_filestore(self, contents=None):
        repo = MemoryRepo()
        fs = FileStore(repo)
        if contents:
            for (path, contents) in contents:
                if contents is None:
                    # Directory
                    continue
                fs.update_file(
                    path, contents,
                    author="Somebody <test@example.com>",
                    parent_revision=None,
                    commit_message="Added by make_filestore")
        return fs

    def test_empty(self):
        # Empty files do not have line endings, but they can be saved
        # nonetheless.
        filestore = self.make_filestore(
            [('test.txt', b'several\nlines\nof\ncontent')])
        f = filestore.get_file('test.txt')
        base_rev = f.last_modified_in_revision
        filestore.update_file(
            'test.txt', b'', 'Test Author <test@example.com>', base_rev)
        curr = filestore.get_file('test.txt')
        self.assertEqual(b'', curr.get_content())

    def test_listing_directory_empty(self):
        filestore = self.make_filestore(
            [('empty/', None)])
        listing = filestore.list_directory('empty')
        self.assertIs(None, listing)
