#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Wikkid filestores.

The volatile filestore is primarily used for tests, and the bzr filestore is
where all the main work happens.
"""


class FileExists(Exception):
    """A file was found where a directory is wanted."""


class UpdateConflicts(Exception):
    """Conflicts were found during updating."""
    def __init__(self, content, basis_rev):
        Exception.__init__(self)
        self.content = content
        self.basis_rev = basis_rev
