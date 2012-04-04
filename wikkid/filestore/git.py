#
# Copyright (C) 2012 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A git filestore using Dulwich.

"""

from dulwich.objects import Blob, Tree, Commit
from dulwich.object_store import tree_lookup_path
from dulwich.repo import Repo
import posixpath
import stat
import time

from zope.interface import implements

from wikkid.errors import FileExists
from wikkid.interface.filestore import FileType, IFile, IFileStore


class FileStore(object):
    """A filestore that just uses an internal map to store data."""

    implements(IFileStore)

    @classmethod
    def from_path(cls, path):
        return cls(Repo(path))

    def __init__(self, repo, ref='HEAD'):
        """Repo is a dulwich repository."""
        self.repo = repo
        self.ref = ref

    @property
    def store(self):
        return self.repo.object_store

    def _get_root(self, revision=None):
        if revision is None:
            revision = self.ref
        try:
            return self.repo[revision].tree
        except KeyError:
            return None

    def get_file(self, path):
        """Return an object representing the file."""
        root_id = self._get_root()
        if root_id is None:
            return None
        try:
            (mode, sha) = tree_lookup_path(self.store.__getitem__,
                root_id, path)
            self.store[sha]
        except KeyError:
            return None
        return File(self.store, mode, sha)

    def update_file(self, path, content, user, parent_revision,
                    commit_message=None):
        """The `user` is updating the file at `path` with `content`."""
        root_id = self._get_root(parent_revision)
        if root_id is None:
            root_tree = Tree()
        else:
            root_tree = self.store[root_id]
        # Find all tree objects involved
        tree = root_tree
        trees = []
        elements = posixpath.split(path.strip("/"))
        for el in elements[:-1]:
            try:
                (mode, sha) = tree[el]
                tree = self.store[sha]
            except KeyError:
                tree = Tree()
            trees.append(tree)
        child = (stat.S_IFREG | 0644, Blob.from_string(content).id)
        for tree, name in zip(reversed(trees), reversed(elements)):
            tree[name] = child
            self.store.add_object(tree)
            child = (stat.S_IFDIR, tree.id)
        root_tree[name] = child
        self.store.add_object(root_tree)
        c = Commit()
        c.tree = root_tree.id
        c.author = user
        c.committer = "Wikkid <wikkid@host>"
        c.author_time = time.time()
        c.commit_time = time.time()
        c.author_timezone = c.commit_timezone = 0
        if commit_message is None:
            commit_message = ""
        c.message = commit_message
        self.store.add_object(c)
        self.repo.refs[self.ref] = c.id

    def list_directory(self, directory_path):
        """Return a list of File objects for in the directory path.

        If the path doesn't exist, returns None.  If the path exists but is
        empty, an empty list is returned.  Otherwise a list of File objects in
        that directory.
        """
        if directory_path is None:
            directory_path = ''
        else:
            directory_path = directory_path.strip("/")
        root_id = self._get_root()
        if root_id is None:
            if directory_path == '':
                return []
            return None
        (mode, sha) = tree_lookup_path(self.store.__getitem__,
            root_id, directory_path)
        if stat.S_ISDIR(mode):
            ret = []
            for (name, mode, sha) in self.store[sha]:
                ret.append(File(self.store, mode, sha))
            return ret
        else:
            return None


class File(object):
    """A Git file object."""

    implements(IFile)

    def __init__(self, store, mode, sha):
        self.store = store
        self.mode = mode
        self.sha = sha

    @property
    def filetype(self):
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
        o = self.store[self.sha]
        if isinstance(o, Blob):
            return o.content
        else:
            return None

    @property
    def _is_directory(self):
        return stat.S_ISDIR(self.mode)

    @property
    def _is_binary(self):
        return '\0' in self.content
