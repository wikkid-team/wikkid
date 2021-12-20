#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The directory resource class.

A directory resource is one where the path specifies a directory in the
filestore.
"""

from zope.interface import implementer

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
        filestore = self.factory.filestore
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
                self.factory.get_resource(
                    '/' + file_path, file_path, file_resource, dir_resource))

        return listing


@implementer(IDirectoryResource)
class DirectoryResource(MissingResource, DirectoryMethods):
    """A directory in the filestore.

    By definition, a directory is also a missing wiki page.
    """

    def __repr__(self):
        return "<DirectoryResource '%s'>" % self.path
