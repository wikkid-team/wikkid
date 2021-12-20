#
# Copyright (C) 2012 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A git filestore using Dulwich.

"""

import datetime
import mimetypes

from dulwich.objects import Blob, Tree, ZERO_SHA
from dulwich.object_store import tree_lookup_path
from dulwich.repo import Repo
from dulwich.walk import Walker
import posixpath
import stat

from zope.interface import implementer

from wikkid.filestore import FileExists, UpdateConflicts
from wikkid.interface.filestore import FileType, IFile, IFileStore


@implementer(IFileStore)
class FileStore(object):
    """A filestore that just uses an internal map to store data."""

    _encoding = 'utf-8'

    @classmethod
    def from_path(cls, path):
        return cls(Repo(path))

    def __init__(self, repo, ref=b'HEAD'):
        """Repo is a dulwich repository."""
        self.repo = repo
        self.ref = ref

    @property
    def store(self):
        return self.repo.object_store

    def _get_root(self, revision=None):
        if revision is None:
            try:
                revision = self.repo.refs[self.ref]
            except KeyError:
                revision = ZERO_SHA
        try:
            return (revision, self.repo[revision].tree)
        except KeyError:
            return None, None

    def get_file(self, path):
        """Return an object representing the file."""
        commit_id, root_id = self._get_root()
        if root_id is None:
            return None
        try:
            (mode, sha) = tree_lookup_path(
                self.store.__getitem__,
                root_id, path.encode(self._encoding))
        except KeyError:
            return None
        return File(
            self.store, mode, sha, path, commit_id, encoding=self._encoding)

    def update_file(self, path, content, author, parent_revision,
                    commit_message=None):
        """The `author` is updating the file at `path` with `content`."""
        commit_id, root_id = self._get_root()
        if root_id is None:
            root_tree = Tree()
        else:
            root_tree = self.store[root_id]
        # Find all tree objects involved
        tree = root_tree
        trees = [root_tree]
        elements = path.strip(posixpath.sep).split(posixpath.sep)
        for el in elements[:-1]:
            try:
                (mode, sha) = tree[el.encode(self._encoding)]
            except KeyError:
                tree = Tree()
            else:
                if not stat.S_ISDIR(mode):
                    raise FileExists(
                        "File %s exists and is not a directory" % el)
                tree = self.store[sha]
            trees.append(tree)
        if elements[-1] in tree:
            (old_mode, old_sha) = tree[elements[-1]]
            if stat.S_ISDIR(old_mode):
                raise FileExists("File %s exists and is a directory" % path)
            if old_sha != parent_revision and parent_revision is not None:
                raise UpdateConflicts(
                    "File conflict %s != %s" % (
                        old_sha, parent_revision), old_sha)
        if not isinstance(content, bytes):
            raise TypeError(content)
        blob = Blob.from_string(content)
        child = (stat.S_IFREG | 0o644, blob.id)
        self.store.add_object(blob)
        assert len(trees) == len(elements)
        for tree, name in zip(reversed(trees), reversed(elements)):
            assert name != ""
            tree[name.encode(self._encoding)] = child
            self.store.add_object(tree)
            child = (stat.S_IFDIR, tree.id)
        if commit_message is None:
            commit_message = ""
        if author is not None:
            author = author.encode(self._encoding)
        self.repo.do_commit(
            ref=self.ref, message=commit_message.encode(self._encoding),
            author=author, tree=child[1])

    def list_directory(self, directory_path):
        """Return a list of File objects for in the directory path.

        If the path doesn't exist, returns None.  If the path exists but is
        empty, an empty list is returned.  Otherwise a list of File objects in
        that directory.
        """
        if directory_path is None:
            directory_path = ''
        else:
            directory_path = directory_path.strip(posixpath.sep)
        commit_id, root_id = self._get_root()
        if directory_path == '':
            sha = root_id
            mode = stat.S_IFDIR
        else:
            if root_id is None:
                return None
            try:
                (mode, sha) = tree_lookup_path(
                    self.store.__getitem__,
                    root_id, directory_path.encode(self._encoding))
            except KeyError:
                return None
        if mode is not None and stat.S_ISDIR(mode):
            ret = []
            for (name, mode, sha) in self.store[sha].items():
                ret.append(
                    File(self.store, mode, sha,
                         posixpath.join(
                             directory_path, name.decode(self._encoding)),
                         commit_id, encoding=self._encoding))
            return ret
        else:
            return None


@implementer(IFile)
class File(object):
    """A Git file object."""

    def __init__(self, store, mode, sha, path, commit_sha, encoding):
        self.store = store
        self.encoding = encoding
        self.mode = mode
        self.sha = sha
        self.path = path
        self.commit_sha = commit_sha
        self.base_name = posixpath.basename(path)
        self.mimetype = mimetypes.guess_type(self.base_name)[0]

    @property
    def file_type(self):
        """Work out the filetype based on the mimetype if possible."""
        if self._is_directory:
            return FileType.DIRECTORY
        else:
            if self.mimetype is None:
                binary = self._is_binary
            else:
                binary = not self.mimetype.startswith('text/')
            if binary:
                return FileType.BINARY_FILE
            else:
                return FileType.TEXT_FILE

    def get_content(self):
        o = self.store[self.sha]
        if isinstance(o, Blob):
            return o.data
        else:
            return None

    @property
    def _is_directory(self):
        return stat.S_ISDIR(self.mode)

    @property
    def _is_binary(self):
        return b'\0' in self.get_content()

    def _get_last_modified_commit(self):
        walker = Walker(
            self.store, include=[self.commit_sha],
            paths=[self.path.encode(self.encoding)])
        return next(iter(walker)).commit

    @property
    def last_modified_in_revision(self):
        return self.sha

    @property
    def last_modified_by(self):
        return self._get_last_modified_commit().author.decode(self.encoding)

    @property
    def last_modified_date(self):
        c = self._get_last_modified_commit()
        return datetime.datetime.utcfromtimestamp(c.commit_time)
