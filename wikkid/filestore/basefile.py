#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""Base classes for other filestores to use."""

import mimetypes

import breezy.urlutils as urlutils

from wikkid.interface.filestore import FileType


class BaseFile(object):
    """Provide common fields and methods and properties for files."""

    def __init__(self, path):
        self.path = path
        self.base_name = urlutils.basename(path)
        self._mimetype = mimetypes.guess_type(self.base_name)[0]

    @property
    def mimetype(self):
        """If the file_type is a directory, return None."""
        if self.file_type == FileType.DIRECTORY:
            return None
        else:
            return self._mimetype
