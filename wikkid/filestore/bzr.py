#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A bzr backed filestore."""

from datetime import datetime
import logging

from zope.interface import implementer
from merge3 import Merge3

from breezy.bzr.generate_ids import gen_file_id
from breezy.errors import BinaryFile
from breezy.osutils import splitpath, split_lines
from breezy.revision import NULL_REVISION
from breezy.textfile import check_text_lines
from breezy.transform import FinalPaths, MalformedTransform
from breezy.urlutils import basename, dirname, joinpath

from wikkid.filestore import FileExists, UpdateConflicts
from wikkid.filestore.basefile import BaseFile
from wikkid.interface.filestore import FileType, IFile, IFileStore


def normalize_line_endings(content, ending=b'\n'):
    return ending.join(content.splitlines())


def get_line_ending(lines):
    """Work out the line ending used in lines."""
    if len(lines) == 0:
        return b'\n'
    first = lines[0]
    if first.endswith(b'\r\n'):
        return b'\r\n'
    # Default to \n if there are no line endings.
    return b'\n'


def get_commit_message(commit_message):
    if commit_message is None or commit_message.strip() == '':
        return 'No description of change given.'
    return commit_message


def normalize_content(content):
    # Default to simple '\n' line endings.
    content = normalize_line_endings(content)
    # Make sure the content ends with a new-line.  This makes
    # end of file conflicts nicer.
    if not content.endswith(b'\n'):
        content += b'\n'
    return content


def iter_paths(path):
    path_segments = splitpath(path)
    while len(path_segments) > 0:
        tail = path_segments.pop()
        if len(path_segments) == 0:
            yield '', tail
        else:
            yield joinpath(*path_segments), tail


def create_parents(tt, path, trans_id):
    prev_trans_id = trans_id
    for parent_path, tail in iter_paths(path):
        trans_id = tt.trans_id_tree_path(parent_path)
        if tt.tree_kind(trans_id) is not None:
            break
        tt.adjust_path(tail, trans_id, prev_trans_id)
        tt.create_directory(trans_id)
        tt.version_file(trans_id=trans_id, file_id=gen_file_id(basename(path)))
        prev_trans_id = trans_id


@implementer(IFileStore)
class FileStore(object):
    """Wraps a Bazaar branch to be a filestore."""

    def __init__(self, tree):
        self.tree = tree
        self.branch = tree.branch
        self.logger = logging.getLogger('wikkid')

    def basis_tree(self):
        return self.tree.basis_tree()

    def get_file(self, path):
        """Return an object representing the file at specified path."""
        if not self.tree.is_versioned(path):
            return None
        else:
            return File(self, path)

    def update_file(self, path, content, author, parent_revision,
                    commit_message=None):
        """Update the file at the specified path with the content.

        This is going to be really interesting when we need to deal with
        conflicts.
        """
        commit_message = get_commit_message(commit_message)
        if parent_revision is None:
            parent_revision = NULL_REVISION
        # Firstly we want to lock the tree for writing.
        with self.tree.lock_write():
            # Look to see if the path is there.  If it is then we are doing an
            # update.  If it isn't we are doing an add.
            if self.tree.is_versioned(path):
                # What if a parent_revision hasn't been set?
                self._update_file(
                    path, content, author, parent_revision,
                    commit_message)
            else:
                self._add_file(path, content, author, commit_message)

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
        content = normalize_content(content)
        t = self.tree.controldir.root_transport
        # Get a transport for the path we want.
        self._ensure_directory_or_nonexistant(dirname(path))
        t = t.clone(dirname(path))
        t.create_prefix()
        # Put the file there.
        # TODO: UTF-8 encode text files?
        t.put_bytes(basename(path), content)
        self.tree.smart_add([t.local_abspath('.')])
        self.tree.commit(
            message=commit_message,
            authors=[author])

    def _get_final_text(self, content, f, parent_revision):
        current_rev = f.last_modified_in_revision
        wt = self.tree
        current_lines = wt.get_file_lines(f.path)
        basis = self.branch.repository.revision_tree(parent_revision)
        basis_lines = basis.get_file_lines(f.path)
        # need to break content into lines.
        ending = get_line_ending(current_lines)
        # If the content doesn't end with a new line, add one.
        new_lines = split_lines(content)
        # Look at the end of the first string.
        new_ending = get_line_ending(new_lines)
        if ending != new_ending:
            # I know this is horribly inefficient, but lets get it working
            # first.
            content = normalize_line_endings(content, ending)
            new_lines = split_lines(content)
        if len(new_lines) > 0 and not new_lines[-1].endswith(ending):
            new_lines[-1] += ending
        merge = Merge3(basis_lines, new_lines, current_lines)
        result = b''.join(merge.merge_lines())  # or merge_regions or whatever
        conflicted = (b'>>>>>>>' + ending) in result
        if conflicted:
            raise UpdateConflicts(result, current_rev)
        return result

    def _update_file(self, path, content, author, parent_revision,
                     commit_message):
        """Update an existing file with the content.

        This method merges the changes in based on the parent revision.
        """
        f = File(self, path)
        wt = self.tree
        with wt.lock_write():
            result = self._get_final_text(content, f, parent_revision)
            wt.controldir.root_transport.put_bytes(path, result)
            wt.commit(
                message=commit_message, authors=[author],
                specific_files=[path])

    def list_directory(self, directory_path):
        """Return a list of File objects for in the directory path.

        If the path doesn't exist, returns None.  If the path exists but is
        empty, an empty list is returned.  Otherwise a list of File objects in
        that directory.
        """
        if directory_path is not None:
            directory = self.get_file(directory_path)
            if directory is None or directory.file_type != FileType.DIRECTORY:
                return None
        listing = []
        wt = self.tree
        with wt.lock_read():
            for fp, fc, fkind, entry in wt.list_files(
                    from_dir=directory_path, recursive=False):
                if fc != 'V':
                    # If the file isn't versioned, skip it.
                    continue
                if directory_path is None:
                    file_path = fp
                else:
                    file_path = joinpath(directory_path, fp)
                listing.append(File(self, file_path))
            return listing


