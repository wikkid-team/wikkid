#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""The server class for the wiki."""

import logging

from breezy.urlutils import basename, dirname, joinpath
from zope.interface import directlyProvides

from wikkid.interface.filestore import FileType
from wikkid.interface.resource import IDefaultPage
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
            if filename.endswith('.txt') or '.' not in file_resource.base_name:
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

    def get_default_resource(self):
        """Return the Home resource."""
        return self.get_resource_at_path('/' + self.DEFAULT_PATH)

    def get_root_resource(self):
        """Return the root resource."""
        return self.get_resource_at_path('/')

    def get_resource_at_path(self, path):
        """Get the resource from the filestore for the specified path.

        The path starts with a slash as proveded through the url traversal,
        the filestore does not expect nor want a leading slash.  It is the
        responsibility of this method to remove the leading slash.
        """
        assert path.startswith('/')
        file_path = path[1:]
        is_default = False
        if file_path == '' or file_path == self.DEFAULT_PATH:
            file_path = self.DEFAULT_PATH
            is_default = True

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

        resource = self.get_resource(
            path, file_path, file_resource, dir_resource)
        if is_default:
            directlyProvides(resource, IDefaultPage)
        return resource

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
