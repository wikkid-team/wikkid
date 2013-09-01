#
# Copyright (C) 2012 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.filestore.git.FileStore."""

from dulwich.objects import Tree, Blob, Commit
from dulwich.repo import MemoryRepo

import posixpath
import stat
import time
from textwrap import dedent

from wikkid.errors import UpdateConflicts
from wikkid.filestore.git import (
    FileStore,
    )
from wikkid.tests import ProvidesMixin, TestCase
from wikkid.tests.filestore import TestFileStore


class TestGitFileStore(TestCase, ProvidesMixin, TestFileStore):
    """Tests for the git filestore and files."""

    def make_filestore(self, contents=None):
        repo = MemoryRepo()
        objects = {"": Tree()}
        if contents:
            for (path, contents) in contents:
                path = path.strip("/")
                (dirname, basename) = posixpath.split(path)
                if contents is not None:
                    o = Blob.from_string(contents)
                    mode = stat.S_IFREG
                else:
                    o = Tree()
                    mode = stat.S_IFDIR
                objects[path] = o
                objects[dirname].add(basename, mode | 0644, o.id)
        c = Commit()
        c.author = c.committer = "Somebody <test@example.com>"
        c.author_time = c.commit_time = time.time()
        c.author_timezone = c.commit_timezone = 0
        c.message = 'Initial commit'
        c.tree = objects[""].id
        objects[None] = c
        repo.object_store.add_object(c)
        repo.object_store.add_objects(
            [(o, p) for (p, o) in objects.iteritems()])
        return FileStore(repo)

    def test_conflicts(self):
        filestore = self.make_filestore(
            [('test.txt', 'one line of content\n')])
        f = filestore.get_file('test.txt')
        base_rev = f.last_modified_in_revision
        # First update succeeds.
        filestore.update_file(
            'test.txt',
            'different line\n',
            'Test Author <test@example.com>',
            base_rev)
        # Second update with same base revision should raise an exception.
        conflicts = self.assertRaises(
            UpdateConflicts,
            filestore.update_file,
            'test.txt',
            'also change the first line\n',
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
            """), conflicts.content)

    def test_conflicts_dos_line_endings(self):
        filestore = self.make_filestore(
            [('test.txt', 'one line of content\r\n')])
        f = filestore.get_file('test.txt')
        base_rev = f.last_modified_in_revision
        # First update succeeds.
        filestore.update_file(
            'test.txt',
            'different line\r\n',
            'Test Author <test@example.com>',
            base_rev)
        # Second update with same base revision should raise an exception.
        conflicts = self.assertRaises(
            UpdateConflicts,
            filestore.update_file,
            'test.txt',
            'also change the first line\r\n',
            'Test Author <test@example.com>',
            base_rev)
        curr = filestore.get_file('test.txt')
        self.assertEqual(
            curr.last_modified_in_revision,
            conflicts.basis_rev)
        self.assertEqual(
            "<<<<<<<\r\n"
            "also change the first line\r\n"
            "=======\r\n"
            "different line\r\n"
            ">>>>>>>\r\n",
            conflicts.content)

    def test_line_endings_unix(self):
        # If the underlying file has unix file endings, and the post param has
        # dos endings, the post param is converted before the merge is
        # attempted.
        filestore = self.make_filestore(
            [('test.txt', 'several\nlines\nof\ncontent')])
        f = filestore.get_file('test.txt')
        base_rev = f.last_modified_in_revision
        # Updating the text with dos endings doesn't convert the file.
        filestore.update_file(
            'test.txt',
            'several\r\nslightly different lines\r\nof\r\ncontent',
            'Test Author <test@example.com>',
            base_rev)
        curr = filestore.get_file('test.txt')
        # New line added too.
        self.assertEqual(
            'several\nslightly different lines\nof\ncontent\n',
            curr.get_content())

    def test_line_endings_new_file(self):
        # Line endings for new files default to '\n'.
        filestore = self.make_filestore()
        filestore.update_file(
            'new-file.txt',
            'some\r\ndos\r\nline\r\nendings',
            'Test Author <test@example.com>',
            None)
        curr = filestore.get_file('new-file.txt')
        # A new line is added to the end too.
        self.assertEqual(
            'some\ndos\nline\nendings\n',
            curr.get_content())

    def test_empty(self):
        # Empty files do not have line endings, but they can be saved
        # nonetheless.
        filestore = self.make_filestore(
            [('test.txt', 'several\nlines\nof\ncontent')])
        f = filestore.get_file('test.txt')
        base_rev = f.last_modified_in_revision
        filestore.update_file(
            'test.txt', '', 'Test Author <test@example.com>', base_rev)
        curr = filestore.get_file('test.txt')
        self.assertEqual('', curr.get_content())
