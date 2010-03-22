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

from wikkid.page import Page
from wikkid.skin import Skin



class ResourceStatus(object):
    """Package lazr.enum and use an Enumerated Type."""
    MISSING = 1 # The file at the address does not exist.
    WIKI_PAGE = 2 # The resource is a wiki page.
    DIRECTORY = 3 # The resource is a directory.
    OTHER_TEXT = 4 # A text file that isn't a wiki page.
    BINARY_FILE = 5 # A (most likely) binary file.


class ResourceInfo(object):
    """Information about a resource."""

    def __init__(self, status, path, display_name, mimetype):
        self.status = status
        self.path = path
        self.display_name = display_name
        self.mimetype = mimetype


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
        return Page(path, self.filestore.get_file(path))

    def get_info(self, path):
        resource = self.filestore.get_file(path)
        if resource is None:
            return ResourceInfo(ResourceStatus.MISSING, path, None, None)
        else:
            return ResourceInfo(ResourceStatus.OTHER_TEXT, path, path, 'text/plain')

