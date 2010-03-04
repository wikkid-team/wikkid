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

"""A volatile filestore.

Used primarily for test purposes, this class should be a fully functional
filestore, albiet one that doesn't remember anything persistently.
"""

from zope.interface import implements

from wikkid.errors import FileExists
from wikkid.interfaces import IFile, IFileStore


class FileStore(object):
    """A filestore that just uses an internal map to store data."""

    implements(IFileStore)

    def __init__(self, files=None):
        """Files is a dictionary containing path to content mapping.

        If the content is None, the path is assumed to be a directory.  If the
        content contains a null character, the file is considered binary.
        """
        if files is None:
            files = {}
        self.files = files

    def get_file(self, path):
        """Return an object representing the file."""
        if path in self.files:
            return File(path, self.files[path])
        else:
            return None

    def update_file(self, path, content, user):
        """The `user` is updating the file at `path` with `content`."""
        # Split the path, and make sure there are directories registered.
        dirs = path.split('/')
        for i in range(1, len(dirs)):
            check_dir_path = '/'.join(dirs[:i])
            check_dir = self.get_file(check_dir_path)
            if check_dir is None:
                # Add it in.
                self.files[check_dir_path] = None
            elif not check_dir.is_directory:
                raise FileExists(
                    "Found a file at '%s' where a directory is needed"
                    % check_dir_path)
            else:
                # Everything's fine.
                pass
        self.files[path] = content


class File(object):
    """A volatile file object."""

    implements(IFile)

    def __init__(self, path, content):
        self.path = path
        self.content = content

    def get_content(self):
        return self.content

    @property
    def is_directory(self):
        return self.content is None

    @property
    def is_binary(self):
        # Directories are considered binary.
        if self.is_directory:
            return True
        return '\0' in self.content
