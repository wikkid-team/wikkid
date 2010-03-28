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

"""The server class for the wiki."""

import logging

from wikkid.interfaces import FileType
from wikkid.page import (
    BinaryFile,
    DirectoryListingPage,
    MissingPage,
    OtherTextPage,
    WikiPage,
    )
from wikkid.skin import Skin


class ResourceInfo(object):
    """Information about a resource."""

    def __init__(self, file_type, path, resource):
        self.file_type = file_type
        self.path = path
        self.resource = resource


class Server(object):
    """The Wikkid wiki server.
    """

    def __init__(self, filestore, user_factory, skin_name=None):
        """Construct the Wikkid Wiki server.

        :param filestore: An `IFileStore` instance.
        :param user_factory: A factory to create users.
        :param skin_name: The name of a skin to use.
        """
        self.filestore = filestore
        self.user_factory = user_factory
        # Need to load the initial templates for the skin.
        if skin_name is None:
            skin_name = 'default'
        self.logger = logging.getLogger('wikkid')
        self.skin = Skin(skin_name)

    def get_page(self, path):
        info = self.get_info(path)
        file_type = info.file_type
        if file_type == FileType.MISSING:
            return MissingPage(self.skin, info)
        elif info.file_type == FileType.DIRECTORY:
            return DirectoryListingPage(self.skin, info)
        elif info.file_type == FileType.TEXT_FILE:
            if info.path.endswith('.txt'):
                return WikiPage(self.skin, info)
            else:
                return OtherTextPage(self.skin, info)
        return WikiPage(self.skin, self.get_info(path))

    def get_info(self, path):
        if path == '':
            path = 'FrontPage'
        resource = self.filestore.get_file(path)
        if resource is None:
            return ResourceInfo(FileType.MISSING, path, None)
        else:
            # Here is where we need to check for a 'wiki' page.
            return ResourceInfo(resource.file_type, path, resource)