@implementer(IFile)
class File(BaseFile):
    """Represents a file in the Bazaar branch."""

    def __init__(self, filestore, path):
        BaseFile.__init__(self, path)
        self.filestore = filestore
        # This isn't entirely necessary.
        self.tree = self.filestore.tree
        self.file_type = self._get_filetype()
        self._last_modified_in_revision = None

    def _get_filetype(self):
        """Work out the filetype based on the mimetype if possible."""
        with self.tree.lock_read():
            is_directory = ('directory' == self.tree.kind(self.path))
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
        with self.tree.lock_read():
            # basis_tree is a revision tree, queries the repositry.
            # to get the stuff off the filesystem use the working tree
            # which needs to start with that.  WorkingTree.open('.').
            # branch = tree.branch.
            return self.tree.get_file_text(self.path)

    @property
    def last_modified_in_revision(self):
        if self._last_modified_in_revision is None:
            try:
                self._last_modified_in_revision = self.tree.get_file_revision(
                    self.path)
            except AttributeError:
                bt = self.tree.basis_tree()
                self._last_modified_in_revision = bt.get_file_revision(
                    self.path)
        return self._last_modified_in_revision

    @property
    def last_modified_by(self):
        """Return the first author for the revision."""
        repo = self.filestore.branch.repository
        rev = repo.get_revision(self.last_modified_in_revision)
        return rev.get_apparent_authors()[0]

    @property
    def last_modified_date(self):
        """Return the last modified date for the revision."""
        repo = self.filestore.branch.repository
        rev = repo.get_revision(self.last_modified_in_revision)
        return datetime.utcfromtimestamp(rev.timestamp)

    @property
    def _is_binary(self):
        """True if the file is binary."""
        try:
            with self.tree.lock_read():
                lines = self.tree.get_file_lines(self.path)
                check_text_lines(lines)
            return False
        except BinaryFile:
            return True

    @property
    def is_directory(self):
        """Is this file a directory?"""
        return 'directory' == self.tree.kind(self.path)

    def update(self, content, user):
        raise NotImplementedError()


class BranchFileStore(FileStore):

    def __init__(self, branch):
        self.branch = branch
        self.tree = branch.basis_tree()
        self.logger = logging.getLogger('wikkid')

    def basis_tree(self):
        return self.tree

    def update_file(self, path, content, author, parent_revision,
                    commit_message=None):
        commit_message = get_commit_message(commit_message)
        with self.branch.lock_write():
            if self.tree.is_versioned(path):
                f = File(self, path)
                content = self._get_final_text(content, f, parent_revision)
            else:
                content = normalize_content(content)
            if not isinstance(content, bytes):
                raise TypeError(content)
            with self.tree.preview_transform() as tt:
                trans_id = tt.trans_id_tree_path(path)
                if tt.tree_kind(trans_id) is not None:
                    tt.delete_contents(trans_id)
                else:
                    name = splitpath(path)[-1]
                    tt.version_file(
                        trans_id=trans_id, file_id=gen_file_id(name))
                    create_parents(tt, path, trans_id)
                tt.create_file([content], trans_id)
                try:
                    tt.commit(self.branch, commit_message, authors=[author])
                except MalformedTransform as e:
                    for conflict in e.conflicts:
                        if conflict[0] == 'non-directory parent':
                            path = FinalPaths(tt).get_path(trans_id)
                            raise FileExists(
                                '%s exists and is not a directory' %
                                conflict[1])
                    raise

            self.tree = self.branch.basis_tree()
