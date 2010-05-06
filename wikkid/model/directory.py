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

"""The directory resource class.

A directory resource is one where the path specifies a directory in the
filestore.
"""

from zope.interface import implements

from wikkid.model.missing import MissingResource
from wikkid.interface.filestore import FileType
from wikkid.interface.resource import IDirectoryResource


class DirectoryMethods(object):
    """Directory methods are used by DirectoryResource and WikiTextFile.

    The methods are only valid on WikiTextFile objects when there is a
    directory with the same name as the wiki file without the '.txt'
    """

    def get_dir_name(self):
        return self.dir_resource.path

    def get_listing(self):
        """Return a list of resources that are in this directory."""
        dir_name = self.get_dir_name()
        filestore = self.server.filestore
        listing = []
        for entry in filestore.list_directory(dir_name):
            if entry.file_type == FileType.DIRECTORY:
                file_resource = None
                dir_resource = entry
            else:
                file_resource = entry
                dir_resource = None
            file_path = entry.path
            listing.append(
                self.server.get_resource(
                    '/' + file_path, file_path, file_resource, dir_resource))

        return listing


class DirectoryResource(MissingResource, DirectoryMethods):
    """A directory in the filestore.

    By definition, a directory is also a missing wiki page.
    """

    implements(IDirectoryResource)

    def __repr__(self):
        return "<DirectoryResource '%s'>" % self.path
