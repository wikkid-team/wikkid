#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.filestore.bzr.FileStore."""

from textwrap import dedent

from breezy.tests import TestCaseWithTransport

from wikkid.filestore import UpdateConflicts
from wikkid.filestore.bzr import (
    BranchFileStore,
    FileStore,
    )
from wikkid.tests import ProvidesMixin
from wikkid.tests.filestore import TestFileStore


class TestBzrFileStore(TestCaseWithTransport, ProvidesMixin, TestFileStore):
    """Tests for the bzr filestore and files."""

    def make_filestore(self, contents=None):
        tree = self.make_branch_and_tree('.')
        if contents:
            self.build_tree_contents(contents)
        tree.smart_add(['.'])
        tree.commit(message='Initial commit', authors=['test@example.com'])
        return FileStore(tree)

    def test_conflicts(self):
        filestore = self.make_filestore(
            [('test.txt', b'one line of content\n')])
        f = filestore.get_file('test.txt')
        base_rev = f.last_modified_in_revision
        # First update succeeds.
        filestore.update_file(
            'test.txt',
            b'different line\n',
            'Test Author <test@example.com>',
            base_rev)
        # Second update with same base revision should raise an exception.
        conflicts = self.assertRaises(
            UpdateConflicts,
            filestore.update_file,
            'test.txt',
            b'also change the first line\n',
            'Test Author <test@example.com>',
            base_rev)
        curr = filestore.get_file('test.txt')
        self.assertEqual(
            curr.last_modified_in_revision,
            conflicts.basis_rev)
        self.assertEqual(dedent("""\
            <<<<<<<
            also change the first line
            =======
            different line
            >>>>>>>
            """).encode(), conflicts.content)

    def test_conflicts_dos_line_endings(self):
        filestore = self.make_filestore(
            [('test.txt', b'one line of content\r\n')])
        f = filestore.get_file('test.txt')
        base_rev = f.last_modified_in_revision
        # First update succeeds.
        filestore.update_file(
            'test.txt',
            b'different line\r\n',
            'Test Author <test@example.com>',
            base_rev)
        # Second update with same base revision should raise an exception.
        conflicts = self.assertRaises(
            UpdateConflicts,
            filestore.update_file,
            'test.txt',
            b'also change the first line\r\n',
            'Test Author <test@example.com>',
            base_rev)
        curr = filestore.get_file('test.txt')
        self.assertEqual(
            curr.last_modified_in_revision,
            conflicts.basis_rev)
        self.assertEqual(
            b"<<<<<<<\r\n"
            b"also change the first line\r\n"
            b"=======\r\n"
            b"different line\r\n"
            b">>>>>>>\r\n",
            conflicts.content)

    def test_line_endings_unix(self):
        # If the underlying file has unix file endings, and the post param has
        # dos endings, the post param is converted before the merge is
        # attempted.
        filestore = self.make_filestore(
            [('test.txt', b'several\nlines\nof\ncontent')])
        f = filestore.get_file('test.txt')
        base_rev = f.last_modified_in_revision
        # Updating the text with dos endings doesn't convert the file.
        filestore.update_file(
            'test.txt',
            b'several\r\nslightly different lines\r\nof\r\ncontent',
            'Test Author <test@example.com>',
            base_rev)
        curr = filestore.get_file('test.txt')
        # New line added too.
        self.assertEqual(
            b'several\nslightly different lines\nof\ncontent\n',
            curr.get_content())

    def test_line_endings_new_file(self):
        # Line endings for new files default to '\n'.
        filestore = self.make_filestore()
        filestore.update_file(
            'new-file.txt',
            b'some\r\ndos\r\nline\r\nendings',
            'Test Author <test@example.com>',
            None)
        curr = filestore.get_file('new-file.txt')
        # A new line is added to the end too.
        self.assertEqual(
            b'some\ndos\nline\nendings\n',
            curr.get_content())

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


class TestBranchFileStore(TestBzrFileStore):

    def make_filestore(self, contents=None):
        tree = self.make_branch_and_tree('.')
        if contents:
            self.build_tree_contents(contents)
        tree.smart_add(['.'])
        tree.commit(message='Initial commit', authors=['test@example.com'])
        return BranchFileStore(tree.branch)
