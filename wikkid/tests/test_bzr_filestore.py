#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.filestore.bzr.FileStore."""

from textwrap import dedent

from bzrlib.tests import TestCaseWithTransport

from wikkid.errors import UpdateConflicts
from wikkid.filestore.bzr import FileStore
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

