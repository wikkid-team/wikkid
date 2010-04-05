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

from wikkid.errors import UpdateConflicts
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

    def __init__(self, path, write_filename, file_resource, dir_resource):
        self.path = path
        self.write_filename = write_filename
        self.file_resource = file_resource
        self.dir_resource = dir_resource


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

    def update_page(self, path, user, rev_id, content, commit_msg):
        """Try to update the page with the specified content.

        TODO: add in the file_id to handle page moves.
        """
        try:
            info = self.get_info(path)
            self.filestore.update_file(
                info.path, content, user.committer_id, rev_id, commit_msg)
        except UpdateConflicts:
            return "conficts, TODO..."

    def get_page(self, path, user):
        if path == '/':
            path = '/' + self.DEFAULT_PATH

        page_name = basename(path)
        check_txt = '.' not in page_name
        if check_txt:
            txt_info = self.get_info(path + '.txt')
            txt_params = (self.skin, txt_info, path, user)
        info = self.get_info(path)
        page_params = (self.skin, info, path, user)
        if info.file_type == FileType.MISSING:
            if check_txt and txt_info.file_type != FileType.MISSING:
                return WikiPage(*txt_params)
            else:
                return MissingPage(*page_params)
        elif info.file_type == FileType.DIRECTORY:
            if check_txt and txt_info.file_type != FileType.MISSING:
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
        file_path = path[1:]
        if file_path == '':
            file_path = self.DEFAULT_PATH

        dir_resource = None
        file_resource = self.filestore.get_file(file_path)
        # If the resource exists and is a file, we are done.
        if file_resource is not None:
            if file_resource.file_type != FileType.DIRECTORY:
                return ResourceInfo(path, file_path, file_resource, None)
            else:
                dir_resource = file_resource
                file_resource = None

        if '.' not in basename(file_path):
            file_path += '.txt'
            file_resource = self.filestore.get_file(file_path)

        return ResourceInfo(path, file_path, file_resource, dir_resource)
