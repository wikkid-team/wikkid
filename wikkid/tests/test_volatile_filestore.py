#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Tests for the wikkid.filestore.volatile.FileStore."""

from wikkid.tests import TestCase
from wikkid.tests.filestore import TestFileStore
from wikkid.filestore.volatile import FileStore


class TestVolatileFileStore(TestCase, TestFileStore):
    """Tests for the volatile filestore and files."""

    def make_filestore(self, contents=None):
        return FileStore(contents)
