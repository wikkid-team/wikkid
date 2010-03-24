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

"""Tests for the wikkid.bzr.FileStore."""

from bzrlib.tests import TestCaseWithTransport

from wikkid.bzr.filestore import FileStore
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

