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

from cStringIO import StringIO

from zope.interface import implements

from bzrlib.errors import BinaryFile
from bzrlib.merge3 import Merge3
from bzrlib.textfile import check_text_path
from bzrlib.urlutils import basename, dirname

from wikkid.errors import FileExists, UpdateConflicts
from wikkid.filestore.basefile import BaseFile
from wikkid.interfaces import FileType, IFile, IFileStore


class FileStore(object):
    """Wraps a Bazaar branch to be a filestore."""

    implements(IFileStore)

    def __init__(self, working_tree):
        self.working_tree = working_tree

    def get_file(self, path):
        """Return an object representing the file at specified path."""
        file_id = self.working_tree.path2id(path)
        if file_id is None:
            return None
        else:
            return File(self.working_tree, path, file_id)

    def update_file(self, path, content, author, parent_revision,
                    commit_message=None):
        """Update the file at the specified path with the content.

        This is going to be really interesting when we need to deal with
        conflicts.
        """
        if commit_message is None or commit_message.strip() == '':
            commit_message = 'No description of change given.'
        # Firstly we want to lock the tree for writing.
        self.working_tree.lock_write()
        try:
            # Look to see if the path is there.  If it is then we are doing an
            # update.  If it isn't we are doing an add.
            file_id = self.working_tree.path2id(path)
            if file_id is None:
                self._add_file(path, content, author, commit_message)
            else:
                # What if a parent_revision hasn't been set?
                self._update_file(
                    file_id, path, content, author, parent_revision,
                    commit_message)
        finally:
            self.working_tree.unlock()

    def _ensure_directory_or_nonexistant(self, dir_path):
        """Ensure the dir_path defines a directory or doesn't exist.

        Walk up the dir_path and make sure that the path either doesn't exist
        at all, or is a directory.  The purpose of this is to make sure we
        don't try to add a file in a directory where the directory has the
        same name as an existing file.
        """
        check = []
        while dir_path:
            check.append(dir_path)
            dir_path = dirname(dir_path)
        while len(check):
            f = self.get_file(check.pop())
            if f is not None:
                if not f.is_directory:
                    raise FileExists(
                        '%s exists and is not a directory' % f.path)

    def _add_file(self, path, content, author, commit_message):
        """Add a new file at the specified path with the content.

        Then commit this new file with the specified commit_message.
        """
        t = self.working_tree.bzrdir.root_transport
        # Get a transport for the path we want.
        self._ensure_directory_or_nonexistant(dirname(path))
        t = t.clone(dirname(path))
        t.create_prefix()
        # Put the file there.
        # TODO: UTF-8 encode text files?
        t.put_bytes(basename(path), content)
        self.working_tree.smart_add([t.local_abspath('.')])
        self.working_tree.commit(
            message=commit_message,
            authors=[author])

    def _update_file(self, file_id, path, content, author, parent_revision,
                     commit_message):
        """Update an existing file with the content.

        This method merges the changes in based on the parent revision.
        """
        f = File(self.working_tree, path, file_id)
        basis_rev = f.last_modified_in_revision
        wt = self.working_tree
        wt.lock_write()
        current_lines = wt.get_file_lines(file_id)
        basis = wt.branch.repository.revision_tree(basis_rev)
        basis_lines = basis.get_file_lines(file_id)
        # need to break content into lines.
        new_lines = StringIO(content).readlines()
        merge = Merge3(basis_lines, new_lines, current_lines)
        result = list(merge.merge_lines()) # or merge_regions or whatever
        conflicted = '>>>>>>>\n' in result
        if conflicted:
            wt.unlock()
            raise UpdateConflicts('add text here', basis_rev)
        else:
            wt.bzrdir.root_transport.put_bytes(path, ''.join(result))
            wt.commit(
                message=commit_message, authors=[author],
                specific_files=[path])
            wt.unlock()


class File(BaseFile):
    """Represents a file in the Bazaar branch."""

    implements(IFile)

    def __init__(self, working_tree, path, file_id):
        BaseFile.__init__(self, path, file_id)
        self.working_tree = working_tree
        self.file_type = self._get_filetype()
        bt = self.working_tree.basis_tree()
        bt.lock_read()
        try:
            inv_file = bt.inventory[self.file_id]
            self.last_modified_in_revision = inv_file.revision
        finally:
            bt.unlock()

    def _get_filetype(self):
        """Work out the filetype based on the mimetype if possible."""
        is_directory = ('directory' == self.working_tree.kind(self.file_id))
        if is_directory:
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
        if self.file_id is None:
            return None
        self.working_tree.lock_read()
        try:
            # basis_tree is a revision tree, queries the repositry.
            # to get the stuff off the filesystem use the working tree
            # which needs to start with that.  WorkingTree.open('.').
            # branch = tree.branch.
            return self.working_tree.get_file_text(self.file_id)
        finally:
            self.working_tree.unlock()

    @property
    def last_modified_by(self):
        """Return the first author for the revision."""
        repo = self.working_tree.branch.repository
        rev = repo.get_revision(self.last_modified_in_revision)
        return rev.get_apparent_authors()[0]

    @property
    def _is_binary(self):
        """True if the file is binary."""
        try:
            check_text_path(self.working_tree.abspath(self.path))
            return False
        except BinaryFile:
            return True

    @property
    def is_directory(self):
        """Is this file a directory?"""
        return 'directory' == self.working_tree.kind(self.file_id)

    def update(self, content, user):
        raise NotImplementedError()
