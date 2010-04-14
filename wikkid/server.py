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
import re

from bzrlib.urlutils import basename, dirname, joinpath

from wikkid.errors import UpdateConflicts
from wikkid.interfaces import FileType
from wikkid.view.binary import BinaryFile
from wikkid.view.pages import (
    ConflictedEditWikiPage,
    DirectoryListingPage,
    EditWikiPage,
    MissingPage,
    OtherTextPage,
    WikiPage,
    )
from wikkid.skin import Skin


WIKI_PAGE = re.compile('^([A-Z]+[a-z]*)+$')
WIKI_PAGE_ELEMENTS = re.compile('([A-Z][a-z]+)')


def expand_wiki_name(name):
    """A wiki name like 'FrontPage' is expanded to 'Front Page'.

    Names that don't match wiki names are unaltered.
    """
    if WIKI_PAGE.match(name):
        name_parts = [
            part for part in WIKI_PAGE_ELEMENTS.split(name) if part]
        return ' '.join(name_parts)
    else:
        return name


class ResourceInfo(object):
    """Information about a resource."""

    def __init__(self, path, title, write_filename, file_resource, dir_resource):
        self.path = path
        self.title = title
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
        self.logger.debug('edit_page: %s, %s', path, user.display_name)
        info = self.get_info(path)

        # If we have a file, and it isn't binary, edit it.
        if info.file_resource is not None:
            file_type = info.file_resource.file_type
            if file_type == FileType.BINARY_FILE:
                raise NotImplementedError(
                    'Binary files are not editable yet.')

        return EditWikiPage(self.skin, info.file_resource, path, user)

    def update_page(self, path, user, rev_id, content, commit_msg):
        """Try to update the page with the specified content.

        TODO: add in the file_id to handle page moves.
        """
        self.logger.debug('update_page: %s, %s', path, user.display_name)
        info = self.get_info(path)
        try:
            self.filestore.update_file(
                info.write_filename, content, user.committer_id,
                rev_id, commit_msg)
            return self.get_page(path, user)
        except UpdateConflicts, e:
            return ConflictedEditWikiPage(
                self.skin, info.file_resource, path, user,
                e.conflict_text, e.rev_id)

    def get_page(self, path, user):
        self.logger.debug('get_page: %s, %s', path, user.display_name)
        info = self.get_info(path)

        if info.file_resource is not None:
            # We are pointing at a file.
            file_type = info.file_resource.file_type
            if file_type == FileType.BINARY_FILE:
                self.logger.debug('%s is a binary file', path)
                return BinaryFile(
                    self.skin, info.file_resource, path, user)
            if (info.file_resource.path.endswith('.txt') or
                '.' not in info.file_resource.base_name):
                return WikiPage(
                    self.skin, info.file_resource, path, user)
            else:
                return OtherTextPage(
                    self.skin, info.file_resource, path, user)
        elif info.dir_resource is not None:
            return DirectoryListingPage(
                self.skin, info.dir_resource, path, user)
        else:
            return MissingPage(self.skin, None, path, user)

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
        preferred_path = self.get_preferred_path(path)
        title = expand_wiki_name(basename(file_path))

        dir_resource = None
        file_resource = self.filestore.get_file(file_path)
        # If the resource exists and is a file, we are done.
        if file_resource is not None:
            if file_resource.file_type != FileType.DIRECTORY:
                return ResourceInfo(
                    preferred_path, title, file_path, file_resource, None)
            else:
                dir_resource = file_resource
                file_resource = None

        if '.' not in basename(file_path):
            file_path += '.txt'
            file_resource = self.filestore.get_file(file_path)

        return ResourceInfo(
            preferred_path, title, file_path, file_resource, dir_resource)

    def get_preferred_path(self, path):
        """Get the preferred path for the path passed in.

        If the path ends with '.txt' and doesn't have any other '.'s in the
        basename, then we prefer to access that file without the '.txt'.

        If the resulting path is the default path, then the preferred path
        should be '/'.
        """
        filename = basename(path)
        if filename.endswith('.txt'):
            filename = filename[:-4]

        if filename == self.DEFAULT_PATH and dirname(path) == '/':
            return '/'
        elif '.' in filename:
            return path
        else:
            return joinpath(dirname(path), filename)

    def get_parent_info(self, resource_info):
        """Get the resource info for the parent of path."""

        if resource_info.path == '/':
            return None
        return self.get_info(dirname(resource_info.path))
