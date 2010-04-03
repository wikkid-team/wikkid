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

from bzrlib.urlutils import basename

from wikkid.interfaces import FileType
from wikkid.views.binary import BinaryFile
from wikkid.views.pages import (
    DirectoryListingPage,
    EditWikiPage,
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

    DEFAULT_PATH = 'Home'

    def __init__(self, filestore, skin_name=None):
        """Construct the Wikkid Wiki server.

        :param filestore: An `IFileStore` instance.
        :param user_factory: A factory to create users.
        :param skin_name: The name of a skin to use.
        """
        self.filestore = filestore
        # Need to load the initial templates for the skin.
        if skin_name is None:
            skin_name = 'default'
        self.logger = logging.getLogger('wikkid')
        self.skin = Skin(skin_name)

    def edit_page(self, path, user):
        if path == '/':
            path = '/' + self.DEFAULT_PATH

        page_name = basename(path)
        if '.' not in page_name:
            txt_info = self.get_info(path + '.txt')
            txt_params = (self.skin, txt_info, path, user)
        info = self.get_info(path)
        page_params = (self.skin, info, path, user)
        if info.file_type == FileType.MISSING:
            if txt_info.file_type != FileType.MISSING:
                return EditWikiPage(*txt_params)
            else:
                return EditWikiPage(*page_params)
        elif info.file_type == FileType.DIRECTORY:
            if txt_info.file_type != FileType.MISSING:
                return EditWikiPage(*txt_params)
            else:
                return EditWikiPage(*page_params)
        elif info.file_type == FileType.TEXT_FILE:
            return EditWikiPage(*page_params)
        elif info.file_type == FileType.BINARY_FILE:
            raise NotImplementedError('Binary files are not editable yet.')
        raise AssertionError('Unknown file type')

    def get_page(self, path, user):
        if path == '/':
            path = '/' + self.DEFAULT_PATH

        page_name = basename(path)
        if '.' not in page_name:
            txt_info = self.get_info(path + '.txt')
            txt_params = (self.skin, txt_info, path, user)
        info = self.get_info(path)
        page_params = (self.skin, info, path, user)
        if info.file_type == FileType.MISSING:
            if txt_info.file_type != FileType.MISSING:
                return WikiPage(*txt_params)
            else:
                return MissingPage(*page_params)
        elif info.file_type == FileType.DIRECTORY:
            if txt_info.file_type != FileType.MISSING:
                return WikiPage(*txt_params)
            else:
                return DirectoryListingPage(*page_params)
        elif info.file_type == FileType.TEXT_FILE:
            if info.path.endswith('.txt'):
                return WikiPage(*page_params)
            else:
                return OtherTextPage(*page_params)
        elif info.file_type == FileType.BINARY_FILE:
            return BinaryFile(*page_params)
        raise AssertionError('Unknown file type')

    def get_info(self, path):
        """Get the resource from the filestore for the specified path.

        The path starts with a slash as proveded through the url traversal,
        the filestore does not expect nor want a leading slash.  It is the
        responsibility of this method to remove the leading slash.
        """
        assert path.startswith('/')
        path = path[1:]
        resource = self.filestore.get_file(path)
        if resource is None:
            return ResourceInfo(FileType.MISSING, path, None)
        else:
            # Here is where we need to check for a 'wiki' page.
            return ResourceInfo(resource.file_type, path, resource)
