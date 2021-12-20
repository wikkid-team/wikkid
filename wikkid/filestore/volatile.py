#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A volatile filestore.

Used primarily for test purposes, this class should be a fully functional
filestore, albiet one that doesn't remember anything persistently.
"""

from datetime import datetime
from itertools import count

from breezy.urlutils import dirname
from zope.interface import implementer

from wikkid.filestore import FileExists
from wikkid.filestore.basefile import BaseFile
from wikkid.interface.filestore import FileType, IFile, IFileStore


@implementer(IFileStore)
class FileStore(object):
    """A filestore that just uses an internal map to store data."""

    def __init__(self, files=None):
        """Files is a list of tuples.

        If the content is None, the path is assumed to be a directory.  If the
        content contains a null character, the file is considered binary.
        """
        self._integer = count(1)
        self.file_id_map = {}
        self.path_map = {}
        if files is None:
            files = []
        user = 'First User <first@example.com'
        for path, content in files:
            if path.endswith('/'):
                self._ensure_dir(path[:-1], user)
            else:
                self._add_file(path, content, user)

    def _ensure_dir(self, path, user):
        # If we are at the start, we are done.
        if not path:
            return
        # If the directory exists, we are done.
        if path in self.path_map:
            # Check to make sure that it is a directory.
            if self.path_map[path].file_type != FileType.DIRECTORY:
                raise FileExists(
                    "Found a file at '%s' where a directory is needed"
                    % path)
            return
        # Check to make sure the parent is in there too.
        self._ensure_dir(dirname(path), user)
        new_dir = File(path, None, next(self._integer), user)
        self.file_id_map[new_dir.file_id] = new_dir
        self.path_map[new_dir.path] = new_dir

    def _add_file(self, path, content, user):
        self._ensure_dir(dirname(path), user)
        new_file = File(path, content, next(self._integer), user)
        self.file_id_map[new_file.file_id] = new_file
        self.path_map[new_file.path] = new_file

    def get_file(self, path):
        """Return an object representing the file."""
        if path in self.path_map:
            return self.path_map[path]
        else:
            return None

    def update_file(self, path, content, user, parent_revision,
                    commit_message=None):
        """The `user` is updating the file at `path` with `content`."""
        existing_file = self.get_file(path)
        if existing_file is None:
            self._add_file(path, content, user)
        else:
            existing_file.content = content
            existing_file.last_modified_by = user
            existing_file.last_modified_date = datetime.utcnow()

    def list_directory(self, directory_path):
        """Return a list of File objects for in the directory path.

        If the path doesn't exist, returns None.  If the path exists but is
        empty, an empty list is returned.  Otherwise a list of File objects in
        that directory.
        """
        if directory_path is None:
            directory_path = ''
        else:
            directory = self.get_file(directory_path)
            if directory is None or not directory._is_directory:
                return None
        listing = []
        for path, value in self.path_map.items():
            path_dir = dirname(path)
            if path_dir == directory_path:
                listing.append(value)
        return listing


@implementer(IFile)
class File(BaseFile):
    """A volatile file object."""

    def __init__(self, path, content, file_id, user):
        BaseFile.__init__(self, path)
        self.file_id = file_id
        self.content = content
        self.last_modified_in_revision = None
        self.last_modified_by = user
        self.last_modified_date = datetime.utcnow()
        self.file_type = self._get_filetype()

    def _get_filetype(self):
        """Work out the filetype based on the mimetype if possible."""
        if self._is_directory:
            return FileType.DIRECTORY
        else:
            if self._mimetype is None:
                binary = self._is_binary
            else:
                binary = not self._mimetype.startswith('text/')
            if binary:
                return FileType.BINARY_FILE
            else:
                return FileType.TEXT_FILE

    def get_content(self):
        return self.content

    @property
    def _is_directory(self):
        return self.content is None

    @property
    def _is_binary(self):
        return b'\0' in self.content
