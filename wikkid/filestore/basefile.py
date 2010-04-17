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

"""Base classes for other filestores to use."""

import mimetypes

import bzrlib.urlutils as urlutils

from wikkid.interface.filestore import FileType


class BaseFile(object):
    """Provide common fields and methods and properties for files."""

    def __init__(self, path, file_id):
        self.path = path
        self.file_id = file_id
        self.base_name = urlutils.basename(path)
        self._mimetype = mimetypes.guess_type(self.base_name)[0]

    @property
    def mimetype(self):
        """If the file_type is a directory, return None."""
        if self.file_type == FileType.DIRECTORY:
            return None
        else:
            return self._mimetype
