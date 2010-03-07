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

"""A bzr backed filestore."""

from zope.interface import implements

from wikkid.interfaces import IFile, IFileStore


class FileStore(object):
    """Wraps a Bazaar branch to be a filestore."""

    implements(IFileStore)

    def __init__(self, branch):
        self.branch = branch

    def get_file(self, path):
        """Return an object representing the file at specified path."""
        return File(self.branch, path)


class File(object):
    """Represents a file in the Bazaar branch."""

    implements(IFile)

    def __init__(self, branch, path):
        self.branch = branch
        self.path = path
        self.file_id = branch.basis_tree().path2id(path)

    def get_content(self):
        if self.file_id is None:
            return None
        self.branch.lock_read()
        try:
            tree = self.branch.basis_tree()
            return tree.get_file_text(self.file_id)
        finally:
            self.branch.unlock()

    def update(self, content, user):
        raise NotImplementedError()
