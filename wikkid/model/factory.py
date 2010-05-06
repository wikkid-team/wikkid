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

from bzrlib.urlutils import basename, dirname, joinpath

from wikkid.interface.filestore import FileType
from wikkid.model.binary import BinaryResource
from wikkid.model.directory import DirectoryResource
from wikkid.model.missing import MissingResource
from wikkid.model.root import RootResource
from wikkid.model.sourcetext import SourceTextFile
from wikkid.model.wikitext import WikiTextFile


class ResourceFactory(object):
    """Factory to create the model objects used by the views."""

    DEFAULT_PATH = 'Home'

    def __init__(self, filestore):
        """Construct the factory.

        :param filestore: An `IFileStore` instance.
        :param user_factory: A factory to create users.
        :param skin_name: The name of a skin to use.
        """
        self.filestore = filestore
        self.logger = logging.getLogger('wikkid')

    def get_resource(self, path, file_path, file_resource, dir_resource):
        """Return the correct type of resource based on the params."""
        filename = basename(file_path)
        if path == '/':
            return RootResource(
                self, path, file_path, file_resource, None)
        elif file_resource is not None:
            # We are pointing at a file.
            file_type = file_resource.file_type
            if file_type == FileType.BINARY_FILE:
                # Binary resources have no associated directory.
                return BinaryResource(
                    self, path, file_path, file_resource, None)
            # This is known to be not entirely right.
            if (filename.endswith('.txt') or
                '.' not in file_resource.base_name):
                return WikiTextFile(
                    self, path, file_path, file_resource,
                    dir_resource)
            else:
                return SourceTextFile(
                    self, path, file_path, file_resource, None)
        elif dir_resource is not None:
            return DirectoryResource(
                self, path, file_path, None, dir_resource)
        else:
            return MissingResource(
                self, path, file_path, None, None)

    def get_resource_at_path(self, path):
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
                return self.get_resource(path, file_path, file_resource, None)
            else:
                dir_resource = file_resource
                file_resource = None

        if '.' not in basename(file_path):
            file_path += '.txt'
            file_resource = self.filestore.get_file(file_path)

        return self.get_resource(path, file_path, file_resource, dir_resource)

    def _is_default(self, dir_name, base_name):
        return base_name == self.DEFAULT_PATH and dir_name == '/'

    def get_preferred_path(self, path):
        """Get the preferred path for the path passed in.

        If the path ends with '.txt' and doesn't have any other '.'s in the
        basename, then we prefer to access that file without the '.txt'.

        If the resulting path is the default path, then the preferred path
        should be '/Home' providing Home is the default path..
        """
        filename = basename(path)
        if filename.endswith('.txt'):
            filename = filename[:-4]

        if path == '/':
            return '/' + self.DEFAULT_PATH
        elif '.' in filename:
            return path
        else:
            return joinpath(dirname(path), filename)

    def get_parent_info(self, resource):
        """Get the resource info for the parent of path."""

        if resource.path == '/':
            return None
        base_name = resource.base_name
        dir_name = resource.dir_name
        if self._is_default(dir_name, base_name):
            return None
        if dir_name == '/':
            dir_name += self.DEFAULT_PATH
        return self.get_resource_at_path(dir_name)
