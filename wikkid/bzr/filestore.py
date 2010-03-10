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

    def __init__(self, working_tree):
        self.working_tree = working_tree

    def get_file(self, path):
        """Return an object representing the file at specified path."""
        return File(self.working_tree, path)


class File(object):
    """Represents a file in the Bazaar branch."""

    implements(IFile)

    def __init__(self, working_tree, path):
        self.working_tree = working_tree
        self.path = path
        self.file_id = self.working_tree.path2id(path)

    def get_content(self):
        if self.file_id is None:
            return None
        branch = self.working_tree.branch
        branch.lock_read()
        try:
            # basis_tree is a revision tree, queries the repositry.
            # to get the stuff off the filesystem use the working tree
            # which needs to start with that.  WorkingTree.open('.').
            # branch = tree.branch.
            return self.working_tree.get_file_text(self.file_id)
        finally:
            branch.unlock()

    def update(self, content, user):
        raise NotImplementedError()
