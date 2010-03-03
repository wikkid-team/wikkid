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

"""Tests for the wikkid.volatile.FileStore."""

from wikkid.interfaces import IFile, IFileStore
from wikkid.tests import TestCase
from wikkid.volatile.filestore import FileStore


class TestVolatileFileStore(TestCase):

    def test_filestore_provides_IFileStore(self):
        filestore = FileStore()
        self.assertProvides(filestore, IFileStore)

    def test_file_provides_IFile(self):
        filestore = FileStore({
                'README': 'Content'})
        readme = filestore.get_file('README')
        self.assertProvides(readme, IFile)
